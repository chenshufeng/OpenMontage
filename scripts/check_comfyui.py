import requests, json

# Check queue
r = requests.get('http://localhost:8000/queue', timeout=5)
print('Queue:', json.dumps(r.json(), indent=2, ensure_ascii=False))

# Check history for recent entries
r2 = requests.get('http://localhost:8000/history', timeout=10)
hist = r2.json()
keys = sorted(hist.keys(), reverse=True)
for k in keys[:5]:
    e = hist[k]
    outs = e.get('outputs', {})
    status = e.get('status', {})
    print(f'{k[:8]}: status={status.get("status_str")}, outputs={list(outs.keys())}')
