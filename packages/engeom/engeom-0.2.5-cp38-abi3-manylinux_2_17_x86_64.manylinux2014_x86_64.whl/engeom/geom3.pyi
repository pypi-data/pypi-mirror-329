from __future__ import annotations

from pathlib import Path
from typing import Tuple, Iterable, List, TypeVar, Iterator, Any

import numpy
from numpy.typing import NDArray
from engeom import DeviationMode, Resample, SelectOp
from .metrology import Length3

Transformable3 = TypeVar("Transformable3", Vector3, Point3, Plane3, Iso3, SurfacePoint3)
PointOrVector3 = TypeVar("PointOrVector3", Vector3, Point3)


class Vector3(Iterable[float]):
    def __init__(self, x: float, y: float, z: float):
        """
        Create a vector in 3D space by specifying the x, y, and z components.
        :param x: the x component of the vector
        :param y: the y component of the vector
        :param z: the z component of the vector
        """
        ...

    @property
    def x(self) -> float:
        ...

    @property
    def y(self) -> float:
        ...

    @property
    def z(self) -> float:
        ...

    def __iter__(self) -> Iterator[float]:
        ...

    def __rmul__(self, other: float) -> Vector3:
        ...

    def __add__(self, other: PointOrVector3) -> PointOrVector3:
        ...

    def __sub__(self, other: Vector3) -> Vector3:
        ...

    def __neg__(self) -> Vector3:
        ...

    def __mul__(self, x: float) -> Vector3:
        ...

    def __truediv__(self, x: float) -> Vector3:
        ...

    def as_numpy(self) -> NDArray[float]:
        """
        Create a numpy array of shape (3,) from the vector.
        """
        ...

    def dot(self, other: Vector3) -> float:
        """
        Calculate the dot product of this vector with another vector.
        :param other: the other vector to calculate the dot product with.
        :return: the dot product of the two vectors.
        """
        ...

    def cross(self, other: Vector3) -> Vector3:
        """
        Calculate the cross product of this vector with another vector.
        :param other: the other vector to calculate the cross product with.
        :return: the cross product of the two vectors.
        """
        ...

    def norm(self) -> float:
        """
        Calculate the norm (length) of the vector.
        :return:
        """

    def normalized(self) -> Vector3:
        """
        Return a normalized version of the vector.
        :return: a new vector that has unit length
        """

    def angle_to(self, other: Vector3) -> float:
        """
        Calculate the smallest angle between this vector and another vector.
        :param other: the other vector to calculate the angle to.
        :return: the angle between the two vectors in radians.
        """
        ...


class Point3(Iterable[float]):
    def __init__(self, x: float, y: float, z: float):
        """
        Create a point in 3D space by specifying the x, y, and z coordinates.

        :param x: the x coordinate of the point
        :param y: the y coordinate of the point
        :param z: the z coordinate of the point
        """
        ...

    @property
    def x(self) -> float:
        ...

    @property
    def y(self) -> float:
        ...

    @property
    def z(self) -> float:
        ...

    def __iter__(self) -> Iterator[float]:
        ...

    @property
    def coords(self) -> Vector3:
        """
        Get the coordinates of the point as a Vector3 object.
        :return: a Vector3 object
        """
        ...

    def __sub__(self, other: PointOrVector3) -> PointOrVector3:
        ...

    def __add__(self, other: Vector3) -> Vector3:
        ...

    def __neg__(self) -> Point3:
        ...

    def __mul__(self, x: float) -> Point3:
        ...

    def __rmul__(self, x: float) -> Point3:
        ...

    def __truediv__(self, x: float) -> Point3:
        ...

    def as_numpy(self) -> NDArray[float]:
        """
        Create a numpy array of shape (2,) from the point.
        """
        ...


