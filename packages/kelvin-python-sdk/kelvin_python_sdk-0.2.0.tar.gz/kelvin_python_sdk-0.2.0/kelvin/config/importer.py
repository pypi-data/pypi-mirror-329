from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Literal, Optional

from pydantic import Field

from kelvin.config.common import AppBaseConfig, AppTypes, ConfigBaseModel, read_schema_file

from .manifest import (
    AppDefaults,
    AppManifest,
    DefaultsDefinition,
    DynamicIODefinition,
    DynamicIoOwnership,
    DynamicIoType,
    Flags,
    IOSchema,
    RuntimeUpdateFlags,
    SchemasDefinition,
)


class RuntimeUpdateConfig(ConfigBaseModel):
    configuration: bool = False


class ImporterFlags(ConfigBaseModel):
    enable_runtime_update: RuntimeUpdateConfig = RuntimeUpdateConfig()


class SchemasConfig(ConfigBaseModel):
    configuration: Optional[str] = None
    io_configuration: Dict[str, str] = {}  # Maps IO names to schema paths


class ImporterIO(ConfigBaseModel):
    name: str
    data_types: List[str] = Field(default=["number", "string", "boolean"])
    control: bool = False


class DeploymentDefaults(ConfigBaseModel):
    system: dict = {}
    configuration: dict = {}


class ImporterConfig(AppBaseConfig):
    type: Literal[AppTypes.importer]
    spec_version: str = "5.0.0"

    flags: ImporterFlags = ImporterFlags()
    importer_io: List[ImporterIO] = []
    ui_schemas: SchemasConfig = SchemasConfig()
    defaults: DeploymentDefaults = DeploymentDefaults()

    def to_manifest(self, read_schemas: bool = True, workdir: Path = Path(".")) -> AppManifest:
        return convert_importer_to_manifest(self, read_schemas=read_schemas, workdir=workdir)


def convert_importer_to_manifest(
    config: ImporterConfig, read_schemas: bool = True, workdir: Path = Path(".")
) -> AppManifest:
    schemas = SchemasDefinition()
    if read_schemas:
        schemas.configuration = (
            read_schema_file(workdir / config.ui_schemas.configuration) if config.ui_schemas.configuration else {}
        )
        schemas.io_configurations = [
            IOSchema(type_name=io, io_schema=read_schema_file(workdir / schema_path) if schema_path else {})
            for io, schema_path in config.ui_schemas.io_configuration.items()
        ]

    return AppManifest(
        name=config.name,
        title=config.title,
        description=config.description,
        type=config.type,
        version=config.version,
        category=config.category,
        flags=Flags(
            spec_version=config.spec_version,
            enable_runtime_update=RuntimeUpdateFlags(configuration=config.flags.enable_runtime_update.configuration),
        ),
        dynamic_io=[
            DynamicIODefinition(
                type_name=io.name,
                data_types=io.data_types,
                ownership=DynamicIoOwnership.owned,
                type=DynamicIoType.both if io.control else DynamicIoType.data,
            )
            for io in config.importer_io
        ],
        schemas=schemas,
        defaults=DefaultsDefinition(
            app=AppDefaults(configuration=config.defaults.configuration), system=config.defaults.system
        ),
    )
