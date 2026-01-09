__version__ = "0.3.2"

from typing import Any, Dict, List, Optional, TypeVar

from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, Response
from typing_extensions import Annotated, Doc, deprecated

from .utils import get_swagger2


# Keep mypy happy with the monkey patching
class FastAPIEx(FastAPI):
    swagger2_url: Optional[str]
    swagger2_tags: Optional[List[Dict[str, Any]]]
    swagger2_docs_url: Optional[str]
    swagger2_redoc_url: Optional[str]
    swagger2_ui_oauth2_redirect_url: Optional[str]
    swagger2_ui_init_oauth: Optional[Dict[str, Any]]
    swagger2_ui_parameters: Optional[Dict[str, Any]]
    swagger2_external_docs: Optional[Dict[str, Any]]
    swagger2_version: str = "2.0"
    swagger2_schema: Optional[Dict[str, Any]]

    swagger2: Any


AppType = TypeVar("AppType", bound="FastAPIEx")


class FastAPISwagger2:
    def __init__(
        self,
        app: AppType,
        swagger2_url: Annotated[
            Optional[str],
            Doc(
                """
                The URL where the Swagger2 schema will be served from.

                If you set it to `None`, no Swagger2 schema will be served publicly, and
                the default automatic endpoints `/swagger2/docs` and `/swagger2/redoc` will also be
                disabled.

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#openapi-url).

                **Example**

                ```python
                from fastapi_swagger2 import FastAPISwagger2

                FastAPISwagger2(app, swagger2_url="/api/v1/swagger2.json")
                ```
                """
            ),
        ] = "/swagger2.json",
        swagger2_tags: Annotated[
            Optional[List[Dict[str, Any]]],
            Doc(
                """
                A list of tags used by Swagger2, these are the same `tags` you can set
                in the *path operations*, like:

                * `@app.get("/users/", tags=["users"])`
                * `@app.get("/items/", tags=["items"])`

                The order of the tags can be used to specify the order shown in
                tools like Swagger UI, used in the automatic path `/docs`.

                It's not required to specify all the tags used.

                The tags that are not declared MAY be organized randomly or based
                on the tools' logic. Each tag name in the list MUST be unique.

                The value of each item is a `dict` containing:

                * `name`: The name of the tag.
                * `description`: A short description of the tag.
                    [CommonMark syntax](https://commonmark.org/) MAY be used for rich
                    text representation.
                * `externalDocs`: Additional external documentation for this tag. If
                    provided, it would contain a `dict` with:
                    * `description`: A short description of the target documentation.
                        [CommonMark syntax](https://commonmark.org/) MAY be used for
                        rich text representation.
                    * `url`: The URL for the target documentation. Value MUST be in
                        the form of a URL.

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-tags).

                **Example**

                ```python
                from fastapi_swagger2 import FastAPISwagger2

                tags_metadata = [
                    {
                        "name": "users",
                        "description": "Operations with users. The **login** logic is also here.",
                    },
                    {
                        "name": "items",
                        "description": "Manage items. So _fancy_ they have their own docs.",
                        "externalDocs": {
                            "description": "Items external docs",
                            "url": "https://fastapi.tiangolo.com/",
                        },
                    },
                ]

                FastAPISwagger2(app, swagger2_tags=tags_metadata)
                ```
                """
            ),
        ] = None,
        swagger2_docs_url: Annotated[
            Optional[str],
            Doc(
                """
                The path to the automatic interactive API documentation.
                It is handled in the browser by Swagger UI.

                The default URL is `/swagger2/docs`. You can disable it by setting it to `None`.

                If `swagger2_url` is set to `None`, this will be automatically disabled.

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls).

                **Example**

                ```python
                from fastapi_swagger2 import FastAPISwagger2

                FastAPISwagger2(app, docs_url="/swagger2/documentation", redoc_url=None)
                ```
                """
            ),
        ] = "/swagger2/docs",
        swagger2_redoc_url: Annotated[
            Optional[str],
            Doc(
                """
                The path to the alternative automatic interactive API documentation
                provided by ReDoc.

                The default URL is `/swagger2/redoc`. You can disable it by setting it to `None`.

                If `swagger2_url` is set to `None`, this will be automatically disabled.

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls).

                **Example**

                ```python
                from fastapi_swagger2 import FastAPISwagger2

                FastAPISwagger2(app, docs_url="/swagger2/documentation", redoc_url="/swagger2/redocumentation")
                ```
                """
            ),
        ] = "/swagger2/redoc",
        swagger2_ui_oauth2_redirect_url: Annotated[
            Optional[str],
            Doc(
                """
                The OAuth2 redirect endpoint for the Swagger2 UI.

                By default it is `/swagger2/docs/oauth2-redirect`.

                This is only used if you use OAuth2 (with the "Authorize" button)
                with Swagger UI.
                """
            ),
        ] = "/swagger2/docs/oauth2-redirect",
        swagger2_ui_init_oauth: Annotated[
            Optional[Dict[str, Any]],
            Doc(
                """
                OAuth2 configuration for the Swagger UI, by default shown at `/swagger2/docs`.

                Read more about the available configuration options in the
                [Swagger UI docs](https://swagger.io/docs/open-source-tools/swagger-ui/usage/oauth2/).
                """
            ),
        ] = None,
        swagger2_ui_parameters: Annotated[
            Optional[Dict[str, Any]],
            Doc(
                """
                Parameters to configure Swagger UI, the autogenerated interactive API
                documentation (by default at `/swagger2/docs`).

                Read more about it in the
                [FastAPI docs about how to Configure Swagger UI](https://fastapi.tiangolo.com/how-to/configure-swagger-ui/).
                """
            ),
        ] = None,
        swagger2_external_docs: Annotated[
            Optional[Dict[str, Any]],
            Doc(
                """
                This field allows you to provide additional external documentation links.
                If provided, it must be a dictionary containing:

                * `description`: A brief description of the external documentation.
                * `url`: The URL pointing to the external documentation. The value **MUST**
                be a valid URL format.

                **Example**:

                ```python
                from fastapi_swagger2 import FastAPISwagger2

                external_docs = {
                    "description": "Detailed API Reference",
                    "url": "https://example.com/api-docs",
                }

                FastAPISwagger2(app, swagger2_external_docs=external_docs)
                ```
                """
            ),
        ] = None,
    ) -> None:
        self.app = app
        self.app.swagger2_url = swagger2_url
        self.app.swagger2_tags = swagger2_tags
        self.app.swagger2_docs_url = swagger2_docs_url
        self.app.swagger2_redoc_url = swagger2_redoc_url
        self.app.swagger2_ui_oauth2_redirect_url = swagger2_ui_oauth2_redirect_url
        self.app.swagger2_ui_init_oauth = swagger2_ui_init_oauth
        self.app.swagger2_ui_parameters = swagger2_ui_parameters
        self.app.swagger2_external_docs = swagger2_external_docs

        self.app.swagger2_version = "2.0"
        self.app.swagger2_schema = None
        if self.app.swagger2_url:
            assert self.app.title, "A title must be provided for Swagger2, e.g.: 'My API'"
            assert self.app.version, "A version must be provided for Swagger2, e.g.: '2.1.0'"

        self.app.swagger2 = self.swagger2

        self.setup()

    def setup(self) -> None:
        if self.app.swagger2_url:
            urls = (server_data.get("url") for server_data in self.app.servers)
            server_urls = {url for url in urls if url}

            async def swagger2(req: Request) -> JSONResponse:
                root_path = req.scope.get("root_path", "").rstrip("/")
                if root_path not in server_urls:
                    if root_path and self.app.root_path_in_servers:
                        self.app.servers.insert(0, {"url": root_path})
                        server_urls.add(root_path)
                return JSONResponse(self.swagger2())

            self.app.add_route(self.app.swagger2_url, swagger2, include_in_schema=False)

            if self.app.swagger2_docs_url:

                async def swagger_ui_html(req: Request) -> HTMLResponse:
                    root_path = req.scope.get("root_path", "").rstrip("/")
                    swagger2_url = root_path + self.app.swagger2_url
                    oauth2_redirect_url = self.app.swagger2_ui_oauth2_redirect_url
                    if oauth2_redirect_url:
                        oauth2_redirect_url = root_path + oauth2_redirect_url
                    return get_swagger_ui_html(
                        openapi_url=swagger2_url,
                        title=f"{self.app.title} - Swagger2 UI",
                        oauth2_redirect_url=oauth2_redirect_url,
                        init_oauth=self.app.swagger2_ui_init_oauth,
                        swagger_ui_parameters=self.app.swagger2_ui_parameters,
                    )

                self.app.add_route(self.app.swagger2_docs_url, swagger_ui_html, include_in_schema=False)

                if self.app.swagger2_ui_oauth2_redirect_url:

                    async def swagger_ui_redirect(req: Request) -> HTMLResponse:
                        return get_swagger_ui_oauth2_redirect_html()

                    self.app.add_route(
                        self.app.swagger2_ui_oauth2_redirect_url,
                        swagger_ui_redirect,
                        include_in_schema=False,
                    )

            if self.app.swagger2_redoc_url:

                async def redoc_html(req: Request) -> HTMLResponse:
                    root_path = req.scope.get("root_path", "").rstrip("/")
                    swagger2_url = root_path + self.app.swagger2_url
                    return get_redoc_html(
                        openapi_url=swagger2_url,
                        title=f"{self.app.title} - Swagger2 ReDoc",
                    )

                self.app.add_route(self.app.swagger2_redoc_url, redoc_html, include_in_schema=False)

    def swagger2(self) -> Dict[str, Any]:
        """
        Generate the Swagger2 schema of the application. This is called by FastAPISwagger2
        internally.

        The first time it is called it stores the result in the attribute
        `app.swagger2_schema`, and next times it is called, it just returns that same
        result. To avoid the cost of generating the schema every time.

        If you need to modify the generated Swagger2 schema, you could modify it.

        Read more in the
        [FastAPI docs for OpenAPI](https://fastapi.tiangolo.com/how-to/extending-openapi/).
        """
        if not self.app.swagger2_schema:
            self.app.swagger2_schema = get_swagger2(
                title=self.app.title,
                version=self.app.version,
                openapi_version=self.app.swagger2_version,
                summary=self.app.summary,
                description=self.app.description,
                terms_of_service=self.app.terms_of_service,
                contact=self.app.contact,
                license_info=self.app.license_info,
                routes=self.app.routes,
                webhooks=self.app.webhooks.routes,
                tags=list(
                    {
                        tag["name"]: tag for tag in (self.app.openapi_tags or []) + (self.app.swagger2_tags or [])
                    }.values()
                ),
                servers=self.app.servers,
                separate_input_output_schemas=self.app.separate_input_output_schemas,
                external_docs=self.app.swagger2_external_docs,
            )
        return self.app.swagger2_schema
