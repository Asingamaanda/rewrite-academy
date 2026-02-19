from manim import *

# ============================================
# SECTION 1: DIFFERENT TYPES OF NUMBERS
# ============================================

class NaturalNumbers(Scene):
    """Natural numbers introduction and properties"""
    def construct(self):
        title = Text("Natural Numbers", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # Definition
        definition = Text("Numbers used for counting", font_size=32, color=YELLOW)
        definition.next_to(title, DOWN, buff=0.5)
        self.play(Write(definition))
        self.wait()
        
        # Show natural numbers
        numbers = VGroup(*[
            Text(str(i), font_size=36) for i in range(1, 15)
        ]).arrange(RIGHT, buff=0.4)
        numbers.next_to(definition, DOWN, buff=0.7)
        
        for num in numbers:
            self.play(FadeIn(num), run_time=0.2)
        self.wait()
        
        dots = Text("...", font_size=36)
        dots.next_to(numbers, RIGHT, buff=0.2)
        self.play(Write(dots))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in [definition, numbers, dots]])
        
        # Properties - Closed under addition
        prop1_title = Text("Property 1: Closed under Addition", font_size=32, color=YELLOW)
        prop1_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(prop1_title))
        
        example1 = MathTex("7 + 9 = 16", font_size=40, color=GREEN)
        example2 = MathTex("25 + 33 = 58", font_size=40, color=GREEN)
        example1.next_to(prop1_title, DOWN, buff=0.5)
        example2.next_to(example1, DOWN, buff=0.3)
        
        self.play(Write(example1))
        self.wait()
        self.play(Write(example2))
        
        check1 = Text("✓ Still natural numbers!", font_size=28, color=GREEN)
        check1.next_to(example2, DOWN, buff=0.5)
        self.play(Write(check1))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in [prop1_title, example1, example2, check1]])
        
        # Properties - Closed under multiplication
        prop2_title = Text("Property 2: Closed under Multiplication", font_size=32, color=YELLOW)
        prop2_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(prop2_title))
        
        mult1 = MathTex("6 \\times 8 = 48", font_size=40, color=GREEN)
        mult2 = MathTex("12 \\times 15 = 180", font_size=40, color=GREEN)
        mult1.next_to(prop2_title, DOWN, buff=0.5)
        mult2.next_to(mult1, DOWN, buff=0.3)
        
        self.play(Write(mult1))
        self.wait()
        self.play(Write(mult2))
        
        check2 = Text("✓ Still natural numbers!", font_size=28, color=GREEN)
        check2.next_to(mult2, DOWN, buff=0.5)
        self.play(Write(check2))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in [prop2_title, mult1, mult2, check2]])
        
        # NOT closed under subtraction
        prop3_title = Text("NOT Closed under Subtraction", font_size=32, color=RED)
        prop3_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(prop3_title))
        
        sub_prob = MathTex("5 - 20 = ?", font_size=40)
        sub_prob.next_to(prop3_title, DOWN, buff=0.5)
        self.play(Write(sub_prob))
        self.wait()
        
        cross = Text("✗ Not a natural number!", font_size=28, color=RED)
        cross.next_to(sub_prob, DOWN, buff=0.5)
        self.play(Write(cross))
        self.wait(2)


class WholeNumbers(Scene):
    """Whole numbers = Natural numbers + 0"""
    def construct(self):
        title = Text("Whole Numbers", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        definition = Text("Natural Numbers + 0", font_size=32, color=YELLOW)
        definition.next_to(title, DOWN, buff=0.5)
        self.play(Write(definition))
        self.wait()
        
        # Show whole numbers
        whole_nums = VGroup(*[
            Text(str(i), font_size=36) for i in range(0, 13)
        ]).arrange(RIGHT, buff=0.4)
        whole_nums.next_to(definition, DOWN, buff=0.7)
        
        # Highlight 0
        whole_nums[0].set_color(YELLOW)
        
        for num in whole_nums:
            self.play(FadeIn(num), run_time=0.2)
        
        dots = Text("...", font_size=36)
        dots.next_to(whole_nums, RIGHT, buff=0.2)
        self.play(Write(dots))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in [definition, whole_nums, dots]])
        
        # Identity element for addition
        identity_title = Text("0 is the Identity Element for Addition", font_size=30, color=YELLOW)
        identity_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(identity_title))
        
        examples = VGroup(
            MathTex("24 + 0 = 24", font_size=36),
            MathTex("157 + 0 = 157", font_size=36),
            MathTex("0 + 89 = 89", font_size=36)
        ).arrange(DOWN, buff=0.4)
        examples.next_to(identity_title, DOWN, buff=0.6)
        
        for ex in examples:
            self.play(Write(ex), run_time=0.8)
        self.wait(2)
        
        note = Text("Adding 0 doesn't change the number!", font_size=26, color=GREEN)
        note.next_to(examples, DOWN, buff=0.6)
        self.play(Write(note))
        self.wait(2)


