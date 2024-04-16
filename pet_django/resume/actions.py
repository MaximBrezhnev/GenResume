import uuid

import PyPDF2
from PyPDF2 import PdfReader
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import StyleSheet1
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate

from pet_django.settings import BASE_DIR


def generate_filename() -> str:
    folder_path = BASE_DIR / "resume" / "documents"
    return str(folder_path / f"{uuid.uuid4()}.pdf")


def form_text_for_pdf(
    key: str,
    value: str | list[str],
    sample_style_sheet: StyleSheet1,
    flowables: list[Paragraph],
) -> None:
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


def generate_document(data: dict[str : str | list[str]]) -> str:
    filename = generate_filename()
    my_doc = SimpleDocTemplate(filename)
    sample_style_sheet = getSampleStyleSheet()
    flowables = []

    pdfmetrics.registerFont(TTFont("Arial", "arial.ttf"))
    sample_style_sheet.add(ParagraphStyle(name="Arial", fontName="Arial"))

    for key, value in data.items():
        form_text_for_pdf(key, value, sample_style_sheet, flowables)

    my_doc.build(flowables)

    return filename.split(".")[0].split("/")[-1]


def extract_text_from_document(document_id: str) -> str:
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


def convert_text_to_dict(text: str) -> list[dict[str : str | list[str]]]:
    position_list = []
    text = "#$Позиция".join(text.split("Позиция"))

    for position_descr in text.split("#$")[1:]:
        data = {}
        for item in position_descr.split(";\n")[:-1]:
            item = item.split(": ")
            key = item[0].replace("\n", "")
            value = item[1].replace("\n", "")

            if len(value.split(", ")) > 1:
                data[key] = value.split(", ")
            else:
                data[key] = value
        position_list.append(data)

    return position_list


def form_dict_for_response(
    position_list: list,
) -> list[dict[str : str | list[str]]]:
    position_list_for_response = []

    for position in position_list:
        data_for_response = {}
        for key, value in position.items():
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
        position_list_for_response.append(data_for_response)

    return position_list_for_response


def get_data_from_document(document_id: str) -> list[dict[str : str | list[str]]]:
    text = extract_text_from_document(document_id)
    data = convert_text_to_dict(text)
    return form_dict_for_response(data)


def reformat_extracted_text(
    text: str, sample_style_sheet: StyleSheet1, flowables: list[Paragraph]
) -> None:
    text = "#$Позиция".join(text.split("Позиция"))

    for position in text.split("#$")[1:]:
        for row in position.split(";\n")[:-1]:
            paragraph = Paragraph(f"{row};", sample_style_sheet["Arial"])
            flowables.append(paragraph)
        flowables.append(Paragraph("<br/><br/>", sample_style_sheet["Normal"]))


def extend_document(document_id: str, data: dict[str:str]) -> str:
    folder_path = BASE_DIR / "resume" / "documents"
    filename = str(folder_path / f"{document_id}.pdf")
    new_filename = generate_filename()

    my_doc = SimpleDocTemplate(new_filename)
    sample_style_sheet = getSampleStyleSheet()
    pdfmetrics.registerFont(TTFont("Arial", "/usr/share/fonts/truetype/arial.ttf"))
    sample_style_sheet.add(ParagraphStyle(name="Arial", fontName="Arial"))
    flowables = []

    existing_pdf = PdfReader(filename)
    for page in existing_pdf.pages:
        reformat_extracted_text(page.extract_text(), sample_style_sheet, flowables)

    for key, value in data.items():
        form_text_for_pdf(key, value, sample_style_sheet, flowables)

    my_doc.build(flowables)
    return new_filename.split(".")[0].split("/")[-1]
