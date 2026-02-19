"""
Combine all waves physics videos into one complete lesson
Includes professional title cards and section dividers
"""

import subprocess
import os
from pathlib import Path

# Define base paths
MEDIA_DIR = Path("media/videos")
PROJECT_MEDIA_DIR = Path("project/media/videos")
OUTPUT_DIR = Path("media/videos/waves_physics/480p15")

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Define video sequence in learning order
video_sequence = [
    # Opening
    ("waves_title_cards", "WavesTitleCard.mp4"),
    
    # Introduction
    ("waves_physics", "WavesIntro.mp4"),
    
    # Section 1: Wave Types
    ("waves_title_cards", "WaveTypesSectionCard.mp4"),
    ("waves_physics", "TransverseWave.mp4"),
    ("waves_physics", "LongitudinalWave.mp4"),
    
    # Section 2: Wave Properties
    ("waves_title_cards", "WaveEquationSectionCard.mp4"),
    ("waves_physics", "WaveEquation.mp4"),
    
    # Section 3: Sound Waves
    ("waves_title_cards", "SoundSectionCard.mp4"),
    ("waves_physics", "SoundSpeed.mp4"),
    
    # Section 4: Light & Energy
    ("waves_title_cards", "LightEnergySectionCard.mp4"),
    ("waves_physics", "EMWave.mp4"),
    ("waves_physics", "PhotonEnergy.mp4"),
    
    # Summary & Closing
    ("waves_physics", "WavesSummary.mp4"),
    ("waves_title_cards", "WavesEndCard.mp4")
]

print("=" * 70)
print("WAVES PHYSICS LESSON COMBINER")
print("=" * 70)
print(f"\nCombining {len(video_sequence)} videos into complete lesson...\n")

# Locate all video files
video_files = []
missing_files = []

for folder, filename in video_sequence:
    # Try multiple locations
    possible_paths = [
        MEDIA_DIR / folder / "480p15" / filename,
        PROJECT_MEDIA_DIR / folder / "480p15" / filename
    ]
    
    found = False
    for path in possible_paths:
        if path.exists():
            video_files.append(str(path))
            print(f"✓ Found: {filename}")
            found = True
            break
    
    if not found:
        missing_files.append(filename)
        print(f"✗ Missing: {filename}")

if missing_files:
    print(f"\n❌ ERROR: {len(missing_files)} video(s) not found!")
    print("Missing files:")
    for file in missing_files:
        print(f"  - {file}")
    print("\nPlease render missing videos first.")
    exit(1)

print(f"\n✓ All {len(video_files)} videos located successfully!\n")

# Create temporary file list for FFmpeg
concat_file = OUTPUT_DIR / "concat_list.txt"
with open(concat_file, 'w') as f:
    for video_path in video_files:
        # Convert to absolute path and use forward slashes
        abs_path = Path(video_path).resolve()
        f.write(f"file '{abs_path}'\n")

print(f"Created concatenation list: {concat_file}\n")

# Output filename
output_file = OUTPUT_DIR / "Waves_Complete_Lesson.mp4"

print("Combining videos with FFmpeg...")
print(f"Output: {output_file}\n")

# FFmpeg command for concatenation
ffmpeg_cmd = [
    'ffmpeg',
    '-f', 'concat',
    '-safe', '0',
    '-i', str(concat_file),
    '-c', 'copy',  # Copy without re-encoding for speed
    '-y',  # Overwrite output file
    str(output_file)
]

try:
    result = subprocess.run(
        ffmpeg_cmd,
        check=True,
        capture_output=True,
        text=True
    )
    
    print("✅ SUCCESS! Complete lesson created!\n")
    
    # Get file size
    file_size = output_file.stat().st_size / (1024 * 1024)  # Convert to MB
    
    print("=" * 70)
    print("LESSON SUMMARY")
    print("=" * 70)
    print(f"Output File: {output_file}")
    print(f"File Size: {file_size:.2f} MB")
    print(f"Total Videos: {len(video_files)}")
    print("\nLesson Structure:")
    print("  • Opening Title Card")
    print("  • Introduction to Waves")
    print("  • Section 1: Wave Types (Transverse & Longitudinal)")
    print("  • Section 2: Wave Properties (v = fλ)")
    print("  • Section 3: Sound Waves (340 m/s)")
    print("  • Section 4: Light & Energy (EM waves, E = hf)")
    print("  • Summary & Closing Card")
    print("=" * 70)
    
    # Clean up temporary file
    concat_file.unlink()
    
except subprocess.CalledProcessError as e:
    print("❌ ERROR during video combination!")
    print(f"FFmpeg error: {e.stderr}")
    exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    exit(1)

print("\n✨ Lesson ready for viewing!")
print(f"Play: {output_file}")
