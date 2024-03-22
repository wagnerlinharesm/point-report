import pdfkit

class PdfUtil:
    @staticmethod
    def html_to_pdf(html):
        return pdfkit.from_string(html, False)