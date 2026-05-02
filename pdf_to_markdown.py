from __future__ import annotations

import argparse
import pathlib
import re
import statistics
from dataclasses import dataclass

from pypdf import PdfReader


LINE_Y_TOLERANCE = 4.5
COLUMN_MARGIN = 24.0


@dataclass
class Span:
    x: float
    y: float
    font_size: float
    text: str


@dataclass
class Line:
    x_min: float
    x_max: float
    y: float
    font_size: float
    text: str


def normalize_span_text(text: str) -> str:
    text = text.replace("\r", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_line_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.;:!?%\]\)])", r"\1", text)
    text = re.sub(r"([\[\(])\s+", r"\1", text)
    if is_heading_like(text):
        text = re.sub(r"\b([A-Z])\s+([A-Z]{2,}\b)", r"\1\2", text)
    return text


def is_heading_like(text: str) -> bool:
    if re.match(r"^(?:[IVXLC]+|[A-Z])\.\s+", text):
        return True
    if text.startswith("TABLE ") or text.startswith("FIG."):
        return True
    letters = [char for char in text if char.isalpha()]
    if len(letters) < 6:
        return False
    uppercase_ratio = sum(char.isupper() for char in letters) / len(letters)
    return uppercase_ratio > 0.75 and len(text) < 120


def is_roman_heading(text: str) -> bool:
    if not re.match(r"^[IVXLC]+\.\s+", text):
        return False
    tail = text.split(".", 1)[1].strip()
    letters = [char for char in tail if char.isalpha()]
    if not letters:
        return False
    uppercase_ratio = sum(char.isupper() for char in letters) / len(letters)
    return uppercase_ratio > 0.85


def is_standalone_line(text: str) -> bool:
    if re.match(r"^\(\d+\)$", text):
        return True
    if text.startswith("TABLE ") or text.startswith("Fig.") or text.startswith("FIG."):
        return True
    if "@" in text:
        return True
    return False


def merge_spans(spans: list[Span]) -> str:
    pieces: list[str] = []
    previous = ""
    for span in sorted(spans, key=lambda item: item.x):
        text = span.text
        if not text:
            continue
        if not pieces:
            pieces.append(text)
            previous = text
            continue
        if text in {"*", "∗", ",", ".", ";", ":", ")", "]", "%", "st", "nd", "rd", "th"}:
            pieces[-1] = pieces[-1] + text
        elif previous.endswith(("(", "[", "/", "-")):
            pieces[-1] = pieces[-1] + text
        else:
            pieces.append(text)
        previous = text
    return normalize_line_text(" ".join(pieces))


def collect_lines(page) -> list[Line]:
    spans: list[Span] = []
    page_width = float(page.mediabox.width)
    segment_gap = page_width * 0.16

    def visitor(text, cm, tm, font_dict, font_size):
        cleaned = normalize_span_text(text)
        if not cleaned:
            return
        spans.append(Span(x=float(tm[4]), y=float(tm[5]), font_size=float(font_size), text=cleaned))

    page.extract_text(visitor_text=visitor)
    spans.sort(key=lambda item: (-item.y, item.x))

    buckets: list[list[Span]] = []
    for span in spans:
        for bucket in buckets:
            if abs(bucket[0].y - span.y) <= LINE_Y_TOLERANCE:
                bucket.append(span)
                break
        else:
            buckets.append([span])

    lines: list[Line] = []
    for bucket in buckets:
        bucket.sort(key=lambda item: item.x)
        segments: list[list[Span]] = [[bucket[0]]]
        for span in bucket[1:]:
            if span.x - segments[-1][-1].x > segment_gap:
                segments.append([span])
            else:
                segments[-1].append(span)

        for segment in segments:
            text = merge_spans(segment)
            if not text or re.match(r"^\d+$", text) or text.startswith("arXiv:"):
                continue
            lines.append(
                Line(
                    x_min=min(item.x for item in segment),
                    x_max=max(item.x for item in segment),
                    y=max(item.y for item in segment),
                    font_size=statistics.median(item.font_size for item in segment),
                    text=text,
                )
            )

    lines.sort(key=lambda item: (-item.y, item.x_min))
    return lines


def estimate_body_font(lines: list[Line]) -> float:
    candidates = [line.font_size for line in lines if len(line.text) >= 30]
    if not candidates:
        candidates = [line.font_size for line in lines]
    return statistics.median(candidates) if candidates else 10.0


def split_page_regions(lines: list[Line], page_width: float) -> tuple[list[Line], list[Line], list[Line]]:
    if not lines:
        return [], [], []

    body_font = estimate_body_font(lines)
    split_x = page_width / 2.0
    right_candidates = [
        line.y
        for line in lines
        if line.x_min >= split_x - COLUMN_MARGIN and len(line.text) >= 20 and line.font_size <= body_font + 1.5
    ]
    top_cutoff = (max(right_candidates) + 12.0) if right_candidates else float("inf")

    abstract_markers = [line.y for line in lines if line.text.lower().startswith("abstract")]
    if abstract_markers:
        top_cutoff = min(top_cutoff, max(abstract_markers) + 5.0)

    top_lines = [line for line in lines if line.y > top_cutoff]
    body_lines = [line for line in lines if line.y <= top_cutoff]
    left_lines = [line for line in body_lines if line.x_min < split_x - 8.0]
    right_lines = [line for line in body_lines if line.x_min >= split_x - 8.0]
    return top_lines, left_lines, right_lines