class IntegerNumbers(Scene):
    """Integer numbers - extending to negatives"""
    def construct(self):
        title = Text("Integers", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        definition = Text("Whole Numbers + Negative Numbers", font_size=32, color=YELLOW)
        definition.next_to(title, DOWN, buff=0.5)
        self.play(Write(definition))
        self.wait()
        
        # Number line showing integers
        number_line = NumberLine(
            x_range=[-6, 6, 1],
            length=11,
            include_numbers=True,
            include_tip=True,
            tip_width=0.2,
            tip_height=0.2
        )
        number_line.shift(DOWN * 0.5)
        self.play(Create(number_line))
        self.wait(2)
        
        # Show extension in both directions
        left_arrow = Arrow(start=LEFT*2, end=LEFT*3, color=YELLOW)
        right_arrow = Arrow(start=RIGHT*2, end=RIGHT*3, color=YELLOW)
        left_arrow.next_to(number_line, LEFT)
        right_arrow.next_to(number_line, RIGHT)
        
        left_text = Text("...", font_size=36).next_to(left_arrow, LEFT)
        right_text = Text("...", font_size=36).next_to(right_arrow, RIGHT)
        
        self.play(GrowArrow(left_arrow), GrowArrow(right_arrow))
        self.play(Write(left_text), Write(right_text))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in [number_line, left_arrow, right_arrow, 
                                              left_text, right_text, definition]])
        
        # Subtraction now works
        sub_title = Text("Now subtraction always works!", font_size=32, color=GREEN)
        sub_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(sub_title))
        
        examples = VGroup(
            MathTex("5 - 8 = -3", font_size=40),
            MathTex("100 - 165 = -65", font_size=40),
            MathTex("300 - 700 = -400", font_size=40)
        ).arrange(DOWN, buff=0.4)
        examples.next_to(sub_title, DOWN, buff=0.6)
        
        for ex in examples:
            self.play(Write(ex), run_time=0.8)
        self.wait(2)
        
        # Additive inverses
        self.play(*[FadeOut(mob) for mob in [sub_title, examples]])
        
        inverse_title = Text("Additive Inverses", font_size=32, color=YELLOW)
        inverse_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(inverse_title))
        
        inv_examples = VGroup(
            MathTex("20 + (-20) = 0", font_size=40),
            MathTex("135 + (-135) = 0", font_size=40),
            MathTex("-47 + 47 = 0", font_size=40)
        ).arrange(DOWN, buff=0.4)
        inv_examples.next_to(inverse_title, DOWN, buff=0.6)
        
        for ex in inv_examples:
            self.play(Write(ex), run_time=0.8)
        self.wait(2)


class RationalNumbers(Scene):
    """Rational numbers - fractions"""
    def construct(self):
        title = Text("Rational Numbers", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # Chocolate sharing problem
        problem = Text("5 people share 12 chocolate slabs equally", font_size=30, color=YELLOW)
        problem.next_to(title, DOWN, buff=0.5)
        self.play(Write(problem))
        self.wait()
        
        # Visual representation
        chocolates = VGroup(*[
            Rectangle(width=0.6, height=0.4, color=ORANGE, fill_opacity=0.7, 
                     stroke_color=WHITE)
            for _ in range(12)
        ]).arrange_in_grid(rows=2, cols=6, buff=0.2)
        chocolates.shift(DOWN * 0.5)
        
        for choc in chocolates:
            self.play(FadeIn(choc), run_time=0.15)
        self.wait()
        
        # Division
        division = MathTex("12 \\div 5 = ?", font_size=36)
        division.next_to(chocolates, DOWN, buff=0.6)
        self.play(Write(division))
        self.wait()
        
        # Answer
        answer = MathTex("= \\frac{12}{5} = 2.4 = 2\\frac{2}{5}", font_size=40, color=GREEN)
        answer.next_to(division, DOWN, buff=0.4)
        self.play(Write(answer))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in [problem, chocolates, division, answer]])
        
        # Definition
        definition = Text("Rational = Can be written as fraction", font_size=30, color=YELLOW)
        definition.next_to(title, DOWN, buff=0.5)
        self.play(Write(definition))
        
        formula = MathTex("\\frac{\\text{integer}}{\\text{integer}}", font_size=40)
        formula.next_to(definition, DOWN, buff=0.5)
        self.play(Write(formula))
        self.wait()
        
        examples = VGroup(
            MathTex("\\frac{3}{4} = 0.75", font_size=32),
            MathTex("\\frac{23}{10} = 2.3", font_size=32),
            MathTex("\\frac{8}{10} = 0.8", font_size=32),
            MathTex("-\\frac{5}{2} = -2.5", font_size=32)
        ).arrange(DOWN, buff=0.3)
        examples.next_to(formula, DOWN, buff=0.6)
        
        for ex in examples:
            self.play(Write(ex), run_time=0.6)
        self.wait(2)


