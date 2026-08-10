"""Generate remaining travel portrait variations."""
import sys
sys.path.insert(0, 'D:\\my\\OpenMontage')
from pathlib import Path
import os
os.environ['COMFYUI_SERVER_URL'] = 'http://localhost:8000'
from tools._comfyui.client import ComfyUIClient

client = ComfyUIClient()
dest_dir = Path('D:/my/OpenMontage/projects')
dest_dir.mkdir(parents=True, exist_ok=True)

remaining = [
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

for var in remaining:
    print(f'Generating: {var["filename"]}...')
    workflow = {
        '1': {'class_type': 'UNETLoader', 'inputs': {'unet_name': 'qwen_image_edit_fp8_e4m3fn.safetensors', 'weight_dtype': 'default'}},
        '2': {'class_type': 'CLIPLoader', 'inputs': {'clip_name': 'qwen_2.5_vl_7b_fp8_scaled.safetensors', 'type': 'qwen_image', 'device': 'cpu'}},
        '3': {'class_type': 'VAELoader', 'inputs': {'vae_name': 'qwen_image_vae.safetensors'}},
        '4': {'class_type': 'LoadImage', 'inputs': {'image': '00010-2487448663.png'}},
        '5': {'class_type': 'TextEncodeQwenImageEdit', 'inputs': {'clip': ['2', 0], 'prompt': var['prompt'], 'vae': ['3', 0], 'image': ['4', 0]}},
        '6': {'class_type': 'CLIPTextEncode', 'inputs': {'clip': ['2', 0], 'text': ''}},
        '7': {'class_type': 'VAEEncode', 'inputs': {'pixels': ['4', 0], 'vae': ['3', 0]}},
        '8': {'class_type': 'KSampler', 'inputs': {'model': ['1', 0], 'seed': var['seed'], 'steps': 20, 'cfg': 3.5, 'sampler_name': 'euler', 'scheduler': 'sgm_uniform', 'positive': ['5', 0], 'negative': ['6', 0], 'latent_image': ['7', 0], 'denoise': 0.85}},
        '9': {'class_type': 'VAEDecode', 'inputs': {'samples': ['8', 0], 'vae': ['3', 0]}},
        '10': {'class_type': 'SaveImage', 'inputs': {'images': ['9', 0], 'filename_prefix': var['filename']}}
    }
    prompt_id = client.submit(workflow)
    print(f'  Submitted: {prompt_id}')

# Wait for all to complete - just poll with very long timeout
import time, requests
running = True
while running:
    r = requests.get('http://localhost:8000/queue', timeout=5)
    q = r.json()
    running = bool(q.get('queue_running') or q.get('queue_pending'))
    if running:
        qr = q.get('queue_running') or []
        qp = q.get('queue_pending') or []
        print(f'  Waiting... running={len(qr)}, pending={len(qp)}')
        time.sleep(10)
    else:
        print('  Queue empty')

# Download results
r = requests.get('http://localhost:8000/history', timeout=10)
hist = r.json()
seen = set()
for entry in hist.values():
    for node_out in entry.get('outputs', {}).values():
        for img in node_out.get('images', []):
            fn = img['filename']
            if fn not in seen and fn.startswith('travel_'):
                seen.add(fn)
                dest = dest_dir / fn
                client.download(img['filename'], img.get('subfolder', ''), dest, img.get('type', 'output'))
                print(f'Downloaded: {fn} ({dest.stat().st_size} bytes)')

print('All done!')
