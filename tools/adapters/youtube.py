"""YouTube 어댑터.

Phase 1: 골격만. Phase 2 에서 실제 구현.

추천 구현:
- youtube-transcript-api: 공식·자동 자막 추출 (가장 가벼움)
- 대안: yt-dlp + Whisper API: 자막 없을 때 음성 인식 fallback
- YouTube Data API v3: 제목/설명/챕터 메타
- 자동 챕터가 있으면 Section 으로 묶기 (없으면 5~10분 단위 슬라이딩)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from source_bundle import SourceBundle


def extract(source: str) -> SourceBundle:
    """YouTube 영상의 자막을 SourceBundle 로 변환.

    Parameters
    ----------
    source : str
        YouTube URL.

    Returns
    -------
    SourceBundle
        - source_type = "youtube"
        - sections: YouTube 챕터 또는 슬라이딩 시간 윈도우
        - metadata: {"video_id", "channel", "duration_sec", "published"}
    """
    # ──────────────────────────────────────────────
    # Phase 2 에서 구현:
    #
    # from youtube_transcript_api import YouTubeTranscriptApi
    # import re
    #
    # m = re.search(r"(?:v=|youtu\.be/)([\w-]+)", source)
    # if not m: raise ValueError(f"YouTube URL 파싱 실패: {source}")
    # video_id = m.group(1)
    #
    # # 자막 (자동 생성 포함). 한국어 우선, 없으면 영어.
    # transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["ko", "en"])
    # # transcript = [{"text": "...", "start": 0.0, "duration": 3.2}, ...]
    #
    # # 메타 (yt-dlp 의 --skip-download --dump-json 또는 oEmbed)
    # meta = fetch_youtube_meta(video_id)
    #
    # # 챕터가 있으면 그 단위로, 없으면 5분 단위 슬라이딩
    # sections = chunk_by_chapters_or_time(transcript, meta.get("chapters"))
    #
    # plain_text = "\n".join(t["text"] for t in transcript)
    #
    # return SourceBundle(
    #     title=meta["title"],
    #     source_type="youtube",
    #     source_path=source,
    #     plain_text=plain_text,
    #     sections=sections,
    #     keywords=meta.get("tags", []),
    #     metadata={
    #         "video_id": video_id,
    #         "channel": meta.get("channel"),
    #         "duration_sec": meta.get("duration"),
    #         "published": meta.get("upload_date"),
    #     },
    # )
    # ──────────────────────────────────────────────

    raise NotImplementedError(
        f"YouTube 어댑터는 아직 stub. Phase 2 에서 구현. ({source})\n"
        "구현 시 youtube-transcript-api 사용. tools/README.md 참고."
    )
