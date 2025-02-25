"""Entrypoint script."""

import argparse
import sys
from pathlib import Path
from typing import Optional, Literal

from langgraph_gen._version import __version__
from langgraph_gen.generate import generate_from_spec


def _rewrite_path_as_import(path: Path) -> str:
    """Rewrite a path as an import statement."""
    return ".".join(path.with_suffix("").parts)


def _generate(
    input_file: Path,
    *,
    language: Literal["python", "typescript"],
    output_file: Optional[Path] = None,
    implementation: Optional[Path] = None,
) -> None:
    """Generate agent code from a YAML specification file.

    Args:
        input_file (Path): Input YAML specification file
        language (Literal["python", "typescript"]): Language to generate code for
        output_file (Optional[Path]): Output Python file path
        implementation (Optional[Path]): Output Python file path for a placeholder implementation
    """
    if language not in ["python", "typescript"]:
        raise NotImplementedError(
            f"Unsupported language: {language} Use one of 'python' or 'typescript'"
        )
    suffix = ".py" if language == "python" else ".ts"
    output_path = output_file or input_file.with_suffix(suffix)

    # Add a _impl.py suffix to the input filename if implementation is not provided
    if implementation is None:
        implementation = input_file.with_name(f"{input_file.stem}_impl{suffix}")

    # Get the implementation relative to the output path
    stub_module = _rewrite_path_as_import(
        output_path.relative_to(implementation.parent)
    )

    spec_as_yaml = input_file.read_text()
    stub, impl = generate_from_spec(
        spec_as_yaml,
        "yaml",
        templates=["stub", "implementation"],
        language=language,
        stub_module=stub_module,
    )
    output_path.write_text(stub)

    implementation.write_text(impl)


def main() -> None:
    """Langgraph-gen CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate LangGraph agent base classes from YAML specs.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("input", type=Path, help="Input YAML specification file")
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        default="python",
        help="Language to generate code for (python, typescript)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output Python file path for agent stub",
        default=None,
    )

    parser.add_argument(
        "--implementation",
        type=Path,
        help="Output Python file path for a placeholder implementation.",
        default=None,
    )

    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()

    if not args.input.exists():
        """Check if input file exists."""
        sys.exit(f"Input file {args.input} does not exist")

    _generate(input_file=args.input, output_file=args.output, language=args.language)


if __name__ == "__main__":
    main()
