import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "paper_skeleton.md"
OUT = HERE / "paper_manuscript.tex"


def esc(text: str) -> str:
    # Unescape markdown escapes first
    text = text.replace("\\_", "_")
    repl = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(repl.get(ch, ch) for ch in text)


def normalize_tex_symbols(text: str) -> str:
    replacements = {
        "±": r"$\pm$",
        "×": r"$\times$",
        "≤": r"$\leq$",
        "≥": r"$\geq$",
        "ρ": r"$\rho$",
        "Δ": r"$\Delta$",
        "−": "-",
        "–": "--",
        "—": "---",
    }
    for source, replacement in replacements.items():
        text = text.replace(source, replacement)
    return text


def strip_heading_number(text: str) -> str:
    return re.sub(r"^\d+(?:\.\d+)*\.?\s+", "", text).strip()


def strip_table_label(text: str) -> str:
    return re.sub(r"^Table\s+[A-Za-z0-9]+\s*(?:—|--+|-)\s*", "", text).strip()


def bibliography_key(text: str, index: int) -> str:
    key = re.sub(r"[^A-Za-z0-9]+", "", text).lower()
    return key or f"ref{index}"


def is_special_block_start(line: str) -> bool:
    stripped = line.strip()
    return (
        stripped == ""
        or stripped == "---"
        or stripped.startswith("#")
        or stripped.startswith("> ")
        or stripped.startswith("- ")
        or re.match(r"^\d+\.\s+", stripped) is not None
        or is_table_line(line)
    )


def inline_md_to_tex(text: str) -> str:
    math_segments = []

    def stash_math(match: re.Match[str]) -> str:
        placeholder = f"@@MATH{len(math_segments)}@@"
        math_segments.append(match.group(0))
        return placeholder

    text = re.sub(r"\$[^$]+\$", stash_math, text)
    text = esc(text)
    text = re.sub(r"\*\*(.+?)\*\*", lambda m: r"\textbf{" + m.group(1) + "}", text)
    text = re.sub(r"\*(.+?)\*", lambda m: r"\textit{" + m.group(1) + "}", text)
    text = re.sub(r"`([^`]+)`", lambda m: r"\texttt{" + m.group(1) + "}", text)
    text = normalize_tex_symbols(text)
    for index, segment in enumerate(math_segments):
        text = text.replace(f"@@MATH{index}@@", segment)
    return text


def is_table_line(line: str) -> bool:
    return line.strip().startswith("|") and line.strip().endswith("|")


def split_table_row(line: str):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return [inline_md_to_tex(c) for c in cells]


def strip_wrapping_emphasis(text: str) -> str:
    text = text.strip()
    if len(text) >= 2 and text.startswith("*") and text.endswith("*"):
        return text[1:-1].strip()
    return text


def parse_bold_metadata(line: str):
    match = re.match(r"^\*\*(.+?):\*\*\s*(.*)$", line.strip())
    if not match:
        return None, None
    return match.group(1).strip().lower(), strip_wrapping_emphasis(match.group(2).strip())


def parse_front_matter(lines: list[str]):
    metadata = {}
    skipped_lines = set()

    for idx, line in enumerate(lines):
        label, value = parse_bold_metadata(line)
        if label is None:
            continue
        metadata[label] = value
        if label in {"working title (v1)", "target venue", "directions active"} or re.match(r"^(author|affiliation|location|email) \d+$", label):
            skipped_lines.add(idx)

    ordinals = ("1st", "2nd", "3rd")
    authors = []
    for index, ordinal in enumerate(ordinals, start=1):
        authors.append(
            {
                "name": metadata.get(f"author {index}", f"{ordinal} Author Name"),
                "affiliation": metadata.get(f"affiliation {index}", f"Author {index} Affiliation"),
                "location": metadata.get(f"location {index}", "City, Country"),
                "email": metadata.get(f"email {index}", f"author{index}@example.com"),
            }
        )

    return metadata.get("working title (v1)"), authors, skipped_lines


