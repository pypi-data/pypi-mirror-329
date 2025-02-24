"""
This module contains helper functions for working with PyVista.
"""

from __future__ import annotations

from typing import List, Any, Dict, Union, Iterable, Tuple

import numpy
from pyvista import ColorLike

from .geom3 import Mesh, Curve3, Vector3, Point3, Iso3
from .metrology import Length3
from .matplotlib import LabelPlace

PlotCoords = Union[Point3, Vector3, Iterable[float]]

try:
    import pyvista
except ImportError:
    pass
else:

    class PlotterHelper:
        def __init__(self, plotter: pyvista.Plotter):
            self.plotter = plotter

        def add_curves(
                self,
                *curves: Curve3,
                color: ColorLike = "w",
                width: float = 5.0,
                label: str | None = None,
                name: str | None = None,
        ) -> List[pyvista.vtkActor]:
            """

            :param curves:
            :param color:
            :param width:
            :param label:
            :param name:
            :return:
            """
            result_list = []
            for curve in curves:
                added = self.plotter.add_lines(
                    curve.points,
                    connected=True,
                    color=color,
                    width=width,
                    label=label,
                    name=name,
                )
                result_list.append(added)

            return result_list

        def add_mesh(self, mesh: Mesh, **kwargs) -> pyvista.vtkActor:
            """

            :param mesh:
            :return:
            """
            if "cmap" in kwargs:
                cmap_extremes = _cmap_extremes(kwargs["cmap"])
                kwargs.update(cmap_extremes)

            prefix = numpy.ones((mesh.faces.shape[0], 1), dtype=mesh.faces.dtype)
            faces = numpy.hstack((prefix * 3, mesh.faces))
            data = pyvista.PolyData(mesh.vertices, faces)
            return self.plotter.add_mesh(data, **kwargs)

        def dimension(
                self,
                length: Length3,
                template: str = "{value:.3f}",
                label_place: LabelPlace = LabelPlace.Outside,
                label_offset: float | None = None,
                text_size: int = 16,
                scale_value: float = 1.0,
        ):
            label_offset = label_offset or max(abs(length.value), 1.0) * 3

            t_a = length.center.scalar_projection(length.a)
            t_b = length.center.scalar_projection(length.b)

            outside = length.center.at_distance(max(t_a, t_b))
            inside = length.center.at_distance(min(t_a, t_b))

            circles = []
            builder = LineBuilder()

            builder.add(inside - length.direction * label_offset * 0.25)
            builder.add(inside)
            circles.append(inside)
            builder.skip()

            circles.append(outside)
            builder.add(outside)
            builder.add(outside + length.direction * label_offset)

            points = numpy.array([_tuplefy(p) for p in circles], dtype=numpy.float64)
            self.plotter.add_points(points, color="black", point_size=4, render_points_as_spheres=True)

            lines = builder.build()
            self.plotter.add_lines(lines, color="black", width=1.5)

            value = length.value * scale_value
            label = pyvista.Label(text=template.format(value=value), position=lines[-1], size=text_size)
            self.plotter.add_actor(label)

        def coordinate_frame(self, iso: Iso3, size: float = 1.0):
            points = numpy.array([[0, 0, 0], [size, 0, 0], [0, size, 0], [0, 0, size]], dtype=numpy.float64)
            points = iso.transform_points(points)

            self.plotter.add_lines(points[[0, 1]], color="red", width=5.0)
            self.plotter.add_lines(points[[0, 2]], color="green", width=5.0)
            self.plotter.add_lines(points[[0, 3]], color="blue", width=5.0)

        def label(self, point: PlotCoords, text: str, **kwargs):
            label = pyvista.Label(text=text, position=_tuplefy(point), **kwargs)
            self.plotter.add_actor(label)

        def arrow(self, start: PlotCoords, direction: PlotCoords,
                  tip_length: float = 0.25,
                  tip_radius: float = 0.1,
                  shaft_radius: float = 0.05,
                  **kwargs):
            pd = pyvista.Arrow(_tuplefy(start), _tuplefy(direction), tip_length=tip_length, tip_radius=tip_radius,
                               shaft_radius=shaft_radius)
            self.plotter.add_mesh(pd, **kwargs, color="black")


    def _cmap_extremes(item: Any) -> Dict[str, ColorLike]:
        working = {}
        try:
            from matplotlib.colors import Colormap
        except ImportError:
            return working
        else:
            if isinstance(item, Colormap):
                over = getattr(item, "_rgba_over", None)
                under = getattr(item, "_rgba_under", None)
                if over is not None:
                    working["above_color"] = over
                if under is not None:
                    working["below_color"] = under
            return working


class LineBuilder:
    def __init__(self):
        self.vertices = []
        self._skip = 1

    def add(self, points: PlotCoords):
        if self.vertices:
            if self._skip > 0:
                self._skip -= 1
            else:
                self.vertices.append(self.vertices[-1])

        self.vertices.append(_tuplefy(points))

    def skip(self):
        self._skip = 2

    def build(self) -> numpy.ndarray:
        return numpy.array(self.vertices, dtype=numpy.float64)


def _tuplefy(item: PlotCoords) -> Tuple[float, float, float]:
    if isinstance(item, (Point3, Vector3)):
        return item.x, item.y, item.z
    else:
        x, y, z, *_ = item
        return x, y, z
