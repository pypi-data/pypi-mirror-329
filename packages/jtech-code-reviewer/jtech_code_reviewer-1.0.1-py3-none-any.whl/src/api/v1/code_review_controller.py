from typing import Optional

from fastapi import APIRouter

from src.api.protocols.code_review_response import CodeReviewResponse
from src.infra.di.dependency_container import DependencyContainer

route = APIRouter()

code_review_service = DependencyContainer.get_code_review_service()


@route.get("/{project_id}/{iid}", tags=["code_review"],
           description="This endpoint receives a message and returns a response.",
           summary="Receive a message and return a response.",
           responses={200: {"description": "Message received and response returned."},
                      400: {"description": "Bad Request"},
                      404: {"description": "Not Found"}},
           response_model=CodeReviewResponse)
def get_code_review(project_id: int, iid: int) -> Optional[CodeReviewResponse]:
    """
    Get code review by project id and iid.

    Args:
        project_id (int): The project id.
        iid (int): The iid.

    Returns:
        CodeReviewResponse: The code review response.
    """
    return code_review_service.code_review(project_id, iid)
