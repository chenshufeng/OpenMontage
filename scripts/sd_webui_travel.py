import requests, json, time, os, base64

API_BASE = 'http://localhost:7860'
SOURCE = r'C:\Users\陈树锋\Documents\ComfyUI\input\00010-2487448663.png'
OUT_DIR = r'D:\my\OpenMontage\projects'

styles = [
    ('sd_webui_mountain',
     'travel portrait of a Chinese man, snowy mountains and alpine lake background, professional photography, cinematic lighting, detailed face, realistic photo, 4k, masterpiece, best quality',
     'snowy mountain, alpine lake, outdoor portrait, natural lighting, shallow depth of field'),
    ('sd_webui_beach',
     'travel portrait of a Chinese man, tropical beach sunset, golden hour, ocean waves, palm trees, professional photography, cinematic, realistic photo, 4k, masterpiece, best quality',
     'beach sunset, tropical, golden hour, outdoor portrait, warm lighting'),
    ('sd_webui_city',
     'travel portrait of a Chinese man, modern european city street, architecture, sunny day, professional photography, cinematic lighting, realistic photo, 4k, masterpiece, best quality',
     'city street, european architecture, sunny day, outdoor portrait, urban'),
    ('sd_webui_forest',
     'travel portrait of a Chinese man, mysterious forest with sunbeams, nature background, professional photography, cinematic, realistic photo, 4k, masterpiece, best quality',
     'forest, sunbeams, mystical, nature, outdoor portrait, shallow depth of field')
]

negative = '(worst quality:2), (low quality:2), normal quality, ugly, blurry, deformed, bad anatomy, watermark, text, signature, extra fingers, bad hands, mutated hands, nsfw'

with open(SOURCE, 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode('utf-8')

for prefix, pos_prompt, style_prompt in styles:
    print(f'\n===== Generating: {prefix} =====')
    full_prompt = f'{pos_prompt}, {style_prompt}'

    payload = {
        'init_images': [img_b64],
        'prompt': full_prompt,
        'negative_prompt': negative,
        'denoising_strength': 0.82,
        'sampler_name': 'Euler a',
        'steps': 25,
        'cfg_scale': 7,
        'width': 768,
        'height': 972,
        'resize_mode': 1,
        'batch_size': 1,
        'seed': -1,
        'override_settings': {
            'sd_model_checkpoint': '繁花10_v10.safetensors [c3b39b9bb6]'
        },
        'override_settings_restore_afterwards': True
    }

    r = requests.post(f'{API_BASE}/sdapi/v1/img2img', json=payload, timeout=300)
    resp = r.json()
    if 'images' not in resp:
        print(f'ERROR: {json.dumps(resp, indent=2)[:500]}')
        continue

    img_data = base64.b64decode(resp['images'][0])
    out_path = os.path.join(OUT_DIR, f'{prefix}.png')
    with open(out_path, 'wb') as f:
        f.write(img_data)
    print(f'Saved: {out_path}')
    seed = resp.get('seed', '?')
    print(f'Seed: {seed}')

print('\n===== All done! =====')
