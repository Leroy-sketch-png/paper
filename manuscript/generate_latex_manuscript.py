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


def inline_md_to_tex(text: str) -> str:
    text = esc(text)
    text = re.sub(r"\*\*(.+?)\*\*", lambda m: r"\textbf{" + m.group(1) + "}", text)
    text = re.sub(r"\*(.+?)\*", lambda m: r"\textit{" + m.group(1) + "}", text)
    text = re.sub(r"`([^`]+)`", lambda m: r"\texttt{" + m.group(1) + "}", text)
    text = normalize_tex_symbols(text)
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
        if label == "working title (v1)" or re.match(r"^(author|affiliation|location|email) \d+$", label):
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
            r"\textbf{" + esc(author["name"]) + r"}\\"
            + esc(author["affiliation"]) + r"\\"
            + esc(author["location"]) + r"\\"
            + esc(author["email"])
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
    out.append(r"\documentclass[11pt]{article}")
    out.append(r"\usepackage[a4paper,margin=1in]{geometry}")
    out.append(r"\usepackage{setspace}")
    out.append(r"\usepackage{booktabs}")
    out.append(r"\usepackage{longtable}")
    out.append(r"\usepackage{array}")
    out.append(r"\usepackage{hyperref}")
    out.append(r"\usepackage{titlesec}")
    out.append(r"\usepackage{enumitem}")
    out.append(r"\usepackage{times}")
    out.append(r"\setstretch{1.15}")
    out.append(r"\titleformat{\section}{\large\bfseries}{\thesection}{0.5em}{}")
    out.append(r"\titleformat{\subsection}{\normalsize\bfseries}{\thesubsection}{0.5em}{}")
    if subtitle:
        out.append(r"\title{\textbf{" + esc(title) + r"}\\\large " + esc(subtitle) + "}")
    else:
        out.append(r"\title{\textbf{" + esc(title) + r"}}")
    out.append(format_author_block(authors))
    out.append(r"\date{May 2026}")
    out.append(r"\begin{document}")
    out.append(r"\maketitle")

    i = 0
    in_itemize = False
    in_enum = False
    in_quote = False

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
            if in_itemize:
                out.append(r"\end{itemize}")
                in_itemize = False
            if in_enum:
                out.append(r"\end{enumerate}")
                in_enum = False
            if in_quote:
                out.append(r"\end{quote}")
                in_quote = False
            out.append("")
            i += 1
            continue

        # Tables
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
                colspec = "|" + "|".join(["p{" + f"{(0.92/cols):.2f}" + r"\linewidth}"] * cols) + "|"
                out.append(r"\begin{longtable}{" + colspec + "}")
                out.append(r"\hline")
                out.append(" & ".join([r"\textbf{" + h + "}" for h in header]) + r" \\")
                out.append(r"\hline")
                out.append(r"\endfirsthead")
                out.append(r"\hline")
                out.append(" & ".join([r"\textbf{" + h + "}" for h in header]) + r" \\")
                out.append(r"\hline")
                out.append(r"\endhead")
                for row in body:
                    row = row + [""] * (cols - len(row))
                    out.append(" & ".join(row[:cols]) + r" \\")
                    out.append(r"\hline")
                out.append(r"\end{longtable}")
                out.append("")
            continue

        # Headings
        if s.startswith("## "):
            if in_itemize:
                out.append(r"\end{itemize}")
                in_itemize = False
            if in_enum:
                out.append(r"\end{enumerate}")
                in_enum = False
            if in_quote:
                out.append(r"\end{quote}")
                in_quote = False
            out.append(r"\section{" + inline_md_to_tex(s[3:].strip()) + "}")
            i += 1
            continue
        if s.startswith("### "):
            if in_itemize:
                out.append(r"\end{itemize}")
                in_itemize = False
            if in_enum:
                out.append(r"\end{enumerate}")
                in_enum = False
            if in_quote:
                out.append(r"\end{quote}")
                in_quote = False
            out.append(r"\subsection{" + inline_md_to_tex(s[4:].strip()) + "}")
            i += 1
            continue
        if s.startswith("#### "):
            if in_itemize:
                out.append(r"\end{itemize}")
                in_itemize = False
            if in_enum:
                out.append(r"\end{enumerate}")
                in_enum = False
            if in_quote:
                out.append(r"\end{quote}")
                in_quote = False
            out.append(r"\subsubsection{" + inline_md_to_tex(s[5:].strip()) + "}")
            i += 1
            continue

        # Blockquotes
        if s.startswith("> "):
            if not in_quote:
                out.append(r"\begin{quote}")
                in_quote = True
            out.append(inline_md_to_tex(s[2:].strip()))
            i += 1
            continue
        else:
            if in_quote:
                out.append(r"\end{quote}")
                in_quote = False

        # Ordered list
        if re.match(r"^\d+\.\s+", s):
            if not in_enum:
                if in_itemize:
                    out.append(r"\end{itemize}")
                    in_itemize = False
                out.append(r"\begin{enumerate}[leftmargin=*]")
                in_enum = True
            item = re.sub(r"^\d+\.\s+", "", s)
            out.append(r"\item " + inline_md_to_tex(item))
            i += 1
            continue
        else:
            if in_enum:
                out.append(r"\end{enumerate}")
                in_enum = False

        # Unordered list
        if s.startswith("- "):
            if not in_itemize:
                out.append(r"\begin{itemize}[leftmargin=*]")
                in_itemize = True
            out.append(r"\item " + inline_md_to_tex(s[2:].strip()))
            i += 1
            continue
        else:
            if in_itemize:
                out.append(r"\end{itemize}")
                in_itemize = False

        # Blank lines
        if s == "":
            out.append("")
            i += 1
            continue

        # Paragraph
        out.append(inline_md_to_tex(s))
        out.append("")
        i += 1

    if in_itemize:
        out.append(r"\end{itemize}")
    if in_enum:
        out.append(r"\end{enumerate}")
    if in_quote:
        out.append(r"\end{quote}")

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
