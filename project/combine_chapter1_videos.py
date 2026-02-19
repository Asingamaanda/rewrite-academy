# Chapter 1 Video Combiner Script
# This script combines all rendered Chapter 1 videos into one complete lesson

import os
import subprocess
from pathlib import Path

# Define the directory where videos are stored
video_dir = Path("media/videos/chapter1_complete/480p15")

# Define the order of videos for the complete lesson
video_order = [
    "NaturalNumbers.mp4",
    "WholeNumbers.mp4",
    "IntegerNumbers.mp4",
    "RationalNumbers.mp4",
    "EstimatingRounding.mp4",
    "ColumnAddition.mp4",
    "ColumnMultiplication.mp4",
    "LongDivision.mp4",
    "LCMExample.mp4",
    "HCFExample.mp4",
    "BiscuitRatio.mp4",
    "SpeedDistanceTime.mp4",
    "Chapter1Summary.mp4"
]

# Check which videos exist
existing_videos = []
for video in video_order:
    video_path = video_dir / video
    if video_path.exists():
        existing_videos.append(video)
        print(f"✓ Found: {video}")
    else:
        print(f"✗ Missing: {video}")

print(f"\nTotal videos found: {len(existing_videos)}/{len(video_order)}")

# Create a file list for FFmpeg
if existing_videos:
    list_file_path = video_dir / "filelist.txt"
    with open(list_file_path, 'w') as f:
        for video in existing_videos:
            # FFmpeg requires the format: file 'filename.mp4'
            f.write(f"file '{video}'\n")
    
    print(f"\n✓ Created file list: {list_file_path}")
    
    # Output file
    output_file = video_dir / "Chapter1_Complete_Lesson.mp4"
    
    # FFmpeg command to concatenate videos
    ffmpeg_cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", str(list_file_path),
        "-c", "copy",
        str(output_file)
    ]
    
    print(f"\nCombining videos into: {output_file}")
    print("This may take a moment...\n")
    
    try:
        result = subprocess.run(ffmpeg_cmd, check=True, capture_output=True, text=True)
        print(f"✓ SUCCESS! Complete lesson created at:")
        print(f"  {output_file}")
        
        # Get file size
        if output_file.exists():
            size_mb = output_file.stat().st_size / (1024 * 1024)
            print(f"\nFile size: {size_mb:.2f} MB")
            
        # Clean up the file list
        list_file_path.unlink()
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error combining videos: {e}")
        print(f"Error output: {e.stderr}")
    except FileNotFoundError:
        print("✗ FFmpeg not found. Please install FFmpeg first.")
        print("\nTo install FFmpeg:")
        print("  1. Download from: https://ffmpeg.org/download.html")
        print("  2. Or use: winget install ffmpeg")
        print("  3. Or use: choco install ffmpeg")
else:
    print("\n✗ No videos found to combine!")
