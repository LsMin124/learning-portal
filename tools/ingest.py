#!/usr/bin/env python3
"""학습 자료 자동 생성 CLI 진입점.

PDF / URL / YouTube 입력 -> SourceBundle -> STUDY/QUIZ/CHEATSHEETS 마크다운.

사용:
    python tools/ingest.py PATH --course ID --stem STEM --label "..." [--dry-run] [--only quiz]

자세한 사용법은 tools/README.md 참조.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# 같은 디렉토리의 모듈 import
sys.path.insert(0, str(Path(__file__).parent))

from source_bundle import SourceBundle
from adapters import pdf as pdf_adapter
from adapters import url as url_adapter
from adapters import youtube as youtube_adapter
from generators import study as study_gen
from generators import quiz as quiz_gen
from generators import cheatsheet as cheat_gen


# ───────── 입력 종류 dispatch ─────────

def detect_source_type(arg: str) -> str:
    """argv 의 첫 인자를 보고 PDF/URL/YouTube 중 판단."""
    if re.match(r"^https?://(www\.)?(youtube\.com|youtu\.be)/", arg):
        return "youtube"
    if re.match(r"^https?://", arg):
        return "url"
    # 그 외는 로컬 파일로 간주
    p = Path(arg)
    if not p.exists():
        sys.exit(f"파일 없음: {arg}")
    if p.suffix.lower() != ".pdf":
        sys.exit(f"PDF 만 지원 (현재): {p.suffix}")
    return "pdf"


ADAPTERS = {
    "pdf":     pdf_adapter.extract,
    "url":     url_adapter.extract,
    "youtube": youtube_adapter.extract,
}


# ───────── 출력 경로 + 정리 ─────────

def output_paths(course: str, stem: str) -> dict[str, Path]:
    root = Path("courses") / course
    return {
        "study": root / "STUDY"       / f"{stem}.md",
        "quiz":  root / "QUIZ"        / f"{stem}.md",
        "cheat": root / "CHEATSHEETS" / f"{stem}.md",
    }


def ensure_course_dirs(course: str) -> None:
    """courses/{course}/{STUDY,QUIZ,CHEATSHEETS} 가 없으면 생성."""
    root = Path("courses") / course
    for sub in ("STUDY", "QUIZ", "CHEATSHEETS"):
        (root / sub).mkdir(parents=True, exist_ok=True)


def course_json_path(course: str) -> Path:
    return Path("courses") / course / "course.json"


def suggest_course_json_update(course: str, stem: str, label: str, pages: int, section_title: str) -> None:
    """course.json 의 sections 에 항목 추가 제안 (실제 수정은 사용자 검토 후 직접).

    완전 자동 갱신은 위험 (사용자가 의도한 위치·라벨이 다를 수 있음). 그래서 제안만 출력.
    """
    cj = course_json_path(course)
    proposed = {"stem": stem, "pages": pages, "label": label}
    section_to = section_title or "(원하는 섹션을 골라 추가)"

    print()
    print("── course.json 갱신 제안 ────────────────────────────────")
    print(f"파일: {cj}")
    print(f"섹션: {section_to}")
    print(f"추가할 항목: {json.dumps(proposed, ensure_ascii=False)}")
    if not cj.exists():
        print(f"경고: {cj} 가 없음. course.json 골격 먼저 작성 필요. tools/README.md 참고.")
    print("─────────────────────────────────────────────────────────")


# ───────── main ─────────

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ingest",
        description="입력 자료 -> STUDY/QUIZ/CHEATSHEETS 자동 생성",
    )
    parser.add_argument("source", help="PDF 경로 | URL | YouTube URL")
    parser.add_argument("--course", required=True, help="코스 ID (courses/{id}/)")
    parser.add_argument("--stem", required=True, help="파일 stem (확장자 제외)")
    parser.add_argument("--label", default="", help="UI 에 표시될 라벨 (예: '01강 OS 개요')")
    parser.add_argument("--section", default="", help="course.json 의 어느 섹션에 넣을지")
    parser.add_argument("--dry-run", action="store_true", help="LLM 호출 없이 SourceBundle 만 확인")
    parser.add_argument("--only", choices=["study", "quiz", "cheat"], help="특정 산출물만 (재생성)")
    parser.add_argument("--overwrite", action="store_true", help="기존 파일 덮어쓰기")
    args = parser.parse_args()

    # 1. 입력 종류 판별 + 어댑터 호출
    stype = detect_source_type(args.source)
    print(f"[1/5] {stype.upper()} 입력 감지: {args.source}")
    extract = ADAPTERS[stype]
    bundle: SourceBundle = extract(args.source)

    if args.label:
        bundle.title = args.label

    # 2. SourceBundle 확인
    in_tok = bundle.estimated_input_tokens()
    print(f"[2/5] SourceBundle 구조화 완료 — 본문 ~{in_tok:,} tokens, {len(bundle.sections)} sections, {len(bundle.keywords)} keywords")

    if args.dry_run:
        print()
        print("── DRY RUN: SourceBundle ────────────────────────────────")
        print(json.dumps(bundle.to_dict(), ensure_ascii=False, indent=2)[:2000])
        print("...")
        print("─────────────────────────────────────────────────────────")
        return

    # 3. 출력 경로 준비
    ensure_course_dirs(args.course)
    paths = output_paths(args.course, args.stem)

    # 기존 파일 보호
    if not args.overwrite:
        existing = [k for k, p in paths.items() if p.exists() and (args.only is None or k == args.only)]
        if existing:
            sys.exit(f"이미 존재함: {existing}. --overwrite 또는 --only 사용.")

    # 4. 생성기 호출
    targets = ["study", "quiz", "cheat"] if args.only is None else [args.only]
    GENERATORS = {"study": study_gen, "quiz": quiz_gen, "cheat": cheat_gen}
    LABELS     = {"study": "STUDY", "quiz": "QUIZ",  "cheat": "CHEATSHEETS"}

    for i, t in enumerate(targets, start=3):
        gen = GENERATORS[t]
        print(f"[{i}/5] {LABELS[t]} 생성 중...")
        markdown = gen.generate(bundle)
        paths[t].write_text(markdown, encoding="utf-8")
        size_kb = len(markdown) / 1024
        print(f"      → {paths[t]} ({size_kb:.1f} KB)")

    # 5. course.json 갱신 제안
    pages = bundle.metadata.get("pages", 0)
    suggest_course_json_update(args.course, args.stem, args.label or bundle.title, pages, args.section)


if __name__ == "__main__":
    main()
