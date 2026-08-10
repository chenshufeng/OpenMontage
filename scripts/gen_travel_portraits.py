"""Generate travel portrait variations using Qwen-Image-Edit via ComfyUI."""
import sys
sys.path.insert(0, 'D:\\my\\OpenMontage')
from pathlib import Path
import os
os.environ['COMFYUI_SERVER_URL'] = 'http://localhost:8000'
from tools._comfyui.client import ComfyUIClient

client = ComfyUIClient()

variations = [
    {
        'seed': 100,
        'prompt': '旅行写真风格：将这个人置于热带海滩，背景是碧蓝海水和白色沙滩，棕榈树，日落金色阳光。人物自然站立，微笑。度假摄影风格，温暖光线，高清',
        'filename': 'travel_beach'
    },
    {
        'seed': 200,
        'prompt': '旅行写真风格：将这个人置于欧洲古老城市街道，背景是石板路和彩色建筑，阳光透过树叶洒落。人物时尚旅行穿搭，自然漫步。街拍风格，电影感色调，细节丰富',
        'filename': 'travel_city'
    },
    {
        'seed': 300,
        'prompt': '旅行写真风格：将这个人置于神秘森林中，背景是高大树木和林间光柱，晨雾缭绕，野花点缀。人物穿着自然色系服装。森系摄影风格，柔和光线，梦幻氛围',
        'filename': 'travel_forest'
    }
]

dest_dir = Path('D:/my/OpenMontage/projects')
dest_dir.mkdir(parents=True, exist_ok=True)

base_workflow = {
    '1': {'class_type': 'UNETLoader', 'inputs': {'unet_name': 'qwen_image_edit_fp8_e4m3fn.safetensors', 'weight_dtype': 'default'}},
    '2': {'class_type': 'CLIPLoader', 'inputs': {'clip_name': 'qwen_2.5_vl_7b_fp8_scaled.safetensors', 'type': 'qwen_image', 'device': 'cpu'}},
    '3': {'class_type': 'VAELoader', 'inputs': {'vae_name': 'qwen_image_vae.safetensors'}},
    '4': {'class_type': 'LoadImage', 'inputs': {'image': '00010-2487448663.png'}},
    '6': {'class_type': 'CLIPTextEncode', 'inputs': {'clip': ['2', 0], 'text': ''}},
    '7': {'class_type': 'VAEEncode', 'inputs': {'pixels': ['4', 0], 'vae': ['3', 0]}},
    '8': {'class_type': 'KSampler', 'inputs': {'model': ['1', 0], 'seed': 42, 'steps': 20, 'cfg': 3.5, 'sampler_name': 'euler', 'scheduler': 'sgm_uniform', 'positive': ['5', 0], 'negative': ['6', 0], 'latent_image': ['7', 0], 'denoise': 0.85}},
    '9': {'class_type': 'VAEDecode', 'inputs': {'samples': ['8', 0], 'vae': ['3', 0]}},
    '10': {'class_type': 'SaveImage', 'inputs': {'images': ['9', 0], 'filename_prefix': 'travel'}}
}

for var in variations:
    print(f'Generating: {var["filename"]} (seed={var["seed"]})...')
    workflow = dict(base_workflow)
    workflow['5'] = {
        'class_type': 'TextEncodeQwenImageEdit',
        'inputs': {'clip': ['2', 0], 'prompt': var['prompt'], 'vae': ['3', 0], 'image': ['4', 0]}
    }
    workflow['8']['inputs']['seed'] = var['seed']
    workflow['10']['inputs']['filename_prefix'] = var['filename']

    prompt_id = client.submit(workflow)
    print(f'  Submitted: {prompt_id}')
    entry = client.poll(prompt_id, timeout=600, interval=5)
    outputs = entry.get('outputs', {}).get('10', {})
    images = outputs.get('images', [])
    if images:
        dest = dest_dir / f'{var["filename"]}.png'
        client.download(images[0]['filename'], images[0].get('subfolder', ''), dest, images[0].get('type', 'output'))
        print(f'  Saved: {dest}')
    else:
        print(f'  No output for {var["filename"]}')

print('All done!')