class SurfacePoint3:
    def __init__(self, x: float, y: float, z: float, nx: float, ny: float, nz: float):
        """
        Create a surface point in 3D space by specifying the x, y, and z coordinates of the point, as well as the x, y,
        and z components of the normal vector.  The normal components will be normalized before being stored, so they
        do not need to be scaled to unit length before being passed to this constructor.

        :param x: the x coordinate of the point
        :param y: the y coordinate of the point
        :param z: the z coordinate of the point
        :param nx: the x component of the normal vector (will be normalized after construction)
        :param ny: the y component of the normal vector (will be normalized after construction)
        :param nz: the z component of the normal vector (will be normalized after construction)
        """
        ...

    @property
    def point(self) -> Point3:
        """
        Get the coordinates of the point as a Point3 object.
        :return: a Point3 object
        """
        ...

    @property
    def normal(self) -> Vector3:
        """
        Get the normal of the point as a Vector3 object.
        :return: a Vector3 object
        """
        ...

    def at_distance(self, distance: float) -> Point3:
        """
        Get the point at a distance along the normal from the surface point.
        :param distance: the distance to move along the normal.
        :return: the point at the distance along the normal.
        """
        ...

    def scalar_projection(self, point: Point3) -> float:
        """
        Calculate the scalar projection of a point onto the axis defined by the surface point position and direction.
        Positive values indicate that the point is in the normal direction from the surface point, while negative values
        indicate that the point is in the opposite direction.

        :param point: the point to calculate the projection of.
        :return: the scalar projection of the point onto the normal.
        """
        ...

    def projection(self, point: Point3) -> Point3:
        """
        Calculate the projection of a point onto the axis defined by the surface point position and direction.

        :param point: the point to calculate the projection of.
        :return: the projection of the point onto the plane.
        """
        ...

    def reversed(self) -> SurfacePoint3:
        """
        Return a new surface point with the normal vector inverted, but the position unchanged.
        :return: a new surface point with the inverted normal vector.
        """
        ...

    def planar_distance(self, point: Point3) -> float:
        """
        Calculate the planar (non-normal) distance between the surface point and a point. This is complementary to the
        scalar projection. A point is projected onto the plane defined by the position and normal of the surface point,
        and the distance between the surface point position and the projected point is returned.  The value will always
        be positive.

        :param point: the point to calculate the distance to.
        :return: the planar distance between the surface point and the point.
        """
        ...

    def get_plane(self) -> Plane3:
        """
        Get the plane defined by the surface point.
        :return: the plane defined by the surface point.
        """
        ...

    def __mul__(self, other: float) -> SurfacePoint3:
        """
        Multiply the position of the surface point by a scalar value. The normal vector is not affected unless the
        scalar is negative, in which case the normal vector is inverted.
        :param other:
        :return:
        """
        ...

    def __rmul__(self, other: float) -> SurfacePoint3:
        """
        Multiply the position of the surface point by a scalar value. The normal vector is not affected unless the
        scalar is negative, in which case the normal vector is inverted.
        :param other:
        :return:
        """
        ...

    def __truediv__(self, other: float) -> SurfacePoint3:
        """
        Divide the position of the surface point by a scalar value. The normal vector is not affected unless the
        scalar is negative, in which case the normal vector is inverted.
        :param other:
        :return:
        """
        ...

    def __neg__(self) -> SurfacePoint3:
        """
        Invert both the position AND the normal vector of the surface point.
        """
        ...


class Iso3:
    """ An isometry (rigid body transformation) in 3D space. """

    def __init__(self, matrix: NDArray[float]):
        """ Create an isometry from a 4x4 matrix. """
        ...

    @staticmethod
    def identity() -> Iso3:
        """ Return the identity isometry. """
        ...

    @staticmethod
    def from_translation(x: float, y: float, z: float) -> Iso3:
        """ Create an isometry representing a translation. """
        ...

    @staticmethod
    def from_rotation(angle: float, a: float, b: float, c: float) -> Iso3:
        """
        Create an isometry representing a rotation around an axis. The axis will be normalized before the rotation is
        applied.
        :param angle: the angle to rotate by in radians.
        :param a: the x component of the rotation axis.
        :param b: the y component of the rotation axis.
        :param c: the z component of the rotation axis.
        :return: the isometry representing the rotation.
        """
        ...

    def __matmul__(self, other: Transformable3) -> Transformable3:
        """
        Multiply another object by the isometry, transforming it and returning a new object of the same type.
        :param other: an object of one of the transformable types
        :return: a new object of the same type as the input object, transformed by the isometry.
        """
        ...

    def inverse(self) -> Iso3:
        """ Return the inverse of the isometry. """
        ...

    def transform_points(self, points: NDArray[float]) -> NDArray[float]:
        """ Transform a set of points by the isometry. This will transform the points by the rotation and translation
        of the isometry.

        :param points: a numpy array of shape (n, 3) containing the points to transform.
        :return: a numpy array of shape (n, 3) containing the transformed points.
        """
        ...

    def transform_vectors(self, vector: NDArray[float]) -> NDArray[float]:
        """ Transform a set of vectors by the isometry. This will only transform the direction of the vectors, not
        their magnitude.

        :param vector: a numpy array of shape (n, 3) containing the vectors to transform.
        :return: a numpy array of shape (n, 3) containing the transformed vectors.
        """
        ...

    def as_numpy(self) -> NDArray[float]:
        """ Return a copy of the 4x4 matrix representation of the isometry. This is a copy operation. """
        ...

    def flip_around_x(self) -> Iso3:
        """ Return a new isometry that flips the isometry 180° around the x-axis. The origin of the isometry will be
        preserved, but the y and z axes will point in the opposite directions. """
        ...

    def flip_around_y(self) -> Iso3:
        """ Return a new isometry that flips the isometry 180° around the y-axis. The origin of the isometry will be
        preserved, but the x and z axes will point in the opposite directions. """
        ...

    def flip_around_z(self) -> Iso3:
        """ Return a new isometry that flips the isometry 180° around the z-axis. The origin of the isometry will be
        preserved, but the x and y axes will point in the opposite directions. """
        ...


