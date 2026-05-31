"""Corporate Finance 12e figure 캡션 위치 탐색기.

PDF 전체를 스캔해 'Figure N.M' 캡션이 실제로 시작되는 0-based 페이지 인덱스를
찾아준다. 결과를 보고 extract_figures() 의 figs dict 를 구성한다.

사용법:
    python tools/find_figures.py 17            # ch17 figure 캡션 스캔
    python tools/find_figures.py 17 --offset 2 # 인쇄 페이지 보정값 적용

판정:
    - 라인이 'Figure N.M' 로 *시작* → 진짜 캡션 (caption page)
    - 본문 중간 'see Figure N.M' → 참조 (ref) — 캡션 페이지가 따로 없을 때만 사용
"""
from __future__ import annotations

import re
import sys

import fitz  # PyMuPDF

PDF = "tools/inbox/financial-management/Corporate Finance, 12th Twelfth edition.pdf"


def _page_has_graphic(page) -> bool:
    """페이지에 figure 그래픽(임베디드 이미지 또는 큰 벡터 panel)이 있는지."""
    page_area = page.rect.width * page.rect.height
    for img in page.get_image_info():
        b = fitz.Rect(img["bbox"])
        if b.width >= 80 and b.height >= 60:
            return True
    biggest = 0.0
    for d in page.get_drawings():
        r = d["rect"]
        biggest = max(biggest, r.width * r.height)
    return biggest >= page_area * 0.04


def scan(chapter: int, offset: int = 0) -> None:
    doc = fitz.open(PDF)
    any_re = re.compile(rf"Figure\s+{chapter}\.(\d+)\b")
    # prose: 'Figure N.M' 뒤에 소문자 단어 → 본문 문장 (illustrates/shows/graphs…)
    prose_re = re.compile(rf"^Figure\s+{chapter}\.\d+\s+[a-z]")

    # fnum -> [{pidx, cap, is_caption(=라인시작·비prose), graphic}]
    cand: dict[str, list[dict]] = {}
    for pidx in range(len(doc)):
        page = doc[pidx]
        text = page.get_text()
        hits: set[str] = set()
        caption_of: dict[str, str] = {}
        for raw in text.splitlines():
            line = raw.strip()
            for m in any_re.finditer(line):
                fnum = f"{chapter}.{m.group(1)}"
                hits.add(fnum)
                if line.startswith(f"Figure {fnum}") and not prose_re.match(line):
                    caption_of.setdefault(fnum, line)
        if not hits:
            continue
        graphic = _page_has_graphic(page)
        for fnum in hits:
            cand.setdefault(fnum, []).append({
                "pidx": pidx,
                "cap": caption_of.get(fnum, ""),
                "is_caption": fnum in caption_of,
                "graphic": graphic,
            })

    keys = sorted(cand, key=lambda s: int(s.split(".")[1]))
    if not keys:
        print(f"(ch{chapter}: 'Figure {chapter}.x' 를 찾지 못함)")
        doc.close()
        return

    def pick(lst: list[dict]) -> dict:
        for c in lst:                       # 1순위: 캡션 라인 + 그래픽
            if c["is_caption"] and c["graphic"]:
                return c
        for c in lst:                       # 2순위: 그래픽 있는 페이지
            if c["graphic"]:
                return c
        for c in lst:                       # 3순위: 캡션 라인
            if c["is_caption"]:
                return c
        return lst[0]                        # 4순위: 첫 언급

    print(f"# ch{chapter}  figs dict (0-based PDF page index)")
    print("figs = {")
    for fnum in keys:
        lst = cand[fnum]
        best = pick(lst)
        pidx = best["pidx"]
        printed = pidx + 1 + offset
        quality = "caption+graphic" if (best["is_caption"] and best["graphic"]) else \
                  "graphic" if best["graphic"] else \
                  "caption-only⚠" if best["is_caption"] else "ref-only⚠"
        cap_short = (best["cap"][:60] + "…") if len(best["cap"]) > 60 else best["cap"]
        others = ",".join(str(c["pidx"]) for c in lst if c["pidx"] != pidx)
        print(f'    "{fnum}": {pidx},  # 교재 p.{printed} [{quality}] {cap_short}')
        if others:
            print(f"        # 다른 후보 page idx: {others}")
    print("}")
    doc.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    ch = int(sys.argv[1])
    off = 0
    if "--offset" in sys.argv:
        off = int(sys.argv[sys.argv.index("--offset") + 1])
    scan(ch, off)
