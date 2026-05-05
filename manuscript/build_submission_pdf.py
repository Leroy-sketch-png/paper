import shutil
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
GENERATOR = HERE / "generate_latex_manuscript.py"
TEX = HERE / "paper_manuscript.tex"
PDF = HERE / "paper_manuscript.pdf"


def run_command(command: list[str], cwd: Path) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def find_latex_engine() -> str | None:
    for engine in ("pdflatex", "xelatex"):
        if shutil.which(engine):
            return engine
    return None


def main() -> None:
    previous_tex = TEX.read_text(encoding="utf-8") if TEX.exists() else None
    previous_tex_mtime = TEX.stat().st_mtime if TEX.exists() else None
    previous_pdf_mtime = PDF.stat().st_mtime if PDF.exists() else None

    run_command([sys.executable, str(GENERATOR)], cwd=ROOT)

    current_tex = TEX.read_text(encoding="utf-8")
    tex_changed = previous_tex != current_tex

    engine = find_latex_engine()
    if engine is None:
        if (
            PDF.exists()
            and not tex_changed
            and previous_tex_mtime is not None
            and previous_pdf_mtime is not None
            and previous_pdf_mtime >= previous_tex_mtime
        ):
            print(f"Reusing existing {PDF}; no LaTeX engine found and manuscript source is unchanged.")
            return
        raise SystemExit(
            "No LaTeX engine found. Install pdflatex or xelatex, or compile manuscript/paper_manuscript.tex in Overleaf."
        )

    compile_command = [engine, "-interaction=nonstopmode", "-halt-on-error", TEX.name]
    run_command(compile_command, cwd=HERE)
    run_command(compile_command, cwd=HERE)

    print(f"Built {PDF}")


if __name__ == "__main__":
    main()