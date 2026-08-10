# -*- coding: utf-8 -*-
"""Close the scene_plan gate with user approval."""
import sys, json
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
from lib.checkpoint import write_checkpoint, read_checkpoint

ROOT = Path(r"d:\my\OpenMontage")
PROJECT = "healing-winter-night"
PIPELINE_DIR = ROOT / "projects"

prev = read_checkpoint(PIPELINE_DIR, PROJECT, "scene_plan")
scene_plan = prev["artifacts"]["scene_plan"]

decisions = [{
    "decision_id": "d17",
    "stage": "scene_plan",
    "category": "concept_selection",
    "subject": "分镜计划批准",
    "options_considered": [
        {"option_id": "approve", "label": "批准 2 镜头交叉溶解分镜", "score": 0.95, "reason": "用户回复'通过'"},
    ],
    "selected": "approve",
    "reason": "用户批准分镜计划。",
    "user_visible": True,
    "user_approved": True,
}]

out = write_checkpoint(
    PIPELINE_DIR, PROJECT, "scene_plan", "completed",
    artifacts={
        "scene_plan": scene_plan,
        "decision_log": {"version": "1.0", "project_id": PROJECT, "decisions": decisions},
    },
    pipeline_type="cinematic",
    style_playbook="custom-healing-warm",
    human_approval_required=True,
    human_approved=True,
)
print("scene_plan gate closed:", out)
