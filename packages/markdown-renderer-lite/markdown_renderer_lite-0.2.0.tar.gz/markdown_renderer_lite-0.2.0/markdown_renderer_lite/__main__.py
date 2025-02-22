import sys
from markdown_renderer_lite.converter import convert_markdown


def main():
    """Entry point for running markdown_renderer_lite as a module."""
    if len(sys.argv) < 2:
        print("Usage: python -m markdown_renderer_lite <input.md>")
        sys.exit(1)

    try:
        html_output = convert_markdown()

    except FileNotFoundError:
        print(f"Error occurred: {sys.exc_info()[1]}")
        sys.exit(1)


if __name__ == "__main__":
    main()
