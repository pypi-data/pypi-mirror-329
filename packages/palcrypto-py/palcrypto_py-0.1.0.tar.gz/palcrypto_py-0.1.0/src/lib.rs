use pyo3::prelude::*;
use palcrypto_rs::aes_crypto::{generate_pal_aes_key, pal_aes_decrypt, pal_aes_encrypt};
use palcrypto_rs::crypto_box_crypto::{generate_pal_key_pair, pal_cb_decrypt, pal_cb_encrypt};

#[pyfunction]
fn generate_aes_key() -> PyResult<Vec<u8>>{
    let key = generate_pal_aes_key();
    Ok(key.as_bytes())
}

#[pyfunction]
fn aes_encrypt(pal_aes_key_bytes: Vec<u8>, plain_bytes:Vec<u8>) -> PyResult<Vec<u8>> {
    let encrypted_bytes = pal_aes_encrypt(pal_aes_key_bytes.as_slice(), plain_bytes.as_slice()).unwrap();
    Ok(encrypted_bytes)
}

#[pyfunction]
fn aes_decrypt(
    pal_aes_key_bytes: Vec<u8>, encrypted_bytes: Vec<u8>,
    nonce_len: Option<usize>) -> PyResult<Vec<u8>> {
    let decrypted_bytes = pal_aes_decrypt(pal_aes_key_bytes.as_slice(), encrypted_bytes.as_slice(), nonce_len).unwrap();
    Ok(decrypted_bytes)
}


#[pyclass]
struct CbKeyPair{
    #[warn(dead_code)]
    pub public_key_bytes: Vec<u8>,
    #[warn(dead_code)]
    pub private_key_bytes: Vec<u8>,
}


#[pymethods]
impl CbKeyPair {
    #[new]
    fn new(public_key_bytes: Vec<u8>, private_key_bytes: Vec<u8>) -> Self {
        Self {public_key_bytes, private_key_bytes}
    }

    fn __str__(&self) -> String{
        format!("Pub: {:?} Pri: {:?}", self.public_key_bytes, self.private_key_bytes)
    }

    #[getter]
    fn public_key_bytes(&self) -> PyResult<Vec<u8>>{
        Ok(self.public_key_bytes.clone())
    }

    #[getter]
    fn private_key_bytes(&self) -> PyResult<Vec<u8>>{
        Ok(self.private_key_bytes.clone())
    }
}

#[pyfunction]
fn generate_cb_key_pair() -> PyResult<CbKeyPair>{
    let key_pair = generate_pal_key_pair();
    Ok(CbKeyPair{public_key_bytes: key_pair.public_key_bytes.to_vec(), private_key_bytes: key_pair.secret_key_bytes
        .to_vec()})
}

#[pyfunction]
fn cb_encrypt(
    peer_pal_crypto_public_key_bytes: Vec<u8>,
    my_pal_crypto_secret_key_bytes: Vec<u8>,
    plain_bytes: Vec<u8>
) -> PyResult<Vec<u8>> {
    let encrypted_bytes = pal_cb_encrypt(peer_pal_crypto_public_key_bytes.as_slice(), my_pal_crypto_secret_key_bytes.as_slice(), plain_bytes.as_slice()).unwrap();
    Ok(encrypted_bytes)
}

#[pyfunction]
fn cb_decrypt(
    peer_pal_crypto_public_key_bytes: Vec<u8>,
    my_pal_crypto_secret_key_bytes: Vec<u8>, encrypted_bytes: Vec<u8>, nonce_len: Option<usize>) -> PyResult<Vec<u8>> {
    let decrypted_bytes = pal_cb_decrypt(peer_pal_crypto_public_key_bytes.as_slice(), my_pal_crypto_secret_key_bytes.as_slice(), encrypted_bytes.as_slice(), nonce_len).unwrap();
    Ok(decrypted_bytes)
}


/// A Python module implemented in Rust.
#[pymodule]
fn palcrypto_py(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_aes_key, m)?)?;
    m.add_function(wrap_pyfunction!(aes_encrypt, m)?)?;
    m.add_function(wrap_pyfunction!(aes_decrypt, m)?)?;

    m.add_class::<CbKeyPair>()?;
    m.add_function(wrap_pyfunction!(generate_cb_key_pair, m)?)?;
    m.add_function(wrap_pyfunction!(cb_encrypt, m)?)?;
    m.add_function(wrap_pyfunction!(cb_decrypt, m)?)?;
    Ok(())
}


