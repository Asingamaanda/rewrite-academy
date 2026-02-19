# CHAPTER 1 VOICEOVER - TIMING BREAKDOWN & PRODUCTION GUIDE

## FILES CREATED
1. chapter1_narration_script.py - Detailed script with recording notes
2. Chapter1_Voiceover_Script.txt - Clean reading script for voice artist

## SCENE-BY-SCENE TIMING GUIDE

| Scene # | Scene Name | Narration Duration | Video Duration | Notes |
|---------|-----------|-------------------|----------------|-------|
| 1 | Title Card | ~12 seconds | Variable | Welcome message |
| 2 | Section 1 Title | ~3 seconds | Variable | Section divider |
| 3 | Natural Numbers | ~35 seconds | ~40-45 seconds | Properties explanation |
| 4 | Whole Numbers | ~25 seconds | ~30-35 seconds | Identity element |
| 5 | Integer Numbers | ~40 seconds | ~45-50 seconds | Number line, inverses |
| 6 | Rational Numbers | ~40 seconds | ~45-50 seconds | Chocolate problem |
| 7 | Irrational Numbers | ~35 seconds | ~40-45 seconds | √2 explanation |
| 8 | Section 2 Title | ~3 seconds | Variable | Section divider |
| 9 | Estimating & Rounding | ~40 seconds | ~45-50 seconds | Chicken problem |
| 10 | Column Addition | ~45 seconds | ~50-55 seconds | Step-by-step method |
| 11 | Column Multiplication | ~40 seconds | ~45-50 seconds | Two-step process |
| 12 | Long Division | ~55 seconds | ~60-65 seconds | Multiple estimates |
| 13 | Section 3 Title | ~3 seconds | Variable | Section divider |
| 14 | LCM Example | ~35 seconds | ~35-40 seconds | Finding LCM |
| 15 | HCF Example | ~45 seconds | ~50-55 seconds | Prime factorization |
| 16 | Section 4 Title | ~3 seconds | Variable | Section divider |
| 17 | Apple Picking Rate | ~30 seconds | ~35-40 seconds | Rate problem |
| 18 | Biscuit Ratio | ~50 seconds | ~55-60 seconds | Recipe scaling |
| 19 | Speed Distance Time | ~45 seconds | ~50-55 seconds | Formula application |
| 20 | Proportion Problem | ~40 seconds | ~45-50 seconds | Combined rates |
| 21 | Chapter Summary | ~45 seconds | ~50-55 seconds | Review |
| 22 | End Card | ~20 seconds | ~25-30 seconds | Congratulations |

**TOTAL NARRATION TIME: ~9-10 minutes**
**TOTAL VIDEO TIME (with visuals): ~11-13 minutes**

## RECORDING RECOMMENDATIONS

### EQUIPMENT NEEDED
- Quality USB microphone (e.g., Blue Yeti, Audio-Technica AT2020)
- Pop filter
- Quiet recording space
- Audacity or Adobe Audition for recording/editing

### RECORDING PROCESS
1. **Warm up** - Read through script 2-3 times before recording
2. **Record in sections** - Record each scene separately for easier editing
3. **Multiple takes** - Record 2-3 takes of each section, choose the best
4. **Mark mistakes** - Clap loudly or snap fingers to mark errors for easy editing
5. **Stay hydrated** - Keep water nearby, take breaks every 15 minutes

### VOICE GUIDELINES
- **Pace**: 140-160 words per minute (natural teaching pace)
- **Tone**: Friendly teacher, not robotic or overly formal
- **Energy**: Consistent enthusiasm, increase slightly for transitions
- **Clarity**: Articulate numbers clearly (e.g., "one hundred and sixty-three")
- **Emphasis**: Stress mathematical terms and final answers

### POST-PRODUCTION CHECKLIST
□ Remove breathing, mouth clicks, background noise
□ Normalize audio levels (-3dB to -6dB peak)
□ Apply gentle compression for consistency
□ Add subtle fade in/out for each scene
□ Export as WAV (for quality) or MP3 320kbps
□ Sync with video using video editing software

## SYNCING NARRATION WITH VIDEO

### METHOD 1: Video Editing Software
1. Import Chapter1_Complete_Lesson_1080p.mp4 into editing software
2. Import all narration audio files
3. Align narration to match visual cues in each scene
4. Adjust timing if needed (speed up/slow down slightly)
5. Mix audio levels (narration primary, background music subtle)
6. Export final video with narration

### METHOD 2: Automated with FFmpeg
```bash
# Example command to add narration audio to video
ffmpeg -i Chapter1_Complete_Lesson_1080p.mp4 -i narration_audio.wav \\
  -c:v copy -c:a aac -b:a 192k -map 0:v:0 -map 1:a:0 \\
  Chapter1_Complete_With_Narration.mp4
```

## ALTERNATIVE: TEXT-TO-SPEECH GENERATION

If recording human voiceover isn't possible, you can use TTS services:

### Recommended TTS Services
1. **Google Cloud Text-to-Speech** (Natural voices, paid)
2. **Amazon Polly** (Multiple voices, paid)
3. **ElevenLabs** (Very natural, paid)
4. **Microsoft Azure TTS** (Good quality, paid)

### Free Options
- **pyttsx3** (Python library, basic quality)
- **gTTS** (Google TTS, free but limited)

Would you like me to create a script to generate TTS narration automatically?

## PRODUCTION TIMELINE

### For Human Voiceover
- Script review: 30 minutes
- Recording session: 60-90 minutes
- Editing: 120-180 minutes
- Syncing with video: 60-90 minutes
- **Total: 4-7 hours**

### For TTS Generation
- Setup: 15 minutes
- Generation: 5-10 minutes
- Quality review: 15 minutes
- Syncing: 30-60 minutes
- **Total: 1-2 hours**

## AUDIO EXPORT SETTINGS

**For professional quality:**
- Format: WAV or FLAC (lossless)
- Sample Rate: 48kHz
- Bit Depth: 24-bit
- Channels: Mono (narration) or Stereo

**For web/distribution:**
- Format: MP3
- Bitrate: 192-320 kbps
- Sample Rate: 44.1kHz or 48kHz

## FINAL VIDEO EXPORT SETTINGS (with narration)

**High Quality (YouTube, archival):**
- Resolution: 1920x1080
- Frame Rate: 60fps
- Video Codec: H.264
- Bitrate: 8-12 Mbps
- Audio Codec: AAC
- Audio Bitrate: 192-256 kbps

**Compressed (web, mobile):**
- Resolution: 1280x720
- Frame Rate: 30fps
- Video Codec: H.264
- Bitrate: 3-5 Mbps
- Audio Codec: AAC
- Audio Bitrate: 128-192 kbps
