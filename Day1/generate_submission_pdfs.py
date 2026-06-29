#!/usr/bin/env python3
"""Generate submission PDFs from Jupyter notebooks."""

import json
import re
from pathlib import Path

from fpdf import FPDF


REPLACEMENTS = {
    "✅": "[OK]",
    "✏️": "",
    "📖": "",
    "🕒": "",
    "📝": "",
    "📌": "",
    "1️⃣": "1.",
    "2️⃣": "2.",
    "3️⃣": "3.",
    "4️⃣": "4.",
    "5️⃣": "5.",
    "—": "-",
    "’": "'",
    "‘": "'",
    "“": '"',
    "”": '"',
}


def clean_text(text: str) -> str:
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)
    return text.encode("latin-1", "replace").decode("latin-1")


def extract_outputs(outputs: list) -> str:
    lines: list[str] = []
    for output in outputs or []:
        otype = output.get("output_type")
        if otype == "stream":
            text = output.get("text", "")
            lines.append(text if isinstance(text, str) else "".join(text))
        elif otype in ("execute_result", "display_data"):
            data = output.get("data", {})
            if "text/plain" in data:
                text = data["text/plain"]
                lines.append(text if isinstance(text, str) else "".join(text))
        elif otype == "error":
            lines.append("\n".join(output.get("traceback", [])))
    return "".join(lines)


class SubmissionPDF(FPDF):
    def header(self) -> None:
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 8, "JALLOW Abdoulie", align="R", new_x="LMARGIN", new_y="NEXT")
        self.ln(1)


def safe_multi_cell(pdf: FPDF, h: float, text: str, **kwargs) -> None:
    if not text.strip():
        pdf.ln(h)
        return
    width = pdf.epw
    chunks = re.findall(r".{1,100}", text) if len(text) > 100 and " " not in text[:120] else [text]
    for chunk in chunks:
        pdf.multi_cell(width, h, chunk, **kwargs)


def write_markdown(pdf: FPDF, source: str) -> None:
    in_code_block = False
    for line in source.split("\n"):
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            pdf.set_font("Courier", "", 9)
            pdf.set_fill_color(245, 245, 245)
            safe_multi_cell(pdf, 4, "  " + line, fill=True)
            continue

        stripped = line.strip()
        if not stripped:
            pdf.ln(2)
            continue

        if stripped in {"---", "***", "___"}:
            pdf.ln(3)
            continue

        if stripped.startswith("# "):
            pdf.set_font("Helvetica", "B", 14)
            text = re.sub(r"\*\*(.+?)\*\*", r"\1", stripped[2:])
            safe_multi_cell(pdf, 8, text)
            pdf.ln(2)
        elif stripped.startswith("## "):
            pdf.set_font("Helvetica", "B", 12)
            text = re.sub(r"\*\*(.+?)\*\*", r"\1", stripped[3:])
            safe_multi_cell(pdf, 7, text)
            pdf.ln(1)
        elif stripped.startswith("### "):
            pdf.set_font("Helvetica", "B", 11)
            text = re.sub(r"\*\*(.+?)\*\*", r"\1", stripped[4:])
            safe_multi_cell(pdf, 6, text)
        elif stripped.startswith("- "):
            pdf.set_font("Helvetica", "", 10)
            text = re.sub(r"`(.+?)`", r"\1", stripped[2:])
            safe_multi_cell(pdf, 5, f"  - {text}")
        else:
            pdf.set_font("Helvetica", "", 10)
            text = re.sub(r"\*\*(.+?)\*\*", r"\1", stripped)
            text = re.sub(r"`(.+?)`", r"\1", text)
            safe_multi_cell(pdf, 5, text)
    pdf.ln(3)


def write_code(pdf: FPDF, source: str, outputs: list) -> None:
    pdf.set_font("Courier", "", 9)
    pdf.set_fill_color(240, 240, 240)
    for line in source.split("\n"):
        safe_multi_cell(pdf, 4, "  " + line, fill=True)
    pdf.ln(2)

    out_text = clean_text(extract_outputs(outputs))
    if out_text.strip():
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(0, 90, 0)
        safe_multi_cell(pdf, 4, "Output:\n" + out_text)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(3)


def notebook_to_pdf(notebook_path: Path, output_path: Path) -> None:
    with notebook_path.open(encoding="utf-8") as f:
        nb = json.load(f)

    pdf = SubmissionPDF()
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    for cell in nb["cells"]:
        source = clean_text("".join(cell.get("source", [])))
        if cell["cell_type"] == "markdown":
            write_markdown(pdf, source)
        elif cell["cell_type"] == "code":
            write_code(pdf, source, cell.get("outputs", []))

    pdf.output(str(output_path))


def main() -> None:
    base = Path(__file__).parent
    notebooks = [
        ("Lab1.ipynb", "JALLOW_Abdoulie_Lab1.pdf"),
        ("Lab1_Server_Health.ipynb", "JALLOW_Abdoulie_Lab1_Server_Health.pdf"),
    ]
    for nb_name, pdf_name in notebooks:
        src = base / nb_name
        dst = base / pdf_name
        notebook_to_pdf(src, dst)
        print(f"Created: {dst}")


if __name__ == "__main__":
    main()
