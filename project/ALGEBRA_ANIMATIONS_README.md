# Grade 12 Algebra - Manim Video Lessons  
## Question 1 Topics - Visual Explanations

---

## 📺 Available Lessons

### 1. **QuadraticFactorization** 
**Topic:** Solving x + x² = 0  
**Method:** Factorization  
**Duration:** ~40 seconds  
**Covers:**
- Rearranging to standard form
- Factoring out common terms  
- Setting each factor = 0
- Finding both solutions

**Render:**
```powershell
..\.venv\Scripts\manim.exe -pql algebra_lessons.py QuadraticFactorization
```

---

### 2. **QuadraticFormula**  
**Topic:** Solving 3x² - 5x + 1 = 0  
**Method:** Quadratic Formula  
**Duration:** ~60 seconds  
**Covers:**
- When to use the quadratic formula
- Identifying a, b, c
- Calculating discriminant
- Applying formula step-by-step
- Rounding to 2 decimal places

**Render:**
```powershell
..\.venv\Scripts\manim.exe -pql algebra_lessons.py QuadraticFormula
```

---

### 3. **QuadraticInequality**  
**Topic:** Solving 2x² - 7 ≤ 5x  
**Method:** Sign diagram on number line  
**Duration:** ~70 seconds  
**Covers:**
- Rearranging inequality
- Finding critical values
- Creating number line
- Testing intervals
- Interval notation

**Render:**
```powershell
..\.venv\Scripts\manim.exe -pql algebra_lessons.py QuadraticInequality
```

---

### 4. **ExponentialEquation**  
**Topic:** Solving 3²ˣ - 9 = 24·3ˣ + 72  
**Method:** Substitution  
**Duration:** ~65 seconds  
**Covers:**
- Recognizing (3ˣ)² pattern
- Substitution technique (y = 3ˣ)
- Solving resulting quadratic
- Rejecting negative exponential
- Equating exponents

**Render:**
```powershell
..\.venv\Scripts\manim.exe -pql algebra_lessons.py ExponentialEquation
```

---

### 5. **SurdEquation**  
**Topic:** Solving √(x² + 14) = 3√x  
**Method:** Squaring both sides + verification  
**Duration:** ~75 seconds  
**Covers:**
- Squaring both sides
- Solving resulting equation
- **CHECKING solutions** (critical!)
- Why checking is essential
- Verifying both answers

**Render:**
```powershell
..\.venv\Scripts\manim.exe -pql algebra_lessons.py SurdEquation
```

---

## 🎨 Visual Features

All lessons include:
- ✅ **Clear step-by-step progression**
- ✅ **Color-coded elements:**
  - 🔵 BLUE: Equations and functions
  - 🟡 YELLOW: Steps and highlights
  - 🔴 RED: Final answers and warnings
  - 🟢 GREEN: Correct solutions
  - 🟠 ORANGE: Warnings and important notes
- ✅ **Animated transformations** showing algebraic steps
- ✅ **Highlighted key concepts** with boxes
- ✅ **Professional math typesetting** (LaTeX)
- ✅ **Pause markers** for voiceover integration

---

## 🎬 Rendering Commands

### Render All Lessons (one by one):
```powershell
cd project
..\.venv\Scripts\manim.exe -pql algebra_lessons.py QuadraticFactorization
..\.venv\Scripts\manim.exe -pql algebra_lessons.py QuadraticFormula
..\.venv\Scripts\manim.exe -pql algebra_lessons.py QuadraticInequality
..\.venv\Scripts\manim.exe -pql algebra_lessons.py ExponentialEquation
..\.venv\Scripts\manim.exe -pql algebra_lessons.py SurdEquation
```

### Quality Options:
- `-ql` = 480p (low quality, fast render)
- `-qm` = 720p (medium quality)
- `-qh` = 1080p (high quality)
- `-qk` = 4K (highest quality, slow render)

### Other Flags:
- `-p` = Preview after rendering
- `-a` = Render all scenes in file
- `--fps 30` = 30 frames per second (smoother)

---

## 📁 Output Locations

Videos are saved to:
```
project/media/videos/algebra_lessons/480p15/
├── QuadraticFactorization.mp4
├── QuadraticFormula.mp4
├── QuadraticInequality.mp4
├── ExponentialEquation.mp4
└── SurdEquation.mp4
```

---

## 🎙️ Voiceover Integration

Each scene has **VOICEOVER comments** marking where narration should go.

Example workflow:
1. Render the video (silent)
2. Read VOICEOVER comments in the code
3. Record/generate audio for each comment
4. Use FFmpeg to combine video + audio
5. Adjust `pause_for_voiceover()` durations to match audio length

**See:** [VOICEOVER_GUIDE.md](VOICEOVER_GUIDE.md) for detailed instructions

---

## 📊 Lesson Structure

Each lesson follows this pattern:

1. **Title Screen** - Topic introduction
2. **Problem Statement** - The equation to solve
3. **Step-by-Step Solution:**
   - Step 1: Initial transformation
   - Step 2: Key algebraic move
   - Step 3: Further simplification
   - Step 4: Final solving
4. **Verification** (for surd equations)
5. **Final Answer** - Highlighted and boxed

---

## 🎯 Educational Goals

These animations are designed to:
- **Show process** not just answer
- **Build confidence** with clear steps
- **Highlight common mistakes** (e.g., rejecting negative exponentials)
- **Emphasize verification** (especially for surd equations)
- **Use consistent notation** matching Grade 12 CAPS curriculum
- **Provide visual memory aids** for exam recall

---

## 💡 Customization Tips

### Change Colors:
Edit the `AlgebraLesson` base class:
```python
COLOR_EQUATION = BLUE      # Change to your preference
COLOR_ANSWER = RED
COLOR_HIGHLIGHT = GREEN
```

### Adjust Speeds:
Modify `run_time` in animations:
```python
self.play(Write(equation), run_time=2)  # Make slower (3) or faster (1)
```

### Add Pauses:
```python
self.wait(3)  # Pause for 3 seconds
self.pause_for_voiceover(5)  # Pause for 5 seconds (marked for audio)
```

---

## ✅ Created Files

1. **[algebra_lessons.py](algebra_lessons.py)** - All 5 animated lessons
2. **[Grade12_Algebra_Notes.md](Grade12_Algebra_Notes.md)** - Written theory
3. **[Question1_WorkedSolutions.md](Question1_WorkedSolutions.md)** - Step-by-step solutions
4. **[Algebra_Formula_Sheet.md](Algebra_Formula_Sheet.md)** - Quick reference

---

## 🚀 Quick Start

1. **Test one lesson:**
   ```powershell
   cd project
   ..\.venv\Scripts\manim.exe -pql algebra_lessons.py QuadraticFactorization
   ```

2. **Open the video:**
   ```
   media\videos\algebra_lessons\480p15\QuadraticFactorization.mp4
   ```

3. **Study while watching:**
   - Read [Grade12_Algebra_Notes.md](Grade12_Algebra_Notes.md)
   - Follow along with the animation
   - Practice with similar problems

---

**Ready to learn algebra visually! 📐🎓**
