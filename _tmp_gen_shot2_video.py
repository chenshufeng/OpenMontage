"""Generate shot_2 video via H3 I2V."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tools.video.comfyui_video import ComfyUIVideo
from tools._comfyui.client import ComfyUIClient

# Paths
WORKFLOW = Path(r"d:\my\OpenMontage\workflow\video_minimax_h3_i2v.json")
FIRST_FRAME = Path(r"d:\my\OpenMontage\projects\healing-winter-night\assets\shot_2_first_frame.png")
OUTPUT = Path(r"d:\my\OpenMontage\projects\healing-winter-night\assets\shot_2_video.mp4")

# 1. Upload first-frame image to ComfyUI
client = ComfyUIClient()
server_filename = client.upload_image(FIRST_FRAME, "shot_2_first_frame.png")
print(f"✅ 首帧图已上传: {server_filename}")

# 2. Load H3 I2V workflow
with open(WORKFLOW, encoding="utf-8") as f:
    workflow = json.load(f)

# 3. Patch prompt (node "105:104") — shot_2: window glass extreme close-up
shot_2_motion_prompt = (
    "全局设定（不变）：窗玻璃表面极近特写，镜头紧贴玻璃。冷蓝冬夜氛围，窗外大雪纷飞。"
    "前景：玻璃上凝结的雾气水珠，颗颗清晰锐利，部分水珠正缓缓向下滑落，留下水痕。"
    "中景：窗外纷飞的大雪，雪花轻柔飘过，整体柔焦虚化。"
    "背景边缘：画面最边缘可见一线暖黄钨丝灯光轮廓（虚化成光晕）。\n\n"
    "分镜时间轴：\n"
    "[0s-2s] 水珠凝结：玻璃表面雾气水珠缓慢凝结变大，部分水珠开始向下滑动，窗外雪花持续飘落。\n"
    "[2s-4s] 水痕滑落：水珠沿玻璃缓缓下滑，留下清晰水痕，水痕透出窗外冷蓝雪光。\n"
    "[4s-6s] 静谧延续：镜头继续缓慢贴近玻璃，水珠与水痕持续，窗外雪幕静谧飘落，画面归于空灵静谧。\n\n"
    "运镜：镜头以极缓慢速度继续推近（slow push in），几乎静止的凝视感，无突兀晃动。\n"
    "光影要求：冷蓝雪光为主，暖黄灯光仅在画面边缘作为细线轮廓，水珠需有真实高光反射，整体低调冷调，避免过曝与画面闪烁。"
)
workflow["105:104"]["inputs"]["prompt"] = shot_2_motion_prompt

# 4. Patch LoadImage node with uploaded filename
workflow["114"]["inputs"]["image"] = server_filename

# 5. Set duration to 6 seconds
workflow["105:111"]["inputs"]["value"] = 6

# 6. Patch output filename_prefix
workflow["92"]["inputs"]["filename_prefix"] = "shot_2_video"

# 7. Call comfyui_video
tool = ComfyUIVideo()
result = tool.execute({
    "prompt": shot_2_motion_prompt,
    "operation": "image_to_video",
    "workflow_json": json.dumps(workflow),
    "output_node": "92",
    "output_path": str(OUTPUT),
    "workflow_name": "MiniMax H3 I2V (灯下的守候 shot_2)",
    "workflow_model": "minimax_h3_fl2va_pruned_int8_convrot",
    "workflow_model_stack": [
        {"name": "minimax_h3_fl2va_pruned_int8_convrot.safetensors", "role": "unet", "quantization": "int8"},
        {"name": "qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors", "role": "clip", "quantization": "nvfp4"},
        {"name": "minimax_h3_video_vae_fp16.safetensors", "role": "vae", "quantization": "fp16"},
        {"name": "minimax_h3_turbo_v4_step600_ema.safetensors", "role": "lora", "strength": 1.0},
    ],
})

if result.success:
    print(f"✅ shot_2 视频生成成功: {result.data['output']}")
    print(f"   时长: {result.data.get('duration_seconds', 'N/A')}s")
    print(f"   尺寸: {result.data.get('width')}x{result.data.get('height')}")
else:
    print(f"❌ 生成失败: {result.error}")
    if result.data:
        print(f"   详情: {json.dumps(result.data, indent=2, ensure_ascii=False)[:500]}")
