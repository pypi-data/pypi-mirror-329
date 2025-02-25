from __future__ import annotations

import copy
import json
import logging
import os
import shv
import typing

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_serializer,
    NonNegativeInt,
)

from g3elements import Zone, Route, Gate

from ..utils import SitesFileDownloader, SitesFilePaths
from ._list_operations import ListOperations


logger = logging.getLogger('typeInfo')


class TypeInfoModel(BaseModel):
    """Root model for TypeInfo models."""
    model_config = ConfigDict(
        extra='allow',
        arbitrary_types_allowed=True,
        validate_assignment=True
        )

    meta: typing.Mapping[str | int, typing.Any] = Field(
        default={}, exclude=True
        )

    @staticmethod
    def _unpack_cpon(data: typing.Any) -> shv.SHVMapType:
        converted = shv.cpon.Cpon.unpack(data)
        if shv.is_shvmap(converted):
            return converted
        raise TypeError('Invalid TypeInfo model structure (expected SHVMap)')

    @classmethod
    def model_validate_cpon(
        cls,
        cpon_data: str | bytes | bytearray,
        *,
        strict: bool | None = None,
        from_attributes: bool | None = None,
        context: dict[str, typing.Any] | None = None
    ) -> typing.Self:
        unpacked = cls._unpack_cpon(cpon_data)
        model = cls.model_validate(
            unpacked,
            strict=strict,
            from_attributes=from_attributes,
            context=context
            )
        if hasattr(unpacked, '_meta'):
            model.meta = unpacked._meta
        return model

    @model_serializer(when_used='json-unless-none')
    def _serialize_shvtype(self) -> typing.Any:
        values: dict[str, typing.Any] = {}
        for field in self.model_fields_set:
            value = getattr(self, field)
            if shv.is_shvbool(value):
                values[field] = bool(value)
            elif shv.is_shvnull(value):
                values[field] = None
            else:
                values[field] = value
        return values

    def add_attrs(self, **new_attrs) -> typing.Self:
        """Add new attributes to the model instance and return an updated copy.

        Returns:
            typing.Self: Updated model instance.
        """
        attrs = self.model_dump(exclude_unset=True)
        attrs.update(new_attrs)
        return self.__class__(**attrs)

    def model_dump_cpon(
        self,
        *,
        indent: NonNegativeInt | None = None,
        indent_char: str = '\t',
        include: (
            set[int] |
            set[str] |
            dict[int, typing.Any] |
            dict[str, typing.Any] |
            None
        ) = None,
        exclude: (
            set[int] |
            set[str] |
            dict[int, typing.Any] |
            dict[str, typing.Any] |
            None
        ) = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool = True
    ) -> str:
        data = self.model_dump(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings
            )
        indentation = indent_char * indent if indent is not None else ''
        cpon_options = shv.CponWriter.Options(indent=indentation.encode())
        contents = shv.SHVMeta.new(data, meta=self.meta)  # type: ignore
        return shv.cpon.Cpon.pack(contents, cpon_options)


# Device descriptions

class TypeInfoDeviceDescriptionPropertyMethod(TypeInfoModel):
    accessGrant: str | None = None
    description: str | None = None
    flags: NonNegativeInt | None = None
    label: str | None = None
    name: str | None = None
    signature: int | None = None


class TypeInfoDeviceDescriptionProperty(TypeInfoModel):
    alarm: str | None = None
    autoload: shv.SHVBool | bool | None = None
    description: str | None = None
    label: str | None = None
    methods: list[TypeInfoDeviceDescriptionPropertyMethod] | None = None
    monitorOptions: dict[str, typing.Any] | None = None
    monitored: shv.SHVBool | bool | None = None
    name: str | None = None
    typeName: str | None = None
    unit: str | None = None


