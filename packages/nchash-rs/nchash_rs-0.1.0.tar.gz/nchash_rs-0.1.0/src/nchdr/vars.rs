use crate::nchdr::attrs::format_attr;
use netcdf::{self, types::NcVariableType};

pub fn fmt_var_info(file: &netcdf::File, var_name: &String) -> String {
    // Take reference to a file and a variable in it, and get all the attributes
    // and their values

    let var_opt = file.variables().find(|var| var.name() == *var_name);

    // Nasty - get rid of unwrap if possible.
    let var = var_opt.unwrap();

    let var_attrs: Vec<netcdf::Attribute> = var.attributes().collect();
    let var_dtype = var.vartype();
    let var_dims: &[netcdf::Dimension<'_>] = var.dimensions();

    let var_dimstr = format_dimensions(var_dims);
    let var_typestr = format_type(&var_dtype);

    let attr_str = format_attrs(&var.name(), var_attrs);

    format!(
        "\t{} {}({}) ;\n{}\n",
        var_typestr,
        var.name(),
        var_dimstr,
        attr_str,
    )

}

fn format_dimensions(dims: &[netcdf::Dimension<'_>]) -> String {
    dims.iter()
        .map(|dim| format!("{}", dim.name()))
        .collect::<Vec<String>>()
        .join(", ")
}

fn format_type(nc_type: &NcVariableType) -> String {
    match nc_type {
        NcVariableType::Compound(_) => "compound".to_string(),
        NcVariableType::Opaque(_) => "opaque".to_string(),
        NcVariableType::Enum(_) => "enum".to_string(),
        NcVariableType::Vlen(_) => "vlen".to_string(),
        NcVariableType::Int(_) => "int".to_string(), // Might want to expand this?
        NcVariableType::Float(float_type) => match float_type {
            netcdf::types::FloatType::F32 => "float".to_string(),
            netcdf::types::FloatType::F64 => "double".to_string(),
        },
        NcVariableType::Char => "char".to_string(),
        NcVariableType::String => "string".to_string(),
    }
}

fn format_attrs(varname: &str, attrs: Vec<netcdf::Attribute>) -> String {
    // Like above, except we want to get all attributes.
    attrs
        .iter()
        .map(|attr| {
            format!(
                "\t\t{}:{} = {} ;",
                varname,
                attr.name(),
                format_attr(attr)
            )
        })
        .collect::<Vec<String>>()
        .join("\n")
}
