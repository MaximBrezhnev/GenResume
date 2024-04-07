import uuid

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

# from reportlab.lib.pagesizes import letter

# from reportlab.platypus import SimpleDocTemplate


def generate_filename():
    return f"{uuid.uuid4()}.pdf"


def generate_document(data, output_filename):
    # doc = SimpleDocTemplate(output_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    content = []

    for key, value in data.items():
        if key == "position_name":
            content.append(Paragraph(f"<b>Позиция</b>: {value}", styles["Normal"]))
        # elif key == "leader_competencies":
        #     list_of_competencies = [v for k, v in value.items()]
        #     content.append(Paragraph(f"<b>Компетенции лидера</b>: "
        #                              f"{['<p>' + c + '</p>' for c in list_of_competencies]}"))
        # elif key == "leader_competencies":
        #     list_of_competencies = [v for k, v in value.items()]
        #     content.append(Paragraph(f"<b>Компетенции лидера</b>: "
        #                              f"{['<p>' + c + '</p>' for c in list_of_competencies]}"))
        # else:
        #     list_of_competencies = [v for k, v in value.items()]
        #     content.append(Paragraph(f"<b>Компетенции лидера</b>: "
        #                              f"{['<p>' + c + '</p>' for c in list_of_competencies]}"))


def extend_document():
    return
