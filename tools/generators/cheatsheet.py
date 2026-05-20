"""CHEATSHEETS (치트시트) 생성기.

prompts/cheatsheet.md 의 규약 (TL;DR + Quick Reference + Mind Map 3섹션) 에 따라
SourceBundle -> 치트시트 마크다운.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from source_bundle import SourceBundle
from generators._llm import call_claude, load_prompt, render_user_input


def generate(bundle: SourceBundle) -> str:
    system_prompt = load_prompt("cheatsheet")
    user_input = render_user_input(bundle)
    # CHEATSHEETS 는 10~25KB. STUDY 와 비슷한 규모.
    return call_claude(system_prompt, user_input, max_tokens=16000)
