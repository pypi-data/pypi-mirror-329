import logging
import typing

from abc import ABC, abstractmethod
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


logger = logging.getLogger('g3visu.meta')


class BaseMeta(BaseModel, ABC):
    """Base class for meta data classes."""
    model_config = ConfigDict(
        alias_generator=to_camel,
        validate_assignment=True,
        populate_by_name=True,
        )

    @classmethod
    @abstractmethod
    def model_validate_system_config(cls, system_config: dict) -> typing.Self:
        pass


class MetaProjectSiteWare(BaseMeta):
    shv_user: str = Field(default="")
    shv_password: str = Field(default="")
    default_language: str
    language_array: list[str]

    @classmethod
    def model_validate_system_config(
        cls, system_config: dict, **kwargs
    ) -> typing.Self:
        project_dict: dict = system_config['Software']['Common']['Project']
        project_data: dict = list(project_dict.values())[0]
        language = project_data['general']['language']
        language_array = ['en', language]

        if str(kwargs['shv_user'])=='None':
            shv_password = ""
            shv_user = ""
            logger.info("No default shv user name defined, using empty string")
        else:
            shv_user = kwargs['shv_user']
            if str(kwargs['shv_password'])=='None':
                shv_password = ""
                logger.info("No default shv user password defined, using empty string")
            else:
                shv_password = kwargs['shv_password']
        return cls(shv_user=shv_user, shv_password=shv_password, default_language=language, language_array=language_array)


class MetaProject(BaseMeta):
    """'_meta.json' file data model for the project."""
    name: str
    siteware: MetaProjectSiteWare

    @classmethod
    def model_validate_system_config(
        cls, system_config: dict, **kwargs
    ) -> typing.Self:
        project_dict: dict = system_config['Software']['Common']['Project']
        project_data: dict = list(project_dict.values())[0]
        name = project_data['general']['location']
        if not name:
            name = project_data['general']['name']
        siteware = MetaProjectSiteWare.model_validate_system_config(
            system_config, shv_user=kwargs['shv_user'], shv_password=kwargs['shv_password']
            )
        return cls(name=name, siteware=siteware)


class MetaZone(BaseMeta):
    """'_meta.json' file data model for the zone."""
    type_: str = Field(default="DepotG3", alias="type")
    name: str = Field(default="")
    gps: tuple[float, float] = Field(default=(0.0, 0.0))
    hp3: dict[str, str] = Field(default={"syncPath": ".app/history"}, alias="HP3")
    visu: dict[str, str] = Field(default={"svgPath": "_files/site.svg"})

    @classmethod
    def model_validate_system_config(
        cls, system_config: dict, **kwargs
    ) -> typing.Self:
        system_dict: dict = system_config['Software']['Common']['System']
        system_data: dict = list(system_dict.values())[0]
        try:
            gps_str = system_data['general']['gps_location']
            gps_str_split = gps_str.split(',')
            gps = (float(gps_str_split[0]), float(gps_str_split[1]))
        except Exception as e:
            logger.warning(f"Could not parse gps from system config: {e}")
            gps = (0.0, 0.0)
        if 'name' not in kwargs:
            logger.warning("No zone name provided, using empty string")
            return cls(gps=gps)
        zone_name = kwargs['name']
        if zone_name not in system_config['Software']:
            logger.error(
                f"Zone name not found in system config: {zone_name}. "
                f"Using empty string"
                )
            return cls(gps=gps)
        zone_dict = system_config['Software'][zone_name]['Zone']
        zone_data = list(zone_dict.values())[0]
        visu_name = zone_data.get('visu', {}).get('name', '')
        if not visu_name:
            visu_name = zone_data['general']['name']
        return cls(name=visu_name, gps=gps)
