""" base classes for creating SVG files """
from html import escape
from pathlib import Path
from typing import Optional


class SvgElement:
    """ general class for describing an element in an SVG and transforming it into
    its XML representation for saving it """
    def __init__(self, tag: str,
                 attributes: Optional[dict[str, str]] = None,
                 content: Optional[str] = None,
                 classes: Optional[list[str]] = None,
                 ):
        self._tag = tag
        self._attributes = attributes or {}
        self._content = content
        self._add_classes(classes)

    @property
    def tag(self) -> str:
        """ the element's tag as a string """
        return self._tag

    def _add_classes(self, classes: Optional[list[str]] = None) -> None:
        """ add new classes to the element's attributes """
        if classes is None or len(classes) == 0:
            return
        if 'class' not in self._attributes:
            self._attributes['class'] = ' '.join(classes)
            return
        for class_name in classes:
            if class_name in self._attributes['class']:
                continue
            self._attributes['class'] += ' ' + class_name

    @property
    def attributes(self) -> dict[str, str]:
        """ dictionary of the element's attributes """
        return self._attributes

    @property
    def classes(self) -> list[str]:
        """ list of the element's classes """
        if 'class' in self._attributes:
            return self._attributes['class'].split(' ')
        return []

    @property
    def content(self) -> Optional[str]:
        """ the element's content as a string """
        return self._content

    def __str__(self) -> str:
        svg_element = f'<{self.tag}'
        for key, value in self.attributes.items():
            svg_element += f' {key}="{escape(value)}"'
        if self.content is not None:
            svg_element += f'>{self.content}</{self.tag}>'
        else:
            svg_element += ' />'
        return svg_element


class SVG:
    """ representation of an SVG file used to collect the contained elements
    and save them into a .svg along with the necessary meta-data
    """
    def __init__(self, width: int, height: int,
                 style: Optional[dict[str, dict[str, str]]] = None,
                 elements: Optional[list[SvgElement]] = None,
                 definitions: Optional[list[SvgElement]] = None):
        self.width = width
        self.height = height
        self.style = style or {}
        self.elements = elements or []
        self.defs = definitions or []

    @property
    def header(self) -> str:
        """ first lines of the .svg file """
        width, height = int(self.width), int(self.height)
        view_x, view_y = 0, 0
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"',
            f'     width="{width}" height="{height}" viewBox="{view_x} {view_y} {width} {height}">',
        ]
        return '\n'.join(lines) + '\n'

    @property
    def style_section(self) -> str:
        """ style section lines of the .svg file """
        style_section = '<style>\n'
        indent = ' ' * 4
        for selector, props in self.style.items():
            style_section += f'{selector} {{\n'
            for name, value in props.items():
                style_section += f'{indent}{name}: {value};\n'
            style_section += '}\n'
        style_section += '</style>\n'
        return style_section

    @property
    def defs_section(self) -> str:
        """ definition section lines of the .svg file """
        defs_section = ''
        indent = ' ' * 4
        if len(self.defs) > 0:
            defs_section += '<defs>\n'
            defs_section += ''.join(indent + str(element) + '\n'
                                    for element in self.defs)
            defs_section += '</defs>\n'
        return defs_section

    @property
    def element_section(self) -> str:
        """ main elements section lines of the .svg file """
        element_section = ''.join(str(element) + '\n'
                                  for element in self.elements)
        return element_section

    @property
    def footer(self) -> str:
        """ last lines of the .svg file """
        return '</svg>\n'

    @property
    def full(self) -> str:
        """ the full raw .svg file """
        full = self.header
        full += self.style_section
        full += self.defs_section
        full += self.element_section
        full += self.footer
        return full

    def save_as(self, file_path: Path) -> None:
        """ save the SVG under given file path """
        with open(file_path, 'w', encoding='utf-8') as out_file:
            out_file.write(self.full)
