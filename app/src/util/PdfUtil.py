from weasyprint import HTML
from io import BytesIO

class PdfUtil:
    @staticmethod
    def html_to_pdf(html):
        pdf_bytes = BytesIO()
        HTML(html).write_pdf(pdf_bytes)
        return pdf_bytes