class SvdBasis3:
    """
    A class representing a basis in 3D space. This class is created from a set of points and will calculate the best
    fitting basis for the points using a singular value decomposition.
    """

    def __init__(self, points: NDArray[float], weights: NDArray[float] | None = None):
        """
        Create a basis from a set of points. The basis will be calculated using a singular value decomposition of the
        points.

        :param points: a numpy array of shape (n, 3) containing the points to calculate the basis from.
        :param weights: a numpy array of shape (n,) containing the weights of the points. If None, all points will be
        weighted equally.
        """
        ...

    def to_iso3(self) -> Iso3:
        """
        Produce an isometry which will transform from the world space to the basis space.

        For example, if the basis is created from a set of points that lie in an arbitrary plane, transforming the
        original points by this isometry will move the points such that all points lie on the XY plane.
        :return: the isometry that transforms from the world space to the basis space.
        """
        ...

    def largest(self) -> Vector3:
        """
        Return the largest normalized basis vector.
        :return: a Vector3 object containing the largest basis vector.
        """
        ...

    def smallest(self) -> Vector3:
        """
        Return the smallest normalized basis vector.
        :return: a Vector3 object containing the smallest basis vector.
        """
        ...

    def basis_variances(self) -> NDArray[float]:
        """
        Return the variances of the basis vectors.
        :return: a numpy array of shape (3,) containing the variances of the basis vectors.
        """
        ...

    def basis_stdevs(self) -> NDArray[float]:
        """
        Return the standard deviations of the basis vectors.
        :return: a numpy array of shape (3,) containing the standard deviations of the basis vectors.
        """
        ...

    def rank(self, tol: float) -> int:
        """
        Retrieve the rank of the decomposition by counting the number of singular values that are
        greater than the provided tolerance.  A rank of 0 indicates that all singular values are
        less than the tolerance, and thus the point set is essentially a single point. A rank of 1
        indicates that the point set is essentially a line. A rank of 2 indicates that the point
        set exists roughly in a plane.  The maximum rank is 3, which indicates that the point set
        cannot be reduced to a lower dimension.

        The singular values do not directly have a clear physical meaning. They are square roots of
        the variance multiplied by the number of points used to compute the basis.  Thus, they can
        be interpreted in relation to each other, and when they are very small.

        This method should be used either when you know roughly what a cutoff tolerance for the
        problem you're working on should be, or when you know the cutoff value should be very
        small.  Otherwise, consider examining the standard deviations of the basis vectors
        instead, as they will be easier to interpret (`basis_stdevs()`).
        :param tol: the tolerance to use when determining the rank.
        :return: the rank of the decomposition.
        """
        ...