def paragraph_gap(lines: list[Line]) -> float:
    gaps = []
    for previous, current in zip(lines, lines[1:]):
        gap = previous.y - current.y
        if 3.0 <= gap <= 40.0:
            gaps.append(gap)
    return statistics.median(gaps) if gaps else 12.0


def join_paragraph(previous: str, current: str) -> str:
    if previous.endswith("-") and current[:1].islower():
        return previous[:-1] + current
    if current.startswith((",", ".", ";", ":", ")", "]", "%")):
        return previous + current
    return previous + " " + current


def render_stream(lines: list[Line]) -> list[str]:
    if not lines:
        return []

    lines = sorted(lines, key=lambda item: (-item.y, item.x_min))
    base_gap = paragraph_gap(lines)
    blocks: list[str] = []
    paragraph = ""
    previous_line: Line | None = None

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            blocks.append(paragraph.strip())
            paragraph = ""

    for line in lines:
        text = line.text.strip()
        if not text:
            continue

        label_match = re.match(r"^(Abstract|Index Terms)\s*[—-]\s*(.+)$", text, flags=re.IGNORECASE)
        if label_match:
            flush_paragraph()
            label = label_match.group(1).title()
            heading_level = "##" if label.lower() == "abstract" else "###"
            blocks.append(f"{heading_level} {label}")
            paragraph = label_match.group(2).strip()
            previous_line = line
            continue

        if is_roman_heading(text):
            flush_paragraph()
            blocks.append(f"## {text}")
            previous_line = None
            continue

        if re.match(r"^[A-Z]\.\s+", text) and len(text) < 80:
            flush_paragraph()
            blocks.append(f"### {text}")
            previous_line = None
            continue

        if is_heading_like(text) and len(text) < 120 and line.font_size >= estimate_body_font(lines):
            flush_paragraph()
            blocks.append(f"### {text.title() if text.isupper() else text}")
            previous_line = None
            continue

        if is_standalone_line(text):
            flush_paragraph()
            blocks.append(text)
            previous_line = None
            continue

        if not paragraph:
            paragraph = text
        else:
            gap = (previous_line.y - line.y) if previous_line else base_gap
            if gap > base_gap * 1.6:
                flush_paragraph()
                paragraph = text
            else:
                paragraph = join_paragraph(paragraph, text)

        previous_line = line

    flush_paragraph()
    return blocks


def extract_title(first_page_lines: list[Line]) -> tuple[str | None, list[Line]]:
    if not first_page_lines:
        return None, first_page_lines

    max_font = max(line.font_size for line in first_page_lines)
    title_lines = [line for line in first_page_lines if line.font_size >= max_font - 1.0]
    if not title_lines:
        return None, first_page_lines

    ordered_title = sorted(title_lines, key=lambda item: -item.y)
    title = " ".join(line.text for line in ordered_title)
    remaining = [line for line in first_page_lines if line not in title_lines]
    return normalize_line_text(title), remaining


def convert_pdf(pdf_path: pathlib.Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages: list[tuple[list[Line], list[Line], list[Line]]] = []
    title: str | None = None

    for page_index, page in enumerate(reader.pages, start=1):
        page_width = float(page.mediabox.width)
        lines = collect_lines(page)
        top_lines, left_lines, right_lines = split_page_regions(lines, page_width)

        if page_index == 1:
            title, top_lines = extract_title(top_lines)

        pages.append((top_lines, left_lines, right_lines))

    output: list[str] = []
    output.append(f"# {title or pdf_path.stem}")
    output.append("")
    output.append(f"Source PDF: {pdf_path.name}")

    for page_index, (top_lines, left_lines, right_lines) in enumerate(pages, start=1):
        output.append("")
        output.append(f"## Page {page_index}")
        output.append("")

        page_blocks = []
        page_blocks.extend(render_stream(top_lines))
        page_blocks.extend(render_stream(left_lines))
        page_blocks.extend(render_stream(right_lines))

        deduped_blocks: list[str] = []
        for block in page_blocks:
            if deduped_blocks and deduped_blocks[-1] == block:
                continue
            deduped_blocks.append(block)

        output.extend(deduped_blocks)

    return "\n\n".join(part for part in output if part is not None)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert a research PDF into agent-friendly Markdown.")
    parser.add_argument("pdf", type=pathlib.Path, help="Path to the input PDF file")
    parser.add_argument("output", type=pathlib.Path, nargs="?", help="Optional output Markdown path")
    args = parser.parse_args()

    pdf_path = args.pdf.resolve()
    output_path = args.output.resolve() if args.output else pdf_path.with_suffix(".md")
    markdown = convert_pdf(pdf_path)
    output_path.write_text(markdown, encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()