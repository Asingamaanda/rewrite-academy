# Grade 12 Calculus Course - Voiceover Guide

## 🎙️ Adding Deep, Slow, Soothing Voiceovers

All scenes have **VOICEOVER** comments marking where narration should be placed. Here's how to add AI-generated voice.

---

## Method 1: Using Edge-TTS (Recommended - Free & High Quality)

### Installation
```powershell
pip install edge-tts
```

### Generate Voiceover Audio

1. **List available voices** (find deep male voices):
```powershell
edge-tts --list-voices | Select-String "Male"
```

Recommended deep voices:
- `en-US-GuyNeural` (Deep, warm)
- `en-GB-RyanNeural` (British, deep)
- `en-AU-WilliamNeural` (Australian, mature)

2. **Create a text file** with your narration for each scene (e.g., `limits_narration.txt`):
```
Welcome to our lesson on limits. Today we'll explore what happens when a function approaches a specific value.
```

3. **Generate audio**:
```powershell
edge-tts --voice "en-US-GuyNeural" --rate "-20%" --file limits_narration.txt --write-media limits_audio.mp3
```

Use `--rate "-20%"` for slower speech (soothing pace).

---

## Method 2: Using gTTS (Simple but Basic Quality)

### Installation
```powershell
pip install gtts
```

### Generate Audio
```python
from gtts import gTTS

text = "Welcome to our lesson on limits..."
tts = gTTS(text=text, lang='en', slow=True)
tts.save("voiceover.mp3")
```

---

## Method 3: Using Piper TTS (High Quality Offline)

### Installation
```powershell
pip install piper-tts
```

Download a deep male voice model and generate audio locally.

---

## Adding Voiceover to Manim Animations

### Option A: Manual Sync (Simple)
1. Generate all voiceover audio files
2. Play them alongside the video
3. Adjust `self.wait()` durations in code to match audio length

### Option B: Integrated Audio (Advanced)

Modify your scene to include audio:

```python
from manim import *
from manim.utils.sounds import add_sound

class IntroductionToLimits(CalculusLesson):
    def construct(self):
        # Add background audio
        self.add_sound("voiceovers/limits_intro.mp3")
        
        # Your existing code...
        title = self.show_title("Introduction to Limits")
        self.wait(3)  # Match audio duration
```

### Option C: Voiceover Plugin (Best for Long Projects)

Install Manim Voiceover:
```powershell
pip install manim-voiceover
pip install edge-tts
```

Update your scene:
```python
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.edge import EdgeService

class IntroductionToLimits(VoiceoverScene):
    def construct(self):
        # Set voice service
        self.set_speech_service(
            EdgeService(voice="en-US-GuyNeural", rate="-20%")
        )
        
        # Add voiceover inline
        with self.voiceover(text="Welcome to our lesson on limits.") as tracker:
            title = Text("Introduction to Limits")
            self.play(Write(title))
            self.wait(tracker.duration)
```

---

## 📝 Scene-by-Scene Narration Scripts

### Scene 1: Limits (limits_narration.txt)

```
Welcome to our lesson on limits. Today we'll explore what happens when a function approaches a specific value.

Let's examine the function f of x equals x squared minus 1, divided by x minus 1.

What happens when x approaches 1? Let's investigate.

If we substitute x equals 1 directly, we get 0 over 0, which is undefined. So we need a different approach.

The solution is to factor the numerator and simplify.

Notice that x minus 1 appears in both the numerator and denominator.

We can cancel these terms, as long as x is not equal to 1.

After cancellation, we're left with simply x plus 1.

Now we can safely substitute x equals 1.

Therefore, the limit as x approaches 1 is equal to 2.

This is the fundamental concept of limits. We found the value the function approaches, even though it's undefined at that exact point.

Understanding limits is essential for calculus. Take your time to practice similar problems.
```

### Scene 2: Derivatives (derivative_narration.txt)

```
In this lesson, we'll discover what a derivative truly means, starting from first principles.

The derivative measures how fast a function is changing. Let's see the formal definition.

This formula finds the slope of the tangent line at any point. Let's visualize what this means.

Let's use a simple parabola, f of x equals x squared, to see this in action.

We'll choose a point on the curve. Let's use x equals 2.

Now, we pick another point, a distance h away. This gives us x plus h.

The line connecting these two points is called a secant line.

The slope of this secant line is f of x plus h, minus f of x, all divided by h.

Now watch carefully. As h gets smaller and smaller, approaching zero, the secant line becomes the tangent line.

This tangent line's slope is the derivative at x equals 2.

The slope of the tangent line at x equals 2 is exactly 4. This is the derivative at that point.

Let's review the concept one more time.

h represents a small change in x.

As h approaches zero, the secant becomes tangent.

The derivative is the slope of the tangent.

It measures instantaneous rate of change.

This is the foundation of differential calculus. Practice visualizing this process with different functions.
```

