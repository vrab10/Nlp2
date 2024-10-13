import requests
from typing import AnyStr
from gentopia.tools.basetool import *
from PyPDF2 import PdfReader
from io import BytesIO

class PDFExtractorArgs(BaseModel):
    pdf_url: str = Field(..., description="URL of the PDF document to be processed.")

class PDFExtractor(BaseTool):
    name = "pdf_read"
    args_schema: Optional[Type[BaseModel]] = PDFExtractorArgs
    description: str = "Fetches a PDF from a given URL and extracts its textual content."

    def _run(self, pdf_url: str) -> AnyStr:
        try:
            # Attempt to fetch the PDF from the provided URL
            pdf_response = requests.get(pdf_url)
            pdf_response.raise_for_status()  # Raise exception for unsuccessful requests

            # Create a BytesIO object from the response content
            pdf_buffer = BytesIO(pdf_response.content)

            # Initialize PDF reader
            pdf_document = PdfReader(pdf_buffer)

            # Extract text from all pages
            extracted_text = ""
            for page in pdf_document.pages:
                extracted_text += page.extract_text()

            return extracted_text  # Return the full extracted text

        except requests.exceptions.RequestException as req_error:
            return f"Failed to retrieve the PDF: {str(req_error)}"
        except Exception as general_error:
            return f"An error occurred during PDF processing: {str(general_error)}"

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Asynchronous operation is not supported.")