def format_author_block(authors: list[dict[str, str]]) -> str:
    author_entries = []
    for author in authors:
        author_entries.append(
            r"\IEEEauthorblockN{" + esc(author["name"]) + r"}"
            + r"\IEEEauthorblockA{" + esc(author["affiliation"]) + r"\\"
            + esc(author["location"]) + r"\\"
            + esc(author["email"]) + r"}"
        )
    return r"\author{" + r"\and ".join(author_entries) + r"}"


def convert(md: str) -> str:
    lines = md.splitlines()

    title = "Label Realism, Data Governance, and Representation Shift"
    subtitle = "Revisiting ML-Based Test Case Prioritization for Continuous Integration"
    abstract = ""
    front_matter_title, authors, metadata_lines = parse_front_matter(lines)

    # Capture title from first heading
    if front_matter_title:
        title = front_matter_title
        subtitle = ""
    else:
        for ln in lines:
            if ln.startswith("# "):
                title = ln[2:].strip()
                break

    out = []
    out.append(r"\documentclass[10pt,conference]{IEEEtran}")
    out.append(r"\usepackage{booktabs}")
    out.append(r"\usepackage{array}")
    out.append(r"\usepackage{cite}")
    out.append(r"\usepackage{hyperref}")
    out.append(r"\usepackage{enumitem}")
    out.append(r"\usepackage{graphicx}")
    out.append(r"\usepackage{balance}")
    out.append(r"\renewcommand{\arraystretch}{1.08}")
    if subtitle:
        out.append(r"\title{" + esc(title) + r"\\" + esc(subtitle) + "}")
    elif ":" in title:
        lead, trail = [part.strip() for part in title.split(":", 1)]
        out.append(r"\title{" + esc(lead) + r":\\" + esc(trail) + "}")
    else:
        out.append(r"\title{" + esc(title) + r"}")
    out.append(format_author_block(authors))
    out.append(r"\begin{document}")
    out.append(r"\maketitle")

    i = 0
    in_itemize = False
    in_enum = False
    in_quote = False
    in_bibliography = False
    in_references_section = False
    last_list_item_index = None
    pending_table_caption = None
    bibliography_index = 1

    # Find and capture abstract block from markdown
    abs_start = None
    for idx, ln in enumerate(lines):
        if ln.strip().lower().startswith("## abstract"):
            abs_start = idx + 1
            break
    if abs_start is not None:
        abs_lines = []
        j = abs_start
        while j < len(lines):
            if lines[j].startswith("## ") and j > abs_start:
                break
            if lines[j].strip() and not lines[j].strip().startswith("---"):
                abs_lines.append(lines[j])
            j += 1
        abstract = " ".join([x.strip() for x in abs_lines if x.strip()])

    if abstract:
        out.append(r"\begin{abstract}")
        out.append(inline_md_to_tex(abstract))
        out.append(r"\end{abstract}")

    # Main body
    while i < len(lines):
        line = lines[i]
        s = line.strip()

        # Skip top title and abstract heading; already handled
        if i == 0 and s.startswith("# "):
            i += 1
            continue
        if i in metadata_lines:
            i += 1
            continue
        if s.lower().startswith("## abstract"):
            i += 1
            while i < len(lines) and not lines[i].startswith("## "):
                i += 1
            continue

        if s == "---":
            if in_bibliography:
                out.append(r"\end{thebibliography}")
                in_bibliography = False
                in_references_section = False
            if in_itemize:
                out.append(r"\end{itemize}")
                in_itemize = False
            if in_enum:
                out.append(r"\end{enumerate}")
                in_enum = False
            last_list_item_index = None
            if in_quote:
                out.append(r"\end{quote}")
                in_quote = False
            out.append("")
            i += 1
            continue

        # Tables
        bold_only = re.match(r"^\*\*(.+?)\*\*$", s)
        if bold_only:
            next_idx = i + 1
            while next_idx < len(lines) and lines[next_idx].strip() == "":
                next_idx += 1
            if next_idx < len(lines) and is_table_line(lines[next_idx]) and bold_only.group(1).strip().lower().startswith("table"):
                pending_table_caption = inline_md_to_tex(strip_table_label(bold_only.group(1).strip()))
                i += 1
                continue

        if is_table_line(line):
            tbl_lines = []
            while i < len(lines) and is_table_line(lines[i]):
                tbl_lines.append(lines[i])
                i += 1
            if len(tbl_lines) >= 2:
                header = split_table_row(tbl_lines[0])
                body = []
                for tr in tbl_lines[2:]:
                    body.append(split_table_row(tr))
                cols = len(header)
                use_star_table = cols >= 4
                env_name = "table*" if use_star_table else "table"
                width_unit = r"\textwidth" if use_star_table else r"\columnwidth"
                if cols >= 5:
                    usable_width = 0.94
                    out.append(r"\begin{" + env_name + r"}[t]")
                    out.append(r"\centering")
                    if pending_table_caption is not None:
                        out.append(r"\caption{" + pending_table_caption + r"}")
                        pending_table_caption = None
                    out.append(r"\scriptsize")
                    out.append(r"\setlength{\tabcolsep}{3pt}")
                elif cols >= 3:
                    usable_width = 0.96
                    out.append(r"\begin{" + env_name + r"}[t]")
                    out.append(r"\centering")
                    if pending_table_caption is not None:
                        out.append(r"\caption{" + pending_table_caption + r"}")
                        pending_table_caption = None
                    out.append(r"\footnotesize")
                    out.append(r"\setlength{\tabcolsep}{4pt}")
                else:
                    usable_width = 0.98
                    out.append(r"\begin{" + env_name + r"}[t]")
                    out.append(r"\centering")
                    if pending_table_caption is not None:
                        out.append(r"\caption{" + pending_table_caption + r"}")
                        pending_table_caption = None
                    out.append(r"\footnotesize")
                    out.append(r"\setlength{\tabcolsep}{5pt}")
                colspec = "|" + "|".join(["p{" + f"{(usable_width/cols):.2f}" + width_unit + "}"] * cols) + "|"
                out.append(r"\begin{tabular}{" + colspec + "}")
                out.append(r"\hline")
                out.append(" & ".join([r"\textbf{" + h + "}" for h in header]) + r" \\")
                out.append(r"\hline")
                for row in body:
                    row = row + [""] * (cols - len(row))
                    out.append(" & ".join(row[:cols]) + r" \\")
                    out.append(r"\hline")
                out.append(r"\end{tabular}")
                out.append(r"\normalsize")
                out.append(r"\setlength{\tabcolsep}{6pt}")
                out.append(r"\end{" + env_name + r"}")
                out.append("")
            continue

        # Headings
        if s.startswith("## "):
            heading_text = strip_heading_number(s[3:].strip())
            if in_bibliography:
                out.append(r"\end{thebibliography}")
                in_bibliography = False
                in_references_section = False
            if in_itemize:
                out.append(r"\end{itemize}")
                in_itemize = False
            if in_enum:
                out.append(r"\end{enumerate}")
                in_enum = False
            last_list_item_index = None
            if in_quote:
                out.append(r"\end{quote}")
                in_quote = False
            if heading_text.lower().startswith("references"):
                out.append(r"\balance")
                in_references_section = True
            else:
                in_references_section = False
                out.append(r"\section{" + inline_md_to_tex(heading_text) + "}")
            i += 1
            continue
        if s.startswith("### "):
            if in_bibliography:
                out.append(r"\end{thebibliography}")
                in_bibliography = False
                in_references_section = False
            if in_itemize:
                out.append(r"\end{itemize}")
                in_itemize = False
            if in_enum:
                out.append(r"\end{enumerate}")
                in_enum = False
            last_list_item_index = None
            if in_quote:
                out.append(r"\end{quote}")
                in_quote = False
            out.append(r"\subsection{" + inline_md_to_tex(strip_heading_number(s[4:].strip())) + "}")
            i += 1
            continue
        if s.startswith("#### "):
            if in_itemize:
                out.append(r"\end{itemize}")
                in_itemize = False
            if in_enum:
                out.append(r"\end{enumerate}")
                in_enum = False
            last_list_item_index = None
            if in_quote:
                out.append(r"\end{quote}")
                in_quote = False
            out.append(r"\subsubsection{" + inline_md_to_tex(strip_heading_number(s[5:].strip())) + "}")
            i += 1
            continue

        # Blockquotes
        if s.startswith("> "):
            if not in_quote:
                out.append(r"\begin{quote}")
                in_quote = True
            out.append(inline_md_to_tex(s[2:].strip()))
            last_list_item_index = None
            i += 1
            continue
        else:
            if in_quote:
                out.append(r"\end{quote}")
                in_quote = False

        # Ordered list
        if re.match(r"^\d+\.\s+", s):
            if in_references_section:
                if not in_bibliography:
                    out.append(r"\begin{thebibliography}{99}")
                    in_bibliography = True
                item = re.sub(r"^\d+\.\s+", "", s)
                out.append(r"\bibitem{" + bibliography_key(item, bibliography_index) + r"} " + inline_md_to_tex(item))
                bibliography_index += 1
                i += 1
                continue
            if not in_enum:
                if in_itemize:
                    out.append(r"\end{itemize}")
                    in_itemize = False
                out.append(r"\begin{enumerate}[leftmargin=*]")
                in_enum = True
            item = re.sub(r"^\d+\.\s+", "", s)
            out.append(r"\item " + inline_md_to_tex(item))
            last_list_item_index = len(out) - 1
            i += 1
            continue
        else:
            if in_enum:
                if (
                    s
                    and not s.startswith("- ")
                    and not s.startswith("> ")
                    and not s.startswith("#")
                    and not is_table_line(line)
                    and s != "---"
                    and last_list_item_index is not None
                ):
                    out[last_list_item_index] += " " + inline_md_to_tex(s)
                    i += 1
                    continue
                out.append(r"\end{enumerate}")
                in_enum = False
                last_list_item_index = None

        # Unordered list
        if s.startswith("- "):
            if in_references_section:
                if not in_bibliography:
                    out.append(r"\begin{thebibliography}{99}")
                    in_bibliography = True
                item = s[2:].strip()
                label_match = re.match(r"^\[([^\]]+)\]\s*(.*)$", item)
                if label_match:
                    key_source = label_match.group(1).strip()
                    entry_text = label_match.group(2).strip() or item
                else:
                    key_source = item
                    entry_text = item
                out.append(r"\bibitem{" + bibliography_key(key_source, bibliography_index) + r"} " + inline_md_to_tex(entry_text))
                bibliography_index += 1
                i += 1
                continue
            if not in_itemize:
                out.append(r"\begin{itemize}[leftmargin=*]")
                in_itemize = True
            out.append(r"\item " + inline_md_to_tex(s[2:].strip()))
            last_list_item_index = len(out) - 1
            i += 1
            continue
        else:
            if in_itemize:
                if (
                    s
                    and not re.match(r"^\d+\.\s+", s)
                    and not s.startswith("> ")
                    and not s.startswith("#")
                    and not is_table_line(line)
                    and s != "---"
                    and last_list_item_index is not None
                ):
                    out[last_list_item_index] += " " + inline_md_to_tex(s)
                    i += 1
                    continue
                out.append(r"\end{itemize}")
                in_itemize = False
                last_list_item_index = None

        # Blank lines
        if s == "":
            out.append("")
            last_list_item_index = None
            i += 1
            continue

        # Paragraphs may be hard-wrapped in markdown source; reflow them.
        paragraph_lines = [s]
        i += 1
        while i < len(lines) and not is_special_block_start(lines[i]):
            paragraph_lines.append(lines[i].strip())
            i += 1
        out.append(inline_md_to_tex(" ".join(paragraph_lines)))
        out.append("")
        last_list_item_index = None

    if in_itemize:
        out.append(r"\end{itemize}")
    if in_enum:
        out.append(r"\end{enumerate}")
    if in_quote:
        out.append(r"\end{quote}")
    if in_bibliography:
        out.append(r"\end{thebibliography}")

    out.append(r"\end{document}")
    tex = "\n".join(out) + "\n"
    # Defensive cleanup for any accidentally doubled command backslashes.
    tex = tex.replace(r"\\textbf{", r"\textbf{")
    tex = tex.replace(r"\\textit{", r"\textit{")
    tex = tex.replace(r"\\texttt{", r"\texttt{")
    return tex


def main():
    md = SRC.read_text(encoding="utf-8")
    tex = convert(md)
    OUT.write_text(tex, encoding="utf-8")
    print(f"Generated {OUT}")


if __name__ == "__main__":
    main()
