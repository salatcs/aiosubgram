from typing import TYPE_CHECKING, TypeVar, Type, Dict, Optional, Any

if TYPE_CHECKING:
    from ..base import BaseClient, KeyType
    from ..types.base import SubgramObject

T = TypeVar("T")

class MethodMixin:
    def __init__(self, *args, **kwargs):
        pass
    if TYPE_CHECKING:
        async def _make_request(
            self, 
            method: str, 
            endpoint: str, 
            response_model: Type[Any],
            key_type: Any,
            params: Optional[Dict] = None,
            json: Optional[Dict] = None
        ) -> Any: ...