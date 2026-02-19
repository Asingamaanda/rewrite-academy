"""
Add Background Music and Narration to Chapter 1 Video
Combines video + narration + background music
"""

import subprocess
from pathlib import Path
import sys

print("=" * 70)
print("ADD BACKGROUND MUSIC & NARRATION TO VIDEO")
print("=" * 70)

# File paths
video_file = Path("media/videos/chapter1_complete/1080p60/Chapter1_Complete_Lesson_1080p.mp4")
narration_file = Path("media/audio/chapter1_narration/Chapter1_Complete_Narration.mp3")
output_dir = Path("media/final_videos")
output_dir.mkdir(parents=True, exist_ok=True)

# Check if video exists
if not video_file.exists():
    print(f"\n✗ Video file not found: {video_file}")
    print("   Please render the high-quality video first.")
    sys.exit(1)

print(f"\n✓ Found video: {video_file.name}")

# Check if narration exists
has_narration = narration_file.exists()
if has_narration:
    print(f"✓ Found narration: {narration_file.name}")
else:
    print(f"⚠ Narration not found: {narration_file.name}")
    print("  Run generate_tts_narration.py first to create narration")
    print("  Continuing without narration...")

# Background music options
print("\n" + "=" * 70)
print("BACKGROUND MUSIC OPTIONS")
print("=" * 70)
print("""
For copyright-free background music, download from:
1. YouTube Audio Library: https://www.youtube.com/audiolibrary
2. Free Music Archive: https://freemusicarchive.org
3. Incompetech: https://incompetech.com
4. Bensound: https://www.bensound.com

Recommended style: Soft ambient, educational, lo-fi
Avoid: Distracting, loud, lyrical music

Save your music file as: media/audio/background_music.mp3
""")

music_file = Path("media/audio/background_music.mp3")
has_music = music_file.exists()

if has_music:
    print(f"✓ Found background music: {music_file.name}")
else:
    print(f"⚠ No background music found at: {music_file}")
    print("  Continuing without background music...")

print("\n" + "=" * 70)
print("CREATING FINAL VIDEO")
print("=" * 70)

# Different scenarios based on available files

if has_narration and has_music:
    # Scenario 1: Video + Narration + Background Music
    print("\nScenario: Video + Narration + Background Music")
    output_file = output_dir / "Chapter1_Complete_With_Narration_And_Music.mp4"
    
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", str(video_file),           # Input video
        "-i", str(narration_file),       # Input narration
        "-i", str(music_file),           # Input music
        "-filter_complex",
        "[1:a]volume=1.0[narration];"    # Narration at full volume
        "[2:a]volume=0.15[music];"       # Music at 15% volume (quiet background)
        "[narration][music]amix=inputs=2:duration=first[audio]",  # Mix audio
        "-map", "0:v",                   # Use video from first input
        "-map", "[audio]",               # Use mixed audio
        "-c:v", "copy",                  # Copy video codec (fast)
        "-c:a", "aac",                   # AAC audio codec
        "-b:a", "192k",                  # Audio bitrate
        "-shortest",                     # End when shortest stream ends
        "-y",                            # Overwrite output
        str(output_file)
    ]

elif has_narration and not has_music:
    # Scenario 2: Video + Narration only
    print("\nScenario: Video + Narration (no background music)")
    output_file = output_dir / "Chapter1_Complete_With_Narration.mp4"
    
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", str(video_file),
        "-i", str(narration_file),
        "-map", "0:v",
        "-map", "1:a",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-y",
        str(output_file)
    ]

elif not has_narration and has_music:
    # Scenario 3: Video + Background Music only
    print("\nScenario: Video + Background Music (no narration)")
    output_file = output_dir / "Chapter1_Complete_With_Music.mp4"
    
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", str(video_file),
        "-i", str(music_file),
        "-filter_complex",
        "[1:a]volume=0.20[music]",       # Music at 20% volume
        "-map", "0:v",
        "-map", "[music]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-y",
        str(output_file)
    ]

else:
    # Scenario 4: No audio available
    print("\n⚠ No narration or music found.")
    print("Please:")
    print("1. Run generate_tts_narration.py to create narration")
    print("2. Download background music to media/audio/background_music.mp3")
    sys.exit(1)

# Run FFmpeg
print(f"\nOutput file: {output_file.name}")
print("Processing... This may take a few minutes.\n")

try:
    result = subprocess.run(
        ffmpeg_cmd,
        capture_output=True,
        text=True,
        check=True
    )
    
    print("=" * 70)
    print("✓ SUCCESS! FINAL VIDEO CREATED!")
    print("=" * 70)
    print(f"\nFile: {output_file}")
    
    if output_file.exists():
        size_mb = output_file.stat().st_size / (1024 * 1024)
        print(f"Size: {size_mb:.2f} MB")
    
    print("\nYour complete educational video is ready!")
    print("It includes:")
    if has_narration:
        print("  ✓ Professional narration")
    if has_music:
        print("  ✓ Background music")
    print("  ✓ High-quality animations (1080p60)")
    
    print("\nYou can now:")
    print("  • Share with students")
    print("  • Upload to YouTube/online platform")
    print("  • Use in classroom presentations")

except subprocess.CalledProcessError as e:
    print("✗ Error processing video")
    print(f"Error message: {e.stderr[:500]}")
    print("\nTroubleshooting:")
    print("1. Make sure FFmpeg is installed")
    print("2. Check that all input files exist")
    print("3. Verify file paths are correct")

except FileNotFoundError:
    print("✗ FFmpeg not found!")
    print("\nTo install FFmpeg:")
    print("  • Windows: winget install ffmpeg")
    print("  • Or download from: https://ffmpeg.org/download.html")

print("\n" + "=" * 70)

# Create a version with different music volume if needed
if has_narration and has_music:
    print("\nTIP: To adjust music volume, edit the 'volume=' values in this script:")
    print("  • Narration: volume=1.0 (100%)")
    print("  • Music: volume=0.15 (15% - quiet background)")
    print("\nFor louder music, try volume=0.25")
    print("For quieter music, try volume=0.10")
