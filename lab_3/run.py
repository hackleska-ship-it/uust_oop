"""Запуск одной из двух частей третьей лабораторной."""

import argparse
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="ЛР №3 — Круги на форме и MVC")
    parser.add_argument("part", choices=("circles", "mvc"), help="Часть лабораторной")
    args = parser.parse_args()
    try:
        if args.part == "circles":
            from part_1.main import main as run_part
        else:
            from part_2.main import main as run_part
    except ModuleNotFoundError as error:
        if error.name and error.name.startswith(("PySide6", "shiboken6")):
            print("Install dependencies: python -m pip install -r requirements.txt", file=sys.stderr)
            return 1
        raise
    return run_part()


if __name__ == "__main__":
    sys.exit(main())