class IrrationalNumbers(Scene):
    """Irrational numbers"""
    def construct(self):
        title = Text("Irrational Numbers", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # Problem
        problem = Text("What number times itself equals 2?", font_size=32, color=YELLOW)
        problem.next_to(title, DOWN, buff=0.5)
        self.play(Write(problem))
        self.wait()
        
        equation = MathTex("? \\times ? = 2", font_size=40)
        equation.next_to(problem, DOWN, buff=0.5)
        self.play(Write(equation))
        self.wait()
        
        # Check some numbers
        checks = VGroup(
            MathTex("1 \\times 1 = 1", font_size=32, color=RED),
            MathTex("2 \\times 2 = 4", font_size=32, color=RED),
            MathTex("1.5 \\times 1.5 = 2.25", font_size=32, color=RED),
            MathTex("1.4 \\times 1.4 = 1.96", font_size=32, color=RED)
        ).arrange(DOWN, buff=0.3)
        checks.next_to(equation, DOWN, buff=0.6)
        
        for check in checks:
            self.play(Write(check), run_time=0.6)
        
        cross = Text("✗ No fraction works!", font_size=28, color=RED)
        cross.next_to(checks, DOWN, buff=0.5)
        self.play(Write(cross))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in [problem, equation, checks, cross]])
        
        # Answer
        answer_text = Text("Answer:", font_size=32, color=YELLOW)
        answer_text.next_to(title, DOWN, buff=0.5)
        self.play(Write(answer_text))
        
        answer = MathTex("\\sqrt{2} \\approx 1.41421356...", font_size=40, color=GREEN)
        answer.next_to(answer_text, DOWN, buff=0.5)
        self.play(Write(answer))
        self.wait()
        
        note = Text("Cannot be written as a fraction!", font_size=28)
        note.next_to(answer, DOWN, buff=0.5)
        self.play(Write(note))
        self.wait(2)
        
        # More examples
        more_title = Text("More Irrational Numbers:", font_size=28, color=YELLOW)
        more_title.next_to(note, DOWN, buff=0.6)
        self.play(Write(more_title))
        
        more_examples = MathTex("\\sqrt{3}, \\sqrt{5}, \\sqrt{10}, \\pi, e", font_size=36)
        more_examples.next_to(more_title, DOWN, buff=0.3)
        self.play(Write(more_examples))
        self.wait(2)


# ============================================
# SECTION 2: CALCULATIONS WITH WHOLE NUMBERS
# ============================================

class EstimatingRounding(Scene):
    """Estimation and rounding off"""
    def construct(self):
        title = Text("Estimating & Rounding", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # Problem
        problem = Text("A shop owner buys chickens at R38 each", font_size=28, color=YELLOW)
        problem.next_to(title, DOWN, buff=0.5)
        self.play(Write(problem))
        
        question = Text("With R10,000, can he buy 250 chickens?", font_size=28)
        question.next_to(problem, DOWN, buff=0.3)
        self.play(Write(question))
        self.wait(2)
        
        # Estimation
        est_title = Text("Let's estimate by rounding:", font_size=26, color=GREEN)
        est_title.next_to(question, DOWN, buff=0.6)
        self.play(Write(est_title))
        
        step1 = MathTex("R38 \\approx R40", font_size=32)
        step1.next_to(est_title, DOWN, buff=0.4)
        self.play(Write(step1))
        self.wait()
        
        step2 = MathTex("250 \\times R40 = R10,000", font_size=32)
        step2.next_to(step1, DOWN, buff=0.3)
        self.play(Write(step2))
        self.wait()
        
        conclusion = Text("Yes! About 250 chickens (maybe a bit more)", 
                         font_size=26, color=GREEN)
        conclusion.next_to(step2, DOWN, buff=0.5)
        self.play(Write(conclusion))
        self.wait(2)
        
        # Exact calculation
        self.play(*[FadeOut(mob) for mob in [problem, question, est_title, 
                                              step1, step2, conclusion]])
        
        exact_title = Text("Exact Calculation:", font_size=32, color=YELLOW)
        exact_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(exact_title))
        
        exact = MathTex("10,000 \\div 38 = 263.15...", font_size=40)
        exact.next_to(exact_title, DOWN, buff=0.5)
        self.play(Write(exact))
        
        answer = Text("Can buy 263 chickens!", font_size=32, color=GREEN)
        answer.next_to(exact, DOWN, buff=0.5)
        self.play(Write(answer))
        self.wait(2)


