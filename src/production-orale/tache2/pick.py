#!/usr/bin/env python3
"""Tire au hasard une consigne de la Tâche 2 depuis data/corpus.txt.

Usage :
    python3 src/production-orale/tache2/pick.py        # une consigne au hasard
    python3 src/production-orale/tache2/pick.py -n 3   # 3 consignes au hasard
"""
from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

CORPUS = Path(__file__).resolve().parent / "data" / "corpus.txt"


def load_subjects(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    return [s for line in lines if (s := line.strip()) and not s.startswith("#")]


def main() -> int:
    parser = argparse.ArgumentParser(description="Tire une consigne de Tâche 2 au hasard.")
    parser.add_argument("-n", type=int, default=1, help="nombre de consignes (défaut : 1)")
    args = parser.parse_args()

    subjects = load_subjects(CORPUS)
    if not subjects:
        print(f"Aucune consigne trouvée dans {CORPUS}", file=sys.stderr)
        return 1

    for subject in random.sample(subjects, min(args.n, len(subjects))):
        print(subject)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
