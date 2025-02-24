from .geom2 import Point2, Vector2, SurfacePoint2
from .geom3 import Point3, Vector3, SurfacePoint3


class Length2:
    def __init__(self, a: Point2, b: Point2, direction: Vector2 | None = None):
        """

        :param a:
        :param b:
        :param direction:
        """
        ...

    @property
    def a(self) -> Point2:
        ...

    @property
    def b(self) -> Point2:
        ...

    @property
    def direction(self) -> Vector2:
        ...

    @property
    def value(self) -> float:
        ...

    @property
    def center(self) -> SurfacePoint2:
        ...


class Length3:
    def __init__(self, a: Point3, b: Point3, direction: Vector3 | None = None):
        """

        :param a:
        :param b:
        :param direction:
        """
        ...

    @property
    def a(self) -> Point3:
        ...

    @property
    def b(self) -> Point3:
        ...

    @property
    def direction(self) -> Vector3:
        ...

    @property
    def value(self) -> float:
        ...

    @property
    def center(self) -> SurfacePoint3:
        ...
