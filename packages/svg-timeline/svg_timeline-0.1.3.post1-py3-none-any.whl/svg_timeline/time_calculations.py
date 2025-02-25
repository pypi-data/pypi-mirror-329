""" classes and functions for easier calculations on datetimes and coordinates """
import calendar
from collections.abc import Iterable
from datetime import datetime

from svg_timeline.geometry import Vector


class TimeGradient:
    """ class for the transfer of dates to canvas coordinates and back """
    def __init__(self, source: Vector, target: Vector, start_date: datetime, end_date: datetime):
        """
        :param source: the point on the canvas that correspond to the start of the gradient
        :param target: the point on the canvas that correspond to the end of the gradient
        :param start_date: the datetime that corresponds to the start of the canvas_vector
        :param end_date: the datetime that corresponds to the end of the canvas_vector
        """
        self._source = source
        self._target = target
        self._start_date = start_date
        self._end_date = end_date

    @property
    def source(self) -> Vector:
        """ the point on the canvas that correspond to the start of the gradient """
        return self._source

    @property
    def target(self) -> Vector:
        """ the point on the canvas that correspond to the end of the gradient """
        return self._target

    @property
    def start_date(self) -> datetime:
        """ the datetime that corresponds to the start of the canvas_vector """
        return self._start_date

    @property
    def end_date(self) -> datetime:
        """ the datetime that corresponds to the end of the canvas_vector """
        return self._end_date

    def coord_to_date(self, coord: Vector) -> datetime:
        """ transform an absolute position on the canvas into a date """
        return self.relative_to_date(self.coord_to_relative(coord=coord))

    def coord_to_relative(self, coord: Vector) -> float:
        """ transform an absolute position on the canvas
        into a relative position on the timeline
        """
        # Transform coordinates so that the timeline start is at (0, 0).
        # (simplifies the following calculations)
        coord_x = coord.x - self._source.x
        coord_y = coord.y - self._source.y
        end_x = self._target.x - self._source.x
        end_y = self._target.y - self._source.y
        # Given a scalar factor 'a', minimize the length of vector 'coord - a * end'.
        # 'a' then describes the relative position on this timeline with the
        # shortest distance to the given coordinates.
        # Solved analytically, this gives:
        numerator = coord_x * end_x + coord_y * end_y
        denominator = end_x**2 + end_y**2
        a = numerator / denominator
        return a

    def date_to_coord(self, date: datetime) -> Vector:
        """ transform a date into a position on the canvas """
        return self.relative_to_coord(self.date_to_relative(date=date))

    def date_to_relative(self, date: datetime) -> float:
        """ transform a date into a relative position on the timeline """
        self_delta = self._end_date - self._start_date
        date_delta = date - self.start_date
        return date_delta / self_delta

    def relative_to_coord(self, relative_position: float) -> Vector:
        """ transform a relative position on the timeline
        into an absolute position on the canvas
        """
        delta = self._target - self._source
        scaled_vector = self._source + (relative_position * delta)
        return scaled_vector

    def relative_to_date(self, relative_position: float) -> datetime:
        """ transform a relative position on the timeline into a date """
        delta = self._end_date - self._start_date
        return self._start_date + relative_position * delta


class TimeSpacing:
    """ base class for semantic datetime spacing within a given range """
    def __init__(self, start_date: datetime, end_date: datetime):
        if not start_date < end_date:
            raise ValueError("start date needs to be smaller than end date")
        self._start_date = start_date
        self._end_date = end_date

    @property
    def start_date(self) -> datetime:
        """ the datetime that corresponds to the start of the time range """
        return self._start_date

    @property
    def end_date(self) -> datetime:
        """ the datetime that corresponds to the end of the time range """
        return self._end_date

    @property
    def labels(self) -> list[str]:
        """ Tic labels
        :return list of tic labels as strings
        """
        raise NotImplementedError

    @property
    def dates(self) -> list[datetime]:
        """ Positions of the tics
        :return list of tic positions as datetime objects
        """
        raise NotImplementedError


class YearBasedTimeSpacing(TimeSpacing):
    """ base class to return one entry per X years """
    _base = 1

    @property
    def _range(self) -> Iterable:
        first = (self._start_date.year // self._base + 1) * self._base
        last = (self._end_date.year // self._base) * self._base
        return range(first, last + self._base, self._base)

    @property
    def dates(self) -> list[datetime]:
        dates = [datetime(year=year, month=1, day=1)
                 for year in self._range]
        return dates

    @property
    def labels(self) -> list[str]:
        labels = [str(value) for value in self._range]
        return labels


class TimeSpacingPerMillennia(YearBasedTimeSpacing):
    """ return one entry per 1000 years
    Note: ISO 8601 only allows years between 0000 and 9999
    """
    _base = 1000


class TimeSpacingPerCentury(YearBasedTimeSpacing):
    """ return one entry per 100 years """
    _base = 100


class TimeSpacingPerDecade(YearBasedTimeSpacing):
    """ return one entry per 10 years """
    _base = 10


class TimeSpacingPerYear(YearBasedTimeSpacing):
    """ return one entry per year """
    _base = 1


class TimeSpacingPerMonth(TimeSpacing):
    """ return one entry per month """
    @property
    def dates(self) -> list[datetime]:
        year = self.start_date.year
        month = self.start_date.month + 1
        dates = []
        while True:
            if month > 12:
                year += 1
                month = 1
            date = datetime(year=year, month=month, day=1)
            if date > self.end_date:
                break
            dates.append(date)
            month += 1
        return dates

    @property
    def labels(self) -> list[str]:
        labels = [calendar.month_abbr[date.month] for date in self.dates]
        return labels


class TimeSpacingPerDay(TimeSpacing):
    """ return one entry per day """
    @property
    def dates(self) -> list[datetime]:
        year = self.start_date.year
        month = self.start_date.month
        _, n_days = calendar.monthrange(year, month)
        day = self.start_date.day + 1
        dates = []
        while True:
            if day > n_days:
                month += 1
                day = 1
                if month > 12:
                    year += 1
                    month = 1
                    _, n_days = calendar.monthrange(year, month)
            date = datetime(year=year, month=month, day=day)
            if date > self.end_date:
                break
            dates.append(date)
            day += 1
        return dates

    @property
    def labels(self) -> list[str]:
        labels = [str(date.day) for date in self.dates]
        return labels
