from typing import Optional

from pydantic import BaseModel, Field

# saved to file
class MainConfigEntity(BaseModel):
    thestage_auth_token: Optional[str] = Field(None, alias='thestage_auth_token')
    thestage_api_url: Optional[str] = Field(None, alias='thestage_api_url')


class DaemonConfigEntity(BaseModel):
    daemon_token: Optional[str] = Field(None, alias='daemon_token')
    backend_api_url: Optional[str] = Field(None, alias='backend_api_url')

# not saved to file
class RuntimeConfigEntity(BaseModel):
    working_directory: Optional[str] = Field(None, alias='working_directory')
    config_global_path: Optional[str] = Field(None, alias='config_global_path')


class ConfigEntity(BaseModel):
    main: MainConfigEntity = Field(default_factory=MainConfigEntity, alias='main')
    runtime: RuntimeConfigEntity = Field(default_factory=RuntimeConfigEntity, alias="runtime") # TODO merge with main
    daemon: DaemonConfigEntity = Field(default_factory=DaemonConfigEntity, alias="daemon") # TODO this should not be in core package
    start_on_daemon: bool = Field(False, alias='start_on_daemon') # TODO this should not be in core package
