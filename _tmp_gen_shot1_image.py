# -*- coding: utf-8 -*-
"""Generate shot_1 first-frame image using Qwen Image 2512 workflow."""
import sys, json
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))

from tools.graphics.comfyui_image import ComfyUIImage

ROOT = Path(r"d:\my\OpenMontage")
PROJECT = "healing-winter-night"
WORKFLOW = ROOT / "workflow" / "image_qwen_Image_2512.json"
OUTPUT = ROOT / "projects" / PROJECT / "assets" / "shot_1_first_frame.png"

# Load and patch the workflow
with open(WORKFLOW, encoding="utf-8") as f:
    workflow = json.load(f)

# Patch positive prompt (node "238:227")
shot_1_prompt = (
    "一位10-12岁的中国女孩，纯东亚人面孔，典型中国人长相，圆圆的脸蛋，单眼皮，暖黄皮肤，乌黑头发，黑色瞳孔，齐眉刘海，扎着低马尾，穿着暖色针织毛衣。"
    "她趴在窗台边，下巴轻轻搁在手臂上，眼神温柔地望向窗外纷飞的大雪，微微哈气在玻璃上凝成白雾。"
    "暖黄的钨丝灯光在她侧脸与发丝上形成柔和轮廓光，窗外冷蓝雪光与室内暖黄灯光冷暖对比。"
    "玻璃上有雾气水珠（前景虚化），窗外飞雪可见（背景柔化虚化）。"
    "色彩：暖黄 #F5C87A 室内 vs 冷蓝 #2B3A55 室外。浅景深，85mm镜头，电影感胶片颗粒，安静冬夜氛围。"
    "竖构图9:16，绝无西方人面孔特征。"
)
workflow["238:227"]["inputs"]["text"] = shot_1_prompt

# Patch negative prompt (node "238:228") — keep existing
negative_prompt = "低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲"
workflow["238:228"]["inputs"]["text"] = negative_prompt

# Patch output filename_prefix (node "60")
workflow["60"]["inputs"]["filename_prefix"] = "shot_1_first_frame"

# Call comfyui_image
tool = ComfyUIImage()
result = tool.execute({
    "prompt": shot_1_prompt,
    "workflow_json": json.dumps(workflow),
    "output_node": "60",
    "output_path": str(OUTPUT),
    "workflow_name": "Qwen Image 2512 (灯下的守候 preset)",
    "workflow_model": "qwen_image_2512_fp8_e4m3fn_scaled_comfyui_4steps_v1.0",
    "workflow_model_stack": [
        {"name": "qwen_image_2512_fp8_e4m3fn_scaled_comfyui_4steps_v1.0.safetensors", "role": "diffusion_model", "quantization": "fp8_e4m3fn"},
        {"name": "qwen_2.5_vl_7b_fp8_scaled.safetensors", "role": "text_encoder", "quantization": "fp8"},
        {"name": "qwen_image_vae.safetensors", "role": "vae"},
        {"name": "Qwen-Image-2512-Lightning-4steps-V1.0-fp32.safetensors", "role": "lora", "strength_model": 1.0},
    ],
})

if result.success:
    print(f"✅ shot_1 首帧生成成功: {result.data['output']}")
    print(f"   尺寸: {result.data['width']}x{result.data['height']}")
    print(f"   耗时: {result.duration_seconds:.1f}s")
    print(f"   Seed: {result.seed}")
else:
    print(f"❌ 生成失败: {result.error}")
    if result.data:
        print(f"   详情: {json.dumps(result.data, ensure_ascii=False, indent=2)}")
