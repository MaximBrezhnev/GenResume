import uuid

import PyPDF2
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate

from pet_django.settings import BASE_DIR


def generate_filename():
    folder_path = BASE_DIR / "resume" / "documents"
    return str(folder_path / f"{uuid.uuid4()}.pdf")


def form_text_for_pdf(key, value, sample_style_sheet, flowables):
    # Потом, возможно, придумать новую идею вместо;
    if key == "position_name":
        paragraph = Paragraph(f"Позиция: {value};", sample_style_sheet["Arial"])
        flowables.append(paragraph)
    elif key == "industry":
        paragraph = Paragraph(f"Отрасль: {value};", sample_style_sheet["Arial"])
        flowables.append(paragraph)
    elif key == "leader_competencies":
        paragraph = Paragraph(
            f"Опыт лидера: {', '.join(value)};", sample_style_sheet["Arial"]
        )
        flowables.append(paragraph)
    elif key == "general_competencies":
        paragraph = Paragraph(
            f"Общий опыт: {', '.join(value)};", sample_style_sheet["Arial"]
        )
        flowables.append(paragraph)
    else:
        paragraph = Paragraph(
            f"Профессиональный опыт: {', '.join(value)};", sample_style_sheet["Arial"]
        )
        flowables.append(paragraph)


def generate_document(data):
    filename = generate_filename()
    my_doc = SimpleDocTemplate(filename)
    sample_style_sheet = getSampleStyleSheet()
    flowables = []

    pdfmetrics.registerFont(TTFont("Arial", "arial.ttf"))
    sample_style_sheet.add(ParagraphStyle(name="Arial", fontName="Arial"))

    for key, value in data.items():
        form_text_for_pdf(key, value, sample_style_sheet, flowables)

    my_doc.build(flowables)

    return filename.split(".")[0].split("\\")[-1]


def extract_text_from_document(document_id):
    text = ""

    folder_path = BASE_DIR / "resume" / "documents"
    filename = folder_path / f"{document_id}.pdf"

    with open(filename, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)

        for page_number in range(num_pages):
            page = pdf_reader.pages[page_number]
            text += page.extract_text()

    return text


def convert_text_to_dict(text):
    data = {}

    for item in text.split(";\n")[:-1]:
        item = item.split(": ")
        key = item[0].replace("\n", "")
        value = item[1].replace("\n", "")

        if len(value.split(", ")) > 1:
            data[key] = value.split(", ")
        else:
            data[key] = value

    return data


def form_dict_for_response(data):
    data_for_response = {}
    for key, value in data.items():
        if key == "Позиция":
            data_for_response["position_name"] = value
        elif key == "Отрасль":
            data_for_response["industry"] = value
        elif key == "Опыт лидера":
            data_for_response["leader_competencies"] = value
        elif key == "Общий опыт":
            data_for_response["general_competencies"] = value
        else:
            data_for_response["professional_competencies"] = value

    return data_for_response


def get_data_from_document(document_id):
    text = extract_text_from_document(document_id)
    data = convert_text_to_dict(text)
    return form_dict_for_response(data)


def extend_document():
    return
