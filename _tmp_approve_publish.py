"""Close publish gate with human approval."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.checkpoint import write_checkpoint

PROJECT = Path(r"d:\my\OpenMontage\projects\healing-winter-night")

# Load existing publish_log
ARTIFACTS = PROJECT / "artifacts"
with open(ARTIFACTS / "publish_log.json", encoding="utf-8") as f:
    publish_log = json.load(f)

# Close gate
decision = {
    "decision_id": "d22",
    "stage": "publish",
    "category": "capability_extension",
    "subject": "Publish approval for healing-winter-night",
    "options_considered": [
        {
            "option_id": "approve_publish",
            "label": "Approve publish package",
            "score": 1.0,
            "reason": "User approved; project complete",
        },
    ],
    "selected": "approve_publish",
    "reason": "用户批准发布包。项目完成。",
    "user_visible": True,
    "user_approved": True,
    "confidence": 1.0,
}

write_checkpoint(
    pipeline_dir=PROJECT.parent,
    project_id=PROJECT.name,
    stage="publish",
    status="completed",
    human_approved=True,
    artifacts={
        "publish_log": publish_log,
        "decision_log": {
            "version": "1.0",
            "project_id": PROJECT.name,
            "decisions": [decision],
        },
    },
)
print(f"✅ publish 阶段已完成 (completed)")