class Plane3:
    """
    A class representing a plane in 3D space. The plane is represented by a unit normal vector and a distance from the
    origin along the normal vector.
    """

    def __init__(self, a: float, b: float, c: float, d: float):
        """
        Create a plane from the equation ax + by + cz + d = 0.
        :param a: the x value of the unit normal vector.
        :param b: the y value of the unit normal vector.
        :param c: the z value of the unit normal vector.
        :param d: the distance from the origin along the normal vector.
        """
        ...

    def inverted_normal(self) -> Plane3:
        """
        Return a new plane with the normal vector inverted.
        :return: a new plane with the inverted normal vector.
        """
        ...

    def signed_distance_to_point(self, point: Point3) -> float:
        """
        Calculate the signed distance from the plane to a point. The distance will be positive if the point is on the
        same side of the plane as the normal vector, and negative if the point is on the opposite side.
        :param point: the point to calculate the distance to.
        :return: the signed distance from the plane to the point.
        """
        ...

    def project_point(self, point: Point3) -> Point3:
        """
        Project a point onto the plane. The projected point will be the closest point on the plane to the input point.
        :param point: the point to project.
        :return: the projected point.
        """
        ...


class Mesh:
    """
    A class holding an unstructured, 3-dimensional mesh of triangles.
    """

    def __init__(
            self,
            vertices: NDArray[float],
            faces: NDArray[numpy.uint32],
            merge_duplicates: bool = False,
            delete_degenerate: bool = False
    ):
        """
        Create an engeom mesh from vertices and triangles.  The vertices should be a numpy array of shape (n, 3), while
        the triangles should be a numpy array of shape (m, 3) containing the indices of the vertices that make up each
        triangle. The triangles should be specified in counter-clockwise order when looking at the triangle from the
        front/outside.

        :param vertices: a numpy array of shape (n, 3) containing the vertices of the mesh.
        :param faces: a numpy array of shape (m, 3) containing the triangles of the mesh, should be uint.
        :param merge_duplicates: merge duplicate vertices and triangles
        :param delete_degenerate: delete degenerate triangles
        """
        ...

    @property
    def aabb(self) -> Aabb3:
        """ Return the axis-aligned bounding box of the mesh. """
        ...

    @staticmethod
    def load_stl(path: str | Path, merge_duplicates: bool = False, delete_degenerate: bool = False) -> Mesh:
        """
        Load a mesh from an STL file. This will return a new mesh object containing the vertices and triangles from the
        file.  Optional parameters can be used to control the behavior of the loader when handling duplicate vertices/
        triangles and degenerate triangles.

        :param path: the path to the STL file to load.
        :param merge_duplicates: merge duplicate vertices and triangles. If None, the default behavior is to do nothing
        :param delete_degenerate: delete degenerate triangles. If None, the default behavior is to do nothing
        :return: the mesh object containing the data from the file.
        """
        ...

    def write_stl(self, path: str | Path):
        """
        Write the mesh to an STL file. This will write the vertices and triangles of the mesh to the file in binary
        format.

        :param path: the path to the STL file to write.
        """
        ...

    def cloned(self) -> Mesh:
        """
        Will return a copy of the mesh. This is a copy of the data, so modifying the returned mesh will not modify the
        original mesh.

        :return:
        """

    def transform_by(self, iso: Iso3):
        """
        Transforms the vertices of the mesh by an isometry. This will modify the mesh in place.  Any copies made of
        the vertices will no longer match the mesh after this operation.
        :param iso: the isometry to transform the mesh by.
        :return: None
        """
        ...

    def append(self, other: Mesh):
        """
        Append another mesh to this mesh. This will add the vertices and triangles from the other mesh to this mesh,
        changing this one and leaving the other one unmodified.

        :param other: the mesh to append to this mesh, will not be modified in this operation
        """
        ...

    @property
    def vertices(self) -> NDArray[float]:
        """
        Will return an immutable view of the vertices of the mesh as a numpy array of shape (n, 3).
        :return: a numpy array of shape (n, 3) containing the vertices of the mesh.
        """
        ...

    @property
    def faces(self) -> NDArray[numpy.uint32]:
        """
        Will return an immutable view of the triangles of the mesh as a numpy array of shape (m, 3).
        :return: a numpy array of shape (m, 3) containing the triangles of the mesh.
        """
        ...

    def split(self, plane: Plane3) -> Tuple[Mesh | None, Mesh | None]:
        """
        Split the mesh by a plane. The plane will divide the mesh into two possible parts and return them as two new
        objects.  If the part lies entirely on one side of the plane, the other part will be None.

        :param plane: the plane to split the mesh by.

        :return: a tuple of two optional meshes, the first being that on the negative side of the plane, the second being
        that on the positive side of the plane.
        """
        ...

    def deviation(self, points: NDArray[float], mode: DeviationMode) -> NDArray[float]:
        """
        Calculate the deviation between a set of points and their respective closest points on the mesh surface. The
        deviation can be calculated in two modes: absolute and normal. In the absolute mode, the deviation is the
        linear distance between the point and the closest point on the mesh. In the normal mode, the deviation is the
        distance along the normal of the closest point on the mesh.  In both cases, the deviation will be positive if
        the point is outside the surface and negative if the point is inside the surface.

        :param points: a numpy array of shape (n, 3) containing the points to calculate the deviation for.
        :param mode: the mode to calculate the deviation in.
        :return: a numpy array of shape (n,) containing the deviation for each point.
        """
        ...

    def sample_poisson(self, radius: float) -> NDArray[float]:
        """
        Sample the surface of the mesh using a Poisson disk sampling algorithm. This will return a numpy array of points
        and their normals that are approximately evenly distributed across the surface of the mesh. The radius parameter
        controls the minimum distance between points.

        Internally, this algorithm will first re-sample each triangle of the mesh with a dense array of points at a
        maximum distance of radius/2, before applying a random poisson disk sampling algorithm to thin the resampled
        points. This means that the output points are not based on the mesh vertices, so large triangles will not be
        under-represented and small triangles will not be over-represented.

        :param radius: the minimum distance between points.
        :return: a numpy array of shape (n, 6) containing the sampled points.
        """
        ...

    def section(self, plane: Plane3, tol: float | None = None) -> List[Curve3]:
        """
        Calculate and return the intersection curves between the mesh and a plane.

        :param plane:
        :param tol:
        :return:
        """
        ...

    def face_select_none(self) -> MeshTriangleFilter:
        """
        Start a filter operation on the faces of the mesh beginning with no faces selected. This will return a filter
        object that can be used to further add or remove faces from the selection.

        :return: a filter object for the triangles of the mesh.
        """
        ...

    def face_select_all(self) -> MeshTriangleFilter:
        """
        Start a filter operation on the faces of the mesh beginning with all faces selected. This will return a filter
        object that can be used to further add or remove faces from the selection.

        :return: a filter object for the triangles of the mesh.
        """
        ...

    def separate_patches(self) -> List[Mesh]:
        """
        Separate the mesh into connected patches. This will return a list of new mesh objects, each containing one
        connected patch of the original mesh. These objects will be clones of the original mesh, so modifying them will
        have no effect on the original mesh.
        :return:
        """

    def create_from_indices(self, indices: List[int]) -> Mesh:
        """
        Create a new mesh from a list of triangle indices. This will build a new mesh object containing only the
        triangles (and their respective vertices) identified by the given list of indices.  Do not allow duplicate
        indices in the list.
        :param indices: the triangle indices to include in the new mesh
        :return:
        """
        ...

    def measure_point_deviation(self, x: float, y: float, z: float, dist_mode: DeviationMode) -> Length3:
        """
        Compute the deviation of a point from this mesh's surface and return it as a measurement object.

        The deviation is the distance from the point to its closest projection onto the mesh using
        the specified distance mode.  The direction of the measurement is the direction between the
        point and the projection, flipped into the positive half-space of the mesh surface at the
        projection point.

        If the distance is less than a very small floating point epsilon, the direction will be
        taken directly from the mesh surface normal.

        The first point `.a` of the measurement is the reference point, and the second point `.b`
        is the test point.

        :param x: the x component of the point to measure
        :param y: the y component of the point to measure
        :param z: the z component of the point to measure
        :param dist_mode: the deviation mode to use
        :return:
        """

    def boundary_first_flatten(self) -> NDArray[float]:
        """

        :return:
        """

    def surface_closest_to(self, x: float, y: float, z: float) -> SurfacePoint3:
        """
        Find the closest point on the surface of the mesh to a given point in space, returning the point and normal
        in the form of a `SurfacePoint3` object.
        :param x: the x coordinate of the point to find the closest point to
        :param y: the y coordinate of the point to find the closest point to
        :param z: the z coordinate of the point to find the closest point to
        :return: a `SurfacePoint3` object containing the closest point and normal
        """
        ...


