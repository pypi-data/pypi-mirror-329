#![allow(clippy::unused_unit)]
use std::fmt::Write;

use capitol::Citation;
use polars::prelude::*;
use pyo3_polars::derive::polars_expr;

#[polars_expr(output_type=String)]
fn cdg_url(inputs: &[Series]) -> PolarsResult<Series> {
    let s = &inputs[0];
    let ca = s.str()?;
    let out: StringChunked = ca.apply_into_string_amortized(|value: &str, output: &mut String| {
        write!(output, "{}", Citation::parse(value).unwrap().to_url()).unwrap();
    });
    Ok(out.into_series())
}
