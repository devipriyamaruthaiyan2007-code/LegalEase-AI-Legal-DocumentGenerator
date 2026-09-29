from io import BytesIO

from docx import Document
from docx.shared import Pt
from fpdf import FPDF


def make_txt(text: str) -> bytes:
    return text.encode("utf-8")


def make_docx(text: str, document_type: str) -> bytes:
    doc = Document()

    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(12)

    doc.add_heading(document_type.upper(), level=0)

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        if line.startswith("# "):
            continue

        if line.startswith("## "):
            doc.add_heading(line[3:].strip(), level=1)
        else:
            doc.add_paragraph(line)

    output = BytesIO()
    doc.save(output)

    return output.getvalue()


def clean_for_pdf(text: str) -> str:
    """
    Replace Unicode characters that the built-in
    FPDF Times font cannot render.
    """

    replacements = {
        "—": "-",
        "–": "-",
        "-": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "…": "...",
        "•": "*",
        "©": "(c)",
        "®": "(R)",
        "™": "(TM)",
        "\u00a0": " ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Remove any remaining characters that
    # cannot be encoded by FPDF core fonts.
    return text.encode("latin-1", errors="replace").decode("latin-1")


def make_pdf(text: str, document_type: str) -> bytes:
    pdf = FPDF()

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    pdf.add_page()

    # -----------------------------
    # TITLE
    # -----------------------------

    pdf.set_font(
        "Times",
        "B",
        16
    )

    title = clean_for_pdf(
        document_type.upper()
    )

    pdf.cell(
        0,
        10,
        title,
        ln=True,
        align="C"
    )

    pdf.ln(5)

    # -----------------------------
    # BODY
    # -----------------------------

    pdf.set_font(
        "Times",
        size=11
    )

    for raw_line in text.splitlines():

        line = raw_line.strip()

        if not line:
            pdf.ln(3)
            continue

        # Skip Markdown H1
        if line.startswith("# "):
            continue

        # Markdown H2
        if line.startswith("## "):

            pdf.ln(2)

            pdf.set_font(
                "Times",
                "B",
                12
            )

            heading = line[3:].strip()

            heading = clean_for_pdf(
                heading
            )

            pdf.multi_cell(
                pdf.epw,
                7,
                heading
            )

            pdf.set_font(
                "Times",
                size=11
            )

            continue

        # Normal paragraph
        line = clean_for_pdf(line)

        # Break extremely long words / URLs
        words = line.split(" ")

        safe_words = []

        for word in words:

            if len(word) <= 70:
                safe_words.append(word)

            else:
                for i in range(
                    0,
                    len(word),
                    70
                ):
                    safe_words.append(
                        word[i:i + 70]
                    )

        safe_line = " ".join(
            safe_words
        )

        pdf.multi_cell(
            pdf.epw,
            6,
            safe_line
        )

    # -----------------------------
    # FOOTER
    # -----------------------------

    pdf.ln(5)

    pdf.set_font(
        "Times",
        "I",
        9
    )

    disclaimer = clean_for_pdf(
        "LegalEase draft. Review by a qualified "
        "legal professional is recommended."
    )

    pdf.multi_cell(
        pdf.epw,
        5,
        disclaimer
    )

    return bytes(pdf.output())