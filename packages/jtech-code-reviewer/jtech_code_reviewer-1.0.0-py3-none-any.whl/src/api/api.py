import time

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from src.api.router import api_router
from src.core.exceptions.mergerequest_bad_request_exception import MergeRequestBadRequestException
from src.core.exceptions.mergerequest_not_found_exception import MergeRequestNotFoundException
from src.infra.config.constants import Constants
from src.infra.config.logging_config import get_logger

LOGGER = get_logger()


async def log_request_data(request: Request, call_next):
    """
    Log the request data.

    Args:
        request (Request): The request instance
        call_next (Callable): The next callable
    """
    LOGGER.info(f"Request: {request.method} {request.url}")
    start_time = time.time()
    body = await request.body()
    if body:
        LOGGER.debug(f">>> Request Body: {body.decode('utf-8')}")
    response = await call_next(request)
    LOGGER.debug(f"<<< Response: {response.status_code}")
    process_time = time.time() - start_time
    LOGGER.debug(f"::: Processed in {process_time:.4f} seconds :::")


class API:
    def __init__(self):
        self.app = self.create_app()
        self.add_middlewares()

    def create_app(self):
        """
        Create the FastAPI app.


        Returns:
            FastAPI: The FastAPI app instance.
        """
        app = FastAPI(
            title=Constants.PROJECT_NAME,
            description=Constants.PROJECT_DESCRIPTION,
            version=Constants.PROJECT_VERSION,
            summary=Constants.PROJECT_DESCRIPTION,
            contact={},
            swagger_ui_parameters={
                "defaultModelsExpandDepth": -1,
                "defaultModelExpandDepth": -1,
                "defaultModelRendering": "example",
                "displayRequestDuration": True,
                "filter": True,
                "oauth2RedirectUrl": "/docs/oauth2-redirect",
                "operationsSorter": "alpha",
                "requestEditorEnabled": True,
                "showRequestHeaders": True,
                "tryItOutEnabled": True,
                "validatorUrl": None,
            })

        @app.exception_handler(MergeRequestNotFoundException)
        async def merge_request_not_found_exception_handler(request: Request, exc: MergeRequestNotFoundException):
            return JSONResponse(
                status_code=exc.error_code,
                content={"message": exc.message}
            )

        @app.exception_handler(MergeRequestBadRequestException)
        async def merge_request_bad_request_exception_handler(request: Request, exc: MergeRequestBadRequestException):
            return JSONResponse(
                status_code=exc.error_code,
                content={"message": exc.message}
            )

        app.include_router(api_router)

        return app

    def add_middlewares(self):
        """
        Add the middlewares to the FastAPI app.
        """
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        # self.app.middleware('http')(log_request_data)
