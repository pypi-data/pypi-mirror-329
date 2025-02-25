""" high level timeline API classes """
from datetime import datetime
from pathlib import Path
from typing import Optional

from svg_timeline.geometry import Vector
from svg_timeline.style import Defaults, DEFAULT_CSS, ClassNames
from svg_timeline.svg import SVG
from svg_timeline.svg_primitives import Rectangle, Line, Text, Circle, Image
from svg_timeline.time_calculations import TimeGradient, TimeSpacing


class TimelinePlot:
    """ representation of a timeline plot
    dates, timespans etc. can be added to this timeline via method calls
    """
    def __init__(self, start_date: datetime, end_date: datetime,
                 time_spacing: TimeSpacing, minor_tics: Optional[TimeSpacing] = None,
                 size: tuple[int, int] = (800, 600)):
        self._width, self._height = size
        self._svg = SVG(self._width, self._height, style=DEFAULT_CSS)

        y = Defaults.arrow_y_position * self._height
        x1 = Defaults.arrow_x_padding * self._width
        x2 = (1 - Defaults.arrow_x_padding) * self._width
        self._time = TimeGradient(source=Vector(x1, y), target=Vector(x2, y),
                                  start_date=start_date, end_date=end_date)
        self._tics = time_spacing
        self._tics_minor = minor_tics
        self._add_timeline()

    def _add_timeline(self):
        line = Line(self._time.source, self._time.target, classes=[ClassNames.TIMEAXIS])
        self._svg.elements.append(line)
        timeline_delta = self._time.target - self._time.source
        tic_delta = 10 * timeline_delta.orthogonal()
        for date, label in zip(self._tics.dates, self._tics.labels):
            tic_base = self._time.date_to_coord(date)
            tic_end = tic_base + tic_delta
            text_start = tic_base + 1.5 * tic_delta
            self._svg.elements.append(Line(source=tic_base, target=tic_end, classes=[ClassNames.MAJOR_TICK]))
            self._svg.elements.append(Text(text_start, label, classes=[ClassNames.MAJOR_TICK]))
        if self._tics_minor is None:
            return
        for date in self._tics_minor.dates:
            tic_base = self._time.date_to_coord(date)
            tic_end = tic_base + 0.5 * tic_delta
            self._svg.elements.append(Line(source=tic_base, target=tic_end, classes=[ClassNames.MINOR_TICK]))

    def add_event(self, date: datetime, text: str,
                  lane: int = 1, classes: Optional[list[str]] = None):
        """ Add an event to the timeline that happened at a single point in time """
        classes = classes or []
        classes += [ClassNames.EVENT]
        event_base = self._time.date_to_coord(date)
        event_end = self.__to_lane_point(date, lane=lane)
        text_coord = self.__to_lane_point(date, lane=(lane+0.5 if lane >= 0 else lane-0.5))
        self._svg.elements += [
            Line(source=event_base, target=event_end, classes=classes),
            Circle(center=event_end, radius=Defaults.event_dot_radius, classes=classes),
            Text(text_coord, text, classes=classes),
        ]

    def add_image(self, date: datetime, image_path: Path, height: float, width: float,
                  lane: int = 1, classes: Optional[list[str]] = None):
        """ Add an image to the timeline that is associated with a single point in time """
        classes = classes or []
        classes += [ClassNames.IMAGE]
        event_base = self._time.date_to_coord(date)
        event_end = self.__to_lane_point(date, lane=lane)
        image_center_left = event_end + height * self.lane_normal
        image_top_left = image_center_left + width/2 * self.lane_normal.orthogonal(ccw=True)
        self._svg.elements += [
            Line(source=event_base, target=event_end, classes=classes),
            Image(top_left=image_top_left, file=image_path, height=height, width=width, classes=classes),
        ]

    def add_timespan(self, start_date: datetime, end_date: datetime, text: str,
                     lane: int = 1, width: Optional[int] = None, classes: Optional[list[str]] = None):
        """ Add an entry to the timeline that is associated with a certain time span """
        classes = classes or []
        classes += [ClassNames.TIMESPAN]
        width = width or Defaults.timespan_width
        half_width_vector = width/2 * self.lane_normal
        if Defaults.timespan_use_start_stilt:
            on_timeline = self.__to_lane_point(start_date, lane=0)
            bottom_timespan = self.__to_lane_point(start_date, lane=lane) - half_width_vector
            self._svg.elements.append(Line(source=on_timeline, target=bottom_timespan, classes=classes))
        if Defaults.timespan_use_end_stilt:
            on_timeline = self.__to_lane_point(end_date, lane=0)
            bottom_timespan = self.__to_lane_point(end_date, lane=lane) - half_width_vector
            self._svg.elements.append(Line(source=on_timeline, target=bottom_timespan, classes=classes))
        start_corner = self.__to_lane_point(start_date, lane=lane) + half_width_vector
        end_corner = self.__to_lane_point(end_date, lane=lane) - half_width_vector
        middle_date = start_date + (end_date - start_date) / 2
        text_coord = self.__to_lane_point(middle_date, lane=lane)
        self._svg.elements += [
            Rectangle(start_corner, end_corner, classes=classes),
            Text(text_coord, text, classes=classes),
        ]

    def add_title(self, title: str, classes: Optional[list[str]] = None):
        """ Add a title that should be printed above the timeline """
        classes = classes or []
        classes += [ClassNames.TITLE]
        text_coord = Vector(x=int(self._width * Defaults.title_x_position),
                            y=int(self._height * Defaults.title_y_position))
        self._svg.elements += [Text(text_coord, title, classes=classes)]

    @property
    def lane_normal(self) -> Vector:
        """ Normal vector orthogonal to the timeline direction
        This vector is used to calculate the positions of the different lanes.
        """
        return (self._time.target - self._time.source).orthogonal(ccw=True)

    def __to_lane_point(self, date: datetime, lane: float = 1) -> Vector:
        date_coord = self._time.date_to_coord(date)
        lane_point = date_coord + lane * Defaults.lane_width * self.lane_normal
        return lane_point

    def save(self, file_path: Path):
        """ Save an SVG of the timeline under the given file path """
        self._svg.save_as(file_path=file_path)
