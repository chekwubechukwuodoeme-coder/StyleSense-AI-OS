from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)

from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(design):

    filename = "Fashion_Design_Report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "StyleSense AI Fashion Design",
            styles["Title"],
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            design.replace("\n", "<br/>"),
            styles["BodyText"],
        )
    )

    doc.build(story)

    return filename