### Scene 3: Power Rule (power_rule_narration.txt)

```
Now that we understand what derivatives mean, let's learn a powerful shortcut: the power rule.

The power rule is one of the most useful tools in calculus. Let's discover the pattern.

Let's see this pattern in action with specific examples.

Example 1: x to the power of 1.

Bring down the exponent 1, then reduce the power by 1. This gives us 1 times x to the power of 0, which equals 1.

Example 2: x squared.

Bring down 2, reduce the power by 1. We get 2x to the power of 1, which is simply 2x.

Example 3: x cubed.

Following the pattern: bring down 3, reduce the power. This gives us 3x squared.

Do you see the pattern? The exponent becomes the coefficient, and the new exponent is one less.

Let's try a more complex example to solidify your understanding.

For f of x equals 5x to the fourth, we apply the power rule.

Step 1: Multiply by the exponent, which is 4.

Step 2: Reduce the exponent by 1.

Step 3: Simplify.

Therefore, the derivative of 5x to the fourth is 20x cubed.

The power rule works for any real number exponent, making it incredibly powerful and efficient.

Practice this rule until it becomes second nature. It's the backbone of differentiation.
```

### Scene 4: Turning Points (turning_points_narration.txt)

```
In this final lesson, we'll discover how derivatives help us find the peaks and valleys of a function: the turning points.

A turning point occurs where the tangent line is horizontal. This means the derivative equals zero.

Let's work through a complete example. Consider the cubic function f of x equals x cubed minus 6x squared plus 9x plus 1.

Let's first see what this function looks like.

Notice the curve has a maximum point and a minimum point. Let's find them mathematically.

Step 1: Find the derivative using the power rule.

Step 2: Set the derivative equal to zero and solve for x.

We can factor out 3 to simplify.

Now factor the quadratic expression.

Therefore, x equals 1 or x equals 3.

These x-values are where our turning points occur. Let's mark them on the graph.

At x equals 1, we have a maximum with a value of 5. At x equals 3, we have a minimum with a value of 1.

Notice the tangent lines are perfectly horizontal at these points, confirming that the slope, or derivative, is zero.

Let's summarize the complete process for finding turning points.

Step 1: Find the derivative f prime of x.

Step 2: Set f prime of x equals zero and solve for x.

Step 3: Substitute x-values into f of x to find y-coordinates.

Step 4: Identify maximum versus minimum.

Follow these four steps, and you'll be able to find any turning point. This skill is essential for optimization problems in calculus.

With practice, finding turning points will become second nature. Keep working through problems, and you'll master this concept.

Congratulations! You've learned the fundamental concepts of calculus. Practice these techniques regularly, and you'll excel in your exams. Good luck!
```

---

## 🎬 Production Workflow

1. **Generate all audio files** first using Edge-TTS:
```powershell
edge-tts --voice "en-US-GuyNeural" --rate "-20%" --text "Your narration here" --write-media output.mp3
```

2. **Test timing** by playing audio while watching the silent animation

3. **Adjust `self.wait()` durations** in the Python code to match

4. **Final render** with proper timing

5. **Combine** video and audio in post-production using:
   - DaVinci Resolve (free)
   - FFmpeg (command line)
   - Adobe Premiere
   - Kdenlive (free)

### FFmpeg Audio Overlay Example:
```powershell
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4
```

---

## 🎯 Tips for Professional Voiceover

1. **Pace**: Use `-20%` to `-30%` rate reduction for learning content
2. **Pauses**: Add natural pauses in narration script using `...` or line breaks
3. **Emphasis**: Use CAPITAL LETTERS for words to emphasize (Edge-TTS respects this)
4. **Multiple takes**: Generate several versions and pick the best
5. **Background music**: Add soft, non-distracting music at 10-20% volume

---

## 🔊 Recommended Voice Settings

**Edge-TTS Best Voices for Education:**
- `en-US-GuyNeural` - Deep, authoritative, American
- `en-GB-RyanNeural` - Deep, clear, British
- `en-US-DavisNeural` - Warm, friendly, conversational

**Optimal Rate:** `-20%` (clear and digestible)

**Sample Command:**
```powershell
edge-tts --voice "en-US-GuyNeural" --rate "-20%" --pitch "-5Hz" --text "Your lesson text" --write-media lesson.mp3
```

---

## ✅ Quick Start

1. Install Edge-TTS:
```powershell
pip install edge-tts
```

2. Create narration file (e.g., `lesson1.txt`)

3. Generate audio:
```powershell
edge-tts --voice "en-US-GuyNeural" --rate "-20%" --file lesson1.txt --write-media lesson1.mp3
```

4. Play alongside your Manim animation!

---

Good luck with your Grade 12 Calculus course! 🎓📐
