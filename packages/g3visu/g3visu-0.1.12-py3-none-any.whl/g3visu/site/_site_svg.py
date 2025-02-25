import json
import os
import logging
import typing

from copy import deepcopy
from lxml import etree

from g3elements import (
    CabinetControlPanel, HeatingMeteo, Zone, is_requestor_loop
)

from ._table import (
    GateTableConstructor, RequestorTableConstructor, HeatingTableConstructor
)
from ..utils import SitesFileDownloader, SitesFilePaths


logger = logging.getLogger('g3visu.site')


def get_site_svg_template() -> etree._ElementTree:
    """Read and parse the library's 'site.svg' file into an lxml etree element.

    Returns:
        etree._ElementTree: The parsed XML tree of the SVG file.
    """
    this_dirname = os.path.dirname(os.path.realpath(__file__))
    site_svg_file = os.path.join(this_dirname, 'site.svg')
    try:
        logger.info(
            'Reading local site SVG file template from "%s"', site_svg_file
            )
        with open(site_svg_file, 'r') as file:
            element = etree.parse(file)
    except (FileNotFoundError, etree.XMLSyntaxError) as error:
        logger.info(
            'Failed to read local site SVG file template: %s', error
            )
    return element


class SiteSVG:
    """'site.svg' file representation and manipulation class."""
    STANDARD_SHV_VISU_TYPE_VARIANT_KEY = 'standard'
    """The standard SHV visu type variant key (default value)."""
    TABLE_TEMPLATE_VISU_TYPE_VARIANT_KEY = 'Template'
    """The table template visu type variant key (default value)."""

    def __init__(
        self,
        visu_types: etree._ElementTree,
        site_svg: etree._ElementTree | None = None
    ) -> None:
        if site_svg is None:
            site_svg = get_site_svg_template()
        self._copy_dimensions(visu_types, site_svg)
        self.visu_types_file = visu_types
        self.site_svg_file = site_svg
        self.gate_table_constructor: GateTableConstructor
        self.requestor_table_constructor: RequestorTableConstructor
        self.heating_table_constructor: HeatingTableConstructor
        self.device_types = self._parse_device_types(visu_types)
        self.template_groups = self._parse_template_groups(site_svg)
        """Visu type name to 'site.svg' visu type group mapping."""

    @classmethod
    def from_local(
        cls,
        visu_types_file: str,
        site_svg_file: str | None = None
    ) -> typing.Self:
        """Create a SiteSVG instance from local files.

        Args:
            visu_types_file (str): Path to the 'visu-types-g3.svg' file.
            site_svg_file (str | None, optional): Path to the 'site.svg' file.\
                If None, the default template will be used. Defaults to None.

        Returns:
            typing.Self: The SiteSVG instance.
        """
        logger.info(
            'Reading local visu types file from "%s"', visu_types_file
            )
        with open(visu_types_file, 'r') as file:
            visu_types = etree.parse(file)
        if site_svg_file is None:
            return cls(visu_types)
        logger.info(
            'Reading local site SVG file from "%s"', site_svg_file
            )
        with open(site_svg_file, 'r') as file:
            site_svg = etree.parse(file)
        return cls(visu_types, site_svg)

    @classmethod
    def from_sites_repo(
        cls,
        visu_types_branch: str = 'master',
        site_svg_file: str | None = None
    ) -> typing.Self:
        """Create a SiteSVG instance from the sites repository.

        Args:
            visu_types_branch (str, optional): The branch of the sites repo\
                to download the 'visu-types-g3.svg' file from.\
                Defaults to 'master'.
            site_svg_file (str | None, optional): Path to the 'site.svg' file.\
                If None, the default template will be used. Defaults to None.

        Raises:
            RuntimeError: If the 'visu-types-g3.svg' file could not be\
                downloaded.

        Returns:
            typing.Self: The SiteSVG instance.
        """
        logger.info(
            'Downloading visu-types-g3.svg from the sites repo (branch "%s")',
            visu_types_branch
            )
        visu_types_str = SitesFileDownloader().read(
            SitesFilePaths.VISU_TYPES_G3, visu_types_branch, decode=False
            )
        if visu_types_str is None:
            raise RuntimeError('Failed to download visu-types-g3.svg')
        visu_types = etree.ElementTree(etree.fromstring(visu_types_str))
        if site_svg_file is None:
            return cls(visu_types)
        logger.info(
            'Reading local site SVG file from "%s"', site_svg_file
            )
        with open(site_svg_file, 'r') as file:
            site_svg = etree.parse(file)
        return cls(visu_types, site_svg)

    @staticmethod
    def _copy_dimensions(
        source: etree._ElementTree, target: etree._ElementTree
    ) -> None:
        logger.debug('Copying dimensions from visu-types-g3.svg to site.svg')
        # get source (visu-types-g3.svg) dimensions
        source_root = source.getroot()
        viewBox = source_root.get("viewBox")
        width = source_root.get("width")
        height = source_root.get("height")
        # get template (site.svg) dimensions
        target_root = target.getroot()
        if viewBox:
            target_root.set("viewBox", viewBox)
        if width:
            target_root.set("width", width)
        if height:
            target_root.set("height", height)

    def _parse_requestor_data(
        self, visu_types: etree._ElementTree
    ) -> etree._Element:
        template_key = self.TABLE_TEMPLATE_VISU_TYPE_VARIANT_KEY
        for child in visu_types.getroot():
            if (
                child.attrib.get('shvVisuType') == 'RequestorData' and
                child.attrib.get('shvVisuTypeVariant') == template_key
            ):
                return child
        raise RuntimeError(
            "RequestorData template was not found in visu-types-g3.svg"
            )

    def _parse_device_types(
        self, visu_types: etree._ElementTree
    ) -> dict[str, dict[str, etree._Element]]:
        """Parse device types from the 'visu-types-g3.svg' file.

        Caveats:
        - data of a device and data of a corresponding device table is stored\
            under the same shvDeviceType key. For example, Gate and GateData\
            are stored under 'Gate_G3'.
        - requestor table data template is searched for during the document\
            traversal manually (see the code below). Reason: RequestorData\
            is not directly bound to any Requestor element via a common\
            shvDeviceType.

        Args:
            visu_types (etree._ElementTree): The parsed 'visu-types-g3.svg'\
                file.

        Raises:
            RuntimeError: If the requestor table template was not found.

        Returns:
            dict[str, dict[str, etree._Element]]: The parsed device types.
        """
        logger.debug('Parsing device types from visu-types-g3.svg')
        standard_key = self.STANDARD_SHV_VISU_TYPE_VARIANT_KEY
        template_key = self.TABLE_TEMPLATE_VISU_TYPE_VARIANT_KEY
        # find requestor table template
        requestor_data = self._parse_requestor_data(visu_types)
        constructor = RequestorTableConstructor(requestor_data)
        self.requestor_table_constructor = constructor
        # parse standard device templates
        types: dict[str, dict[str, etree._Element]] = {}
        for child in visu_types.getroot():
            if 'shvDeviceType' not in child.attrib:
                continue
            device_type = str(child.attrib['shvDeviceType'])
            device_type_data = types.setdefault(device_type, {})
            visu_type = str(child.attrib.get('shvVisuType'))
            visu_type_variant = str(
                child.attrib.get('shvVisuTypeVariant', standard_key)
                )
            if visu_type == 'Requestor':  # set requestor table template
                device_type_data[template_key] = requestor_data
            elif (
                visu_type == 'GateData' and
                visu_type_variant == template_key
            ):
                self.gate_table_constructor = GateTableConstructor(child)
            elif (
                visu_type == 'HeatingTable' and
                visu_type_variant == template_key
            ):
                self.heating_table_constructor = HeatingTableConstructor(child)
            device_type_data[visu_type_variant] = child
        for attr in [
            'gate_table_constructor',
            'requestor_table_constructor',
            'heating_table_constructor'
        ]:
            if getattr(self, attr, None) is None:
                raise RuntimeError(f"{attr} is not initialized.")
        return types

    def _parse_template_groups(
        self, site_svg: etree._ElementTree
    ) -> dict[str, etree._Element]:
        logger.debug('Parsing template groups from site.svg')
        groups: dict[str, etree._Element] = {}
        for child in site_svg.getroot():
            if not child.tag.endswith('g'):
                continue
            inkscape_ns = '{http://www.inkscape.org/namespaces/inkscape}'
            group = str(child.attrib[f'{inkscape_ns}label'])
            groups[group] = child
        return groups

    def get_device_type(
        self,
        type_name: str,
        type_variant: str | None = None,
        copy: bool = False
    ) -> etree._Element:
        """Get a device type from the 'visu-types-g3.svg' file.

        Args:
            type_name (str): The device type name.
            type_variant (str | None, optional): The device type variant.\
                Defaults to None.
            copy (bool, optional): If True, a deep copy of the device type\
                will be returned. Defaults to False.

        Returns:
            etree._Element: The device type XML element.
        """
        if not type_variant:
            type_variant = self.STANDARD_SHV_VISU_TYPE_VARIANT_KEY
        logger.debug(
            'Getting device type "%s/%s" (copy=%s)',
            type_name, type_variant, copy
            )
        if copy:
            return deepcopy(self.device_types[type_name][type_variant])
        return self.device_types[type_name][type_variant]

    def get_device_type_group(
        self, type_name: str, type_variant: str | None = None
    ) -> etree._Element:
        """Get the device type group from the 'site.svg' file.

        Args:
            type_name (str): The device type name.
            type_variant (str | None, optional): The device type variant.\
                Defaults to None.

        Returns:
            etree._Element: The device type group XML element.
        """
        device = self.get_device_type(type_name, type_variant, copy=False)
        visu_type_name = str(device.attrib['shvVisuType'])
        logger.debug(
            'Getting device type group "%s" for device type "%s/%s"',
            visu_type_name, type_name, type_variant
            )
        return self.template_groups[visu_type_name]

    def _find_label_element(
        self, element: etree._Element
    ) -> etree._Element | None:
        for child in element:
            if child.text == 'label':
                return child
            label_element = self._find_label_element(child)
            if label_element is not None:
                return label_element
        return None

    def _add_device_default(
        self,
        type_name: str,
        type_variant: str | None = None,
        name: str | None = None,
        shv_path: str | None = None,
    ) -> None:
        device = self.get_device_type(type_name, type_variant, copy=True)
        if name:
            label_element = self._find_label_element(device)
            if label_element is not None:
                label_element.text = name
        if shv_path:
            device.attrib['shvPath'] = shv_path
        group = self.get_device_type_group(type_name, type_variant)
        group.append(device)

    def _add_requestor(
        self,
        type_name: str,
        name: str | None,
        shv_path: str | None,
        row_names: typing.Sequence[str] | None = None
    ) -> None:
        # add requestor
        standard_key = self.STANDARD_SHV_VISU_TYPE_VARIANT_KEY
        self._add_device_default(type_name, standard_key, name, shv_path)
        # add requestor table
        group = self.template_groups['RequestorData']
        table = self.requestor_table_constructor.construct(
            root=group,
            label=name or 'label',
            row_names=row_names or []
            )
        table.attrib['shvPath'] = shv_path or ''

    def _add_gate(
        self,
        name: str | None,
        shv_path: str | None,
        column_names: typing.Sequence[str] | None = None,
        row_count: int = 0
    ) -> None:
        # add gate
        standard_key = self.STANDARD_SHV_VISU_TYPE_VARIANT_KEY
        self._add_device_default('Gate_G3', standard_key, name, shv_path)
        # add gate table
        table_template_key = self.TABLE_TEMPLATE_VISU_TYPE_VARIANT_KEY
        group = self.get_device_type_group('Gate_G3', table_template_key)
        table = self.gate_table_constructor.construct(
            root=group,
            label=name or 'label',
            column_names=column_names or [],
            row_count=row_count
            )
        table.attrib['shvPath'] = shv_path or ''

    def _add_heating(
        self,
        name: str | None,
        shv_path: str | None,
        row_names: typing.Sequence[str] | None = None,
    ) -> None:
        table_template_key = self.TABLE_TEMPLATE_VISU_TYPE_VARIANT_KEY
        group = self.get_device_type_group('Heating_G3', table_template_key)
        table = self.heating_table_constructor.construct(
            root=group,
            label=name or 'label',
            row_names=row_names or []
            )
        table.attrib['shvPath'] = shv_path or ''

    def add_element(
        self,
        type_name: str,
        type_variant: str | None = None,
        name: str | None = None,
        shv_path: str | None = None,
        **kwargs
    ) -> None:
        """Add an XML element to the 'site.svg' file.

        Args:
            type_name (str): The type name of the element.
            type_variant (str | None, optional): The type variant of the\
                element. Defaults to None (standard variant).
            name (str | None, optional): The name of the element. Defaults to\
                None.
            shv_path (str | None, optional): The SHV path of the element.\
                Defaults to None.
        """
        logger.debug(
            'Adding element of type "%s/%s" (name=%s, shv_path=%s)',
            type_name, type_variant, name, shv_path
            )
        if type_name == 'Gate_G3':
            self._add_gate(
                name,
                shv_path,
                column_names=kwargs['column_names'],
                row_count=kwargs['row_count']
                )
        elif type_name == 'Vetra_G3':
            self._add_requestor(
                type_name, name, shv_path, row_names=kwargs['row_names']
                )
        elif type_name == 'Heating_G3':
            self._add_heating(
                name,
                shv_path,
                row_names=kwargs['row_names']
                )
        elif kwargs.get('is_requestor_loop', False):
            self._add_requestor(
                type_name, name, shv_path, row_names=kwargs['row_names']
                )
        else:
            self._add_device_default(
                type_name, type_variant, name, shv_path, **kwargs
                )

    def to_file(self, file_path: str) -> None:
        """Write the 'site.svg' file to a local file.

        Args:
            file_path (str): The path to the output file.
        """
        self.site_svg_file.write(
            file_path,
            pretty_print=True,
            xml_declaration=True,
            encoding='utf-8'
            )

    def update_from_system_config(
        self, system_config: dict, zone_name: str
    ) -> None:
        """Update the site SVG file from system config data.

        Args:
            system_config (dict): SystemDict data.
            zone_name (str): The name of the zone.
        """
        logger.info(
            'Updating site SVG file from system config data (zone "%s")',
            zone_name
            )
        SystemConfigDictConnector(zone_name, system_config, self).update()

    def update_from_system_config_local_file(
        self, file_path: str, zone_name: str
    ) -> None:
        """Update the site SVG file from a local system config file.

        Args:
            file_path (str): Path to the system config file.
            zone_name (str): The name of the zone.
        """
        logger.info(
            'Parsing system config file "%s"', os.path.abspath(file_path)
            )
        with open(file_path, 'r') as file:
            system_config = json.load(file)
        self.update_from_system_config(system_config, zone_name)


