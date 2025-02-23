from agi_med_protos import AbstractClient
from . import DigitalAssistantOCRRequest, DigitalAssistantOCRResponse, DigitalAssistantOCRStub, DocType


class OCRClient(AbstractClient):
    def __init__(self, address) -> None:
        super().__init__(address)
        self._stub = DigitalAssistantOCRStub(self._channel)

    def __call__(self, document: bytes, type_: DocType, request_id: str = "") -> str:
        request = DigitalAssistantOCRRequest(Document=document, Type=type_, RequestId=request_id)
        response: DigitalAssistantOCRResponse = self._stub.GetTextResponse(request)
        return response.Text
