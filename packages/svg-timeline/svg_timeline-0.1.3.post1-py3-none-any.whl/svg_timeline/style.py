""" Singleton to store styling defaults """
from dataclasses import dataclass
from enum import StrEnum


@dataclass
class __TimelineStyle:
    title_x_position: float = 1/2
    title_y_position: float = 1/17
    title_size_factor: float = 1/15

    lane_width: float = 30

    arrow_y_position: float = 0.9
    arrow_x_padding: float = 0.03

    event_dot_radius: float = 3

    timespan_width: float = 18
    timespan_use_start_stilt: bool = False
    timespan_use_end_stilt: bool = False


Defaults = __TimelineStyle()


class ClassNames(StrEnum):
    """ string constants for all the class names that are commonly used for styling via CSS """
    TITLE = 'title'
    TIMEAXIS = 'time_axis'
    MINOR_TICK = 'minor_tick'
    MAJOR_TICK = 'major_tick'
    EVENT = 'event'
    TIMESPAN = 'timespan'
    IMAGE = 'image'
    WHITE_TEXT = 'white_text'
    COLOR_A = 'color_a'
    COLOR_B = 'color_b'
    COLOR_C = 'color_c'
    COLOR_D = 'color_d'
    COLOR_E = 'color_e'


DEFAULT_CSS = {
    ':root': {
        '--color_a': '#003f5c',
        '--color_b': '#58508d',
        '--color_c': '#bc5090',
        '--color_d': '#ff6361',
        '--color_e': '#ffa600',
    },
    f'path.{ClassNames.COLOR_A}': {'stroke': 'var(--color_a)'},
    f'path.{ClassNames.COLOR_B}': {'stroke': 'var(--color_b)'},
    f'path.{ClassNames.COLOR_C}': {'stroke': 'var(--color_c)'},
    f'path.{ClassNames.COLOR_D}': {'stroke': 'var(--color_d)'},
    f'path.{ClassNames.COLOR_E}': {'stroke': 'var(--color_e)'},
    f'rect.{ClassNames.COLOR_A}, circle.{ClassNames.COLOR_A}': {'fill': 'var(--color_a)'},
    f'rect.{ClassNames.COLOR_B}, circle.{ClassNames.COLOR_B}': {'fill': 'var(--color_b)'},
    f'rect.{ClassNames.COLOR_C}, circle.{ClassNames.COLOR_C}': {'fill': 'var(--color_c)'},
    f'rect.{ClassNames.COLOR_D}, circle.{ClassNames.COLOR_D}': {'fill': 'var(--color_d)'},
    f'rect.{ClassNames.COLOR_E}, circle.{ClassNames.COLOR_E}': {'fill': 'var(--color_e)'},
    'svg': {
        'background': 'white',
    },
    'path': {
        'stroke': 'black',
        'stroke-width': '2pt',
        'fill': 'none',
    },
    'text': {
        'font-size': '10pt',
        'font-family': 'Liberation Sans',
        'fill': 'black',
        'text-anchor': 'middle',
        'dominant-baseline': 'central',
    },
    'circle, rect': {
        'fill': 'black',
    },
    f'text.{ClassNames.TITLE}': {
        'font-size': '20pt',
    },
    f'path.{ClassNames.TIMEAXIS}': {
        'stroke-width': '3pt',
    },
    f'path.{ClassNames.MAJOR_TICK}': {
        'stroke-width': '2pt',
    },
    f'path.{ClassNames.MINOR_TICK}': {
        'stroke-width': '1pt',
    },
    f'path.{ClassNames.EVENT}': {
        'stroke-width': '2pt',
    },
    f'circle.{ClassNames.EVENT}': {
        'radius': '3pt',
    },
    f'path.{ClassNames.TIMESPAN}': {
        'stroke-width': '1pt',
    },
    f'text.{ClassNames.TIMESPAN}': {
        'font-size': '9pt',
    },
    f'path.{ClassNames.IMAGE}': {
        'stroke-width': '2pt',
    },
    f'text.{ClassNames.WHITE_TEXT}': {
        'fill': 'white',
    },
}
