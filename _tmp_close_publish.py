"""Write publish_log for user review."""
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.checkpoint import write_checkpoint

PROJECT = Path(r"d:\my\OpenMontage\projects\healing-winter-night")
ARTIFACTS = PROJECT / "artifacts"
OUTPUT = PROJECT / "healing-winter-night_final.mp4"

# ── 1. Build publish_log ─────────────────────────────────────────────
publish_log = {
    "version": "1.0",
    "entries": [
        {
            "platform": "local_export",
            "status": "exported",
            "export_path": str(OUTPUT),
            "timestamp": datetime.now().isoformat(),
            "metadata_used": {
                "title": "灯下的守候",
                "description": "治愈系冬夜短片。女孩趴在窗台望雪，暖黄灯光守护着安静的时刻。",
                "hashtags": ["治愈", "冬夜", "雪", "灯光", "短片", "healing", "winternight"],
            },
        }
    ],
    "metadata": {
        "hero_output": {
            "path": str(OUTPUT),
            "title": "灯下的守候",
            "duration_seconds": 12.38,
            "resolution": "480x864",
            "aspect_ratio": "9:16",
            "format": "mp4",
        },
        "derivative_outputs": [],
        "poster_frame_notes": "建议截取 3s 处女孩侧脸特写作为封面（冷暖光交汇瞬间）",
        "distribution_notes": {
            "primary_platform": "TikTok / 抖音",
            "aspect_ratio": "9:16 竖屏",
            "tone": "治愈、安静、温暖",
            "target_audience": "喜欢治愈系内容的年轻用户",
        },
        "project_summary": {
            "concept": "《灯下的守候》— 女孩趴窗望雪的治愈瞬间",
            "emotional_arc": "安静 → 温暖 → 被守护",
            "total_duration_seconds": 12.38,
            "shots_count": 2,
            "generation_pipeline": "ComfyUI (Qwen Image 2512 + MiniMax H3 I2V)",
            "render_runtime": "FFmpeg (fallback from Remotion)",
            "total_cost_usd": 0,
        },
    },
}

# Save artifact
ARTIFACTS.mkdir(parents=True, exist_ok=True)
publish_path = ARTIFACTS / "publish_log.json"
with open(publish_path, "w", encoding="utf-8") as f:
    json.dump(publish_log, f, indent=2, ensure_ascii=False)
print(f"✅ publish_log.json 已保存")

# ── 2. Write checkpoint (awaiting human approval) ────────────────────
decision = {
    "decision_id": "d21",
    "stage": "publish",
    "category": "capability_extension",
    "subject": "Publish package for healing-winter-night",
    "options_considered": [
        {
            "option_id": "export_only",
            "label": "Local export only",
            "score": 1.0,
            "reason": "Simplest approach; user can manually upload to platforms",
        },
        {
            "option_id": "tiktok_upload",
            "label": "Auto-upload to TikTok",
            "score": 0.0,
            "reason": "No API credentials configured; manual upload preferred",
            "rejected_because": "No API access",
        },
    ],
    "selected": "export_only",
    "reason": "本地导出成片，用户可自行上传至目标平台。",
    "user_visible": True,
    "user_approved": False,
    "confidence": 1.0,
}

write_checkpoint(
    pipeline_dir=PROJECT.parent,
    project_id=PROJECT.name,
    stage="publish",
    status="awaiting_human",  # Requires human approval
    human_approved=False,
    artifacts={
        "publish_log": publish_log,
        "decision_log": {
            "version": "1.0",
            "project_id": PROJECT.name,
            "decisions": [decision],
        },
    },
)
print(f"✅ publish 阶段等待人工审批 (awaiting_human)")
