from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO


class PointReportGenerator:
    @staticmethod
    def generate_pdf(worker, points, month, year):
        buffer = BytesIO()  # Buffer para armazenar o PDF
        c = canvas.Canvas(buffer, pagesize=letter)  # Criando o objeto canvas

        # Define o título do relatório e o adiciona ao PDF
        title = f"Funcionário: {worker.username} - Mês/Ano: {month}/{year}"
        c.drawString(30, 800, title)  # Posição do título no documento

        # Variáveis para controlar a posição do texto
        y_position = 780
        line_height = 18

        # Loop para adicionar informações de cada ponto no documento
        for point in points:
            y_position = PointReportGenerator.__add_point_to_canvas(c, point, y_position, line_height)

            # Checagem para adicionar nova página se necessário
            if y_position < 50:
                c.showPage()
                y_position = 800

        c.showPage()
        c.save()

        buffer.seek(0)
        return buffer.getvalue().decode('iso-8859-1')  # Retorna o conteúdo do PDF em bytes

    @staticmethod
    def __add_point_to_canvas(canvas, point, y_position, line_height):
        # Formata e adiciona um ponto (registro de presença) ao canvas
        point_details = f"Dia: {point.date}, Situação: {point.situation}, Horas trabalhadas: {point.work_time}"
        canvas.drawString(50, y_position, point_details)
        y_position -= line_height

        # Detalhes dos períodos
        for period in point.periods:
            y_position -= line_height
            period_details = f"Entrada: {period.begin_time}, Saída: {period.end_time}, Horas: {period.work_time}"
            canvas.drawString(60, y_position, period_details)

        return y_position  # Retorna a nova posição vertical após adicionar o ponto
