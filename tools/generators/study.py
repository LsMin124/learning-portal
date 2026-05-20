"""STUDY (학습 노트) 생성기.

prompts/study.md 의 규약에 따라 SourceBundle -> 학습 노트 마크다운.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from source_bundle import SourceBundle
from generators._llm import call_claude, load_prompt, render_user_input


def generate(bundle: SourceBundle) -> str:
    system_prompt = load_prompt("study")
    user_input = render_user_input(bundle)
    # STUDY 는 가장 긴 산출물 (8~20KB). max_tokens 넉넉히.
    return call_claude(system_prompt, user_input, max_tokens=16000)
