import sys, os, time, requests
sys.path.insert(0, 'D:\\my\\OpenMontage')
from pathlib import Path
os.environ['COMFYUI_SERVER_URL'] = 'http://localhost:8000'
from tools._comfyui.client import ComfyUIClient

client = ComfyUIClient()
dest_dir = Path('D:/my/OpenMontage/projects')

# Wait for queue to finish
print('Waiting for ComfyUI queue to finish...')
for attempt in range(60):
    try:
        r = requests.get('http://localhost:8000/queue', timeout=10)
        q = r.json()
        qr = q.get('queue_running') or []
        qp = q.get('queue_pending') or []
        if len(qr) == 0 and len(qp) == 0:
            print('Queue is empty!')
            break
        print(f'  Running: {len(qr)}, Pending: {len(qp)} (attempt {attempt+1})')
    except Exception as e:
        print(f'  Connection issue: {e}')
    time.sleep(15)

# Download results
print('Downloading results...')
r = requests.get('http://localhost:8000/history', timeout=30)
hist = r.json()
seen = set()

# Sort by time (approximate) - newer ones have more recent timestamps
for prompt_id in sorted(hist.keys(), reverse=True):
    entry = hist[prompt_id]
    status = entry.get('status', {}).get('status_str', '')
    for node_id, node_out in entry.get('outputs', {}).items():
        for img in node_out.get('images', []):
            fn = img['filename']
            if fn not in seen and fn.startswith('travel_'):
                seen.add(fn)
                dest = dest_dir / fn
                try:
                    client.download(img['filename'], img.get('subfolder', ''), dest, img.get('type', 'output'))
                    print(f'{fn}: {dest.stat().st_size} bytes')
                except Exception as e:
                    print(f'{fn}: Download error: {e}')

print(f'Total images: {len(seen)}')
print('Files in projects/:')
for f in sorted(dest_dir.glob('travel_*')):
    print(f'  {f.name} - {f.stat().st_size} bytes')
