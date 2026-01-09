from typing import Any, Dict, List, Optional, Union

from fastapi.openapi.models import (
    BaseModelWithConfig,
    Components,
    ExternalDocumentation,
    Info,
    PathItem,
    Reference,
    Server,
    Tag,
)


class Swagger2(BaseModelWithConfig):
    swagger: str
    info: Info
    jsonSchemaDialect: Optional[str] = None
    servers: Optional[List[Server]] = None
    # Using Any for Specification Extensions
    paths: Optional[Dict[str, Union[PathItem, Any]]] = None
    webhooks: Optional[Dict[str, Union[PathItem, Reference]]] = None
    components: Optional[Components] = None
    security: Optional[List[Dict[str, List[str]]]] = None
    tags: Optional[List[Tag]] = None
    externalDocs: Optional[ExternalDocumentation] = None
