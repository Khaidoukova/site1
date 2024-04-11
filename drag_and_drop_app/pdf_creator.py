import tempfile

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak
from PyPDF2 import PdfMerger
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


def create_dog_owner_pdf(owner, dog, dog_classes, judge, competition, signs):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    filename = temp_file.name

    doc = SimpleDocTemplate(filename, pagesize=letter, encoding='utf-8')
    elements = []

    #  pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
    # Регистрация шрифта DejaVu Sans
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))

    styles = getSampleStyleSheet()
    style = styles['Normal']
    #  style.fontName = 'Arial'

    for dog_class in dog_classes:
        data = [
            ['Хозяин', owner],
            ['Собака', dog],
            ['Класс собаки', dog_class],
            ['Судья', judge],
            ['Соревнование', competition],
            ['№', 'Название знака', 'Штраф', 'Комментарии']
        ]
        index = 1

        for sign in signs:
            data.append([index, sign, '', ''])
            index += 1

        table = Table(data, colWidths=[1.3*inch, 2.5*inch, 1.3*inch, 1.8*inch, 2.1*inch])

        table.setStyle(TableStyle([
            #  ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTWEIGHT', (0, 0), (-1, -1), 'BOLD'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            ('SPAN', (1, 0), (3, 0)),
            ('SPAN', (1, 1), (3, 1)),
            ('SPAN', (1, 2), (3, 2)),
            ('SPAN', (1, 3), (3, 3)),
            ('SPAN', (1, 4), (3, 4)),

        ]))

        elements.append(table)
        elements.append(PageBreak())

    doc.build(elements)

    merger = PdfMerger()
    merger.append(filename)
    with tempfile.NamedTemporaryFile(delete=False) as merged_file:
        merger.write(merged_file.name)
    merger.close()

    return merged_file.name