class MeshTriangleFilter:
    def collect(self) -> List[int]:
        """
        Collect the final indices of the triangles that passed the filter.
        :return:
        """
        ...

    def create_mesh(self) -> Mesh:
        """
        Create a new mesh from the filtered triangles. This will build a new mesh object containing only the triangles
        (and their respective vertices) that are still retained in the filter.
        :return:
        """
        ...

    def facing(self, x: float, y: float, z: float, angle: float, mode: SelectOp) -> MeshTriangleFilter:
        """

        :param x:
        :param y:
        :param z:
        :param angle:
        :param mode:
        :return:
        """
        ...

    def near_mesh(
            self,
            other: Mesh,
            all_points: bool,
            distance_tol: float,
            mode: SelectOp,
            planar_tol: float | None = None,
            angle_tol: float | None = None,
    ) -> MeshTriangleFilter:
        """
        Reduce the list of indices to only include triangles that are within a certain distance of
        their closest projection onto another mesh. The distance can require that all points of the
        triangle are within the tolerance, or just one.

        There are two additional optional tolerances that can be applied.

        1. A planar tolerance, which checks the distance of the vertex projected onto the plane of
           the reference mesh triangle and looks at how far it is from the projection point. This
           is useful to filter out triangles that go past the edge of the reference mesh.
        2. An angle tolerance, which checks the angle between the normal of the current triangle
           and the normal of the reference triangle. This is useful to filter out triangles that
           are not facing the same direction as the reference mesh.

        :param other: the mesh to use as a reference
        :param all_points: if True, all points of the triangle must be within the tolerance, if False, only one point
        :param distance_tol: the maximum distance between the triangle and its projection onto the reference mesh
        :param mode:
        :param planar_tol: the maximum in-plane distance between the triangle and its projection onto the reference mesh
        :param angle_tol: the maximum angle between the normals of the triangle and the reference mesh
        """
        ...


