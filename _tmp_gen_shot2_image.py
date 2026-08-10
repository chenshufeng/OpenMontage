"""Generate shot_2 first-frame image via Qwen Image 2512."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tools.graphics.comfyui_image import ComfyUIImage

# Paths
WORKFLOW = Path(r"d:\my\OpenMontage\workflow\image_qwen_Image_2512.json")
OUTPUT = Path(r"d:\my\OpenMontage\projects\healing-winter-night\assets\shot_2_first_frame.png")

# Load Qwen Image workflow
with open(WORKFLOW, encoding="utf-8") as f:
    workflow = json.load(f)

# Patch positive prompt (node "238:227") — shot_2: window glass extreme close-up, no human
shot_2_prompt = (
    "竖构图9:16，电影感静帧。窗玻璃表面的极近特写，镜头紧贴玻璃。"
    "前景：玻璃上凝结的雾气水珠，颗颗清晰锐利，部分水珠正缓缓向下滑落。"
    "中景：窗外纷飞的大雪，雪花轻柔飘过，整体柔焦虚化。"
    "背景边缘：画面最边缘可见一线暖黄钨丝灯光轮廓（虚化成光晕）。"
    "色彩：冷蓝 #2B3A55 主导画面，暖黄 #F5C87A 仅在画面边缘作为细线轮廓光。"
    "极浅景深，135mm镜头压缩感，电影感胶片颗粒，空灵静谧冬夜氛围。"
    "纯景物，绝无人物面孔。"
)
workflow["238:227"]["inputs"]["text"] = shot_2_prompt

# Patch negative prompt (node "238:228")
negative_prompt = (
    "人脸, 人物, 文字, 低质量, 模糊, 变形, 多余肢体, 过曝, 噪点, "
    "卡通, 动画, 插画, 西方人面孔"
)
workflow["238:228"]["inputs"]["text"] = negative_prompt

# Patch output filename_prefix (node "60")
workflow["60"]["inputs"]["filename_prefix"] = "shot_2_first_frame"

# Execute
tool = ComfyUIImage()
result = tool.execute({
    "prompt": shot_2_prompt,
    "workflow_json": json.dumps(workflow),
    "output_node": "60",
    "output_path": str(OUTPUT),
    "workflow_name": "Qwen Image 2512 (灯下的守候 shot_2 preset)",
    "workflow_model": "qwen_image_2512_fp8_e4m3fn_scaled_comfyui_4steps_v1.0",
    "workflow_model_stack": [
        {"name": "qwen_image_2512_fp8_e4m3fn_scaled_comfyui_4steps_v1.0", "role": "unet", "quantization": "fp8"},
        {"name": "qwen_2.5_vl_7b_fp8_scaled", "role": "clip", "quantization": "fp8"},
        {"name": "qwen_image_vae", "role": "vae"},
        {"name": "Qwen-Image-2512-Lightning-4steps", "role": "lora", "strength": 1.0},
    ],
})

if result.success:
    print(f"✅ shot_2 首帧生成成功: {result.data['output']}")
    print(f"   耗时: {result.data.get('generation_time_seconds', 'N/A')}s")
else:
    print(f"❌ 生成失败: {result.error}")
