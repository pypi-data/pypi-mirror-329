from ._base_classes import ProteanService
from .models import QuestionResponse, QuestionRequest, VectorSearchResponse, VectorSearchRequest


class Chat(ProteanService):
    SERVICE_BASE_PATH: str = "/api/chat-service"

    def question(
            self,
            *,
            question_request: QuestionRequest
    ) -> QuestionResponse:
        """Creates a response for the provided prompt and parameters."""
        return self.call(
            "POST",
            f"{self.SERVICE_BASE_PATH}/question",
            json=question_request.model_dump(by_alias=True, exclude_none=True),
            response_type=QuestionResponse
        )


class Vector(ProteanService):
    SERVICE_BASE_PATH: str = "/api/vector-service/vectors"

    def search(
            self,
            *,
            vector_search_request: VectorSearchRequest
    ) -> VectorSearchResponse:
        """Search in the vector datastore based on the provided query."""
        return self.call(
            "POST",
            f"{self.SERVICE_BASE_PATH}/search",
            json=vector_search_request.model_dump(by_alias=True, exclude_none=True),
            response_type=VectorSearchResponse
        )
