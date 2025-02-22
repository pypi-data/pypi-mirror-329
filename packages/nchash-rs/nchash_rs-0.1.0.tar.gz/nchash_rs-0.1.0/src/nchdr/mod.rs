mod attrs;
mod dims;
mod vars;

use netcdf::{self};
use std::path::Path;

use attrs::fmt_attr_info;
use dims::fmt_dim_info;
use vars::fmt_var_info;

pub fn nchdr(fname: String) -> Result<String, String> {
    // Dynamically build back up the output of ncdump -h $fname

    let mut ncdump = String::new();

    let f_path = Path::new(fname.as_str());

    let file: netcdf::File = match netcdf::open(f_path) {
        Ok(file) => file,
        Err(_) => return Err("NetCDF: Unknown file format".to_string()),
    };

    let file_stem = match extract_fname(&f_path) {
        Ok(stem) => stem,
        Err(_) => return Err("Could not decode filename".to_string()),
    };

    ncdump.push_str(&fmt_skeleton_opening(&file_stem));
    

    let variables: Vec<_> = file.variables().collect();
    let dimensions: Vec<_> = file.dimensions().collect();
    let global_attrs: Vec<_> = file.attributes().collect();

    ncdump.push_str(&format!("{}", "dimensions:"));
    for dim in dimensions {
        ncdump.push_str(&fmt_dim_info(&file, &dim.name()));
    }

    ncdump.push_str(&format!("{}", "variables:"));
    for var in variables {
        ncdump.push_str(&fmt_var_info(&file, &var.name()));
    }

    ncdump.push_str(&format!("{}", "\n// global attributes:\n"));
    for attr in global_attrs {
        ncdump.push_str(&fmt_attr_info(&file, attr.name()));
    }
    
    ncdump.push_str(&fmt_skeleton_close());

    Ok(ncdump)
}

fn fmt_skeleton_opening(f_stem: &str) -> String {
    format!("netcdf {} {{\n", f_stem).to_string()

}

fn fmt_skeleton_close() -> String { 
    "}\n".to_string()
}

fn extract_fname<'a>(f_handle: &'a std::path::Path) -> Result<&str, &str> {
    // Take the file handle, get the file stem, extract it.

    match f_handle.file_stem() {
        Some(stem) => match stem.to_str() {
            Some(stem_str) => Ok(stem_str),
            None => Err("Could not convert file stem to valid utf-8 string"),
        },
        None => Err("Could not identify filename"),
    }
}
