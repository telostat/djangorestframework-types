from typing import Any, Dict, List, Mapping, Optional, Union

from django.template.response import SimpleTemplateResponse
from rest_framework.request import Request

class Response(SimpleTemplateResponse):
    data: Any
    exception: bool = ...
    content_type: Optional[str] = ...
    _headers: Dict[str, Any]
    def __init__(
        self,
        data: Any = ...,
        status: Optional[int] = ...,
        template_name: Optional[str] = ...,
        headers: Optional[Mapping[str, str]] = ...,
        exception: bool = ...,
        content_type: Optional[str] = ...,
    ): ...
    @property
    def rendered_content(self): ...
    @property
    def status_text(self) -> str: ...
