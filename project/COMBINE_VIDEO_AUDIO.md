# Combining Video and Voiceover

## Step 1: Install FFmpeg (if not already installed)
Download from: https://ffmpeg.org/download.html
Or use: `winget install ffmpeg`

## Step 2: Combine Video + Audio

Run this command to overlay your voiceover onto the video:

```powershell
ffmpeg -i ..\media\videos\calculus_lessons\480p15\IntroductionToLimits.mp4 -i limits_voiceover.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest IntroductionToLimits_WithVoiceover.mp4
```

This will create: **IntroductionToLimits_WithVoiceover.mp4** with your deep, slow voiceover!

## Files Created:
- ✓ limits_narration.txt - Full narration script
- ✓ limits_voiceover.mp3 - AI-generated voiceover (Guy Neural voice, -20% slower)

## Audio Details:
- Voice: en-US-GuyNeural (deep, warm, professional)
- Speed: 20% slower than normal (soothing pace)
- Duration: Matches your 5-minute video timing

## Next Steps:
1. Listen to `limits_voiceover.mp3` to preview
2. If you like it, run the FFmpeg command above to combine
3. The final video will have your personalized voiceover!

## Alternative: Manual Timing
You can also manually sync the audio by:
1. Playing the MP3 alongside the video
2. Using video editing software (DaVinci Resolve, Kdenlive) for precise timing
3. Adjusting pauses in the Manim code if needed
