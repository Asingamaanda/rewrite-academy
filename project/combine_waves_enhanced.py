"""
Combine waves physics videos with ENHANCED structure
- Clear topic signaling with section cards
- Learning objectives before each section
- Transition cards between related topics
- "Did You Know?" and "Key Concept" cards
- Detailed subtopic numbering (1.1, 1.2, 4.1, 4.2)
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

# ENHANCED video sequence with detailed structure
video_sequence = [
    # ===== OPENING =====
    ("waves_title_cards_enhanced", "WavesTitleCard.mp4"),
    
    # ===== INTRODUCTION =====
    ("waves_physics", "WavesIntro.mp4"),
    
    # ===== SECTION 1: TYPES OF WAVES =====
    ("waves_title_cards_enhanced", "WaveTypesSectionCard.mp4"),  # Objectives + Topics 1.1, 1.2
    
    # Topic 1.1: Transverse Waves
    ("waves_physics", "TransverseWave.mp4"),
    
    # Clear transition signal
    ("waves_title_cards_enhanced", "TransitionToLongitudinal.mp4"),
    
    # Topic 1.2: Longitudinal Waves
    ("waves_physics", "LongitudinalWave.mp4"),
    
    # ===== SECTION 2: WAVE PROPERTIES =====
    ("waves_title_cards_enhanced", "KeyConceptWaveEquation.mp4"),  # Key concept highlight
    ("waves_title_cards_enhanced", "WaveEquationSectionCard.mp4"),  # Detailed equation breakdown
    ("waves_physics", "WaveEquation.mp4"),
    
    # ===== SECTION 3: SOUND WAVES =====
    ("waves_title_cards_enhanced", "DidYouKnowSound.mp4"),  # Fun fact
    ("waves_title_cards_enhanced", "SoundSectionCard.mp4"),  # Topic 3.1 with characteristics
    ("waves_physics", "SoundSpeed.mp4"),
    
    # ===== SECTION 4: LIGHT & ENERGY =====
    ("waves_title_cards_enhanced", "TransitionToLight.mp4"),  # Compare sound vs light
    ("waves_title_cards_enhanced", "LightEnergySectionCard.mp4"),  # Topics 4.1, 4.2
    
    # Topic 4.1: Electromagnetic Waves
    ("waves_physics", "EMWave.mp4"),
    
    # Topic 4.2: Photon Energy
    ("waves_physics", "PhotonEnergy.mp4"),
    
    # ===== SUMMARY & CLOSING =====
    ("waves_physics", "WavesSummary.mp4"),
    ("waves_title_cards_enhanced", "WavesEndCard.mp4")
]

print("=" * 80)
print("ENHANCED WAVES PHYSICS LESSON COMBINER")
print("Structured Learning with Clear Topic Signals")
print("=" * 80)
print(f"\nCombining {len(video_sequence)} videos into enhanced lesson...\n")

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
concat_file = OUTPUT_DIR / "concat_list_enhanced.txt"
with open(concat_file, 'w') as f:
    for video_path in video_files:
        # Convert to absolute path and use forward slashes
        abs_path = Path(video_path).resolve()
        f.write(f"file '{abs_path}'\n")

print(f"Created concatenation list: {concat_file}\n")

# Output filename
output_file = OUTPUT_DIR / "Waves_Complete_Lesson_Enhanced.mp4"

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
    
    print("✅ SUCCESS! Enhanced lesson created!\n")
    
    # Get file size
    file_size = output_file.stat().st_size / (1024 * 1024)  # Convert to MB
    
    print("=" * 80)
    print("ENHANCED LESSON SUMMARY")
    print("=" * 80)
    print(f"Output File: {output_file}")
    print(f"File Size: {file_size:.2f} MB")
    print(f"Total Videos: {len(video_files)}")
    print("\nEnhanced Lesson Structure:")
    print("\n  📖 OPENING")
    print("     • Professional title card")
    print("     • Introduction to waves")
    print("\n  📚 SECTION 1: Types of Waves")
    print("     • Learning objectives card")
    print("     • Topic 1.1: Transverse Waves")
    print("     • Transition card (⊥ to ∥)")
    print("     • Topic 1.2: Longitudinal Waves")
    print("\n  🔢 SECTION 2: Wave Properties & Mathematics")
    print("     • 'Key Concept' highlight")
    print("     • Detailed equation breakdown (v, f, λ)")
    print("     • Wave equation demonstration")
    print("\n  🔊 SECTION 3: Sound Waves")
    print("     • 'Did You Know?' fun fact")
    print("     • Comprehensive characteristics")
    print("     • Topic 3.1: Echo & speed calculation")
    print("\n  💡 SECTION 4: Light & Electromagnetic Energy")
    print("     • Transition card (Sound vs Light)")
    print("     • Topic 4.1: Electromagnetic waves (c = 3×10⁸ m/s)")
    print("     • Topic 4.2: Quantum energy (E = hf)")
    print("\n  🎯 CLOSING")
    print("     • Summary of all concepts")
    print("     • End card with key takeaways")
    print("\n" + "=" * 80)
    print("\n✨ Features of Enhanced Lesson:")
    print("  ✓ Clear learning objectives before each section")
    print("  ✓ Numbered subtopics (1.1, 1.2, 3.1, 4.1, 4.2)")
    print("  ✓ Smooth transitions between topics")
    print("  ✓ 'Key Concept' and 'Did You Know?' cards")
    print("  ✓ Detailed variable explanations")
    print("  ✓ Visual comparison cards")
    print("=" * 80)
    
    # Clean up temporary file
    concat_file.unlink()
    
except subprocess.CalledProcessError as e:
    print("❌ ERROR during video combination!")
    print(f"FFmpeg error: {e.stderr}")
    exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    exit(1)

print("\n✨ Enhanced lesson ready for viewing!")
print(f"Play: {output_file}")
