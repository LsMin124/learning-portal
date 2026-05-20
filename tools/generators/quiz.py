"""QUIZ (퀴즈) 생성기.

prompts/quiz.md 의 규약 (14문항, 4 카테고리, details 토글) 에 따라
SourceBundle -> 퀴즈 마크다운.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from source_bundle import SourceBundle
from generators._llm import call_claude, load_prompt, render_user_input


def generate(bundle: SourceBundle) -> str:
    system_prompt = load_prompt("quiz")
    user_input = render_user_input(bundle)
    # QUIZ 는 보통 6~10KB. max_tokens 보수적.
    return call_claude(system_prompt, user_input, max_tokens=12000)
