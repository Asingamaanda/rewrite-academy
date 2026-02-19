# Render all Chapter 1 scenes at high quality (1080p60) and combine them
# This creates a complete, detailed, professional-quality lesson video

import subprocess
from pathlib import Path
import time

# Python executable path
python_exe = "C:/Users/NefefLocal/Documents/class/.venv/Scripts/python.exe"

# All scenes in order with their files
scenes_to_render = [
    # Title cards
    ("project/chapter1_title_cards.py", "TitleCard"),
    
    # Section 1: Number Types
    ("project/chapter1_title_cards.py", "NumberTypesSectionCard"),
    ("project/chapter1_complete.py", "NaturalNumbers"),
    ("project/chapter1_complete.py", "WholeNumbers"),
    ("project/chapter1_complete.py", "IntegerNumbers"),
    ("project/chapter1_complete.py", "RationalNumbers"),
    ("project/chapter1_complete.py", "IrrationalNumbers"),
    
    # Section 2: Calculations
    ("project/chapter1_title_cards.py", "CalculationsSectionCard"),
    ("project/chapter1_complete.py", "EstimatingRounding"),
    ("project/chapter1_complete.py", "RoundingPractice"),
    ("project/chapter1_complete.py", "Compensating"),
    ("project/chapter1_complete.py", "ColumnAddition"),
    ("project/chapter1_complete.py", "ColumnMultiplication"),
    ("project/chapter1_complete.py", "LongDivision"),
    
    # Section 3: Multiples and Factors
    ("project/chapter1_title_cards.py", "MultiplesFactorsSectionCard"),
    ("project/chapter1_complete.py", "LCMExample"),
    ("project/chapter1_complete.py", "HCFExample"),
    
    # Section 4: Ratio, Rate, Proportion
    ("project/chapter1_title_cards.py", "RatioRateSectionCard"),
    ("project/chapter1_complete.py", "ApplePickingRate"),
    ("project/chapter1_complete.py", "BiscuitRatio"),
    ("project/chapter1_complete.py", "SpeedDistanceTime"),
    ("project/chapter1_complete.py", "ProportionProblem"),
    
    # Summary and End
    ("project/chapter1_complete.py", "Chapter1Summary"),
    ("project/chapter1_title_cards.py", "EndCard"),
]

print("=" * 70)
print("CHAPTER 1 - HIGH QUALITY (1080p60) RENDERING")
print("=" * 70)
print(f"\nTotal scenes to render: {len(scenes_to_render)}")
print("\nThis will take some time. Please be patient...\n")

start_time = time.time()
successful_renders = []
failed_renders = []

for idx, (file_path, scene_name) in enumerate(scenes_to_render, 1):
    print(f"\n[{idx}/{len(scenes_to_render)}] Rendering: {scene_name}")
    print("-" * 70)
    
    cmd = [
        python_exe,
        "-m", "manim",
        "-qh",  # High quality: 1080p60
        "--disable_caching",
        file_path,
        scene_name
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✓ SUCCESS: {scene_name}")
            successful_renders.append((file_path, scene_name))
        else:
            print(f"✗ FAILED: {scene_name}")
            print(f"Error: {result.stderr[:200]}")
            failed_renders.append((file_path, scene_name))
    
    except subprocess.TimeoutExpired:
        print(f"✗ TIMEOUT: {scene_name} (took longer than 5 minutes)")
        failed_renders.append((file_path, scene_name))
    except Exception as e:
        print(f"✗ ERROR: {scene_name} - {str(e)}")
        failed_renders.append((file_path, scene_name))

elapsed_time = time.time() - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)

print("\n" + "=" * 70)
print("RENDERING COMPLETE")
print("=" * 70)
print(f"Success: {len(successful_renders)}/{len(scenes_to_render)}")
print(f"Failed: {len(failed_renders)}")
print(f"Time taken: {minutes}m {seconds}s")

if failed_renders:
    print("\nFailed renders:")
    for file_path, scene in failed_renders:
        print(f"  - {scene}")

print("\n" + "=" * 70)
print("COMBINING VIDEOS")
print("=" * 70)

# Now combine all the high-quality videos
video_dirs = [
    Path("media/videos/chapter1_complete/1080p60"),
    Path("media/videos/chapter1_title_cards/1080p60")
]

# Build list of video files in order
video_files = []
for file_path, scene_name in scenes_to_render:
    if "title_cards" in file_path:
        video_path = Path("media/videos/chapter1_title_cards/1080p60") / f"{scene_name}.mp4"
    else:
        video_path = Path("media/videos/chapter1_complete/1080p60") / f"{scene_name}.mp4"
    
    if video_path.exists():
        video_files.append(video_path)
        print(f"✓ Found: {scene_name}.mp4")
    else:
        print(f"✗ Missing: {scene_name}.mp4")

print(f"\nTotal videos for combination: {len(video_files)}")

if video_files:
    # Create file list
    output_dir = Path("media/videos/chapter1_complete/1080p60")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    list_file = output_dir / "hq_filelist.txt"
    with open(list_file, 'w') as f:
        for video_path in video_files:
            abs_path = video_path.absolute()
            path_str = str(abs_path).replace('\\', '/')
            f.write(f"file '{path_str}'\n")
    
    # Output file
    output_file = output_dir / "Chapter1_Complete_Lesson_1080p.mp4"
    
    # FFmpeg command for high quality combination
    ffmpeg_cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", str(list_file),
        "-c:v", "libx264",  # Re-encode for better compatibility
        "-preset", "medium",
        "-crf", "18",  # High quality (lower = better, 18 is visually lossless)
        "-c:a", "aac",
        "-b:a", "192k",
        "-y",
        str(output_file)
    ]
    
    print(f"\nCombining videos into: {output_file.name}")
    print("This may take a few minutes...\n")
    
    try:
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and output_file.exists():
            size_mb = output_file.stat().st_size / (1024 * 1024)
            
            print("=" * 70)
            print("✓ SUCCESS! COMPLETE HIGH-QUALITY LESSON CREATED!")
            print("=" * 70)
            print(f"\nFile: {output_file}")
            print(f"Size: {size_mb:.2f} MB")
            print(f"Quality: 1080p60 (Full HD)")
            print(f"Scenes: {len(video_files)}")
            
            # Clean up
            list_file.unlink()
            
            print("\nLesson includes:")
            print("  • Opening title card")
            print("  • 4 section dividers")
            print("  • All number types (Natural, Whole, Integer, Rational, Irrational)")
            print("  • All calculation methods (Estimation, Addition, Multiplication, Division)")
            print("  • Multiples and Factors (LCM, HCF)")
            print("  • Ratio, Rate, and Proportion problems")
            print("  • Complete chapter summary")
            print("  • Closing end card")
            
        else:
            print(f"✗ Error combining videos")
            print(f"FFmpeg output: {result.stderr[:500]}")
    
    except FileNotFoundError:
        print("✗ FFmpeg not found. Please install FFmpeg.")
    except Exception as e:
        print(f"✗ Error: {e}")
else:
    print("\n✗ No videos found to combine!")

total_time = time.time() - start_time
total_minutes = int(total_time // 60)
total_seconds = int(total_time % 60)

print(f"\nTotal time: {total_minutes}m {total_seconds}s")
print("=" * 70)
