"""Generate shot_1 video via H3 I2V."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tools.video.comfyui_video import ComfyUIVideo
from tools._comfyui.client import ComfyUIClient

# Paths
WORKFLOW = Path(r"d:\my\OpenMontage\workflow\video_minimax_h3_i2v.json")
FIRST_FRAME = Path(r"d:\my\OpenMontage\projects\healing-winter-night\assets\shot_1_first_frame.png")
OUTPUT = Path(r"d:\my\OpenMontage\projects\healing-winter-night\assets\shot_1_video.mp4")

# 1. Upload first-frame image to ComfyUI
client = ComfyUIClient()
server_filename = client.upload_image(FIRST_FRAME, "shot_1_first_frame.png")
print(f"✅ 首帧图已上传: {server_filename}")

# 2. Load H3 I2V workflow
with open(WORKFLOW, encoding="utf-8") as f:
    workflow = json.load(f)

# 3. Patch prompt (node "105:104")
shot_1_motion_prompt = (
    "全局设定（不变）：暖黄怀旧的冬夜室内。10-12岁中国女孩（纯东亚人面孔，乌黑头发，齐眉刘海，低马尾，暖色针织毛衣）趴在窗台边，下巴搁在手臂上。"
    "窗外大雪纷飞，窗玻璃上凝结着雾气与水珠，暖黄钨丝灯光柔和地照亮她的侧脸，写实电影质感，冷暖对比光影。\n\n"
    "分镜时间轴：\n"
    "[0s-2s] 静谧与呼吸感：女孩保持趴窗望雪的姿势，睫毛轻微颤动，胸口随呼吸轻微起伏，钨丝灯光呈现极细微的呼吸式明暗波动，她侧脸的轮廓光随之微微明暗，窗外雪花持续缓慢飘落。\n"
    "[2s-4s] 视线收回与眨眼：她的视线从远处的大雪缓缓收回，缓慢地眨动一下眼睛，玻璃上的一滴水珠缓缓滑落并反射出光点，她哈出的白雾在玻璃上轻微扩散变淡。\n"
    "[4s-6s] 转头与浅笑：她轻轻转头看向镜头右侧，嘴角轻轻上扬成一个含蓄的抿嘴浅笑（不露齿），钨丝灯光柔和地照亮她转正后的脸庞，面部亮度缓缓提升。\n\n"
    "运镜：镜头以极缓慢的速度推近（slow push in），同时带轻微的手持呼吸感与前景虚化光斑的缓慢位移，营造身临其境的凝视感，无突兀晃动。\n"
    "光影要求：暖黄灯光为主光源并带呼吸式细微明暗波动，窗外冷蓝雪光作为侧逆光，玻璃水珠、白雾需有真实高光反射，整体低调暖调，避免过曝与画面闪烁。"
)
workflow["105:104"]["inputs"]["prompt"] = shot_1_motion_prompt

# 4. Patch LoadImage node with uploaded filename
workflow["114"]["inputs"]["image"] = server_filename

# 5. Set duration to 6 seconds
workflow["105:111"]["inputs"]["value"] = 6

# 6. Patch output filename_prefix
workflow["92"]["inputs"]["filename_prefix"] = "shot_1_video"

# 7. Call comfyui_video
tool = ComfyUIVideo()
result = tool.execute({
    "prompt": shot_1_motion_prompt,
    "operation": "image_to_video",
    "workflow_json": json.dumps(workflow),
    "output_node": "92",
    "output_path": str(OUTPUT),
    "workflow_name": "MiniMax H3 I2V (灯下的守候 shot_1)",
    "workflow_model": "minimax_h3_fl2va_pruned_int8_convrot",
    "workflow_model_stack": [
        {"name": "minimax_h3_fl2va_pruned_int8_convrot.safetensors", "role": "unet", "quantization": "int8"},
        {"name": "qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors", "role": "clip", "quantization": "nvfp4"},
        {"name": "minimax_h3_video_vae_fp16.safetensors", "role": "vae", "quantization": "fp16"},
        {"name": "minimax_h3_turbo_v4_step600_ema.safetensors", "role": "lora", "strength": 1.0},
    ],
})

if result.success:
    print(f"✅ shot_1 视频生成成功: {result.data['output']}")
    print(f"   时长: {result.data.get('duration_seconds', 'N/A')}s")
    print(f"   尺寸: {result.data.get('width')}x{result.data.get('height')}")
else:
    print(f"❌ 生成失败: {result.error}")
    if result.data:
        print(f"   详情: {json.dumps(result.data, indent=2, ensure_ascii=False)[:500]}")
