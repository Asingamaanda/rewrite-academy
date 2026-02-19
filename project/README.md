# 📐 Grade 12 Calculus - Complete Manim Course

A structured, professional-quality educational animation series for South African Grade 12 learners rewriting matric. Built with **Manim Community Edition**.

---

## 🎯 Project Overview

This project contains **4 comprehensive lessons** covering essential Grade 12 Calculus topics:

1. **Introduction to Limits** - Understanding function behavior as x approaches a value
2. **Derivative from First Principles** - Visual proof of what derivatives really mean
3. **The Power Rule** - The most important differentiation shortcut
4. **Finding Turning Points** - Using derivatives to find maxima and minima

---

## 📁 Project Structure

```
project/
├── scenes/
│   ├── base_lesson.py             # Reusable base class with consistent styling
│   ├── limits.py                  # Scene 1: Limits
│   ├── derivative_definition.py   # Scene 2: Derivatives from first principles
│   ├── power_rule.py              # Scene 3: Power rule pattern
│   ├── turning_points.py          # Scene 4: Finding maxima/minima
│   ├── quadratic_scene.py         # (Previous parabola examples)
│   └── quantum_basics.py          # (Previous quantum physics demo)
├── calculus_main.py               # Main entry point for all calculus scenes
├── VOICEOVER_GUIDE.md             # Complete guide for adding voiceovers
└── README.md                      # This file
```

---

## 🎨 Design Philosophy

### Visual Consistency
- **BLUE** = Functions f(x)
- **YELLOW** = Derivatives f'(x) and important steps
- **RED** = Final answers and conclusions
- **GREEN** = Highlights and positive points

### Educational Focus
- Clear, large text (readable on all screens)
- 2-second pauses after major concepts
- Step-by-step progression
- No overwhelming effects
- Beginner-friendly explanations

### Target Audience
Grade 12 students rewriting matric who need:
- Deep conceptual understanding
- Visual learning support
- Slow, clear explanations
- Confidence-building content

---

## 🚀 Quick Start

### 1. Prerequisites

Ensure you have:
- Python 3.9-3.11 installed
- Virtual environment active
- Manim installed (already done in your setup)

### 2. Render a Scene

From the `class` directory (where `.venv` is located):

```powershell
# Scene 1: Limits
.venv\Scripts\manim.exe -pql project\calculus_main.py IntroductionToLimits

# Scene 2: Derivatives
.venv\Scripts\manim.exe -pql project\calculus_main.py DerivativeDefinition

# Scene 3: Power Rule
.venv\Scripts\manim.exe -pql project\calculus_main.py PowerRule

# Scene 4: Turning Points
.venv\Scripts\manim.exe -pql project\calculus_main.py TurningPoints
```

### 3. Quality Options

- `-ql` = Low quality (480p) - **Fast for testing**
- `-qm` = Medium quality (720p)
- `-qh` = High quality (1080p) - **Recommended for final**
- `-qk` = 4K quality (2160p)

Example for high quality:
```powershell
.venv\Scripts\manim.exe -pqh project\calculus_main.py IntroductionToLimits
```

Remove `-p` flag if you don't want auto-preview:
```powershell
.venv\Scripts\manim.exe -ql project\calculus_main.py PowerRule
```

---

## 🎬 Adding Voiceovers

This project includes **complete voiceover placeholders** and narration scripts.

See **[VOICEOVER_GUIDE.md](VOICEOVER_GUIDE.md)** for:
- Full narration scripts for all 4 scenes
- Step-by-step instructions using Edge-TTS (free, high quality)
- Recommended deep, soothing male voices
- Audio integration methods
- Production workflow

**Quick Voice Generation:**
```powershell
pip install edge-tts

edge-tts --voice "en-US-GuyNeural" --rate "-20%" --text "Your lesson text here" --write-media output.mp3
```

---

## 📚 Scene Details

### Scene 1: Introduction to Limits
**Duration:** ~2-3 minutes  
**Concepts:**
- Limit notation
- Indeterminate forms (0/0)
- Algebraic simplification
- Cancellation technique

**Example:** lim(x→1) of (x² - 1)/(x - 1) = 2

---

