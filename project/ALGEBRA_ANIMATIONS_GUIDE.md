# Grade 12 Algebra - Complete Animation Suite  
## 9 Visual Lessons by Asi

---

## 📚 Overview

This collection contains **9 comprehensive animated algebra lessons** using Manim Community Edition:
- **7 Core Topics:** Covering typical Grade 12 Question 1 exam content
- **2 Bonus Techniques:** Advanced methods for deeper understanding

All animations feature:
- ✅ Color-coded steps (Blue=equations, Yellow=steps, Red=answers, Green=highlights)
- ✅ Step-by-step visual progression
- ✅ Voiceover markers for future narration
- ✅ Professional LaTeX formatting
- ✅ CAPS curriculum aligned

---

## 🎬 Core Exam Topics

### 1. QuadraticFactorization
**Problem:** x + x² = 0  
**Method:** Factorization  
**Skills:** Rearranging, factoring common terms, zero product property  
**Duration:** ~40 seconds | 38 animations

```powershell
..\.venv\Scripts\manim.exe -pql algebra_lessons.py QuadraticFactorization
```

---

### 2. QuadraticFormula
**Problem:** 3x² - 5x + 1 = 0  
**Method:** Quadratic formula application  
**Skills:** Identifying a, b, c; discriminant calculation; simplifying surds  
**Duration:** ~60 seconds | 45+ animations

```powershell
..\.venv\Scripts\manim.exe -pql algebra_lessons.py QuadraticFormula
```

---

### 3. QuadraticInequality
**Problem:** 2x² - 7 ≤ 5x  
**Method:** Sign analysis with number line  
**Skills:** Factorization, critical values, interval testing, notation  
**Duration:** ~70 seconds | 55+ animations

```powershell
..\.venv\Scripts\manim.exe -pql algebra_lessons.py QuadraticInequality
```

---

### 4. ExponentialEquation
**Problem:** 3²ˣ - 9 = 24·3ˣ + 72  
**Method:** Substitution (let y = 3ˣ)  
**Skills:** Recognizing patterns, substitution, solving auxiliary equation  
**Duration:** ~65 seconds | 50+ animations

```powershell
..\.venv\Scripts\manim.exe -pql algebra_lessons.py ExponentialEquation
```

---

### 5. SurdEquation
**Problem:** √(x² + 14) = 3√x  
**Method:** Squaring both sides with verification  
**Skills:** Domain restrictions, expanding (a+b)², checking validity  
**Duration:** ~50 seconds | 42 animations

```powershell
..\.venv\Scripts\manim.exe -pql algebra_lessons.py SurdEquation
```

---

### 6. SimultaneousEquations
**Problem:** 5x - y = 4 AND x² - x + y² = 4 - 3y  
**Method:** Substitution (linear into non-linear)  
**Skills:** Expression, substitution, expansion, finding multiple solutions  
**Duration:** ~60 seconds | 48+ animations  
**Solutions:** (0; -4) and (1; 1)

```powershell
..\.venv\Scripts\manim.exe -pql algebra_lessons.py SimultaneousEquations
```

---

### 7. ExponentLaws
**Problem:** 4²⁴ + 8¹⁶ + 16¹² + 64⁸ = 2^k, find k  
**Method:** Convert to common base  
**Skills:** Powers of 2, (aᵐ)ⁿ = aᵐⁿ, adding like terms  
**Duration:** ~55 seconds | 45+ animations  
**Answer:** k = 50

```powershell
..\.venv\Scripts\manim.exe -pql algebra_lessons.py ExponentLaws
```

---

## 🌟 Bonus Advanced Techniques

### 8. DifferenceOfSquares
**Pattern:** a² - b² = (a - b)(a + b)  
**Examples:** x² - 25 and 9x² - 16y²  
**Skills:** Pattern recognition, identifying perfect squares  
**Duration:** ~45 seconds | 35+ animations

```powershell
..\.venv\Scripts\manim.exe -pql algebra_lessons.py DifferenceOfSquares
```

---

