use crate::bounding::Aabb3;
use crate::common::{DeviationMode, SelectOp};
use crate::conversions::{array_to_faces, array_to_points3, faces_to_array, points_to_array3};
use crate::geom3::{Curve3, Iso3, Plane3, SurfacePoint3};
use crate::metrology::Length3;
use engeom::common::points::dist;
use engeom::common::{Selection, SplitResult};
use numpy::ndarray::{Array1, ArrayD};
use numpy::{IntoPyArray, PyArray1, PyArrayDyn, PyReadonlyArrayDyn};
use pyo3::exceptions::{PyIOError, PyValueError};
use pyo3::prelude::*;
use std::path::PathBuf;

#[pyclass]
pub struct Mesh {
    inner: engeom::Mesh,
    vertices: Option<Py<PyArrayDyn<f64>>>,
    faces: Option<Py<PyArrayDyn<u32>>>,
}

impl Mesh {
    pub fn get_inner(&self) -> &engeom::Mesh {
        &self.inner
    }

    pub fn from_inner(inner: engeom::Mesh) -> Self {
        Self {
            inner,
            vertices: None,
            faces: None,
        }
    }
}

impl Clone for Mesh {
    fn clone(&self) -> Self {
        Self::from_inner(self.inner.clone())
    }
}

#[pymethods]
impl Mesh {
    #[new]
    #[pyo3(signature=(vertices, faces, merge_duplicates = false, delete_degenerate = false))]
    fn new<'py>(
        vertices: PyReadonlyArrayDyn<'py, f64>,
        faces: PyReadonlyArrayDyn<'py, u32>,
        merge_duplicates: bool,
        delete_degenerate: bool,
    ) -> PyResult<Self> {
        let vertices = array_to_points3(&vertices.as_array())?;
        let faces = array_to_faces(&faces.as_array())?;
        let mesh = engeom::Mesh::new_with_options(
            vertices,
            faces,
            false,
            merge_duplicates,
            delete_degenerate,
            None,
        )
        .map_err(|e| PyValueError::new_err(e.to_string()))?;

        Ok(Self::from_inner(mesh))
    }

    #[getter]
    fn aabb(&self) -> Aabb3 {
        Aabb3::from_inner(*self.inner.aabb())
    }

    #[staticmethod]
    #[pyo3(signature=(path, merge_duplicates = false, delete_degenerate = false))]
    fn load_stl(path: PathBuf, merge_duplicates: bool, delete_degenerate: bool) -> PyResult<Self> {
        let mesh = engeom::io::read_mesh_stl(&path, merge_duplicates, delete_degenerate)
            .map_err(|e| PyIOError::new_err(e.to_string()))?;

        Ok(Self::from_inner(mesh))
    }

    fn transform_by(&mut self, iso: &Iso3) {
        self.inner.transform(iso.get_inner());
    }

    fn surface_closest_to(&self, x: f64, y: f64, z: f64) -> SurfacePoint3 {
        let p = engeom::Point3::new(x, y, z);
        SurfacePoint3::from_inner(self.inner.surf_closest_to(&p))
    }

    fn append(&mut self, other: &Mesh) -> PyResult<()> {
        self.inner
            .append(&other.inner)
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }

    fn cloned(&self) -> Self {
        self.clone()
    }

    fn write_stl(&self, path: PathBuf) -> PyResult<()> {
        engeom::io::write_mesh_stl(&path, &self.inner)
            .map_err(|e| PyIOError::new_err(e.to_string()))
    }

    #[getter]
    fn vertices<'py>(&mut self, py: Python<'py>) -> &Bound<'py, PyArrayDyn<f64>> {
        if self.vertices.is_none() {
            let array = points_to_array3(self.inner.vertices());
            self.vertices = Some(array.into_pyarray(py).unbind());
        }
        self.vertices.as_ref().unwrap().bind(py)
    }

    #[getter]
    fn faces<'py>(&mut self, py: Python<'py>) -> &Bound<'py, PyArrayDyn<u32>> {
        if self.faces.is_none() {
            let faces = faces_to_array(self.inner.faces());
            self.faces = Some(faces.into_pyarray(py).unbind());
        }

        self.faces.as_ref().unwrap().bind(py)
    }

    fn __repr__(&self) -> String {
        format!(
            "<Mesh {} vertices, {} faces>",
            self.inner.vertices().len(),
            self.inner.faces().len()
        )
    }

    fn split(&self, plane: &Plane3) -> PyResult<(Option<Self>, Option<Self>)> {
        match self.inner.split(&plane.inner) {
            SplitResult::Pair(mesh1, mesh2) => {
                Ok((Some(Self::from_inner(mesh1)), Some(Self::from_inner(mesh2))))
            }
            SplitResult::Negative => Ok((Some(self.clone()), None)),
            SplitResult::Positive => Ok((None, Some(self.clone()))),
        }
    }

    fn deviation<'py>(
        &self,
        py: Python<'py>,
        points: PyReadonlyArrayDyn<'py, f64>,
        mode: DeviationMode,
    ) -> PyResult<Bound<'py, PyArray1<f64>>> {
        let points = array_to_points3(&points.as_array())?;
        let mut result = Array1::zeros(points.len());

        for (i, point) in points.iter().enumerate() {
            let closest = self.inner.surf_closest_to(point);
            let normal_dev = closest.scalar_projection(point);

            result[i] = match mode {
                // Copy the sign of the normal deviation
                DeviationMode::Point => dist(&closest.point, point) * normal_dev.signum(),
                DeviationMode::Plane => normal_dev,
            }
        }

        Ok(result.into_pyarray(py))
    }

    fn measure_point_deviation(&self, x: f64, y: f64, z: f64, dist_mode: DeviationMode) -> Length3 {
        let point = engeom::Point3::new(x, y, z);
        Length3::from_inner(self.inner.measure_point_deviation(&point, dist_mode.into()))
    }

    fn boundary_first_flatten<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyArrayDyn<f64>>> {
        let edges = self
            .inner
            .calc_edges()
            .map_err(|e| PyValueError::new_err(e.to_string()))?;

        let values = edges
            .boundary_first_flatten()
            .map_err(|e| PyValueError::new_err(e.to_string()))?;

        let mut result = ArrayD::zeros(vec![values.len(), 2]);
        for (i, p) in values.iter().enumerate() {
            result[[i, 0]] = p.x;
            result[[i, 1]] = p.y;
        }

        Ok(result.into_pyarray(py))
    }

    fn sample_poisson<'py>(&self, py: Python<'py>, radius: f64) -> Bound<'py, PyArrayDyn<f64>> {
        let sps = self.inner.sample_poisson(radius);
        let mut result = ArrayD::zeros(vec![sps.len(), 6]);
        for (i, sp) in sps.iter().enumerate() {
            result[[i, 0]] = sp.point.x;
            result[[i, 1]] = sp.point.y;
            result[[i, 2]] = sp.point.z;
            result[[i, 3]] = sp.normal.x;
            result[[i, 4]] = sp.normal.y;
            result[[i, 5]] = sp.normal.z;
        }
        result.into_pyarray(py)
    }

    #[pyo3(signature=(plane, tol = None))]
    fn section(&self, plane: Plane3, tol: Option<f64>) -> PyResult<Vec<Curve3>> {
        let results = self
            .inner
            .section(plane.get_inner(), tol)
            .map_err(|e| PyValueError::new_err(e.to_string()))?;

        Ok(results.into_iter().map(Curve3::from_inner).collect())
    }

    fn face_select_all<'py>(
        slf: PyRef<Self>,
        py: Python<'py>,
    ) -> PyResult<Bound<'py, MeshTriangleFilter>> {
        let indices = slf.inner.face_select(Selection::All).collect();
        MeshTriangleFilter {
            mesh: slf.into(),
            indices,
        }
        .into_pyobject(py)
    }

    fn face_select_none<'py>(
        slf: PyRef<Self>,
        py: Python<'py>,
    ) -> PyResult<Bound<'py, MeshTriangleFilter>> {
        let indices = slf.inner.face_select(Selection::None).collect();
        MeshTriangleFilter {
            mesh: slf.into(),
            indices,
        }
        .into_pyobject(py)
    }

    fn create_from_indices(&self, indices: Vec<usize>) -> Self {
        Self::from_inner(self.inner.create_from_indices(&indices))
    }

    fn separate_patches(&self) -> Vec<Self> {
        let patch_groups = self.inner.get_patches();
        patch_groups
            .into_iter()
            .map(|indices| self.create_from_indices(indices))
            .collect()
    }
}

