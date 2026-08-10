"""Write asset_manifest and close assets gate."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.checkpoint import write_checkpoint

PROJECT = Path(r"d:\my\OpenMontage\projects\healing-winter-night")
ARTIFACTS = PROJECT / "artifacts"

# ── 1. Build asset_manifest ──────────────────────────────────────────
manifest = {
    "version": "1.0",
    "assets": [
        {
            "id": "shot_1_first_frame",
            "type": "image",
            "path": "assets/shot_1_first_frame.png",
            "source_tool": "comfyui_image",
            "scene_id": "shot_1",
            "prompt": "一位10-12岁的中国女孩，纯东亚人面孔，典型中国人长相，圆圆的脸蛋，单眼皮，暖黄皮肤，乌黑头发，黑色瞳孔，齐眉刘海，扎着低马尾，穿着暖色针织毛衣。她趴在窗台边，下巴轻轻搁在手臂上，眼神温柔地望向窗外纷飞的大雪，微微哈气在玻璃上凝成白雾。暖黄的钨丝灯光在她侧脸与发丝上形成柔和轮廓光，窗外冷蓝雪光与室内暖黄灯光冷暖对比。玻璃上有雾气水珠（前景虚化），窗外飞雪可见（背景柔化虚化）。色彩：暖黄 #F5C87A 室内 vs 冷蓝 #2B3A55 室外。浅景深，85mm镜头，电影感胶片颗粒，安静冬夜氛围。竖构图9:16，绝无西方人面孔特征。",
            "model": "qwen_image_2512_fp8_e4m3fn_scaled_comfyui_4steps_v1.0",
            "cost_usd": 0,
            "resolution": "864x1536",
            "format": "png",
            "subtype": "generated",
            "generation_summary": "Qwen Image 2512 via ComfyUI custom workflow, 4-step Lightning LoRA",
            "provider": "comfyui",
        },
        {
            "id": "shot_1_video",
            "type": "video",
            "path": "assets/shot_1_video.mp4",
            "source_tool": "comfyui_video",
            "scene_id": "shot_1",
            "prompt": "全局设定（不变）：暖黄怀旧的冬夜室内。10-12岁中国女孩（纯东亚人面孔，乌黑头发，齐眉刘海，低马尾，暖色针织毛衣）趴在窗台边，下巴搁在手臂上。窗外大雪纷飞，窗玻璃上凝结着雾气与水珠，暖黄钨丝灯光柔和地照亮她的侧脸，写实电影质感，冷暖对比光影。分镜时间轴：[0s-2s] 静谧与呼吸感 [2s-4s] 视线收回与眨眼 [4s-6s] 转头与浅笑。运镜：slow push in。",
            "model": "minimax_h3_fl2va_pruned_int8_convrot",
            "cost_usd": 0,
            "duration_seconds": 6.58,
            "resolution": "480x864",
            "format": "mp4",
            "subtype": "generated",
            "generation_summary": "MiniMax H3 I2V via ComfyUI custom workflow, Turbo 4-step LoRA, 24fps",
            "provider": "comfyui",
        },
        {
            "id": "shot_2_first_frame",
            "type": "image",
            "path": "assets/shot_2_first_frame.png",
            "source_tool": "comfyui_image",
            "scene_id": "shot_2",
            "prompt": "竖构图9:16，电影感静帧。窗玻璃表面的极近特写，镜头紧贴玻璃。前景：玻璃上凝结的雾气水珠，颗颗清晰锐利，部分水珠正缓缓向下滑落。中景：窗外纷飞的大雪，雪花轻柔飘过，整体柔焦虚化。背景边缘：画面最边缘可见一线暖黄钨丝灯光轮廓（虚化成光晕）。色彩：冷蓝 #2B3A55 主导画面，暖黄 #F5C87A 仅在画面边缘作为细线轮廓光。极浅景深，135mm镜头压缩感，电影感胶片颗粒，空灵静谧冬夜氛围。纯景物，绝无人物面孔。",
            "model": "qwen_image_2512_fp8_e4m3fn_scaled_comfyui_4steps_v1.0",
            "cost_usd": 0,
            "resolution": "864x1536",
            "format": "png",
            "subtype": "generated",
            "generation_summary": "Qwen Image 2512 via ComfyUI custom workflow, 4-step Lightning LoRA",
            "provider": "comfyui",
        },
        {
            "id": "shot_2_video",
            "type": "video",
            "path": "assets/shot_2_video.mp4",
            "source_tool": "comfyui_video",
            "scene_id": "shot_2",
            "prompt": "全局设定（不变）：窗玻璃表面极近特写，镜头紧贴玻璃。冷蓝冬夜氛围，窗外大雪纷飞。前景：玻璃上凝结的雾气水珠，颗颗清晰锐利，部分水珠正缓缓向下滑落，留下水痕。中景：窗外纷飞的大雪，雪花轻柔飘过，整体柔焦虚化。背景边缘：画面最边缘可见一线暖黄钨丝灯光轮廓（虚化成光晕）。分镜时间轴：[0s-2s] 水珠凝结 [2s-4s] 水痕滑落 [4s-6s] 静谧延续。运镜：slow push in。",
            "model": "minimax_h3_fl2va_pruned_int8_convrot",
            "cost_usd": 0,
            "duration_seconds": 6.58,
            "resolution": "480x864",
            "format": "mp4",
            "subtype": "generated",
            "generation_summary": "MiniMax H3 I2V via ComfyUI custom workflow, Turbo 4-step LoRA, 24fps",
            "provider": "comfyui",
        },
    ],
    "total_cost_usd": 0,
    "metadata": {
        "generation_pipeline": "ComfyUI (Qwen Image 2512 + MiniMax H3 I2V)",
        "audio_note": "H3 I2V 自动生成含环境音轨的视频，无需额外音频资产",
        "total_assets": 4,
        "asset_breakdown": {
            "images": 2,
            "videos": 2,
        },
    },
}

# Save artifact
ARTIFACTS.mkdir(parents=True, exist_ok=True)
manifest_path = ARTIFACTS / "asset_manifest.json"
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
print(f"✅ asset_manifest.json 已保存")

# ── 2. Close assets gate ─────────────────────────────────────────────
decision = {
    "decision_id": "d18",
    "stage": "assets",
    "category": "motion_commitment",
    "subject": "Assets generation approval for shot_1 and shot_2",
    "options_considered": [
        {
            "option_id": "approve_all",
            "label": "Approve all 4 assets (2 images + 2 videos)",
            "score": 1.0,
            "reason": "User approved both shots; all assets generated successfully with $0 cost",
        },
        {
            "option_id": "regenerate_shot_1",
            "label": "Regenerate shot_1",
            "score": 0.0,
            "reason": "Not needed; user approved",
        },
        {
            "option_id": "regenerate_shot_2",
            "label": "Regenerate shot_2",
            "score": 0.0,
            "reason": "Not needed; user approved",
        },
    ],
    "selected": "approve_all",
    "reason": "用户批准 shot_1（女孩趴窗望雪）和 shot_2（窗玻璃水珠特写）两段视频。4 个资产全部生成完毕（2 首帧图 + 2 视频），总成本 $0。",
    "user_visible": True,
    "user_approved": True,
    "confidence": 1.0,
}

write_checkpoint(
    pipeline_dir=PROJECT.parent,
    project_id=PROJECT.name,
    stage="assets",
    status="completed",
    human_approved=True,
    artifacts={
        "asset_manifest": manifest,  # Pass the dict, not the path
        "decision_log": {
            "version": "1.0",
            "project_id": PROJECT.name,
            "decisions": [decision],
        },
    },
)
print(f"✅ assets 阶段门控已关闭 (completed)")
