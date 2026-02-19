# Enhanced Chapter 1 Video Combiner with Title Cards
# Combines all videos with section dividers

import os
import subprocess
from pathlib import Path

# Define directories
complete_dir = Path("media/videos/chapter1_complete/480p15")
titlecards_dir = Path("media/videos/chapter1_title_cards/480p15")

# Define the full lesson structure with title cards
lesson_structure = [
    # Opening
    ("title_cards", "TitleCard.mp4"),
    
    # Section 1: Number Types
    ("title_cards", "NumberTypesSectionCard.mp4"),
    ("complete", "NaturalNumbers.mp4"),
    ("complete", "WholeNumbers.mp4"),
    ("complete", "IntegerNumbers.mp4"),
    ("complete", "RationalNumbers.mp4"),
    
    # Section 2: Calculations
    ("title_cards", "CalculationsSectionCard.mp4"),
    ("complete", "EstimatingRounding.mp4"),
    ("complete", "ColumnAddition.mp4"),
    ("complete", "ColumnMultiplication.mp4"),
    ("complete", "LongDivision.mp4"),
    
    # Section 3: Multiples and Factors
    ("title_cards", "MultiplesFactorsSectionCard.mp4"),
    ("complete", "LCMExample.mp4"),
    ("complete", "HCFExample.mp4"),
    
    # Section 4: Ratio, Rate, Proportion
    ("title_cards", "RatioRateSectionCard.mp4"),
    ("complete", "BiscuitRatio.mp4"),
    ("complete", "SpeedDistanceTime.mp4"),
    
    # Closing
    ("complete", "Chapter1Summary.mp4"),
    ("title_cards", "EndCard.mp4"),
]

# Check which videos exist and build file list
existing_videos = []
missing_videos = []

print("Checking for videos...\n")

for source, filename in lesson_structure:
    if source == "complete":
        video_path = complete_dir / filename
    else:  # title_cards
        video_path = titlecards_dir / filename
    
    if video_path.exists():
        existing_videos.append(str(video_path))
        print(f"✓ {filename}")
    else:
        missing_videos.append(filename)
        print(f"✗ MISSING: {filename}")

print(f"\nTotal videos: {len(existing_videos)}/{len(lesson_structure)}")

if missing_videos:
    print(f"\nMissing {len(missing_videos)} videos:")
    for video in missing_videos:
        print(f"  - {video}")

# Create file list for FFmpeg
if existing_videos:
    list_file_path = complete_dir / "enhanced_filelist.txt"
    
    with open(list_file_path, 'w') as f:
        for video_path in existing_videos:
            # Use absolute path and escape backslashes
            abs_path = Path(video_path).absolute()
            # FFmpeg on Windows needs forward slashes or escaped backslashes
            path_str = str(abs_path).replace('\\', '/')
            f.write(f"file '{path_str}'\n")
    
    print(f"\n✓ Created file list: {list_file_path}")
    
    # Output file
    output_file = complete_dir / "Chapter1_Enhanced_Complete_Lesson.mp4"
    
    # FFmpeg command
    ffmpeg_cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", str(list_file_path),
        "-c", "copy",
        "-y",  # Overwrite output file if it exists
        str(output_file)
    ]
    
    print(f"\nCombining {len(existing_videos)} videos into enhanced lesson...")
    print(f"Output: {output_file}\n")
    
    try:
        result = subprocess.run(ffmpeg_cmd, check=True, capture_output=True, text=True)
        print("=" * 60)
        print("✓ SUCCESS! Enhanced complete lesson created!")
        print("=" * 60)
        print(f"\nLocation: {output_file}")
        
        if output_file.exists():
            size_mb = output_file.stat().st_size / (1024 * 1024)
            print(f"Size: {size_mb:.2f} MB")
            print(f"Videos combined: {len(existing_videos)}")
            
        # Clean up the file list
        list_file_path.unlink()
        
        print("\nLesson Structure:")
        print("  1. Title Card (Introduction)")
        print("  2. Section 1: Number Types (4 videos)")
        print("  3. Section 2: Calculations (4 videos)")
        print("  4. Section 3: Multiples & Factors (2 videos)")
        print("  5. Section 4: Ratio, Rate & Proportion (2 videos)")
        print("  6. Chapter Summary")
        print("  7. End Card")
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error combining videos: {e}")
        print(f"Error output: {e.stderr}")
    except FileNotFoundError:
        print("✗ FFmpeg not found. Please install FFmpeg first.")
        print("\nInstallation options:")
        print("  • winget install ffmpeg")
        print("  • choco install ffmpeg")
        print("  • Download from: https://ffmpeg.org/download.html")
else:
    print("\n✗ No videos found to combine!")