class TypeInfoDeviceDescription(TypeInfoModel):
    properties: list[TypeInfoDeviceDescriptionProperty] | None = None

    def get_prop(
        self, prop_name: str
    ) -> TypeInfoDeviceDescriptionProperty:
        if self.properties is None:
            raise ValueError("properties is None")
        return ListOperations(self.properties).get(item_name=prop_name)

    @property
    def root_prop(self) -> TypeInfoDeviceDescriptionProperty:
        if self.properties is None:
            raise ValueError("properties is None")
        return ListOperations(self.properties).get(item_name='')

    @property
    def status_prop(self) -> TypeInfoDeviceDescriptionProperty:
        if self.properties is None:
            raise ValueError("properties is None")
        return ListOperations(self.properties).get(item_name='status')

    @status_prop.setter
    def status_prop(
        self, new_status_prop: TypeInfoDeviceDescriptionProperty
    ) -> None:
        if self.properties is None:
            raise ValueError("properties is None")
        ListOperations(self.properties).add(
            item_name="status",
            item_data=new_status_prop,
            replace_if_exists=True
            )

    def get_root_method(
        self, meth_name: str
    ) -> TypeInfoDeviceDescriptionPropertyMethod:
        if self.root_prop.methods is None:
            raise ValueError("root_prop.methods is None")
        return ListOperations(self.root_prop.methods).get(item_name=meth_name)

    def del_prop(self, prop_name: str) -> None:
        if self.properties is None:
            raise ValueError("properties is None")
        ListOperations(self.properties).delete(item_name=prop_name)

    def del_root_method(self, meth_name: str) -> None:
        if self.root_prop.methods is None:
            raise ValueError("root_prop.methods is None")
        ListOperations(self.root_prop.methods).delete(item_name=meth_name)


# Types

class TypeInfoTypeField(TypeInfoModel):
    alarm: str | None = None
    alarmLevel: int | None = None
    description: str | None = None
    label: str | None = None
    name: str | None = None
    typeName: str | None = None
    value: typing.Any | None = None


class TypeInfoType(TypeInfoModel):
    fields: list[TypeInfoTypeField] | None = None
    name: str | None = None
    typeName: str | None = None

    def get_field(self, field_name: str) -> TypeInfoTypeField:
        if self.fields is None:
            raise ValueError("No fields to get")
        return ListOperations(self.fields).get(item_name=field_name)

    def del_field(self, field_name: str) -> None:
        if self.fields is None:
            raise ValueError("No fields to get")
        ListOperations(self.fields).delete(item_name=field_name)


# TypeInfo (main)

