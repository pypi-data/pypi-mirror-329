mod nchdr;

use std;
use std::os::unix::fs::MetadataExt;
use md5;
use std::fs;
use std::time::SystemTime;
use regex::Regex;

use crate::nchdr::nchdr;

use pyo3::{exceptions::PyException, prelude::*};

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}


#[pyfunction]
fn parse_args(argv : Vec<String>) -> PyResult<u8>{
    // parser = argparse.ArgumentParser(description="Run nchash on one or more netCDF files")
    // parser.add_argument("-n","--noname", help="Do not include filename in the hash (default False)", action='store_true')
    // parser.add_argument("-m","--nomtime", help="Do not include file modification time the hash (default False)", action='store_true')
    // parser.add_argument("inputs", help="netCDF files", nargs='+')

    // return parser.parse_args(args)

    Ok(0)
}

#[pyfunction]
fn main(argv : Vec<String>) -> () {
    // hashes = defaultdict(list)

    // for ncinput in args.inputs:
    //     try:
    //         nchash = NCDataHash(ncinput,args.noname,args.nomtime)
    //         print(nchash.gethash() + "  " + ncinput)
    //     except NotNetcdfFileError as e:
    //         sys.stderr.write(str(e))
}

#[pyfunction]
fn main_argv() -> () {

    // args = parse_args(sys.argv[1:])
    // main(args)
}

#[pyclass(extends=PyException)]
struct NotNetcdfFileError{
    fname: String,
}

#[pymethods]
impl NotNetcdfFileError{
    #[new]
    fn new(fname: String) -> Self {
        NotNetcdfFileError { fname }
    }

    fn __str__(&self) -> String {
        format!("{} is not a netCDF format file\n", self.fname.to_string())
    }
}

#[pyclass]
struct NCDataHash{
    filename : String,
    noname : bool,
    no_mtime : bool,
    // Not generated at initialisation 
    mtime : Option<f64>,
    ncdump: Option<String>,
    hashstring : Option<String>,
}

#[pymethods]
impl NCDataHash {
    #[new]
    #[pyo3(signature = (filename, noname=None, nomtime=None))]
    fn new( filename : String, noname : Option<bool>, nomtime : Option<bool>) -> Self {
        NCDataHash {
            filename,
            noname : noname.unwrap_or(false),
            no_mtime : nomtime.unwrap_or(false),
            mtime: None,
            ncdump : None,
            hashstring: None,
        }
    }

    fn getmtime(&mut self) -> Option<f64> {
        // Get the time that our file was last modified.
        let meta = fs::metadata(&self.filename).ok()?;
        let mod_time = meta.modified().ok()?;
        let mtime = mod_time.duration_since(SystemTime::UNIX_EPOCH).ok()?.as_secs_f64();

        self.mtime = Some(mtime);

        Some(mtime)
    }

    fn getheader(&mut self) -> PyResult<String> {
        // Call ncdump -h here (nchdr maybe?) 
        let mut header_str = match nchdr(self.filename.clone()) {
            Ok(header_str) => header_str,
            Err(e) => return Err(PyErr::new::<PyException, _>(e))
        };

        if self.noname {
            let re = Regex::new(r"^netcdf.*\{\n").unwrap();
            header_str = re.replace_all(&header_str, "{\n").to_string();

        }
        self.ncdump = Some(header_str.clone());

        Ok(header_str)

    }

    fn makehash(&mut self) -> PyResult<()> {

        let mut hashstr = match std::fs::metadata(&self.filename) {
            Ok(md) => md.size().to_string(),
            Err(e) => return Err(PyErr::new::<PyException, _>(e))
        };

        let ncdump = match &self.ncdump {
            Some(s) => s,
            None => return Err(PyErr::new::<PyException,_>("mtime not found"))
        };

        if self.no_mtime {
            hashstr.push_str(&ncdump);
        } else {
            hashstr.push_str(&self.mtime.unwrap().to_string());
            hashstr.push_str(&ncdump);
        }

        let digest = md5::compute(hashstr);

        self.hashstring = Some(format!("{:x}", digest));

        Ok(())

    }

    fn gethash(&mut self) -> PyResult<String> {

        if !self.no_mtime {
            self.getmtime();
        }

        let _ = self.getheader();
        match self.makehash() {
            Ok(()) => {
                match &self.hashstring {
                    Some(hashstring) => Ok(hashstring.clone()),
                    None => Err(PyErr::new::<PyException,_>("Failed to generate hash"))
                }
            },
            Err(_) => return Err(PyErr::new::<PyException,_>("Failed to generate hash"))
        }
    }
}



/// A Python module implemented in Rust.
#[pymodule]
fn nchash_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(parse_args,m)?)?;
    m.add_function(wrap_pyfunction!(main,m)?)?;
    m.add_function(wrap_pyfunction!(main_argv,m)?)?;
    m.add_class::<NotNetcdfFileError>()?;
    m.add_class::<NCDataHash>()?;


    Ok(())
}
