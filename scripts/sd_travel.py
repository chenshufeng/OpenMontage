import requests, json, time, sys, os

API_BASE = 'http://localhost:8000'
INPUT_IMAGE = '00010-2487448663.png'

styles = [
    ('sd_travel_mountain', 'travel portrait, a Chinese man standing in front of snowy mountains and alpine lake, professional photography, cinematic lighting, detailed clothing, high quality, realistic photo, 4k, highly detailed face'),
    ('sd_travel_beach', 'travel portrait, a Chinese man on a tropical beach at sunset, golden hour lighting, ocean waves, palm trees, professional photography, cinematic, realistic photo, 4k'),
    ('sd_travel_city', 'travel portrait, a Chinese man walking in a modern european city street, architecture, sunny day, professional photography, cinematic lighting, realistic photo, 4k, detailed'),
    ('sd_travel_forest', 'travel portrait, a Chinese man in a mystical forest with sunbeams filtering through trees, nature, professional photography, cinematic, realistic photo, 4k, detailed')
]

negative = '(worst quality:2), (low quality:2), normal quality, ugly, blurry, deformed, ugly body, bad anatomy, watermark, text, signature, extra fingers, bad hands, mutated hands'

for prefix, pos_prompt in styles:
    print(f'\n===== Generating: {prefix} =====')

    prompt_wf = {
        '2': {'class_type': 'CheckpointLoaderSimple', 'inputs': {'ckpt_name': 'v1-5-pruned-emaonly-fp16.safetensors'}},
        '1': {'class_type': 'LoadImage', 'inputs': {'image': INPUT_IMAGE}},
        '3': {'class_type': 'CLIPTextEncode', 'inputs': {'text': pos_prompt, 'clip': ['2', 1]}},
        '4': {'class_type': 'CLIPTextEncode', 'inputs': {'text': negative, 'clip': ['2', 1]}},
        '5': {'class_type': 'VAEEncode', 'inputs': {'pixels': ['1', 0], 'vae': ['2', 2]}},
        '6': {'class_type': 'KSampler', 'inputs': {
            'model': ['2', 0], 'seed': 42, 'steps': 25, 'cfg': 7.0,
            'sampler_name': 'euler', 'scheduler': 'normal',
            'positive': ['3', 0], 'negative': ['4', 0],
            'latent_image': ['5', 0], 'denoise': 0.75
        }},
        '7': {'class_type': 'VAEDecode', 'inputs': {'samples': ['6', 0], 'vae': ['2', 2]}},
        '8': {'class_type': 'SaveImage', 'inputs': {'images': ['7', 0], 'filename_prefix': prefix}}
    }

    r = requests.post(f'{API_BASE}/prompt', json={'prompt': prompt_wf}, timeout=10)
    resp = r.json()
    if 'error' in resp:
        print(f'ERROR: {resp["error"]}')
        print(json.dumps(resp, indent=2))
        continue
    prompt_id = resp['prompt_id'][:8]
    print(f'Prompt ID: {prompt_id}')

    while True:
        r = requests.get(f'{API_BASE}/queue', timeout=10)
        q = r.json()
        running = q.get('queue_running', [])
        pending = q.get('queue_pending', [])
        if prompt_id not in str(running) and prompt_id not in str(pending):
            print('Done!')
            break
        time.sleep(5)

print('\n===== All done! =====')
