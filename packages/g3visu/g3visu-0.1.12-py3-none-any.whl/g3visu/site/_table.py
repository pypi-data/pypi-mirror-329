import abc
import typing
import logging

from collections import namedtuple
from copy import deepcopy
from lxml import etree


logger = logging.getLogger('g3visu.site')


Bbox = namedtuple('Bbox', ['x', 'y', 'width', 'height'])


class BaseTableConstructor:
    CHID_TEMPLATES: dict[str, str] = {}

    def __init__(self, template: etree._Element) -> None:
        self.template = template

    def new_table(self, root: etree._Element) -> etree._Element:
        table = deepcopy(self.template)
        root.append(table)
        return table

    def get_tag(self, key: str, **format_kwargs) -> str:
        if key not in self.CHID_TEMPLATES:
            logger.warning('Failed to retrieve a chid template for "%s"', key)
            return ''
        template = self.CHID_TEMPLATES[key]
        return template.format(**format_kwargs)

    @staticmethod
    def calculate_group_bbox(group: etree._Element) -> Bbox:
        """x, y, wifdth, height"""
        min_x, min_y, max_x, max_y = (
            float('inf'), float('inf'), float('-inf'), float('-inf')
        )
        for element in group.iter():
            if element.tag.endswith('rect'):
                x = float(element.get('x', 0))
                y = float(element.get('y', 0))
                width = float(element.get('width', 0))
                height = float(element.get('height', 0))
                min_x, min_y = min(min_x, x), min(min_y, y)
                max_x, max_y = max(max_x, x + width), max(max_y, y + height)
        return Bbox(min_x, min_y, max_x - min_x, max_y - min_y)

    def reposition_group(
        self,
        group: etree._Element,
        new_x: int | float | None = None,
        new_y: int | float | None = None
    ) -> None:
        bbox = self.calculate_group_bbox(group)
        translate_x = new_x - bbox.x if new_x is not None else 0
        translate_y = new_y - bbox.y if new_y is not None else 0
        transform = group.get('transform', '')
        trasnlate = f'translate({translate_x} {translate_y}) {transform}'
        group.set('transform', trasnlate)

    def reposition_element(
        self,
        element: etree._Element,
        new_x: int | float | None = None,
        new_y: int | float | None = None
    ) -> None:
        if new_x is not None:
            element.set('x', str(new_x))
        if new_y is not None:
            element.set('y', str(new_y))

    def find_bounding_box(self, table: etree._Element) -> etree._Element:
        return self.find_component_by_attrs(table, chid='boundingBox')

    def resize_bounding_box(
        self,
        table: etree._Element,
        new_x: int | float | None = None,
        new_y: int | float | None = None,
        new_width: int | float | None = None,
        new_height: int | float | None = None
    ) -> None:
        bounding_box = self.find_bounding_box(table)
        if new_x is not None:
            bounding_box.set('x', str(new_x))
        if new_y is not None:
            bounding_box.set('y', str(new_y))
        if new_width is not None:
            bounding_box.set('width', str(new_width))
        if new_height is not None:
            bounding_box.set('height', str(new_height))

    def find_component_by_attrs(
        self, root: etree._Element, **attrs
    ) -> etree._Element:
        attrs_str = " and ".join(
            f'@{name}="{value}"' for name, value in attrs.items()
            )
        component = root.find(f".//*[{attrs_str}]")
        assert component is not None
        return component

    def find_component_by_text(
        self, root: etree._Element, text: str
    ) -> etree._Element:
        result = root.xpath(
            f".//svg:tspan[contains(text(), '{text}')]",
            namespaces={'svg': "http://www.w3.org/2000/svg"}
            )
        assert isinstance(result, list), 'Unexpected search result type'
        assert len(result) == 1, 'Search result is empty or is not unique'
        component = result[0]
        assert isinstance(component, etree._Element), 'Unexpected component'
        return component

    def format_label(self, table: etree._Element, label: str) -> None:
        element = self.find_component_by_attrs(table, shvAlarmPosition='right')
        element.text = label

    @staticmethod
    def remove_template_cell(template: etree._Element) -> None:
        parent = template.getparent()
        if parent is None:
            return
        parent.remove(template)

    @abc.abstractmethod
    def construct(
        self, root: etree._Element, *args, **kwargs
    ) -> etree._Element:
        ...


