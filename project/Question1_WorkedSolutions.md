# QUESTION 1 - Worked Solutions
## Grade 12 Mathematics Exam Paper

---

## 1.1.1 Solve for x: x + x² = 0 (2 marks)

**Solution:**
```
x + x² = 0
x² + x = 0                    [Rearrange in standard form]
x(x + 1) = 0                  [Factor out x]
x = 0  or  x + 1 = 0         [Set each factor = 0]
x = 0  or  x = -1            [Solve]
```

**Answer: x = 0 or x = -1** ✓

---

## 1.1.2 Solve for x: 3x² - 5x + 1 = 0 (correct to TWO decimal places) (3 marks)

**Solution:**

Using quadratic formula: x = (-b ± √(b² - 4ac)) / 2a

Where a = 3, b = -5, c = 1

```
x = (-(-5) ± √((-5)² - 4(3)(1))) / (2×3)
x = (5 ± √(25 - 12)) / 6
x = (5 ± √13) / 6
x = (5 ± 3.6056) / 6

x = (5 + 3.6056)/6  or  x = (5 - 3.6056)/6
x = 8.6056/6        or  x = 1.3944/6
x = 1.434...        or  x = 0.232...
x = 1.43            or  x = 0.23      [Round to 2 decimal places]
```

**Answer: x = 1.43 or x = 0.23** ✓

---

## 1.1.3 Solve for x: 2x² - 7 ≤ 5x (4 marks)

**Solution:**

Step 1: Rearrange to standard form
```
2x² - 7 ≤ 5x
2x² - 5x - 7 ≤ 0
```

Step 2: Solve 2x² - 5x - 7 = 0 to find critical values

Factor:
```
2x² - 5x - 7 = 0
(2x - 7)(x + 1) = 0
2x - 7 = 0  or  x + 1 = 0
x = 7/2    or  x = -1
x = 3.5    or  x = -1
```

Step 3: Test intervals

| Interval | Test value | 2x²-5x-7 | Sign |
|----------|-----------|----------|------|
| x < -1 | x = -2 | 2(4)-5(-2)-7 = 11 | + |
| -1 < x < 3.5 | x = 0 | 0-0-7 = -7 | - |
| x > 3.5 | x = 4 | 2(16)-5(4)-7 = 5 | + |

Step 4: Choose intervals where ≤ 0 (negative or zero)

**Answer: -1 ≤ x ≤ 3.5** or **x ∈ [-1; 3.5]** ✓

---

## 1.1.4 Solve for x: 3²ˣ - 9 = 24·3ˣ + 72 (4 marks)

**Solution:**

Step 1: Simplify and substitute
```
3²ˣ - 9 = 24·3ˣ + 72
(3ˣ)² - 9 = 24·3ˣ + 72        [Note: 3²ˣ = (3ˣ)²]

Let y = 3ˣ                     [Substitution]

y² - 9 = 24y + 72
y² - 24y - 9 - 72 = 0
y² - 24y - 81 = 0
```

Step 2: Factor the quadratic
```
(y - 27)(y + 3) = 0
y = 27  or  y = -3
```

Step 3: Substitute back y = 3ˣ
```
3ˣ = 27     or    3ˣ = -3
3ˣ = 3³     or    [Reject - exponential cannot be negative]
x = 3
```

**Answer: x = 3** ✓

---

## 1.1.5 Solve for x: √(x² + 14) = 3√x (4 marks)

**Solution:**

Step 1: Square both sides
```
√(x² + 14) = 3√x
[√(x² + 14)]² = [3√x]²
x² + 14 = 9x              [Note: (3√x)² = 9x]
```

Step 2: Rearrange and solve
```
x² - 9x + 14 = 0
(x - 7)(x - 2) = 0
x = 7  or  x = 2
```

Step 3: CHECK both solutions (essential!)

**Check x = 7:**
```
LHS: √(7² + 14) = √(49 + 14) = √63 = √(9×7) = 3√7
RHS: 3√7
LHS = RHS ✓
```

**Check x = 2:**
```
LHS: √(2² + 14) = √(4 + 14) = √18 = √(9×2) = 3√2
RHS: 3√2
LHS = RHS ✓
```

Both solutions are valid.

**Answer: x = 2 or x = 7** ✓

---

## 1.2 Solve for x and y simultaneously: (5 marks)
### 5x - y = 4 and x² - x + y² = 4 - 3y

**Solution:**

Step 1: From the linear equation, express y in terms of x
```
5x - y = 4
y = 5x - 4          ...equation (*)
```

Step 2: Substitute into the second equation
```
x² - x + y² = 4 - 3y
x² - x + (5x - 4)² = 4 - 3(5x - 4)
```

Step 3: Expand the left side
```
x² - x + (25x² - 40x + 16) = 4 - 15x + 12
x² - x + 25x² - 40x + 16 = 16 - 15x
26x² - 41x + 16 = 16 - 15x
```

Step 4: Rearrange and simplify
```
26x² - 41x + 16 - 16 + 15x = 0
26x² - 26x = 0
26x(x - 1) = 0
x = 0  or  x = 1
```

Step 5: Find corresponding y values using equation (*)

**For x = 0:**
```
y = 5(0) - 4 = -4
```

**For x = 1:**
```
y = 5(1) - 4 = 1
```

Step 6: VERIFY solutions in BOTH original equations

**Solution 1: (0; -4)**
```
5x - y = 4:           5(0) - (-4) = 4 ✓
x² - x + y² = 4 - 3y: 0 - 0 + 16 = 4 - 3(-4) = 16 ✓
```

**Solution 2: (1; 1)**
```
5x - y = 4:           5(1) - 1 = 4 ✓
x² - x + y² = 4 - 3y: 1 - 1 + 1 = 4 - 3(1) = 1 ✓
```

**Answer: x = 0, y = -4 or x = 1, y = 1** ✓
Or: **(0; -4) and (1; 1)** ✓

---

## 1.3 Determine, without using a calculator, the value of k in: (3 marks)
### 4²⁴ + 8¹⁶ + 16¹² + 64⁸ = 2ᵏ

**Solution:**

Step 1: Express each term as a power of 2
```
4 = 2²    →  4²⁴ = (2²)²⁴ = 2⁴⁸
8 = 2³    →  8¹⁶ = (2³)¹⁶ = 2⁴⁸
16 = 2⁴   →  16¹² = (2⁴)¹² = 2⁴⁸
64 = 2⁶   →  64⁸ = (2⁶)⁸ = 2⁴⁸
```

Step 2: Substitute
```
4²⁴ + 8¹⁶ + 16¹² + 64⁸ = 2ᵏ
2⁴⁸ + 2⁴⁸ + 2⁴⁸ + 2⁴⁸ = 2ᵏ
```

Step 3: Add the terms
```
4 × 2⁴⁸ = 2ᵏ
```

Step 4: Express 4 as a power of 2
```
2² × 2⁴⁸ = 2ᵏ
2⁵⁰ = 2ᵏ
```

Step 5: Equate exponents
```
k = 50
```

**Answer: k = 50** ✓

---

## TOTAL: [25 marks]

### Marking Breakdown:
- 1.1.1: 2 marks
- 1.1.2: 3 marks
- 1.1.3: 4 marks
- 1.1.4: 4 marks
- 1.1.5: 4 marks
- 1.2: 5 marks
- 1.3: 3 marks
