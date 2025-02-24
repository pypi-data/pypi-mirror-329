use crate::geom2::{Point2, SurfacePoint2, Vector2};
use crate::geom3::{Point3, SurfacePoint3, Vector3};
use engeom::metrology::Measurement;
use engeom::UnitVec2;
use pyo3::prelude::*;

#[pyclass]
pub struct Length2 {
    inner: engeom::metrology::Length2,
}

impl Length2 {
    pub fn get_inner(&self) -> &engeom::metrology::Length2 {
        &self.inner
    }

    pub fn from_inner(inner: engeom::metrology::Length2) -> Self {
        Self { inner }
    }
}

#[pymethods]
impl Length2 {
    fn __repr__(&self) -> String {
        format!(
            "Length2(a=({}, {}), b=({}, {}), direction=({}, {}))",
            self.inner.a.x,
            self.inner.a.y,
            self.inner.b.x,
            self.inner.b.y,
            self.inner.direction.x,
            self.inner.direction.y,
        )
    }

    #[new]
    #[pyo3(signature=(a, b, direction = None))]
    pub fn new(a: Point2, b: Point2, direction: Option<Vector2>) -> Self {
        let d = direction.map(|v| UnitVec2::new_normalize(*v.get_inner()));
        Self::from_inner(engeom::metrology::Length2::new(
            *a.get_inner(),
            *b.get_inner(),
            d,
        ))
    }

    #[getter]
    pub fn value(&self) -> f64 {
        self.inner.value()
    }

    #[getter]
    pub fn a(&self) -> Point2 {
        Point2::from_inner(self.inner.a)
    }

    #[getter]
    pub fn b(&self) -> Point2 {
        Point2::from_inner(self.inner.b)
    }

    #[getter]
    pub fn direction(&self) -> Vector2 {
        Vector2::from_inner(self.inner.direction.into_inner())
    }

    #[getter]
    pub fn center(&self) -> SurfacePoint2 {
        SurfacePoint2::from_inner(self.inner.center())
    }

    fn reversed(&self) -> Self {
        Self::from_inner(self.inner.reversed())
    }
}

#[pyclass]
pub struct Length3 {
    inner: engeom::metrology::Length3,
}

impl Length3 {
    pub fn get_inner(&self) -> &engeom::metrology::Length3 {
        &self.inner
    }

    pub fn from_inner(inner: engeom::metrology::Length3) -> Self {
        Self { inner }
    }
}

#[pymethods]
impl Length3 {
    fn __repr__(&self) -> String {
        format!(
            "Length3(a=({}, {}, {}), b=({}, {}, {}), direction=({}, {}, {}))",
            self.inner.a.x,
            self.inner.a.y,
            self.inner.a.z,
            self.inner.b.x,
            self.inner.b.y,
            self.inner.b.z,
            self.inner.direction.x,
            self.inner.direction.y,
            self.inner.direction.z,
        )
    }

    #[new]
    #[pyo3(signature=(a, b, direction = None))]
    pub fn new(a: Point3, b: Point3, direction: Option<Vector3>) -> Self {
        let d = direction.map(|v| engeom::UnitVec3::new_normalize(*v.get_inner()));
        Self::from_inner(engeom::metrology::Length3::new(
            *a.get_inner(),
            *b.get_inner(),
            d,
        ))
    }

    #[getter]
    pub fn value(&self) -> f64 {
        self.inner.value()
    }

    #[getter]
    pub fn a(&self) -> Point3 {
        Point3::from_inner(self.inner.a)
    }

    #[getter]
    pub fn b(&self) -> Point3 {
        Point3::from_inner(self.inner.b)
    }

    #[getter]
    pub fn direction(&self) -> Vector3 {
        Vector3::from_inner(self.inner.direction.into_inner())
    }

    #[getter]
    pub fn center(&self) -> SurfacePoint3 {
        SurfacePoint3::from_inner(self.inner.center())
    }

    fn reversed(&self) -> Self {
        Self::from_inner(self.inner.reversed())
    }
}