class CurveStation3:
    """
    A class representing a station along a curve in 3D space. The station is represented by a point on the curve, a
    tangent (direction) vector, and a length along the curve.
    """

    @property
    def point(self) -> Point3:
        """ The 3d position in space on the curve. """
        ...

    @property
    def direction(self) -> Vector3:
        """ The tangent (direction) vector of the curve at the station. """
        ...

    @property
    def direction_point(self) -> SurfacePoint3:
        """
        A `SurfacePoint3` object representing the point on the curve and the curve's tangent/direction vector.
        """
        ...

    @property
    def index(self) -> int:
        """ The index of the previous vertex on the curve, at or before the station. """
        ...

    @property
    def length_along(self) -> float:
        """ The length along the curve from the start of the curve to the station. """
        ...


class Curve3:
    """
    A class representing a polyline in 3D space. The curve is represented by a set of vertices and the segments
    between them.
    """

    def __init__(self, vertices: NDArray[float], tol: float = 1.0e-6):
        """
        Create a curve from a set of vertices. The vertices should be a numpy array of shape (n, 3).

        :param vertices: a numpy array of shape (n, 3) containing the vertices of the curve.
        :param tol: the inherent tolerance of the curve; points closer than this distance will be considered the same.
        """
        ...

    def clone(self) -> Curve3:
        """
        Will return a copy of the curve. This is a copy of the data, so modifying the returned curve will not modify
        the original curve.

        :return: a copy of the curve.
        """
        ...

    def length(self) -> float:
        """
        Return the total length of the curve in the units of the vertices.

        :return: the length of the curve.
        """
        ...

    @property
    def points(self) -> NDArray[float]:
        """
        Will return an immutable view of the vertices of the mesh as a numpy array of shape (n, 3).
        :return: a numpy array of shape (n, 3) containing the vertices of the mesh.
        """
        ...

    def at_length(self, length: float) -> CurveStation3:
        """
        Return a station along the curve at the given length. The length is measured from the start of the curve to the
        station. If the length is greater than the length of the curve or less than 0, an error will be raised.

        :param length: the length along the curve to return the station at.
        :return: a `CurveStation3` object representing the station along the curve.
        """
        ...

    def at_fraction(self, fraction: float) -> CurveStation3:
        """
        Return a station along the curve at the given fraction of the length of the curve. If the fraction is greater
        than 1 or less than 0, an error will be raised.

        :param fraction: the fraction of the length of the curve to return the station at.
        :return: a `CurveStation3` object representing the station along the curve.
        """
        ...

    def at_closest_to_point(self, point: Point3) -> CurveStation3:
        """
        Return a station along the curve at the closest point to the given point. The station will be the point on the
        curve that is closest to the given point.

        :param point: the point to find the closest station to.
        :return: a `CurveStation3` object representing the station along the curve.
        """
        ...

    def at_front(self) -> CurveStation3:
        """
        Return a station at the front of the curve. This is equivalent to calling `at_length(0)`.

        :return: a `CurveStation3` object representing the station at the front of the curve.
        """
        ...

    def at_back(self) -> CurveStation3:
        """
        Return a station at the back of the curve. This is equivalent to calling `at_length(length)`.

        :return: a `CurveStation3` object representing the station at the back of the curve.
        """
        ...

    def resample(self, resample: Resample) -> Curve3:
        """
        Resample the curve using the given resampling method. The resampling method can be one of the following:

        - `Resample.ByCount(count: int)`: resample the curve to have the given number of points.
        - `Resample.BySpacing(distance: float)`: resample the curve to have points spaced by the given distance.
        - `Resample.ByMaxSpacing(distance: float)`: resample the curve to have points spaced by a maximum distance.

        :param resample: the resampling method to use.
        :return: a new curve object with the resampled vertices.
        """
        ...

    def simplify(self, tolerance: float) -> Curve3:
        """
        Simplify the curve using the Ramer-Douglas-Peucker algorithm. This will remove vertices from the curve that are
        within the given tolerance of the line between the previous and next vertices.

        :param tolerance: the tolerance to use when simplifying the curve.
        :return: a new curve object with the simplified vertices.
        """
        ...

    def transformed_by(self, iso: Iso3) -> Curve3:
        """
        Transform the curve by an isometry. This will return a new curve object with the transformed vertices.

        :param iso: the isometry to transform the curve by.
        :return: a new curve object with the transformed vertices.
        """
        ...


