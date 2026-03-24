from enum import Enum

from pydantic import BaseModel, Field, model_validator


class PlatformInfo(BaseModel):
    id: str
    name: str


class Platform(Enum):
    CKAN = PlatformInfo(id="ckan", name="CKAN")
    OPENDATASOFT = PlatformInfo(id="opendatasoft", name="Opendatasoft")
    DKAN = PlatformInfo(id="dkan", name="DKAN")
    DATAVERSE = PlatformInfo(id="dataverse", name="Dataverse")
    IHSNNADA = PlatformInfo(id="ihsnnada", name="IHSN NADA")
    KAGGLE = PlatformInfo(id="kaggle", name="Kaggle")
    MTNARDS = PlatformInfo(id="mtnards", name="MTNA Rich Data Services")
    POSTMAN = PlatformInfo(id="postman", name="Postman")
    USCENSUS = PlatformInfo(id="uscensus", name="U.S. Census")
    SOCRATA = PlatformInfo(id="socrata", name="Socrata")


class ServerInfo(BaseModel):
    id: str
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)
    host: str | None = Field(default=None)
    home: str | None = Field(default=None)
    platform: str | None = Field(default=None)
    publisher: list[str] | None = Field(default_factory=list)
    spatial: list[str] | None = Field(default_factory=list)
    version: str | None = Field(default=None)
    postman: dict | None = Field(default=None)

    @model_validator(mode="before")
    @classmethod
    def init_default_values(cls, values):
        if values.get("host") is None:
            values["host"] = values.get("id")
        if values.get("home") is None:
            values["home"] = f"https://{values.get('host')}"
            if values.get("platform") and values["platform"] == "mtnards":
                values["home"] += "/rds"
        if values.get("name") is None:
            values["name"] = values.get("id")
        return values


class MtnaRsdServerInfo(ServerInfo):
    pass


class SocrataServerInfo(ServerInfo):
    pass


class ResourceInfo(BaseModel):
    class Type(Enum):
        CATALOG = "Catalog"
        DATASET = "Dataset"
        PLATFORM = "Platform"
        SERVER = "Server"

    uri: str
    type: Type | None = Field(default=None)
    platform: Platform | None = Field(default=None)
    host: str | None = Field(default=None)
    host_resource_id: str | None = Field(default=None)
