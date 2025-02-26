use pyo3::prelude::*;
use std::io::Cursor;
use calamine::{Reader, Xlsx, DataType};
use chrono::NaiveDateTime;

#[derive(Debug)]
enum LoadError {
    CsvError(csv::Error),
    ExcelError(String),
    UnknownFormat,
}

#[derive(Debug)]
enum InferredType {
    Int,
    Float,
    Str,
    DateTime,
    Date,
    Unknown,
}

impl InferredType {
    fn from_string(s: &str) -> Self {
        // Try integer first
        if let Ok(_) = s.parse::<i64>() {
            return InferredType::Int;
        }
        
        // Try float
        if let Ok(_) = s.parse::<f64>() {
            return InferredType::Float;
        }
        
        // Try datetime (common formats)
        let datetime_formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
            "%d/%m/%Y %H:%M:%S",
            "%m/%d/%Y %H:%M:%S",
        ];
        
        for format in datetime_formats.iter() {
            if NaiveDateTime::parse_from_str(s, format).is_ok() {
                return InferredType::DateTime;
            }
        }
        
        // Try date (common formats)
        let date_formats = [
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%m/%d/%Y",
        ];
        
        for format in date_formats.iter() {
            if chrono::NaiveDate::parse_from_str(s, format).is_ok() {
                return InferredType::Date;
            }
        }
        
        // Default to string
        InferredType::Str
    }
    
    fn to_string(&self) -> String {
        match self {
            InferredType::Int => "int".to_string(),
            InferredType::Float => "float".to_string(),
            InferredType::Str => "str".to_string(),
            InferredType::DateTime => "datetime".to_string(),
            InferredType::Date => "date".to_string(),
            InferredType::Unknown => "unknown".to_string(),
        }
    }
}

impl std::fmt::Display for LoadError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            LoadError::CsvError(e) => write!(f, "CSV error: {}", e),
            LoadError::ExcelError(e) => write!(f, "Excel error: {}", e),
            LoadError::UnknownFormat => write!(f, "Unknown or unsupported file format"),
        }
    }
}

impl From<LoadError> for PyErr {
    fn from(err: LoadError) -> PyErr {
        pyo3::exceptions::PyValueError::new_err(err.to_string())
    }
}

fn try_load_csv(content: &[u8]) -> Result<(Vec<Vec<String>>, Vec<Vec<String>>), LoadError> {
    let cursor = Cursor::new(content);
    let mut rdr = csv::ReaderBuilder::new()
        .flexible(true)
        .has_headers(false)  // We'll handle headers manually
        .from_reader(cursor);
    
    let mut data = Vec::new();
    let mut types = Vec::new();
    
    // Process all rows
    for result in rdr.records() {
        let record = result.map_err(LoadError::CsvError)?;
        let row_data: Vec<String> = record.iter().map(|s| s.to_string()).collect();
        let row_types: Vec<String> = row_data.iter()
            .map(|cell| InferredType::from_string(cell).to_string())
            .collect();
        
        data.push(row_data);
        types.push(row_types);
    }
    
    Ok((data, types))
}

fn excel_datetime_to_string(days_since_1900: f64) -> String {
    // Excel's date system starts from 1900-01-01, but has a bug treating 1900 as a leap year
    // We'll convert it to a timestamp and then format it
    const SECONDS_PER_DAY: f64 = 86400.0;
    const EXCEL_TO_UNIX_DAYS: f64 = 25569.0; // Days between 1900-01-01 and 1970-01-01
    
    let unix_timestamp = ((days_since_1900 - EXCEL_TO_UNIX_DAYS) * SECONDS_PER_DAY) as i64;
    
    if let Some(dt) = chrono::NaiveDateTime::from_timestamp_opt(unix_timestamp, 0) {
        dt.format("%Y-%m-%d %H:%M:%S").to_string()
    } else {
        format!("{}", days_since_1900) // Fallback to original number if conversion fails
    }
}

fn try_load_excel(content: &[u8]) -> Result<(Vec<Vec<String>>, Vec<Vec<String>>), LoadError> {
    // Create a cursor over the bytes
    let cursor = Cursor::new(content);
    
    // Open the workbook directly from the cursor
    let mut workbook = match Xlsx::new(cursor) {
        Ok(wb) => wb,
        Err(e) => return Err(LoadError::ExcelError(e.to_string())),
    };

    let mut data = Vec::new();
    let mut types = Vec::new();
    
    // Get all sheet names first
    let sheet_names = workbook.sheet_names().to_owned();
    
    // Process each sheet
    for name in &sheet_names {
        // Add sheet name separator row
        data.push(vec![format!("sheet_name|{}", name)]);
        types.push(vec!["str".to_string()]); // Type for sheet name row
        
        // Get and process sheet data
        if let Some(Ok(range)) = workbook.worksheet_range(name) {
            for row in range.rows() {
                let row_data: Vec<String> = row.iter().map(|cell| match cell {
                    DataType::Empty => String::new(),
                    DataType::String(s) => s.to_string(),
                    DataType::Float(f) => format!("{}", f),
                    DataType::Int(i) => i.to_string(),
                    DataType::Bool(b) => b.to_string(),
                    DataType::Error(e) => format!("{}", e),
                    DataType::DateTime(d) => excel_datetime_to_string(*d),
                }).collect();
                
                // Only process non-empty rows
                if row_data.iter().any(|cell| !cell.is_empty()) {
                    // Infer types for the row
                    let row_types: Vec<String> = row_data.iter()
                        .map(|cell| InferredType::from_string(cell).to_string())
                        .collect();
                    
                    data.push(row_data);
                    types.push(row_types);
                }
            }
        }
    }

    if data.is_empty() {
        Err(LoadError::ExcelError("No valid sheets found in workbook".to_string()))
    } else {
        Ok((data, types))
    }
}

#[pyfunction]
fn load_tabular_data(content: Vec<u8>) -> PyResult<(Vec<Vec<String>>, Vec<Vec<String>>)> {
    // Try CSV first
    match try_load_csv(&content) {
        Ok(result) => Ok(result),
        Err(_) => {
            // If CSV fails, try Excel
            try_load_excel(&content).map_err(Into::into)
        }
    }
}

#[pymodule]
fn tabular_data_loader(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(load_tabular_data, m)?)?;
    Ok(())
}
