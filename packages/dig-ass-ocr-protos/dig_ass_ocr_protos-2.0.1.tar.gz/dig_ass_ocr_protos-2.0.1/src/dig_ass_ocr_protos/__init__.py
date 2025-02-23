__version__ = "2.0.1"

from .DigitalAssistantOCR_pb2 import DigitalAssistantOCRRequest, DigitalAssistantOCRResponse, DocType
from .DigitalAssistantOCR_pb2_grpc import DigitalAssistantOCR, DigitalAssistantOCRServicer, DigitalAssistantOCRStub

from .client import OCRClient