### 9. CompletingTheSquare
**Problem:** x² + 6x + 5 = 0  
**Method:** Completing the square  
**Skills:** "Half and square" technique, perfect square trinomials  
**Duration:** ~55 seconds | 48+ animations  
**Solutions:** x = -1 or x = -5

```powershell
..\.venv\Scripts\manim.exe -pql algebra_lessons.py CompletingTheSquare
```

---

## 🚀 Quick Render Commands

### Render All Core Topics (7 scenes)
```powershell
..\.venv\Scripts\manim.exe -pql algebra_lessons.py QuadraticFactorization QuadraticFormula QuadraticInequality ExponentialEquation SurdEquation SimultaneousEquations ExponentLaws
```

### Render All Including Bonus (9 scenes)
```powershell
..\.venv\Scripts\manim.exe -pql algebra_lessons.py QuadraticFactorization QuadraticFormula QuadraticInequality ExponentialEquation SurdEquation SimultaneousEquations ExponentLaws DifferenceOfSquares CompletingTheSquare
```

### High Quality Render (1080p)
For final production videos:
```powershell
..\.venv\Scripts\manim.exe -pqh algebra_lessons.py [SceneName]
```

### Render by Category

**Quadratics focus:**
```powershell
..\.venv\Scripts\manim.exe -pql algebra_lessons.py QuadraticFactorization QuadraticFormula QuadraticInequality CompletingTheSquare
```

**Exponentials & Surds:**
```powershell
..\.venv\Scripts\manim.exe -pql algebra_lessons.py ExponentialEquation SurdEquation ExponentLaws
```

**Advanced techniques:**
```powershell
..\.venv\Scripts\manim.exe -pql algebra_lessons.py SimultaneousEquations DifferenceOfSquares CompletingTheSquare
```

---

## 📂 Output Location

Videos render to:
```
project/media/videos/algebra_lessons/480p15/[SceneName].mp4
```

For 1080p:
```
project/media/videos/algebra_lessons/1080p60/[SceneName].mp4
```

---

## 🎙️ Adding Voiceover

Each scene has `VOICEOVER:` comments throughout the code marking narration points. To add audio:

1. Extract narration text from code comments
2. Create script file (e.g., `quadratic_narration.txt`)
3. Generate audio with Edge-TTS:
   ```powershell
   ..\.venv\Scripts\python.exe -m edge_tts -t "Your narration text" -v en-US-GuyNeural --rate=-20% -f output.mp3
   ```
4. Combine with FFmpeg:
   ```powershell
   ffmpeg -i [SceneName].mp4 -i narration.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 [SceneName]_WithVoice.mp4
   ```

---

## 🎨 Customization

### Change Colors
Edit these constants in `AlgebraLesson` class:
```python
COLOR_EQUATION = BLUE
COLOR_STEP = YELLOW
COLOR_ANSWER = RED
COLOR_HIGHLIGHT = GREEN
```

### Adjust Timing
Modify `pause_for_voiceover(duration)` calls or `wait()` between animations.

### Font Sizes
```python
FONT_TITLE = 48
FONT_EQUATION = 40
FONT_STEP = 32
```

---

## 📖 Related Materials

- **Grade12_Algebra_Notes.md** - Comprehensive theory notes
- **Question1_WorkedSolutions.md** - Step-by-step exam solutions
- **Algebra_Formula_Sheet.md** - Quick reference formulas
- **VOICEOVER_GUIDE.md** - Calculus narration scripts

---

## ✅ Progress Tracker

- [x] QuadraticFactorization (rendered ✓)
- [ ] QuadraticFormula
- [ ] QuadraticInequality
- [ ] ExponentialEquation
- [ ] SurdEquation
- [ ] SimultaneousEquations
- [ ] ExponentLaws
- [ ] DifferenceOfSquares
- [ ] CompletingTheSquare

---

**Created by:** Asi  
**Framework:** Manim Community v0.19.2  
**Curriculum:** South African CAPS Grade 12  
**Total Animations:** 9 scenes, ~400+ individual animations  
**Total Duration:** ~8-9 minutes of educational content