class Aabb3:
    """
    A class representing an axis-aligned bounding box in 3D space. The box is defined by its minimum and maximum
    """

    def __init__(self, x_min: float, y_min: float, z_min: float, x_max: float, y_max: float, z_max: float):
        """
        Create an axis-aligned bounding box from the minimum and maximum coordinates.
        :param x_min: the minimum x coordinate of the box.
        :param y_min: the minimum y coordinate of the box.
        :param z_min: the minimum z coordinate of the box.
        :param x_max: the maximum x coordinate of the box.
        :param y_max: the maximum y coordinate of the box.
        :param z_max: the maximum z coordinate of the box.
        """
        ...

    @property
    def min(self) -> Point3:
        """ The minimum point of the box. """
        ...

    @property
    def max(self) -> Point3:
        """ The maximum point of the box. """
        ...

    @property
    def center(self) -> Point3:
        """ The center point of the box. """
        ...

    @property
    def extent(self) -> Vector3:
        """ The extent of the box. """
        ...

    @staticmethod
    def at_point(x: float, y: float, z: float, w: float, h: float | None = None, l: float | None = None) -> Aabb3:
        """
        Create an AABB centered at a point with a given width and height.
        :param x: the x-coordinate of the center of the AABB.
        :param y: the y-coordinate of the center of the AABB.
        :param z: the z-coordinate of the center of the AABB.
        :param w: the width of the AABB.
        :param h: the height of the AABB. If not provided, the AABB will be square.
        :param l: the length of the AABB. If not provided, the AABB will be square.
        :return: a new AABB object.
        """
        ...

    @staticmethod
    def from_points(points: NDArray[float]) -> Aabb3:
        """
        Create an AABB that bounds a set of points. If the point array is empty or the wrong shape, an error will be
        thrown.
        :param points: a numpy array of shape (N, 2) containing the points to bound
        :return: a new AABB object
        """
        ...

    def expand(self, d: float) -> Aabb3:
        """
        Expand the AABB by a given distance in all directions. The resulting height and
        width will be increased by 2 * d.

        :param d: the distance to expand the AABB by.
        :return: a new AABB object with the expanded bounds.
        """
        ...

    def shrink(self, d: float) -> Aabb3:
        """
        Shrink the AABB by a given distance in all directions. The resulting height and
        width will be decreased by 2 * d.

        :param d: the distance to shrink the AABB by.
        :return: a new AABB object with the shrunk bounds.
        """
        ...