class TypeInfo(TypeInfoModel):
    """'TypeInfo.cpon' file data model."""
    blacklistedPaths: dict[str, None]
    deviceDescriptions: dict[str, TypeInfoDeviceDescription]
    devicePaths: dict[str, str]
    extraTags: dict[str, dict[str, str]]
    systemPathsRoots: dict[str, typing.Any]
    types: dict[str, TypeInfoType]

    @classmethod
    def model_validate_local_file(
        cls,
        filepath: str,
        *,
        strict: bool | None = None,
        context: dict[str, typing.Any] | None = None
    ) -> typing.Self:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = file.read()
        return cls.model_validate_cpon(data, strict=strict, context=context)

    @classmethod
    def model_validate_sites_repo(
        cls,
        branch: str = 'master',
        *,
        strict: bool | None = None,
        from_attributes: bool | None = None,
        context: dict[str, typing.Any] | None = None
    ) -> typing.Self:
        data = SitesFileDownloader().read(SitesFilePaths.TYPE_INFO, branch)
        assert isinstance(data, str)
        return cls.model_validate_cpon(
            data,
            strict=strict,
            from_attributes=from_attributes,
            context=context
            )

    @staticmethod
    def is_decimal_type(type_data: TypeInfoType) -> bool:
        return hasattr(type_data, 'decPlaces')

    @staticmethod
    def is_enum_type(type_data: TypeInfoType) -> bool:
        return getattr(type_data, 'typeName', '').casefold() == 'enum'

    @staticmethod
    def is_bitfield_type(type_data: TypeInfoType) -> bool:
        return getattr(type_data, 'typeName', '').casefold() == 'bitfield'

    def get_status_type_from_device_name(self, name: str) -> TypeInfoType:
        device_desc = self.deviceDescriptions[name]
        status_name = device_desc.status_prop.typeName
        assert status_name is not None
        return self.types[status_name]

    @staticmethod
    def _update_device_description(
        device_description: TypeInfoDeviceDescription,
        exclude_root_methods: list[str] | None = None,
        exclude_properties: list[str] | None = None,
    ) -> None:
        if exclude_root_methods:
            for meth in exclude_root_methods:
                device_description.del_root_method(meth)
        if exclude_properties:
            for prop in exclude_properties:
                device_description.del_prop(prop)

    @staticmethod
    def _update_status_type(
        status_type: TypeInfoType,
        exclude_status_fields: list[str]
    ) -> None:
        for field in exclude_status_fields:
            status_type.del_field(field)

    def update_device(
        self,
        device_name: str,
        exclude_root_methods: list[str] | None = None,
        exclude_properties: list[str] | None = None,
        exclude_status_fields: list[str] | None = None
    ) -> None:
        description = self.deviceDescriptions[device_name]
        self._update_device_description(
            description, exclude_root_methods, exclude_properties
            )
        if exclude_status_fields:
            status_type = self.get_status_type_from_device_name(device_name)
            self._update_status_type(status_type, exclude_status_fields)

    def create_child_device(
        self,
        device_name: str,
        parent_device_name: str,
        exclude_root_methods: list[str] | None = None,
        exclude_properties: list[str] | None = None,
        exclude_status_fields: list[str] | None = None
    ) -> None:
        # create and update the child device description
        # as a copy of the parent device description
        parent_description = self.deviceDescriptions[parent_device_name]
        child_description = copy.deepcopy(parent_description)
        self._update_device_description(
            child_description, exclude_root_methods, exclude_properties
            )
        # add reference to the parent device description
        child_description = child_description.add_attrs(
            restrictionOfDevice=parent_device_name
            )
        # add the new child device description to device descriptions
        self.deviceDescriptions[device_name] = child_description
        if exclude_status_fields:
            # create and update the child status type
            # as a copy of the parent status type
            parent_status_type = self.get_status_type_from_device_name(
                parent_device_name
                )
            child_status_type = copy.deepcopy(parent_status_type)
            self._update_status_type(child_status_type, exclude_status_fields)
            # udpate status type name in the child description
            parent_status_name = child_description.status_prop.typeName
            child_status_name = f'Status{device_name}'
            child_description.status_prop.typeName = child_status_name
            # add reference to the parent status type
            child_status_type = child_status_type.add_attrs(
                restrictionOfType=parent_status_name
                )
            # add the new status type to TypeInfo types
            self.types[child_status_name] = child_status_type

    def update_superior_system(
        self,
        exclude_methods: list[str] | None = None,
        exclude_status_fields: list[str] | None = None
    ) -> None:
        system = self.deviceDescriptions['System_G3']
        if exclude_methods:
            sup_system_prop = system.get_prop('SuperiorSystem')
            assert sup_system_prop.methods is not None
            list_ops_methods = ListOperations(sup_system_prop.methods)
            for meth in exclude_methods:
                list_ops_methods.delete(meth)
        if exclude_status_fields:
            sup_system_status = self.types['StatusSuperiorSystem']
            self._update_status_type(sup_system_status, exclude_status_fields)

    def update_from_system_config(
        self, system_config: dict, zone_name: str
    ) -> None:
        logger.info(
            'Updating TypeInfo CPON file from system config data (zone "%s")',
            zone_name
            )
        SystemDictConnector(zone_name, system_config, self).update()

    def update_from_system_config_local_file(
        self, file_path: str, zone_name: str
    ) -> None:
        logger.info(
            'Parsing system config file "%s"', os.path.abspath(file_path)
            )
        with open(file_path, 'r') as file:
            system_config = json.load(file)
        self.update_from_system_config(system_config, zone_name)


