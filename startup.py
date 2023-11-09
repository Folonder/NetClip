from fastapi import FastAPI
from app.infrastructure.clipboard import Clipboard
from app.infrastructure.requests_client import RequestsClient
from app.service.clipboard_transfer import ClipboardTransfer


app = FastAPI()


if __name__ == "__main__":
    clipboard_transfer = ClipboardTransfer(RequestsClient(), Clipboard())