class RoundingPractice(Scene):
    """Rounding to nearest 10, 100"""
    def construct(self):
        title = Text("Rounding Numbers", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # Example:83 goats at R243 each
        example = Text("83 goats sold at R243 each", font_size=32, color=YELLOW)
        example.next_to(title, DOWN, buff=0.5)
        self.play(Write(example))
        self.wait()
        
        # Round to nearest 100
        round100_title = Text("Round to nearest 100:", font_size=28, color=GREEN)
        round100_title.next_to(example, DOWN, buff=0.6)
        self.play(Write(round100_title))
        
        round1 = MathTex("83 \\approx 100", font_size=36)
        round2 = MathTex("R243 \\approx R200", font_size=36)
        round1.next_to(round100_title, DOWN, buff=0.4).shift(LEFT * 2)
        round2.next_to(round1, RIGHT, buff=1)
        
        self.play(Write(round1), Write(round2))
        self.wait()
        
        calc1 = MathTex("100 \\times R200 = R20,000", font_size=36, color=BLUE)
        calc1.next_to(round1, DOWN, buff=0.5).shift(RIGHT)
        self.play(Write(calc1))
        self.wait(2)
        
        # Round to nearest 10
        self.play(*[FadeOut(mob) for mob in [round100_title, round1, round2, calc1]])
        
        round10_title = Text("Round to nearest 10:", font_size=28, color=GREEN)
        round10_title.next_to(example, DOWN, buff=0.6)
        self.play(Write(round10_title))
        
        round3 = MathTex("83 \\approx 80", font_size=36)
        round4 = MathTex("R243 \\approx R240", font_size=36)
        round3.next_to(round10_title, DOWN, buff=0.4).shift(LEFT * 2)
        round4.next_to(round3, RIGHT, buff=1)
        
        self.play(Write(round3), Write(round4))
        self.wait()
        
        calc2 = MathTex("80 \\times R240 = R19,200", font_size=36, color=BLUE)
        calc2.next_to(round3, DOWN, buff=0.5).shift(RIGHT)
        self.play(Write(calc2))
        self.wait()
        
        # Exact answer
        exact = MathTex("\\text{Exact: } 83 \\times R243 = R20,169", 
                       font_size=32, color=YELLOW)
        exact.next_to(calc2, DOWN, buff=0.6)
        self.play(Write(exact))
        self.wait(2)


class Compensating(Scene):
    """Compensating for rounding errors"""
    def construct(self):
        title = Text("Compensating for Errors", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # Problem
        problem = MathTex("R823 - R273", font_size=40, color=YELLOW)
        problem.next_to(title, DOWN, buff=0.5)
        self.play(Write(problem))
        self.wait()
        
        # Round to nearest 100
        step1_title = Text("Step 1: Round to nearest 100", font_size=28, color=GREEN)
        step1_title.next_to(problem, DOWN, buff=0.6)
        self.play(Write(step1_title))
        
        rounded = MathTex("R800 - R300 = R500", font_size=36)
        rounded.next_to(step1_title, DOWN, buff=0.4)
        self.play(Write(rounded))
        self.wait(2)
        
        # Compensate
        step2_title = Text("Step 2: Compensate for errors", font_size=28, color=GREEN)
        step2_title.next_to(rounded, DOWN, buff=0.6)
        self.play(Write(step2_title))
        
        error1 = MathTex("823 \\to 800: \\text{ error of } +23", font_size=30)
        error2 = MathTex("273 \\to 300: \\text{ error of } -27", font_size=30)
        error1.next_to(step2_title, DOWN, buff=0.4)
        error2.next_to(error1, DOWN, buff=0.3)
        
        self.play(Write(error1))
        self.wait()
        self.play(Write(error2))
        self.wait()
        
        # Correction
        correction = MathTex("R500 + R23 + R27 = R550", font_size=36, color=BLUE)
        correction.next_to(error2, DOWN, buff=0.5)
        self.play(Write(correction))
        self.wait()
        
        # Exact answer
        exact = MathTex("\\text{Exact: } R823 - R273 = R550", 
                       font_size=32, color=GREEN)
        exact.next_to(correction, DOWN, buff=0.5)
        box = SurroundingRectangle(exact, color=YELLOW, buff=0.2)
        self.play(Write(exact))
        self.play(Create(box))
        self.wait(2)


class ColumnAddition(Scene):
    """Adding in columns"""
    def construct(self):
        title = Text("Addition in Columns", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # Problem: 3758 + 5486
        problem = MathTex("3758 + 5486", font_size=36, color=YELLOW)
        problem.next_to(title, DOWN, buff=0.5)
        self.play(Write(problem))
        self.wait()
        
        # Set up column format
        col_setup = VGroup(
            MathTex("3758", font_size=40),
            MathTex("+\\,5486", font_size=40),
            Line(LEFT * 0.8, RIGHT * 0.8, color=WHITE)
        ).arrange(DOWN, buff=0.2)
        col_setup.next_to(problem, DOWN, buff=0.8)
        
        for item in col_setup:
            self.play(Write(item), run_time=0.6)
        self.wait()
        
        # Add units
        units_step = Text("Units: 8 + 6 = 14 (write 4, carry 1)", 
                         font_size=24, color=GREEN)
        units_step.next_to(col_setup, RIGHT, buff=1)
        self.play(Write(units_step))
        
        result1 = MathTex("4", font_size=40)
        result1.next_to(col_setup, DOWN, buff=0.1).align_to(col_setup[0], RIGHT)
        self.play(Write(result1))
        self.wait()
        
        # Add tens
        self.play(FadeOut(units_step))
        tens_step = Text("Tens: 5 + 8 + 1 = 14 (write 4, carry 1)", 
                        font_size=24, color=GREEN)
        tens_step.next_to(col_setup, RIGHT, buff=1)
        self.play(Write(tens_step))
        
        result2 = MathTex("44", font_size=40)
        result2.move_to(result1.get_center()).align_to(col_setup[0], RIGHT)
        self.play(Transform(result1, result2))
        self.wait()
        
        # Add hundreds
        self.play(FadeOut(tens_step))
        hundreds_step = Text("Hundreds: 7 + 4 + 1 = 12 (write 2, carry 1)", 
                           font_size=24, color=GREEN)
        hundreds_step.next_to(col_setup, RIGHT, buff=1)
        self.play(Write(hundreds_step))
        
        result3 = MathTex("244", font_size=40)
        result3.move_to(result1.get_center()).align_to(col_setup[0], RIGHT)
        self.play(Transform(result1, result3))
        self.wait()
        
        # Add thousands
        self.play(FadeOut(hundreds_step))
        thousands_step = Text("Thousands: 3 + 5 + 1 = 9", 
                            font_size=24, color=GREEN)
        thousands_step.next_to(col_setup, RIGHT, buff=1)
        self.play(Write(thousands_step))
        
        result4 = MathTex("9244", font_size=40, color=YELLOW)
        result4.move_to(result1.get_center()).align_to(col_setup[0], RIGHT)
        self.play(Transform(result1, result4))
        self.wait()
        
        box = SurroundingRectangle(result1, color=GREEN, buff=0.2)
        self.play(Create(box))
        self.wait(2)


class ColumnMultiplication(Scene):
    """Multiplying in columns"""
    def construct(self):
        title = Text("Multiplication in Columns", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # Problem: 3489 × 47
        problem = MathTex("3489 \\times 47", font_size=36, color=YELLOW)
        problem.next_to(title, DOWN, buff=0.5)
        self.play(Write(problem))
        self.wait()
        
        # Set up
        setup = VGroup(
            MathTex("3489", font_size=36),
            MathTex("\\times\\,\\,\\,47", font_size=36),
            Line(LEFT * 0.9, RIGHT * 0.9, color=WHITE)
        ).arrange(DOWN, buff=0.2)
        setup.next_to(problem, DOWN, buff=0.8)
        
        for item in setup:
            self.play(Write(item), run_time=0.6)
        self.wait()
        
        # Multiply by 7
        step1 = Text("First: 3489 × 7", font_size=26, color=GREEN)
        step1.next_to(setup, RIGHT, buff=1.5)
        self.play(Write(step1))
        
        result1 = MathTex("24423", font_size=36)
        result1.next_to(setup, DOWN, buff=0.1).align_to(setup[0], RIGHT)
        self.play(Write(result1))
        self.wait()
        
        # Multiply by 40
        self.play(FadeOut(step1))
        step2 = Text("Then: 3489 × 40", font_size=26, color=GREEN)
        step2.next_to(setup, RIGHT, buff=1.5)
        self.play(Write(step2))
        
        result2 = MathTex("139560", font_size=36)
        result2.next_to(result1, DOWN, buff=0.1).align_to(setup[0], RIGHT)
        self.play(Write(result2))
        self.wait()
        
        # Add them
        self.play(FadeOut(step2))
        step3 = Text("Add the results", font_size=26, color=GREEN)
        step3.next_to(setup, RIGHT, buff=1.5)
        self.play(Write(step3))
        
        line2 = Line(LEFT * 0.9, RIGHT * 0.9, color=WHITE)
        line2.next_to(result2, DOWN, buff=0.1)
        self.play(Create(line2))
        
        final = MathTex("163983", font_size=36, color=YELLOW)
        final.next_to(line2, DOWN, buff=0.1).align_to(setup[0], RIGHT)
        self.play(Write(final))
        
        box = SurroundingRectangle(final, color=GREEN, buff=0.2)
        self.play(Create(box))
        self.wait(2)


class LongDivision(Scene):
    """Long division"""
    def construct(self):
        title = Text("Long Division", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # Problem: 13254 ÷ 56
        problem = MathTex("13254 \\div 56", font_size=40, color=YELLOW)
        problem.next_to(title, DOWN, buff=0.5)
        self.play(Write(problem))
        self.wait(2)
        
        # Estimate 1: 200 × 56
        est1_title = Text("Estimate: How many 56s in 13254?", font_size=28, color=GREEN)
        est1_title.next_to(problem, DOWN, buff=0.6)
        self.play(Write(est1_title))
        
        est1 = MathTex("200 \\times 56 = 11200", font_size=32)
        est1.next_to(est1_title, DOWN, buff=0.4)
        self.play(Write(est1))
        self.wait()
        
        remain1 = MathTex("13254 - 11200 = 2054", font_size=32)
        remain1.next_to(est1, DOWN, buff=0.3)
        self.play(Write(remain1))
        self.wait(2)
        
        # Estimate 2: 30 × 56
        est2 = MathTex("30 \\times 56 = 1680", font_size=32)
        est2.next_to(remain1, DOWN, buff=0.4)
        self.play(Write(est2))
        self.wait()
        
        remain2 = MathTex("2054 - 1680 = 374", font_size=32)
        remain2.next_to(est2, DOWN, buff=0.3)
        self.play(Write(remain2))
        self.wait(2)
        
        # Estimate 3: 6 × 56
        est3 = MathTex("6 \\times 56 = 336", font_size=32)
        est3.next_to(remain2, DOWN, buff=0.4)
        self.play(Write(est3))
        self.wait()
        
        remain3 = MathTex("3374 - 336 = 38", font_size=32)
        remain3.next_to(est3, DOWN, buff=0.3)
        self.play(Write(remain3))
        self.wait(2)
        
        # Answer
        self.play(*[FadeOut(mob) for mob in [est1_title, est1, remain1, est2, 
                                              remain2, est3, remain3]])
        
        answer = MathTex("13254 \\div 56 = 200 + 30 + 6 = 236", 
                        font_size=36, color=GREEN)
        answer.next_to(problem, DOWN, buff=0.8)
        self.play(Write(answer))
        
        remainder_note = MathTex("\\text{Remainder: } 38", font_size=32)
        remainder_note.next_to(answer, DOWN, buff=0.4)
        self.play(Write(remainder_note))
        
        final = MathTex("= 236 \\frac{38}{56} = 236.68", font_size=32, color=YELLOW)
        final.next_to(remainder_note, DOWN, buff=0.4)
        self.play(Write(final))
        
        box = SurroundingRectangle(final, color=GREEN, buff=0.2)
        self.play(Create(box))
        self.wait(2)


# ============================================
# SECTION 3: MULTIPLES AND FACTORS
# ============================================

class LCMExample(Scene):
    """Lowest Common Multiple"""
    def construct(self):
        title = Text("Lowest Common Multiple (LCM)", font_size=44, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # Find LCM of 6 and 15
        question = Text("Find LCM of 6 and 15", font_size=32, color=YELLOW)
        question.next_to(title, DOWN, buff=0.5)
        self.play(Write(question))
        self.wait()
        
        # Multiples of 6
        mult6_title = Text("Multiples of 6:", font_size=28, color=GREEN)
        mult6_title.next_to(question, DOWN, buff=0.6).to_edge(LEFT, buff=1)
        self.play(Write(mult6_title))
        
        mult6 = Text("6, 12, 18, 24, 30, 36, 42, 48, 54, 60, ...", font_size=26)
        mult6.next_to(mult6_title, DOWN, buff=0.3)
        self.play(Write(mult6))
        self.wait()
        
        # Multiples of 15
        mult15_title = Text("Multiples of 15:", font_size=28, color=GREEN)
        mult15_title.next_to(mult6, DOWN, buff=0.5).to_edge(LEFT, buff=1)
        self.play(Write(mult15_title))
        
        mult15 = Text("15, 30, 45, 60, 75, 90, ...", font_size=26)
        mult15.next_to(mult15_title, DOWN, buff=0.3)
        self.play(Write(mult15))
        self.wait(2)
        
        # Common multiples
        common_title = Text("Common multiples:", font_size=28, color=YELLOW)
        common_title.next_to(mult15, DOWN, buff=0.6).to_edge(LEFT, buff=1)
        self.play(Write(common_title))
        
        common = Text("30, 60, 90, ...", font_size=26, color=BLUE)
        common.next_to(common_title, DOWN, buff=0.3)
        self.play(Write(common))
        self.wait()
        
        # LCM
        lcm = Text("LCM(6, 15) = 30", font_size=36, color=GREEN)
        lcm.next_to(common, DOWN, buff=0.6)
        box = SurroundingRectangle(lcm, color=YELLOW, buff=0.2)
        self.play(Write(lcm))
        self.play(Create(box))
        self.wait(2)


class HCFExample(Scene):
    """Highest Common Factor"""
    def construct(self):
        title = Text("Highest Common Factor (HCF)", font_size=44, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # Find HCF of 2310 and 3510
        question = Text("Find HCF of 2310 and 3510", font_size=32, color=YELLOW)
        question.next_to(title, DOWN, buff=0.5)
        self.play(Write(question))
        self.wait()
        
        # Prime factorization of 2310
        pf1_title = Text("Prime factorization of 2310:", font_size=28, color=GREEN)
        pf1_title.next_to(question, DOWN, buff=0.6).to_edge(LEFT, buff=1)
        self.play(Write(pf1_title))
        
        pf1 = MathTex("2310 = 2 \\times 3 \\times 5 \\times 7 \\times 11", font_size=28)
        pf1.next_to(pf1_title, DOWN, buff=0.3)
        self.play(Write(pf1))
        self.wait()
        
        # Prime factorization of 3510
        pf2_title = Text("Prime factorization of 3510:", font_size=28, color=GREEN)
        pf2_title.next_to(pf1, DOWN, buff=0.5).to_edge(LEFT, buff=1)
        self.play(Write(pf2_title))
        
        pf2 = MathTex("3510 = 2 \\times 3 \\times 3 \\times 5 \\times 13", font_size=28)
        pf2.next_to(pf2_title, DOWN, buff=0.3)
        self.play(Write(pf2))
        self.wait(2)
        
        # Common factors
        common_title = Text("Common prime factors:", font_size=28, color=YELLOW)
        common_title.next_to(pf2, DOWN, buff=0.6).to_edge(LEFT, buff=1)
        self.play(Write(common_title))
        
        common = MathTex("2, 3, 5", font_size=28, color=BLUE)
        common.next_to(common_title, DOWN, buff=0.3)
        self.play(Write(common))
        self.wait()
        
        # HCF
        hcf_calc = MathTex("HCF = 2 \\times 3 \\times 5 = 30", font_size=32, color=GREEN)
        hcf_calc.next_to(common, DOWN, buff=0.6)
        box = SurroundingRectangle(hcf_calc, color=YELLOW, buff=0.2)
        self.play(Write(hcf_calc))
        self.play(Create(box))
        self.wait(2)


# ============================================
# SECTION 4: RATIO, RATE, AND PROPORTION
# ============================================

class ApplePickingRate(Scene):
    """Rate problem - apple picking"""
    def construct(self):
        title = Text("Rate: Apple Picking", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # Moeneba picks 5 apples/minute
        rate = Text("Moeneba picks 5 apples per minute", font_size=32, color=YELLOW)
        rate.next_to(title, DOWN, buff=0.5)
        self.play(Write(rate))
        self.wait()
        
        # Create apple icons
        apple = Circle(radius=0.15, color=RED, fill_opacity=0.7)
        apples = VGroup(*[apple.copy() for _ in range(5)])
        apples.arrange(RIGHT, buff=0.2)
        apples.next_to(rate, DOWN, buff=0.5)
        
        clock = Text("1 min", font_size=24)
        clock.next_to(apples, LEFT, buff=0.5)
        
        self.play(Write(clock))
        for a in apples:
            self.play(FadeIn(a), run_time=0.2)
        self.wait(2)
        
        # How many in 15 minutes?
        question = Text("How many apples in 15 minutes?", font_size=28, color=GREEN)
        question.next_to(apples, DOWN, buff=0.6)
        self.play(Write(question))
        self.wait()
        
        calc = MathTex("5 \\times 15 = 75 \\text{ apples}", font_size=36, color=YELLOW)
        calc.next_to(question, DOWN, buff=0.5)
        self.play(Write(calc))
        self.wait(2)
        
        box = SurroundingRectangle(calc, color=GREEN, buff=0.2)
        self.play(Create(box))
        self.wait(2)


class BiscuitRatio(Scene):
    """Ratio problem - biscuit recipe"""
    def construct(self):
        title = Text("Ratio: Biscuit Recipe", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # Recipe ratio
        recipe = Text("Recipe ratio - Flour:Oatmeal:Cocoa", font_size=28, color=YELLOW)
        recipe.next_to(title, DOWN, buff=0.5)
        self.play(Write(recipe))
        
        ratio = MathTex("5:2:1", font_size=48, color=GREEN)
        ratio.next_to(recipe, DOWN, buff=0.4)
        self.play(Write(ratio))
        self.wait(2)
        
        # Visual representation
        flour_rect = Rectangle(width=2.5, height=0.4, color=YELLOW, fill_opacity=0.6)
        oat_rect = Rectangle(width=1.0, height=0.4, color=ORANGE, fill_opacity=0.6)
        cocoa_rect = Rectangle(width=0.5, height=0.4, color=RED_E, fill_opacity=0.6)
        
        rects = VGroup(flour_rect, oat_rect, cocoa_rect).arrange(RIGHT, buff=0.3)
        rects.next_to(ratio, DOWN, buff=0.6)
        
        flour_label = Text("5 parts", font_size=20).next_to(flour_rect, DOWN, buff=0.2)
        oat_label = Text("2 parts", font_size=20).next_to(oat_rect, DOWN, buff=0.2)
        cocoa_label = Text("1 part", font_size=20).next_to(cocoa_rect, DOWN, buff=0.2)
        
        self.play(Create(flour_rect), Write(flour_label))
        self.wait(0.5)
        self.play(Create(oat_rect), Write(oat_label))
        self.wait(0.5)
        self.play(Create(cocoa_rect), Write(cocoa_label))
        self.wait(2)
        
        # Problem: If 500g flour is used
        problem = Text("If we use 500g of flour...", font_size=28, color=YELLOW)
        problem.next_to(cocoa_label, DOWN, buff=0.8)
        self.play(Write(problem))
        self.wait()
        
        # Calculate
        calc1 = MathTex("\\text{1 part} = 500 \\div 5 = 100\\text{g}", font_size=28)
        calc1.next_to(problem, DOWN, buff=0.4)
        self.play(Write(calc1))
        self.wait()
        
        calc2 = MathTex("\\text{Oatmeal} = 2 \\times 100 = 200\\text{g}", 
                       font_size=28, color=ORANGE)
        calc2.next_to(calc1, DOWN, buff=0.3)
        self.play(Write(calc2))
        self.wait()
        
        calc3 = MathTex("\\text{Cocoa} = 1 \\times 100 = 100\\text{g}", 
                       font_size=28, color=RED)
        calc3.next_to(calc2, DOWN, buff=0.3)
        self.play(Write(calc3))
        self.wait(2)
        
        box = SurroundingRectangle(VGroup(calc2, calc3), color=GREEN, buff=0.2)
        self.play(Create(box))
        self.wait(2)


class SpeedDistanceTime(Scene):
    """Rate problem - speed, distance, time"""
    def construct(self):
        title = Text("Speed, Distance & Time", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # Formula triangle
        triangle = Triangle(color=YELLOW, fill_opacity=0.3)
        triangle.scale(1.5).shift(UP * 0.5)
        
        d_label = MathTex("D", font_size=40).move_to(triangle.get_top() + DOWN * 0.3)
        s_label = MathTex("S", font_size=40).move_to(triangle.get_bottom() + UP * 0.3 + LEFT * 0.4)
        t_label = MathTex("T", font_size=40).move_to(triangle.get_bottom() + UP * 0.3 + RIGHT * 0.4)
        
        self.play(Create(triangle))
        self.play(Write(d_label), Write(s_label), Write(t_label))
        self.wait()
        
        line_h = Line(triangle.get_left() + RIGHT * 0.3, triangle.get_right() + LEFT * 0.3)
        line_h.move_to(triangle.get_center() + DOWN * 0.25)
        line_v = Line(triangle.get_center() + UP * 0.25, triangle.get_center() + DOWN * 0.75)
        
        self.play(Create(line_h), Create(line_v))
        self.wait(2)
        
        # Formulas
        formulas = VGroup(
            MathTex("S = \\frac{D}{T}", font_size=28),
            MathTex("D = S \\times T", font_size=28),
            MathTex("T = \\frac{D}{S}", font_size=28)
        ).arrange(RIGHT, buff=0.8)
        formulas.next_to(triangle, DOWN, buff=0.8)
        
        for f in formulas:
            self.play(Write(f), run_time=0.7)
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in [triangle, d_label, s_label, t_label, 
                                              line_h, line_v, formulas]])
        
        # Example problem
        problem = Text("A car travels 360 km in 4 hours", font_size=32, color=YELLOW)
        problem.next_to(title, DOWN, buff=0.5)
        self.play(Write(problem))
        
        question = Text("What is the speed?", font_size=28)
        question.next_to(problem, DOWN, buff=0.4)
        self.play(Write(question))
        self.wait()
        
        # Solution
        formula = MathTex("S = \\frac{D}{T}", font_size=36)
        formula.next_to(question, DOWN, buff=0.6)
        self.play(Write(formula))
        self.wait()
        
        substitution = MathTex("S = \\frac{360\\text{ km}}{4\\text{ hours}}", font_size=36)
        substitution.next_to(formula, DOWN, buff=0.5)
        self.play(Write(substitution))
        self.wait()
        
        answer = MathTex("S = 90\\text{ km/h}", font_size=40, color=GREEN)
        answer.next_to(substitution, DOWN, buff=0.5)
        self.play(Write(answer))
        
        box = SurroundingRectangle(answer, color=YELLOW, buff=0.2)
        self.play(Create(box))
        self.wait(2)


class ProportionProblem(Scene):
    """Direct proportion problem"""
    def construct(self):
        title = Text("Proportion Problem", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # Ratio of pickers
        problem = Text("Moeneba:Kate:Garth pick at ratio 5:15:12", 
                      font_size=28, color=YELLOW)
        problem.next_to(title, DOWN, buff=0.5)
        self.play(Write(problem))
        self.wait()
        
        # In 10 minutes
        time = Text("In 10 minutes:", font_size=28, color=GREEN)
        time.next_to(problem, DOWN, buff=0.6)
        self.play(Write(time))
        
        results = VGroup(
            MathTex("\\text{Moeneba: } 5 \\times 10 = 50 \\text{ apples}", font_size=28),
            MathTex("\\text{Kate: } 15 \\times 10 = 150 \\text{ apples}", font_size=28),
            MathTex("\\text{Garth: } 12 \\times 10 = 120 \\text{ apples}", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        results.next_to(time, DOWN, buff=0.5)
        
        for r in results:
            self.play(Write(r), run_time=0.8)
        self.wait()
        
        # Total
        total_line = Line(LEFT * 3, RIGHT * 3, color=WHITE)
        total_line.next_to(results, DOWN, buff=0.3)
        self.play(Create(total_line))
        
        total = MathTex("\\text{Total: } 50 + 150 + 120 = 320 \\text{ apples}", 
                       font_size=32, color=GREEN)
        total.next_to(total_line, DOWN, buff=0.3)
        self.play(Write(total))
        
        box = SurroundingRectangle(total, color=YELLOW, buff=0.2)
        self.play(Create(box))
        self.wait(2)


# ============================================
# CHAPTER SUMMARY
# ============================================

class Chapter1Summary(Scene):
    """Complete Chapter 1 Summary"""
    def construct(self):
        title = Text("Chapter 1: Complete Summary", font_size=44, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        sections = VGroup(
            Text("1. Types of Numbers", font_size=26, color=YELLOW),
            Text("   • Natural, Whole, Integers, Rational, Irrational", font_size=22),
            Text("2. Calculations", font_size=26, color=YELLOW),
            Text("   • Estimating, Rounding, Compensating", font_size=22),
            Text("   • Column Addition, Multiplication, Division", font_size=22),
            Text("3. Multiples & Factors", font_size=26, color=YELLOW),
            Text("   • LCM (Lowest Common Multiple)", font_size=22),
            Text("   • HCF (Highest Common Factor)", font_size=22),
            Text("4. Ratio, Rate & Proportion", font_size=26, color=YELLOW),
            Text("   • Ratios in recipes and mixtures", font_size=22),
            Text("   • Rates: speed, picking, production", font_size=22),
            Text("   • Direct proportion problems", font_size=22)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        sections.next_to(title, DOWN, buff=0.6).shift(LEFT * 2)
        
        for section in sections:
            self.play(Write(section), run_time=0.5)
        
        self.wait(2)
        
        # Key skills
        skills_title = Text("Key Skills Developed:", font_size=28, color=GREEN)
        skills_title.to_edge(DOWN, buff=2)
        self.play(Write(skills_title))
        
        skills  = VGroup(
            Text("✓ Number sense & properties", font_size=22),
            Text("✓ Mental math & estimation", font_size=22),
            Text("✓ Problem-solving strategies", font_size=22),
            Text("✓ Real-world applications", font_size=22)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        skills.next_to(skills_title, DOWN, buff=0.3).align_to(skills_title, LEFT)
        
        for skill in skills:
            self.play(Write(skill), run_time=0.5)
        
        self.wait(3)
