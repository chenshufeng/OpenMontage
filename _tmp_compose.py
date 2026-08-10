"""Compose final video via Remotion."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tools.video.video_compose import VideoCompose

PROJECT = Path(r"d:\my\OpenMontage\projects\healing-winter-night")
ARTIFACTS = PROJECT / "artifacts"
OUTPUT = PROJECT / "healing-winter-night_final.mp4"

# Load edit_decisions and asset_manifest
with open(ARTIFACTS / "edit_decisions.json", encoding="utf-8") as f:
    edit_decisions = json.load(f)

with open(ARTIFACTS / "asset_manifest.json", encoding="utf-8") as f:
    asset_manifest = json.load(f)

# Resolve asset paths (relative to project dir)
for asset in asset_manifest["assets"]:
    asset["path"] = str(PROJECT / asset["path"])

print("📋 Edit decisions loaded:")
print(f"   Cuts: {len(edit_decisions['cuts'])}")
print(f"   Transitions: {len(edit_decisions['transitions'])}")
print(f"   Render runtime: {edit_decisions['render_runtime']}")

print("\n📦 Asset manifest loaded:")
for asset in asset_manifest["assets"]:
    print(f"   - {asset['id']}: {asset['type']} ({asset['path']})")

# Compose video
tool = VideoCompose()
result = tool.execute({
    "operation": "render",
    "output_path": str(OUTPUT),
    "edit_decisions": edit_decisions,
    "asset_manifest": asset_manifest,
})

if result.success:
    print(f"\n✅ 成片渲染成功: {result.data['output']}")
    print(f"   时长: {result.data.get('duration_seconds', 'N/A')}s")
    print(f"   尺寸: {result.data.get('width')}x{result.data.get('height')}")
else:
    print(f"\n❌ 渲染失败: {result.error}")
    if result.data:
        print(f"   详情: {json.dumps(result.data, indent=2, ensure_ascii=False)[:1000]}")
