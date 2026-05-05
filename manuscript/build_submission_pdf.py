import shutil
import subprocess
import sys
import os
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
GENERATOR = HERE / "generate_latex_manuscript.py"
TEX = HERE / "paper_manuscript.tex"
PDF = HERE / "paper_manuscript.pdf"


def clean_latex_intermediates() -> None:
    for suffix in (".aux", ".out", ".toc"):
        candidate = TEX.with_suffix(suffix)
        if candidate.exists():
            candidate.unlink()


def run_command(command: list[str], cwd: Path) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def candidate_engine_paths(engine: str) -> list[str]:
    candidates = []
    on_path = shutil.which(engine)
    if on_path:
        candidates.append(on_path)

    local_app_data = os.environ.get("LOCALAPPDATA")
    program_files = os.environ.get("ProgramFiles")
    program_files_x86 = os.environ.get("ProgramFiles(x86)")

    if local_app_data:
        candidates.append(str(Path(local_app_data) / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64" / f"{engine}.exe"))
    if program_files:
        candidates.append(str(Path(program_files) / "MiKTeX" / "miktex" / "bin" / "x64" / f"{engine}.exe"))
        candidates.append(str(Path(program_files) / "MiKTeX 2.9" / "miktex" / "bin" / "x64" / f"{engine}.exe"))
    if program_files_x86:
        candidates.append(str(Path(program_files_x86) / "MiKTeX 2.9" / "miktex" / "bin" / "x64" / f"{engine}.exe"))

    for year in (2026, 2025, 2024, 2023):
        candidates.append(str(Path("C:/texlive") / str(year) / "bin" / "windows" / f"{engine}.exe"))

    return candidates


def find_latex_engine() -> str | None:
    for engine in ("pdflatex", "xelatex"):
        for candidate in candidate_engine_paths(engine):
            if Path(candidate).exists():
                return candidate
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

    if tex_changed:
        clean_latex_intermediates()

    compile_command = [engine, "-interaction=nonstopmode", "-halt-on-error", TEX.name]
    run_command(compile_command, cwd=HERE)
    run_command(compile_command, cwd=HERE)

    print(f"Built {PDF}")


if __name__ == "__main__":
    main()