class SystemConfigDictConnector:
    EXCLUDED_SHV_TYPES = [
        'CabinetConvertor_G3',
        'CabinetFuse_G3',
        'CabinetUps_G3',
        'DRRController_G3',
        'SPIEController_G3',
        'VecomController_G3',
        'RoutingTable_G3',
        'HeatingContactor_G3',
        'HeatingMeteo_G3',
        'SignalSymbol_G3',
        'System_G3',
        'SystemSafety_G3',
        'GPIO_G3'
        ]

    def __init__(
        self, zone_name: str, system: dict, site_svg: SiteSVG
    ) -> None:
        self.zone_name = zone_name
        self.shv_types = system['Visu']
        self.zone = Zone.from_system_config(zone_name, system)  # type: ignore
        self.file = site_svg

    def get_type(self, device_data: dict) -> tuple[str, str]:
        """Get the SHV device type and variant for a device.

        Args:
            device_data (dict): SWDeviceDict data.

        Returns:
            tuple[str, str]: The SHV device type and variant.
        """
        logger.debug(
            'Getting SHV device type for device "%s"',
            device_data['general']['name']
            )
        if (
            not (visu_data := device_data.get('visu', {})) or
            not (shv_type := visu_data.get('shvDeviceType', ''))
        ):
            return ('', '')
        assert isinstance(shv_type, str)
        if (shv_type_data := self.shv_types.get(shv_type)):
            if shv_type_data.get('restricted_to'):
                shv_type = shv_type_data['restricted_to']
                assert isinstance(shv_type, str)
        shv_type_variant = visu_data.get(
            'SHVDeviceTypeVariant', SiteSVG.STANDARD_SHV_VISU_TYPE_VARIANT_KEY
            )
        return (shv_type, shv_type_variant)

    def get_kwargs(
        self, element, shv_type: str, shv_type_variant: str
    ) -> dict:
        """Get the table constructor kwargs for a device.

        Args:
            element (Any): The element to get the kwargs for.
            shv_type (str): The SHV device type.
            shv_type_variant (str): The SHV device type variant.

        Returns:
            dict: The table constructor kwargs.
        """
        logger.debug(
            'Getting table constructor kwargs for SHV device type "%s/%s"',
            shv_type, shv_type_variant
            )
        type_data = self.shv_types.get(shv_type)
        if type_data is None:
            return {}
        type_variants = type_data.get('type_variants', {})
        type_variant = type_variants.get(shv_type_variant)
        if type_variant is None:
            return {}
        if shv_type == 'Gate_G3':
            return {
                'column_names': type_variant[0],
                'row_count': type_variant[1]
            }
        if shv_type == 'Heating_G3':
            return {'row_names': type_variant}
        if shv_type == 'Vetra_G3':
            return {'row_names': type_variant, 'is_requestor_loop': False}
        if is_requestor_loop(element):
            return {'row_names': type_variant, 'is_requestor_loop': True}
        return {}

    def update(self) -> None:
        """Update the site SVG file from the system config data."""
        logger.info('Adding elements to site.svg')
        for element in self.zone.all_elements:
            if isinstance(element, (CabinetControlPanel, HeatingMeteo)):
                logger.debug(
                    'Ignoring element "%s"of SHV device type "%s"',
                    element.name, type(element).__name__
                    )
                continue
            device_data = element.data.get('device_dict')
            if not device_data:
                logger.warning(
                    'No device data found for element "%s"', element.name
                    )
                continue
            shv_type, shv_type_variant = self.get_type(device_data)
            if not shv_type:
                logger.warning(
                    'No SHV type found for element "%s"', element.name
                    )
                continue
            if shv_type in self.EXCLUDED_SHV_TYPES:
                logger.debug(
                    'Ignoring element "%s"of SHV device type "%s"',
                    element.name, shv_type
                    )
                continue
            try:
                kwargs = self.get_kwargs(element, shv_type, shv_type_variant)
                if kwargs:
                    key = SiteSVG.STANDARD_SHV_VISU_TYPE_VARIANT_KEY
                    logger.debug(
                        'Changing SHV type variant from "%s/%s" to "%s/%s" '
                        'for element "%s"',
                        shv_type, shv_type_variant, shv_type, key, element.name
                        )
                    shv_type_variant = key
                self.file.add_element(
                    shv_type,
                    shv_type_variant,
                    element.name,
                    element.shv_path,
                    **kwargs
                    )
            except KeyError as err:
                logger.warning(
                    'Failed to add element "%s" of type "%s/%s" (%s)',
                    element.name, shv_type, shv_type_variant, err
                    )
                continue
