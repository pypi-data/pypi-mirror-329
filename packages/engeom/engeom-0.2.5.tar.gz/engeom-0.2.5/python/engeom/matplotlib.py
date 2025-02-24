from typing import List, Iterable, Tuple, Union
from enum import Enum
import matplotlib.lines
import numpy
from .geom2 import Curve2, Circle2, Aabb2, Point2, Vector2, SurfacePoint2
from .metrology import Length2

PlotCoords = Union[Point2, Vector2, Iterable[float]]


class LabelPlace(Enum):
    Outside = 1
    Inside = 2
    OutsideRev = 3


try:
    from matplotlib.pyplot import Axes, Circle
    from matplotlib.colors import ListedColormap
except ImportError:
    pass
else:

    class GomColorMap(ListedColormap):
        def __init__(self):
            colors = numpy.array(
                [
                    [1, 0, 160],
                    [1, 0, 255],
                    [0, 254, 255],
                    [0, 160, 0],
                    [0, 254, 0],
                    [255, 255, 0],
                    [255, 128, 0],
                    [255, 1, 0],
                ],
                dtype=numpy.float64,
            )
            colors /= 256.0
            colors = numpy.hstack((colors, numpy.ones((len(colors), 1))))
            super().__init__(colors)
            self.set_under("magenta")
            self.set_over("darkred")

    GOM_CMAP = GomColorMap()

    def set_aspect_fill(ax: Axes):
        """
        Set the aspect ratio of a Matplotlib Axes (subplot) object to be 1:1 in x and y, while also having it expand
        to fill all available space.

        In comparison to the set_aspect('equal') method, this method will also expand the plot to prevent the overall
        figure from shrinking.  It does this by manually re-checking the x and y limits and adjusting whichever is the
        limiting value. Essentially, it will honor the larger of the two existing limits which were set before this
        function was called, and will only expand the limits on the other axis to fill the remaining space.

        Call this function after all visual elements have been added to the plot and any manual adjustments to the axis
        limits are performed. If you use fig.tight_layout(), call this function after that.
        :param ax: a Matplotlib Axes object
        :return: None
        """
        x0, x1 = ax.get_xlim()
        y0, y1 = ax.get_ylim()

        bbox = ax.get_window_extent()
        width, height = bbox.width, bbox.height

        x_scale = width / (x1 - x0)
        y_scale = height / (y1 - y0)

        if y_scale > x_scale:
            y_range = y_scale / x_scale * (y1 - y0)
            y_mid = (y0 + y1) / 2
            ax.set_ylim(y_mid - y_range / 2, y_mid + y_range / 2)
        else:
            x_range = x_scale / y_scale * (x1 - x0)
            x_mid = (x0 + x1) / 2
            ax.set_xlim(x_mid - x_range / 2, x_mid + x_range / 2)

    class AxesHelper:
        def __init__(self, ax: Axes, skip_aspect=False, hide_axes=False):
            self.ax = ax
            if not skip_aspect:
                ax.set_aspect("equal", adjustable="datalim")

            if hide_axes:
                ax.axis("off")

        def set_bounds(self, box: Aabb2):
            """
            Set the bounds of a Matplotlib Axes object.
            :param box: an Aabb2 object
            :return: None
            """
            self.ax.set_xlim(box.min.x, box.max.x)
            self.ax.set_ylim(box.min.y, box.max.y)

        def plot_circle(self, *circle: Circle2 | Iterable[float], **kwargs):
            """
            Plot a circle on a Matplotlib Axes object.
            :param circle: a Circle2 object
            :param kwargs: keyword arguments to pass to the plot function
            :return: None
            """
            from matplotlib.pyplot import Circle

            for cdata in circle:
                if isinstance(cdata, Circle2):
                    c = Circle((cdata.center.x, cdata.center.y), cdata.r, **kwargs)
                else:
                    x, y, r, *_ = cdata
                    c = Circle((x, y), r, **kwargs)
                self.ax.add_patch(c)

        def plot_curve(self, curve: Curve2, **kwargs):
            """
            Plot a curve on a Matplotlib Axes object.
            :param curve: a Curve2 object
            :param kwargs: keyword arguments to pass to the plot function
            :return: None
            """
            self.ax.plot(curve.points[:, 0], curve.points[:, 1], **kwargs)

        def dimension(
            self,
            length: Length2,
            side_shift: float = 0,
            template: str = "{value:.3f}",
            fontsize: int = 10,
            label_place: LabelPlace = LabelPlace.Outside,
            label_offset: float | None = None,
            fontname: str | None = None,
        ):
            pad_scale = self._font_height(12) * 1.5
            center = length.center.shift_orthogonal(side_shift)
            leader_a = center.projection(length.a)
            leader_b = center.projection(length.b)

            if label_place == LabelPlace.Inside:
                label_offset = label_offset or 0.0
                label_coords = center.at_distance(label_offset)
                self.arrow(label_coords, leader_a)
                self.arrow(label_coords, leader_b)
            elif label_place == LabelPlace.Outside:
                label_offset = label_offset or pad_scale * 3
                label_coords = leader_b + length.direction * label_offset
                self.arrow(leader_a - length.direction * pad_scale, leader_a)
                self.arrow(label_coords, leader_b)
            elif label_place == LabelPlace.OutsideRev:
                label_offset = label_offset or pad_scale * 3
                label_coords = leader_a - length.direction * label_offset
                self.arrow(leader_b + length.direction * pad_scale, leader_b)
                self.arrow(label_coords, leader_a)

            # Do we need sideways leaders?
            self._line_if_needed(pad_scale, length.a, leader_a)
            self._line_if_needed(pad_scale, length.b, leader_b)

            kwargs = {"ha": "center", "va": "center", "fontsize": fontsize}
            if fontname is not None:
                kwargs["fontname"] = fontname

            result = self.annotate_text_only(
                template.format(value=length.value),
                label_coords,
                bbox=dict(boxstyle="round,pad=0.3", ec="black", fc="white"),
                **kwargs,
            )

        def _line_if_needed(self, pad: float, actual: Point2, leader_end: Point2):
            half_pad = pad * 0.5
            v: Vector2 = leader_end - actual
            if v.norm() < half_pad:
                return
            work = SurfacePoint2(*actual, *v)
            t1 = work.scalar_projection(leader_end) + half_pad
            self.arrow(actual, work.at_distance(t1), arrow="-")

        def annotate_text_only(self, text: str, pos: PlotCoords, **kwargs):
            """
            Annotate a Matplotlib Axes object with text only.
            :param text: the text to annotate
            :param pos: the position of the annotation
            :param kwargs: keyword arguments to pass to the annotate function
            :return: None
            """
            return self.ax.annotate(text, xy=_tuplefy(pos), **kwargs)

        def arrow(self, start: PlotCoords, end: PlotCoords, arrow="-|>"):
            """
            Plot an arrow on a Matplotlib Axes object.
            :param start: the start point of the arrow
            :param end: the end point of the arrow
            :param kwargs: keyword arguments to pass to the arrow function
            :return: None
            """
            self.ax.annotate(
                "",
                xy=_tuplefy(end),
                xytext=_tuplefy(start),
                arrowprops=dict(arrowstyle=arrow, fc="black"),
            )

        def _font_height(self, font_size: int) -> float:
            """Get the height of a font in data units."""
            fig_dpi = self.ax.figure.dpi
            font_height_inches = font_size * 1.0 / 72.0
            font_height_px = font_height_inches * fig_dpi

            px_per_data = self._get_scale()
            return font_height_px / px_per_data

        def _get_scale(self) -> float:
            """Get the scale of the plot in data units per pixel."""
            x0, x1 = self.ax.get_xlim()
            y0, y1 = self.ax.get_ylim()

            bbox = self.ax.get_window_extent()
            width, height = bbox.width, bbox.height

            # Units are pixels per data unit
            x_scale = width / (x1 - x0)
            y_scale = height / (y1 - y0)

            return min(x_scale, y_scale)

def _tuplefy(item: PlotCoords) -> Tuple[float, float]:
    if isinstance(item, (Point2, Vector2)):
        return item.x, item.y
    else:
        x, y, *_ = item
        return x, y