### Scene 2: Derivative from First Principles
**Duration:** ~3-4 minutes  
**Concepts:**
- Formal derivative definition
- Secant vs tangent lines
- Visual h → 0 animation
- Instantaneous rate of change

**Key Animation:** Secant line smoothly becomes tangent using `ValueTracker`

---

### Scene 3: The Power Rule
**Duration:** ~3-4 minutes  
**Concepts:**
- Pattern recognition (x¹ → 1, x² → 2x, x³ → 3x²)
- General formula: d/dx(xⁿ) = n·xⁿ⁻¹
- Worked example: 5x⁴ → 20x³

**Pedagogy:** Emphasizes the "bring down, reduce by 1" pattern

---

### Scene 4: Finding Turning Points
**Duration:** ~4-5 minutes  
**Concepts:**
- Setting f'(x) = 0
- Solving quadratic equations
- Identifying maxima vs minima
- Visual representation on cubic function

**Example:** f(x) = x³ - 6x² + 9x + 1  
**Turning points:** (1, 5) maximum, (3, 1) minimum

---

## 🛠️ Customization

### Modifying Lessons

All scenes inherit from `CalculusLesson` base class. To customize:

```python
from scenes.base_lesson import CalculusLesson

class MyCustomLesson(CalculusLesson):
    def construct(self):
        # Use helper methods
        title = self.show_title("My Lesson", "Subtitle")
        equation = self.show_equation(r"f(x) = x^2")
        self.pause_for_voiceover(3)
```

### Available Helper Methods

| Method | Purpose |
|--------|---------|
| `show_title()` | Display lesson title |
| `show_equation()` | Write mathematical equations |
| `show_explanation()` | Add explanatory text |
| `highlight_box()` | Draw attention to content |
| `pause_for_voiceover()` | Wait for narration |
| `clear_all()` | Remove all objects |

---

## 🎓 Educational Features

### Why This Approach Works

1. **Visual + Auditory Learning:** Animations + voiceover cater to multiple learning styles
2. **Slow Pacing:** 2-second pauses allow processing time
3. **Repetition:** Key concepts shown multiple ways
4. **Color Coding:** Consistent colors reduce cognitive load
5. **Step-by-Step:** No jumps in logic

### Recommended Usage

For students:
1. Watch each scene 2-3 times
2. Pause and take notes
3. Practice similar problems
4. Re-watch if concepts are unclear

For teachers:
1. Use as lesson introductions
2. Pause for class discussion
3. Assign as homework review
4. Reference specific timestamps

---

## 📊 Rendering Output

Videos are saved to:
```
media/videos/
├── limits/480p15/IntroductionToLimits.mp4
├── derivative_definition/480p15/DerivativeDefinition.mp4
├── power_rule/480p15/PowerRule.mp4
└── turning_points/480p15/TurningPoints.mp4
```

Change quality settings to get different resolutions (720p, 1080p, etc.)

---

## 🐛 Troubleshooting

### "manim not recognized"
Use full path to manim:
```powershell
.venv\Scripts\manim.exe -pql project\calculus_main.py SceneName
```

### "No module named 'scenes'"
Make sure you're running from the `class` directory, not inside `project/`

### Render is slow
Use `-ql` for testing, `-qh` only for final output

### Animation timing feels off
Adjust `run_time` and `self.wait()` values in scene files

---

## 📈 Next Steps

1. ✅ Render all 4 scenes in low quality to preview
2. ✅ Generate voiceover audio using Edge-TTS
3. ✅ Adjust timing to match audio
4. ✅ Render in high quality (-qh)
5. ✅ Combine video + audio using FFmpeg or video editor
6. ✅ Share with students!

---

## 🙏 Credits

- **Manim Community Edition** - Animation framework
- **3Blue1Brown** - Original Manim creator
- **Edge-TTS** - Free, high-quality text-to-speech

---

## 📄 License

Educational use. Free to modify and share with students.

---

## 💡 Pro Tips

1. **Batch render** all scenes overnight before exam time
2. **Upload to YouTube** with timestamps for easy navigation
3. **Create playlists** by topic
4. **Add subtitles** for accessibility
5. **Test on mobile** - ensure text is readable

---

**Made with ❤️ for Grade 12 learners. You've got this! 🎓📐**
