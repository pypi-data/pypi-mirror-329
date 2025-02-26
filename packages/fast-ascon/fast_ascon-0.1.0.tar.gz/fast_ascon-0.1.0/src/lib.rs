use ascon_aead::{Ascon128, Ascon128a, Ascon80pq, Key, Nonce}; 
use ascon_aead::aead::{Aead, KeyInit, Payload};

use ascon_hash::{AsconAHash, AsconHash, Digest};
use pyo3::exceptions::PyException;
use pyo3::{prelude::*, types::*};

#[pyfunction]
fn encrypt(key: &[u8], nonce: &[u8], associateddata: &[u8], plaintext: &[u8], variant: &str) -> PyResult<Vec<u8>> {

    let payload = Payload { msg: plaintext, aad: associateddata };

    if variant == "Ascon-128" {
        let key = Key::<Ascon128>::from_slice(key);
        let cipher = Ascon128::new(key);

        let nonce = Nonce::<Ascon128>::from_slice(nonce);

        let ciphertext = cipher.encrypt(nonce, payload);

        match ciphertext {
            Ok(result) => Ok(result),
            Err(_) => Err(PyException::new_err("encryption failed"))
        }

    } else if variant == "Ascon-128a" {
        let key = Key::<Ascon128a>::from_slice(key);
        let cipher = Ascon128a::new(key);

        let nonce = Nonce::<Ascon128a>::from_slice(nonce);

        let ciphertext = cipher.encrypt(nonce, payload);

        match ciphertext {
            Ok(result) => Ok(result),
            Err(_) => Err(PyException::new_err("encryption failed"))
        }
    } else if variant == "Ascon-80pq" {
        let key = Key::<Ascon80pq>::from_slice(key);
        let cipher = Ascon80pq::new(key);

        let nonce = Nonce::<Ascon80pq>::from_slice(nonce);

        let ciphertext = cipher.encrypt(nonce, payload);

        match ciphertext {
            Ok(result) => Ok(result),
            Err(_) => Err(PyException::new_err("encryption failed"))
        }
    } else {
        Err(PyException::new_err("unsupported variant"))
    }
}

#[pyfunction]
fn decrypt(key: &[u8], nonce: &[u8], associateddata: &[u8], ciphertext: &[u8], variant: &str) -> PyResult<Vec<u8>> {
    let payload = Payload { msg: ciphertext, aad: associateddata };

    if variant == "Ascon-128" {
        let key = Key::<Ascon128>::from_slice(key);
        let cipher = Ascon128::new(key);

        let nonce = Nonce::<Ascon128>::from_slice(nonce);

        let ciphertext = cipher.decrypt(nonce, payload);

        match ciphertext {
            Ok(result) => Ok(result),
            Err(_) => Err(PyException::new_err("encryption failed"))
        }

    } else if variant == "Ascon-128a" {
        let key = Key::<Ascon128a>::from_slice(key);
        let cipher = Ascon128a::new(key);

        let nonce = Nonce::<Ascon128a>::from_slice(nonce);

        let ciphertext = cipher.decrypt(nonce, payload);

        match ciphertext {
            Ok(result) => Ok(result),
            Err(_) => Err(PyException::new_err("encryption failed"))
        }
    } else if variant == "Ascon-80pq" {
        let key = Key::<Ascon80pq>::from_slice(key);
        let cipher = Ascon80pq::new(key);

        let nonce = Nonce::<Ascon80pq>::from_slice(nonce);

        let ciphertext = cipher.encrypt(nonce, payload);

        match ciphertext {
            Ok(result) => Ok(result),
            Err(_) => Err(PyException::new_err("encryption failed"))
        }
    } else {
        Err(PyException::new_err("unsupported variant"))
    }
}

#[pyfunction]
fn hash(message: &[u8], variant: &str) -> PyResult<Vec<u8>> {
    if variant == "Ascon-Hash" {
        let mut hasher = AsconHash::new();
        hasher.update(message);
        let digest = hasher.finalize();
        Ok(digest.to_vec())
    } else if variant == "Ascon-Hasha" {
        let mut hasher = AsconAHash::new();
        hasher.update(message);
        let digest = hasher.finalize();
        Ok(digest.to_vec())
    } else {
        Err(PyException::new_err("invalid variant"))
    }
}
/// A Python module implemented in Rust.
#[pymodule]
fn fast_ascon(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(encrypt, m)?)?;
    m.add_function(wrap_pyfunction!(decrypt, m)?)?;
    m.add_function(wrap_pyfunction!(hash, m)?)?;


    Ok(())
}