class GateTableConstructor(BaseTableConstructor):
    CHID_TEMPLATES = {
        'Time': 'row{i}/timeCreated',
        'Vehicle Id': 'row{i}/vehicleId',
        'Route': 'row{i}/route',
        'Line number': 'row{i}/lineNumber'
        }

    def add_cell(
        self,
        template: etree._Element,
        pos_x: int | float,
        pos_y: int | float,
        text: str,
        text_placeholder: str,
        addnext_to: etree._Element
    ) -> etree._Element:
        cell = deepcopy(template)
        addnext_to.addnext(cell)
        self.reposition_group(cell, new_x=pos_x, new_y=pos_y)
        text_element = self.find_component_by_text(cell, text_placeholder)
        text_element.text = text
        return cell

    def construct(  # type: ignore
        self,
        root: etree._Element,
        label: str,
        column_names: typing.Sequence[str],
        row_count: int
    ) -> etree._Element:
        if not column_names:
            raise ValueError('A table must have at least one column.')
        table = self.new_table(root)
        self.format_label(table, label)
        header_cell_template = self.find_component_by_attrs(
            table, id='gGateTableHeader'
            )
        row_cell_template = self.find_component_by_attrs(
            table, id='gGateTableRow'
            )
        header_cell_bbox = self.calculate_group_bbox(header_cell_template)
        row_cell_bbox = self.calculate_group_bbox(header_cell_template)
        addnext_to = header_cell_template
        for i, name in enumerate(column_names):
            addnext_to = self.add_cell(
                template=header_cell_template,
                pos_x=header_cell_bbox.x + header_cell_bbox.width * i,
                pos_y=header_cell_bbox.y,
                text=name,
                text_placeholder='Column name',
                addnext_to=addnext_to
            )
            for j in range(row_count):
                addnext_to = self.add_cell(
                    template=row_cell_template,
                    pos_x=row_cell_bbox.x + row_cell_bbox.width * i,
                    pos_y=row_cell_bbox.y + row_cell_bbox.height * (j + 1),
                    text='...',
                    text_placeholder='Row text',
                    addnext_to=addnext_to
                )
                tag_element = self.find_component_by_text(
                    root=addnext_to, text='...'
                    )
                tag_element.set('chid', self.get_tag(key=name, i=j))
        self.remove_template_cell(header_cell_template)
        self.remove_template_cell(row_cell_template)
        self.resize_bounding_box(
            table,
            new_x=header_cell_bbox.x,
            new_y=header_cell_bbox.y,
            new_width=header_cell_bbox.width * (i + 1),
            new_height=header_cell_bbox.height * (j + 2)
            )
        return table


class BaseRowTableConstructor(BaseTableConstructor):
    ROW_NAMES_TO_ROW_IDS: dict[str, str] = {}

    def find_row_templates(
        self, table: etree._Element
    ) -> dict[str, etree._Element]:
        return {
            row_id: self.find_component_by_attrs(table, id=row_id)
            for row_id in self.ROW_NAMES_TO_ROW_IDS.values()
            }

    def set_row_name(self, row: etree._Element, name: str) -> None:
        row_name_component = self.find_component_by_text(row, 'Row name')
        row_name_component.text = name

    def set_row_tag(self, row: etree._Element, tag: str) -> None:
        row_tag_component = self.find_component_by_text(row, 'Row text')
        row_tag_component.text = '...'
        row_tag_component.set('chid', tag)

    def add_row(
        self, template: etree._Element, name: str, pos_y: int | float
    ) -> etree._Element:
        row = deepcopy(template)
        self.reposition_group(row, new_y=pos_y)
        self.set_row_name(row, name)
        self.set_row_tag(row, self.get_tag(key=name))
        return row

    def construct(  # type: ignore
        self,
        root: etree._Element,
        label: str,
        row_names: typing.Sequence[str]
    ) -> etree._Element:
        if not row_names:
            raise ValueError('A table must have at least one row.')
        table = self.new_table(root)
        self.format_label(table, label)
        templates = self.find_row_templates(table)
        for template in templates.values():
            self.remove_template_cell(template)
        bounding_box = self.find_bounding_box(table)
        g_bounding_box = bounding_box.getparent()
        assert g_bounding_box is not None
        row_height = self.calculate_group_bbox(template).height
        y_start = float(bounding_box.get('y') or 0)
        for i, row_name in enumerate(row_names):
            if row_name not in self.ROW_NAMES_TO_ROW_IDS:
                logger.warning('Invalid row name "%s"', row_name)
                continue
            row_id = self.ROW_NAMES_TO_ROW_IDS[row_name]
            row = self.add_row(
                template=templates[row_id],
                name=row_name,
                pos_y=y_start + row_height * i
                )
            g_bounding_box.insert(0, row)
        self.resize_bounding_box(table, new_height=row_height * (i + 1))
        return table


class HeatingTableConstructor(BaseRowTableConstructor):
    CHID_TEMPLATES = {
        'Heating state': 'heatingState',
        'Rail': 'tempRail',
        'Air': 'tempAir',
        'Wet': 'wetConditions'
        }

    ROW_NAMES_TO_ROW_IDS = {
        'Heating state': 'gHeatingTableRowNoSymbol',
        'Rail': 'gHeatingTableRowTemp',
        'Air': 'gHeatingTableRowTemp',
        'Wet': 'gHeatingTableRowDrop'
        }


class RequestorTableConstructor(BaseRowTableConstructor):
    CHID_TEMPLATES = {
        'Vehicle ID': 'vehicleId',
        'Line number': 'lineNumber',
        'Route code': 'routeCode',
        'Service number': 'serviceNumber',
        'Vehicle type': 'vehicleType',
        'Direction': 'direction',
        'Category': 'category',
        'Stand number': 'stand',
        'Transceiver position': 'side',
        'Remote cmd': 'remoteCommand',
        'RTS button pressed': 'readyToStart'
        }

    def __init__(self, template: etree._Element) -> None:
        super().__init__(template)
        self._set_row_names_to_row_ids_dict()

    def _set_row_names_to_row_ids_dict(self) -> None:
        self.ROW_NAMES_TO_ROW_IDS = dict.fromkeys(
            self.CHID_TEMPLATES.keys(), 'gRequestorTableRow'
            )
