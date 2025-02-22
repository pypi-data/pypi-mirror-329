use pyo3::prelude::*;
use std::collections::HashMap;
use std::sync::Mutex;

#[pyclass]
struct Vocab {
    map: Mutex<HashMap<String, i32>>,
    default_index: i32,
}

#[pymethods]
impl Vocab {
    #[new]
    fn new() -> Self {
        Vocab {
            map: Mutex::new(HashMap::new()),
            default_index: 0,
        }
    }

    fn __setitem__(&self, key: String, value: i32) {
        let mut map = self.map.lock().unwrap();
        map.insert(key, value);
    }

    fn __getitem__(&self, key: String) -> Option<i32> {
        let map = self.map.lock().unwrap();
        map.get(&key).copied()
    }

    fn __len__(&self) -> usize {
        let map = self.map.lock().unwrap();
        map.len()
    }

    fn __contains__(&self, key: String) -> bool {
        let map = self.map.lock().unwrap();
        map.contains_key(&key)
    }

    fn __delitem__(&self, key: String) {
        let mut map = self.map.lock().unwrap();
        map.remove(&key);
    }

    fn items(&self) -> Vec<(String, i32)> {
        let map = self.map.lock().unwrap();
        map.iter().map(|(k, v)| (k.clone(), *v)).collect()
    }

    fn set_default_index(&mut self, default_index: i32) {
        self.default_index = default_index;
    }

    fn get_default_index(&self) -> i32 {
        self.default_index
    }

    fn keys(&self) -> Vec<String> {
        let map = self.map.lock().unwrap();
        map.keys().cloned().collect()
    }

    fn values(&self) -> Vec<i32> {
        let map = self.map.lock().unwrap();
        map.values().cloned().collect()
    }

    fn clear(&self) {
        let mut map = self.map.lock().unwrap();
        map.clear();
    }
}

#[pymodule]
fn rust_vocab(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Vocab>()?;
    Ok(())
}