#[pyclass]
pub struct MeshTriangleFilter {
    mesh: Py<Mesh>,
    indices: Vec<usize>,
}

#[pymethods]
impl MeshTriangleFilter {
    fn __repr__(&self) -> String {
        format!("<MeshTriangleFilter {} triangles>", self.indices.len())
    }

    fn facing<'py>(
        mut slf: PyRefMut<'py, Self>,
        py: Python<'py>,
        x: f64,
        y: f64,
        z: f64,
        angle: f64,
        mode: SelectOp,
    ) -> PyResult<Bound<'py, Self>> {
        let normal = engeom::UnitVec3::new_normalize([x, y, z].into());
        let temp = slf.mesh.bind(py).borrow();
        let i = slf.indices.clone();
        slf.indices = temp
            .inner
            .face_select(Selection::Indices(i))
            .facing(&normal, angle, mode.into())
            .collect();
        slf.into_pyobject(py)
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }

    #[pyo3(signature=(other, all_points, distance_tol, mode, planar_tol = None, angle_tol = None))]
    fn near_mesh<'py>(
        mut slf: PyRefMut<'py, Self>,
        py: Python<'py>,
        other: PyRef<Mesh>,
        all_points: bool,
        distance_tol: f64,
        mode: SelectOp,
        planar_tol: Option<f64>,
        angle_tol: Option<f64>,
    ) -> PyResult<Bound<'py, Self>> {
        let temp = slf.mesh.bind(py).borrow();
        let i = slf.indices.clone();
        slf.indices = temp
            .inner
            .face_select(Selection::Indices(i))
            .near_mesh(
                &other.inner,
                all_points,
                distance_tol,
                planar_tol,
                angle_tol,
                mode.into(),
            )
            .collect();
        slf.into_pyobject(py)
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }

    fn collect(&self) -> Vec<usize> {
        self.indices.clone()
    }

    fn create_mesh(&self, py: Python<'_>) -> Mesh {
        self.mesh
            .bind(py)
            .borrow()
            .create_from_indices(self.indices.clone())
    }
}
