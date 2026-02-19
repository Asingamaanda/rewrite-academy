# Grade 12 Algebra - Complete Study Notes
## Question 1 Topics: Equations & Exponents

---

## 1.1.1 Quadratic Equations: Factorization Method

### Theory
When solving quadratic equations, always:
1. Move all terms to one side (= 0)
2. Factor if possible
3. Set each factor = 0
4. Solve for x

### Example: x + x² = 0

**Step 1:** Rearrange
```
x² + x = 0
```

**Step 2:** Factor out common term
```
x(x + 1) = 0
```

**Step 3:** Set each factor = 0
```
x = 0  OR  x + 1 = 0
x = 0  OR  x = -1
```

**Answer:** x = 0 or x = -1

### Key Point
- Always check: Does it factor easily? If yes, use factorization!

---

## 1.1.2 Quadratic Equations: Quadratic Formula

### Theory
When a quadratic equation **doesn't factor nicely**, use the quadratic formula:

**For ax² + bx + c = 0:**
```
x = (-b ± √(b² - 4ac)) / (2a)
```

### Example: 3x² - 5x + 1 = 0 (correct to 2 decimal places)

**Step 1:** Identify a, b, c
```
a = 3
b = -5
c = 1
```

**Step 2:** Calculate discriminant (b² - 4ac)
```
Δ = (-5)² - 4(3)(1)
Δ = 25 - 12
Δ = 13
```

**Step 3:** Apply formula
```
x = (-(-5) ± √13) / (2×3)
x = (5 ± √13) / 6
```

**Step 4:** Calculate both solutions
```
x = (5 + √13) / 6        OR    x = (5 - √13) / 6
x = (5 + 3.606) / 6      OR    x = (5 - 3.606) / 6
x = 8.606 / 6            OR    x = 1.394 / 6
x = 1.43                 OR    x = 0.23
```

**Answer:** x = 1.43 or x = 0.23

### Key Points
- Discriminant (Δ) tells you about solutions:
  - Δ > 0: Two real solutions
  - Δ = 0: One repeated solution
  - Δ < 0: No real solutions
- Round only at the FINAL answer, not during calculations

---

## 1.1.3 Quadratic Inequalities

### Theory
To solve ax² + bx + c ≤ 0 or ax² + bx + c ≥ 0:
1. Move all terms to one side
2. Solve the equation (replace ≤ or ≥ with =)
3. Draw a sign diagram OR use a parabola sketch
4. Choose intervals that satisfy the inequality

### Example: 2x² - 7 ≤ 5x

**Step 1:** Rearrange to standard form
```
2x² - 7 ≤ 5x
2x² - 5x - 7 ≤ 0
```

**Step 2:** Solve 2x² - 5x - 7 = 0 (find critical values)

Try factorization:
```
2x² - 5x - 7 = 0
(2x - 7)(x + 1) = 0
```

Critical values:
```
2x - 7 = 0  →  x = 7/2 = 3.5
x + 1 = 0   →  x = -1
```

**Step 3:** Draw sign diagram
```
         -           +           -
    ←-------|---------|-------→
           -1        3.5
```

Test intervals:
- x = -2: 2(-2)² - 5(-2) - 7 = 8 + 10 - 7 = 11 > 0 ✗
- x = 0: 2(0)² - 5(0) - 7 = -7 < 0 ✓
- x = 4: 2(4)² - 5(4) - 7 = 32 - 20 - 7 = 5 > 0 ✗

**Step 4:** Choose intervals where expression ≤ 0

**Answer:** -1 ≤ x ≤ 3.5 or x ∈ [-1; 3.5]

### Key Points
- For ≤ or ≥, use **closed intervals** [a; b] (include endpoints)
- For < or >, use **open intervals** (a; b) (exclude endpoints)
- Parabola opens UP if a > 0, opens DOWN if a < 0

---

## 1.1.4 Exponential Equations

### Theory
To solve exponential equations:
1. Express all terms with the **same base**
2. If bases are equal, exponents must be equal
3. Substitute if needed (let y = bˣ)

### Example: 3²ˣ - 9 = 24·3ˣ + 72

**Step 1:** Simplify 3²ˣ
```
3²ˣ = (3ˣ)²
```

**Step 2:** Make substitution: Let y = 3ˣ
```
(3ˣ)² - 9 = 24·3ˣ + 72
y² - 9 = 24y + 72
y² - 24y - 9 - 72 = 0
y² - 24y - 81 = 0
```

**Step 3:** Solve quadratic for y
```
(y - 27)(y + 3) = 0
y = 27  OR  y = -3
```

**Step 4:** Substitute back: y = 3ˣ
```
3ˣ = 27     OR    3ˣ = -3
3ˣ = 3³     OR    [No solution - exponential always positive]
x = 3
```

**Answer:** x = 3

### Key Points
- Exponential function aˣ is **always positive**, so reject negative values
- Common substitution: If you see a²ˣ and aˣ, let y = aˣ
- Remember: 9 = 3², 27 = 3³, 81 = 3⁴

---

## 1.1.5 Radical (Surd) Equations

### Theory
To solve equations with square roots:
1. Isolate the radical on one side
2. Square both sides
3. Solve the resulting equation
4. **CHECK your answers** (squaring can introduce false solutions)

### Example: √(x² + 14) = 3√x

**Step 1:** Square both sides
```
(√(x² + 14))² = (3√x)²
x² + 14 = 9x
```

