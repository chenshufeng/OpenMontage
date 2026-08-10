import sys
sys.path.insert(0, 'D:\\my\\OpenMontage')
from pathlib import Path
import os
os.environ['COMFYUI_SERVER_URL'] = 'http://localhost:8000'
from tools._comfyui.client import ComfyUIClient

client = ComfyUIClient()
dest_dir = Path('D:/my/OpenMontage/projects')
dest_dir.mkdir(parents=True, exist_ok=True)

# Check history for outputs with "travel" prefix
r = __import__('requests').get('http://localhost:8000/history', timeout=10)
hist = r.json()
results = []

for prompt_id, entry in hist.items():
    outputs = entry.get('outputs', {})
    for node_id, node_out in outputs.items():
        for img in node_out.get('images', []):
            fn = img['filename']
            if fn.startswith('travel_'):
                results.append((img, prompt_id))

print(f'Found {len(results)} travel images')

# Download each unique output
seen = set()
for img, pid in results:
    fn = img['filename']
    if fn not in seen:
        seen.add(fn)
        dest = dest_dir / fn
        client.download(img['filename'], img.get('subfolder', ''), dest, img.get('type', 'output'))
        print(f'{fn}: {dest} ({dest.stat().st_size} bytes)')
