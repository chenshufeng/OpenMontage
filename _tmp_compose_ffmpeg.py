"""Compose final video via FFmpeg (fallback)."""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

PROJECT = Path(r"d:\my\OpenMontage\projects\healing-winter-night")
ASSETS = PROJECT / "assets"
OUTPUT = PROJECT / "healing-winter-night_final.mp4"

# Input files
SHOT_1 = ASSETS / "shot_1_video.mp4"
SHOT_2 = ASSETS / "shot_2_video.mp4"

print("🎬 FFmpeg 合成模式")
print(f"   Shot 1: {SHOT_1.name}")
print(f"   Shot 2: {SHOT_2.name}")
print(f"   Output: {OUTPUT.name}")

# FFmpeg command: concat with crossfade transition
# - shot_1 (6.58s) + shot_2 (6.58s) with 0.8s crossfade at 6s
# - Total duration: ~12.36s

cmd = [
    "ffmpeg",
    "-y",  # overwrite output
    "-i", str(SHOT_1),
    "-i", str(SHOT_2),
    "-filter_complex",
    # Video: crossfade at 6s (offset = 6.58 - 0.8 = 5.78)
    "[0:v][1:v]xfade=transition=fade:duration=0.8:offset=5.78[v];"
    # Audio: crossfade at 6s
    "[0:a][1:a]acrossfade=d=0.8[a]",
    "-map", "[v]",
    "-map", "[a]",
    "-c:v", "libx264",
    "-preset", "medium",
    "-crf", "23",
    "-c:a", "aac",
    "-b:a", "192k",
    "-movflags", "+faststart",
    str(OUTPUT),
]

print("\n⚙️  执行 FFmpeg...")
print(f"   命令: {' '.join(cmd[:10])}...")

try:
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=300,
    )
    
    if result.returncode == 0:
        print(f"\n✅ 成片合成成功: {OUTPUT}")
        
        # Verify with ffprobe
        probe_cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "stream=width,height,duration,r_frame_rate,codec_name",
            "-of", "json",
            str(OUTPUT),
        ]
        probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)
        if probe_result.returncode == 0:
            info = json.loads(probe_result.stdout)
            for stream in info.get("streams", []):
                if stream.get("codec_name") == "h264":
                    print(f"   尺寸: {stream['width']}x{stream['height']}")
                    print(f"   时长: {float(stream['duration']):.2f}s")
                    print(f"   帧率: {stream['r_frame_rate']}")
    else:
        print(f"\n❌ FFmpeg 失败:")
        print(result.stderr[:2000])
        
except subprocess.TimeoutExpired:
    print("\n❌ FFmpeg 超时 (300s)")
except Exception as e:
    print(f"\n❌ 错误: {e}")