class SystemDictConnector:
    def __init__(
        self,
        zone_name: str,
        system_data: dict,  # SystemDict
        type_info: TypeInfo
    ) -> None:
        self.system = system_data
        self.zone = Zone.from_system_config(zone_name, system_data)  # type: ignore  # noqa
        self.type_info = type_info

    def update_device_descriptions(self) -> None:
        logger.info("Updating deviceDescriptions...")
        for type_data in self.system['Visu'].values():
            exclude_root_methods = []
            exclude_properties = []
            exclude_status_fields = []
            for var_data in type_data['vars'].values():
                var = var_data['name']
                if not var_data['is_deleted']:
                    continue
                if var.startswith('method'):
                    exclude_root_methods.append(var.removeprefix('method/'))
                elif var.startswith('status'):
                    exclude_status_fields.append(var.removeprefix('status/'))
                else:
                    exclude_properties.append(var)
            if type_data['restricted_to']:
                self.type_info.create_child_device(
                    device_name=type_data['type'],
                    parent_device_name=type_data['restricted_to'],
                    exclude_properties=exclude_properties,
                    exclude_root_methods=exclude_root_methods,
                    exclude_status_fields=exclude_status_fields
                    )
            else:
                self.type_info.update_device(
                    device_name=type_data['type'],
                    exclude_properties=exclude_properties,
                    exclude_root_methods=exclude_root_methods,
                    exclude_status_fields=exclude_status_fields
                )
        logger.info("deviceDescriptions updated successfully.")

    def update_device_paths(self) -> None:
        logger.info("Updating device paths...")
        self.type_info.devicePaths.clear()
        for element in self.zone.all_elements:
            path = element.shv_path
            visu_data = element.data.get('device_dict', {}).get('visu', {})
            visu_type = visu_data.get('shvDeviceType', '')
            if path and (visu_type or 'system' in path.lower()):
                if(path == "systemSafety"):
                    path_systemSafety = "systemSafety/SafeLogic"
                    self.type_info.devicePaths[path_systemSafety] = visu_type
                else:
                    self.type_info.devicePaths[path] = visu_type
        logger.info("Device paths updated successfully.")

    def update_gpio(self) -> None:
        logger.info("Updating GPIO device types...")
        gpio_inputs = self.type_info.types['GPIOInputs'].add_attrs(
            siteSpecificLocalization=True
            )
        self.type_info.types['GPIOInputs'] = gpio_inputs
        gpio_outputs = self.type_info.types['GPIOOutputs'].add_attrs(
            siteSpecificLocalization=True
            )
        self.type_info.types['GPIOOutputs'] = gpio_outputs
        logger.info("GPIO device types updated successfully.")

    def update_status_buttons(self) -> None:
        logger.info("Updating StatusButtons device type...")
        buttons = self.type_info.types['StatusButtons'].add_attrs(
            siteSpecificLocalization=True
            )
        self.type_info.types['StatusButtons'] = buttons
        logger.info("StatusButtons device updated successfully.")

    def update_extra_tags(self) -> None:
        logger.info("Updating extraTags...")
        tags = self.type_info.extraTags
        tags.clear()
        if self.zone.is_safety:
            key = f'{self.zone.shv_path}/method/setNormal'
            tags[key] = {"safetyManager": "systemSafety"}
        for route in self.zone.find_by_type(Route):
            tags[route.shv_path] = {"startGate": route.layout.entry_gate.name}
        logger.info("extraTags updated successfully.")

    def update_blacklisted_paths(self) -> None:
        logger.info("Updating blacklistedPaths...")
        # remove default
        default = 'devices/zone/Zone/gate/G01/requestMemory'
        if default in self.type_info.blacklistedPaths:
            del self.type_info.blacklistedPaths[default]
        # add actual gates
        for gate in self.zone.find_by_type(Gate):
            gate_visu_data = gate.data.get('device_dict', {}).get('visu', {})
            gate_visu_type_name = gate_visu_data.get('shvDeviceType', '')
            if not gate_visu_type_name:
                logger.warning(f'Gate "{gate.name}" does not have a Visu type')
                continue
            gate_visu_type = self.system['Visu'][gate_visu_type_name]
            request_memory = gate_visu_type['vars']['requestMemory']
            if request_memory['is_blacklisted']:
                key = f'{gate.shv_path}/requestMemory'
                self.type_info.blacklistedPaths[key] = None
        logger.info("blacklistedPaths updated successfully.")

    def update(self) -> None:
        logger.info("Updating typeInfo...")
        self.update_device_descriptions()
        self.update_device_paths()
        self.update_gpio()
        self.update_status_buttons()
        self.update_extra_tags()
        self.update_blacklisted_paths()
        logger.info("typeInfo updated successfully.")
