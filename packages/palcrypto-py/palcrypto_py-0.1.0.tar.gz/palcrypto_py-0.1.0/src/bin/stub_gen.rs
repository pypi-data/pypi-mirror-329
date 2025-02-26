use pyo3_stub_gen::Result;
use palcrypto_py::stub_info;

fn main() -> Result<()> {
    // `stub_info` is a function defined by `define_stub_info_gatherer!` macro.
    let stub = stub_info()?;
    stub.generate()?;
    Ok(())
}