**Step 2:** Rearrange and solve
```
x² - 9x + 14 = 0
(x - 7)(x - 2) = 0
x = 7  OR  x = 2
```

**Step 3:** CHECK both solutions

For x = 7:
```
LHS: √(7² + 14) = √(49 + 14) = √63 = 3√7 ✓
RHS: 3√7 ✓
```

For x = 2:
```
LHS: √(2² + 14) = √(4 + 14) = √18 = 3√2 ✓
RHS: 3√2 ✓
```

**Answer:** x = 2 or x = 7

### Key Points
- ALWAYS check answers in the original equation
- Domain restriction: √x requires x ≥ 0
- Simplify surds: √18 = √(9×2) = 3√2

---

## 1.2 Simultaneous Equations (One Linear, One Non-Linear)

### Theory
When solving one linear and one quadratic equation:
1. Use **substitution method**
2. Express one variable from the linear equation
3. Substitute into the non-linear equation
4. Solve and find both variables

### Example: 5x - y = 4 and x² - x + y² = 4 - 3y

**Step 1:** From linear equation, express y in terms of x
```
5x - y = 4
y = 5x - 4
```

**Step 2:** Substitute into second equation
```
x² - x + y² = 4 - 3y
x² - x + (5x - 4)² = 4 - 3(5x - 4)
```

**Step 3:** Expand and simplify
```
x² - x + 25x² - 40x + 16 = 4 - 15x + 12
26x² - 41x + 16 = 16 - 15x
26x² - 41x + 15x = 0
26x² - 26x = 0
26x(x - 1) = 0
```

**Step 4:** Solve for x
```
x = 0  OR  x = 1
```

**Step 5:** Find corresponding y values

For x = 0:
```
y = 5(0) - 4 = -4
```

For x = 1:
```
y = 5(1) - 4 = 1
```

**Answer:** (0; -4) or (1; 1)

### Key Points
- Always substitute back to find the second variable
- Check both solutions in BOTH original equations
- Solutions are coordinate pairs (x; y)

---

## 1.3 Exponent Laws & Simplification

### Theory - Exponent Laws
```
1. aᵐ × aⁿ = aᵐ⁺ⁿ
2. aᵐ ÷ aⁿ = aᵐ⁻ⁿ
3. (aᵐ)ⁿ = aᵐⁿ
4. (ab)ⁿ = aⁿbⁿ
5. a⁰ = 1
6. a⁻ⁿ = 1/aⁿ
```

### Express as Powers of 2
```
4 = 2²
8 = 2³
16 = 2⁴
32 = 2⁵
64 = 2⁶
```

### Example: 4²⁴ + 8¹⁶ + 16¹² + 64⁸ = 2ᵏ

**Step 1:** Convert each term to base 2
```
4²⁴ = (2²)²⁴ = 2⁴⁸
8¹⁶ = (2³)¹⁶ = 2⁴⁸
16¹² = (2⁴)¹² = 2⁴⁸
64⁸ = (2⁶)⁸ = 2⁴⁸
```

**Step 2:** Add the terms
```
2⁴⁸ + 2⁴⁸ + 2⁴⁸ + 2⁴⁸ = 4 × 2⁴⁸
```

**Step 3:** Express 4 as a power of 2
```
4 × 2⁴⁸ = 2² × 2⁴⁸ = 2⁵⁰
```

**Answer:** k = 50

### Key Points
- Always express numbers as powers of the **same base**
- When adding same powers: n·aᵐ = aˡᵒᵍₐ⁽ⁿ⁾ × aᵐ
- Simplify: 4 × 2⁴⁸ = 2² × 2⁴⁸ = 2⁵⁰

---

## Summary Table: When to Use Each Method

| Equation Type | Method | Example |
|--------------|--------|---------|
| x² + bx + c = 0 (factors nicely) | Factorization | x² + 5x + 6 = 0 |
| ax² + bx + c = 0 (doesn't factor) | Quadratic Formula | 3x² - 5x + 1 = 0 |
| ax² + bx + c ≤ 0 | Inequality (sign diagram) | 2x² - 5x - 7 ≤ 0 |
| aˣ terms | Same base, equate exponents | 3²ˣ = 27 |
| Mix of aˣ and a²ˣ | Substitution | 9ˣ - 3ˣ = 6 |
| √(...) = ... | Square both sides + check | √(x + 3) = 5 |
| One linear + one quadratic | Substitution | y = 2x; x² + y² = 5 |
| Exponent simplification | Convert to same base | 4⁸ × 8⁴ = 2ᵏ |

---

## Common Mistakes to Avoid

❌ **Don't:**
1. Divide by x without considering x = 0
2. Forget to check surd equation solutions
3. Round during calculations (only round final answer)
4. Forget domain restrictions (√x needs x ≥ 0)
5. Accept negative values for exponential equations (aˣ > 0 always)

✅ **Do:**
1. Always move all terms to one side for quadratics
2. Check critical values are included/excluded correctly in inequalities
3. Verify simultaneous equation solutions in BOTH equations
4. Show all working clearly
5. Express final answers in simplest form

---

## Practice Problems (Try These!)

1. Solve for x: 2x² + 7x - 4 = 0 (2 decimal places)
2. Solve for x: x² - 6x + 5 ≤ 0
3. Solve for x: 2ˣ⁺¹ = 8ˣ⁻¹
4. Solve for x: √(2x + 3) = x (check your answer!)
5. Find k: 27ˣ + 9ˣ = 3ᵏ

**Good luck with your studies! 📚**
