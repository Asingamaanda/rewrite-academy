from manim import *
import numpy as np

# ============================================================================
# BASE CLASS FOR ALGEBRA LESSONS
# ============================================================================

class AlgebraLesson(Scene):
    """Base class for Grade 12 Algebra lessons with consistent styling"""
    
    # Color scheme
    COLOR_EQUATION = BLUE
    COLOR_STEP = YELLOW
    COLOR_ANSWER = RED
    COLOR_HIGHLIGHT = GREEN
    COLOR_WARNING = ORANGE
    
    # Font sizes
    FONT_TITLE = 44
    FONT_SUBTITLE = 32
    FONT_EQUATION = 40
    FONT_STEP = 28
    FONT_LABEL = 24
    
    def show_title(self, title_text, subtitle_text=None):
        """Display lesson title"""
        title = Text(title_text, font_size=self.FONT_TITLE, color=self.COLOR_EQUATION, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        
        group = VGroup(title)
        
        if subtitle_text:
            subtitle = Text(subtitle_text, font_size=self.FONT_SUBTITLE, color=WHITE)
            subtitle.next_to(title, DOWN, buff=0.3)
            group.add(subtitle)
        
        self.play(Write(title), run_time=2)
        if subtitle_text:
            self.play(FadeIn(subtitle), run_time=1.5)
        
        self.wait(2)
        return group
    
    def show_equation(self, latex_str, color=None, position=ORIGIN):
        """Display mathematical equation"""
        if color is None:
            color = self.COLOR_EQUATION
        
        equation = MathTex(latex_str, font_size=self.FONT_EQUATION, color=color)
        equation.move_to(position)
        return equation
    
    def show_step(self, text, position=DOWN*2.5, color=None):
        """Display explanation text"""
        if color is None:
            color = WHITE
        
        explanation = Text(text, font_size=self.FONT_STEP, color=color)
        explanation.move_to(position)
        return explanation
    
    def highlight_box(self, mobject, color=YELLOW):
        """Create highlighting box around object"""
        box = SurroundingRectangle(mobject, color=color, buff=0.15)
        self.play(Create(box), run_time=1.5)
        self.wait(1)
        return box
    
    def pause_for_voiceover(self, duration=2):
        """Pause for voiceover narration"""
        self.wait(duration)
    
    def clear_all(self):
        """Clear all objects from scene"""
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


# ============================================================================
# SCENE 1: QUADRATIC EQUATIONS - FACTORIZATION
# ============================================================================

class QuadraticFactorization(AlgebraLesson):
    def construct(self):
        # VOICEOVER: "Welcome to quadratic equations. Let's learn how to solve them by factorization."
        
        title = self.show_title("Quadratic Equations", "Factorization Method")
        self.play(title.animate.scale(0.7).to_edge(UP, buff=0.3), run_time=1.5)
        
        # Problem
        problem_text = Text("Solve for x:", font_size=self.FONT_STEP)
        problem_text.shift(UP*2)
        self.play(Write(problem_text), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # VOICEOVER: "We have x plus x squared equals zero."
        
        equation = self.show_equation(r"x + x^2 = 0", position=UP*1)
        self.play(Write(equation), run_time=2)
        self.pause_for_voiceover(3)
        
        # Step 1: Rearrange
        step1 = self.show_step("Step 1: Rearrange in standard form", position=ORIGIN)
        self.play(FadeIn(step1), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # VOICEOVER: "First, rearrange in standard form: x squared plus x equals zero."
        
        eq_step1 = self.show_equation(r"x^2 + x = 0", color=self.COLOR_STEP, position=DOWN*0.8)
        self.play(TransformMatchingTex(equation.copy(), eq_step1), run_time=2)
        self.pause_for_voiceover(3)
        
        self.play(FadeOut(step1), run_time=0.8)
        
        # Step 2: Factor
        step2 = self.show_step("Step 2: Factor out common term", position=ORIGIN)
        self.play(FadeIn(step2), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # VOICEOVER: "Factor out the common term x."
        
        eq_step2 = self.show_equation(r"x(x + 1) = 0", color=self.COLOR_STEP, position=DOWN*0.8)
        self.play(TransformMatchingTex(eq_step1, eq_step2), run_time=2)
        self.pause_for_voiceover(3)
        
        # Highlight factors
        box1 = SurroundingRectangle(eq_step2[0][0], color=YELLOW)
        box2 = SurroundingRectangle(eq_step2[0][2:5], color=YELLOW)
        self.play(Create(box1), Create(box2), run_time=1.5)
        self.pause_for_voiceover(2)
        
        self.play(FadeOut(box1), FadeOut(box2), FadeOut(step2), run_time=0.8)
        
        # Step 3: Set each factor = 0
        step3 = self.show_step("Step 3: Set each factor equal to zero", position=ORIGIN)
        self.play(FadeIn(step3), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # VOICEOVER: "Set each factor equal to zero."
        
        eq_step3a = self.show_equation(r"x = 0", color=self.COLOR_STEP, position=DOWN*1.2+LEFT*2)
        eq_or = Text("or", font_size=self.FONT_STEP, color=WHITE)
        eq_or.move_to(DOWN*1.2)
        eq_step3b = self.show_equation(r"x + 1 = 0", color=self.COLOR_STEP, position=DOWN*1.2+RIGHT*2)
        
        self.play(
            Write(eq_step3a),
            Write(eq_or),
            Write(eq_step3b),
            run_time=2
        )
        self.pause_for_voiceover(3)
        
        self.play(FadeOut(step3), run_time=0.8)
        
        # Step 4: Solve
        step4 = self.show_step("Step 4: Solve for x", position=ORIGIN)
        self.play(FadeIn(step4), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # VOICEOVER: "The first solution is x equals zero."
        
        sol1 = self.show_equation(r"x = 0", color=self.COLOR_ANSWER, position=DOWN*2+LEFT*2)
        sol2 = self.show_equation(r"x = -1", color=self.COLOR_ANSWER, position=DOWN*2+RIGHT*2)
        
        self.play(
            TransformMatchingTex(eq_step3a.copy(), sol1),
            TransformMatchingTex(eq_step3b.copy(), sol2),
            run_time=2
        )
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "And the second solution is x equals negative one."
        
        self.play(FadeOut(step4), run_time=0.8)
        self.wait(1)
        
        # Final answer
        self.play(
            *[FadeOut(mob) for mob in [problem_text, equation, eq_step2, eq_step3a, eq_or, eq_step3b]],
            run_time=1
        )
        
        final = self.show_equation(r"x = 0 \text{ or } x = -1", color=self.COLOR_ANSWER)
        final.scale(1.2)
        self.play(
            sol1.animate.move_to(final.get_center()),
            sol2.animate.move_to(final.get_center()),
            run_time=1.5
        )
        self.remove(sol1, sol2)
        self.play(Write(final), run_time=2)
        
        answer_box = self.highlight_box(final, color=self.COLOR_ANSWER)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "So our final answer is x equals zero or x equals negative one."
        
        self.wait(2)


# ============================================================================
# SCENE 2: QUADRATIC FORMULA
# ============================================================================

class QuadraticFormula(AlgebraLesson):
    def construct(self):
        # VOICEOVER: "When a quadratic doesn't factor nicely, we use the quadratic formula."
        
        title = self.show_title("Quadratic Formula", "For equations that don't factor easily")
        self.play(title.animate.scale(0.7).to_edge(UP, buff=0.3), run_time=1.5)
        
        # Show the formula
        formula_label = Text("The Quadratic Formula:", font_size=self.FONT_STEP)
        formula_label.shift(UP*2)
        self.play(Write(formula_label), run_time=1.5)
        self.pause_for_voiceover(2)
        
        formula = self.show_equation(
            r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
            color=self.COLOR_HIGHLIGHT,
            position=UP*0.8
        )
        self.play(Write(formula), run_time=3)
        self.pause_for_voiceover(4)
        
        # VOICEOVER: "For any quadratic equation a x squared plus b x plus c equals zero."
        
        box = self.highlight_box(formula, color=self.COLOR_HIGHLIGHT)
        self.pause_for_voiceover(2)
        
        self.play(FadeOut(box), FadeOut(formula_label), run_time=1)
        self.wait(1)
        
        # Example problem
        example_text = Text("Example:", font_size=self.FONT_STEP)
        example_text.shift(UP*2)
        self.play(
            Transform(title, example_text),
            formula.animate.scale(0.6).to_edge(RIGHT).shift(UP*2),
            run_time=1.5
        )
        
        problem = self.show_equation(r"3x^2 - 5x + 1 = 0", position=UP*1)
        self.play(Write(problem), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "Let's solve 3 x squared minus 5 x plus 1 equals zero."
        
        # Identify a, b, c
        identify = Text("Identify a, b, c:", font_size=self.FONT_STEP)
        identify.shift(ORIGIN)
        self.play(FadeIn(identify), run_time=1.5)
        self.pause_for_voiceover(2)
        
        abc_group = VGroup(
            MathTex("a = 3", font_size=32, color=YELLOW),
            MathTex("b = -5", font_size=32, color=YELLOW),
            MathTex("c = 1", font_size=32, color=YELLOW)
        ).arrange(RIGHT, buff=0.8).shift(DOWN*0.8)
        
        self.play(Write(abc_group), run_time=2)
        self.pause_for_voiceover(3)
        
        self.play(FadeOut(identify), run_time=0.8)
        
        # Calculate discriminant
        disc_text = Text("Calculate discriminant:", font_size=self.FONT_STEP)
        disc_text.shift(ORIGIN)
        self.play(FadeIn(disc_text), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # VOICEOVER: "First, calculate the discriminant: b squared minus 4 a c."
        
        discriminant = self.show_equation(
            r"\Delta = b^2 - 4ac = (-5)^2 - 4(3)(1)",
            position=DOWN*1.2
        )
        self.play(Write(discriminant), run_time=2)
        self.pause_for_voiceover(3)
        
        disc_calc = self.show_equation(r"= 25 - 12 = 13", position=DOWN*2)
        self.play(Write(disc_calc), run_time=2)
        self.pause_for_voiceover(3)
        
        self.play(FadeOut(disc_text), run_time=0.8)
        self.wait(1)
        
        # Apply formula
        self.play(
            *[FadeOut(mob) for mob in [abc_group, discriminant, disc_calc]],
            run_time=1
        )
        
        apply_text = Text("Apply the formula:", font_size=self.FONT_STEP)
        apply_text.shift(UP*0.3)
        self.play(FadeIn(apply_text), run_time=1.5)
        self.pause_for_voiceover(2)
        
        solution = self.show_equation(
            r"x = \frac{-(-5) \pm \sqrt{13}}{2(3)} = \frac{5 \pm \sqrt{13}}{6}",
            position=DOWN*0.5
        )
        self.play(Write(solution), run_time=3)
        self.pause_for_voiceover(4)
        
        # Calculate values
        values = VGroup(
            MathTex(r"x = \frac{5 + 3.606}{6} = 1.43", font_size=32, color=self.COLOR_ANSWER),
            MathTex(r"x = \frac{5 - 3.606}{6} = 0.23", font_size=32, color=self.COLOR_ANSWER)
        ).arrange(DOWN, buff=0.5).shift(DOWN*2)
        
        self.play(Write(values), run_time=3)
        self.pause_for_voiceover(4)
        
        # VOICEOVER: "So x equals 1.43 or 0.23, correct to two decimal places."
        
        self.play(FadeOut(apply_text), run_time=0.8)
        self.wait(1)
        
        # Final answer
        self.play(
            *[FadeOut(mob) for mob in [problem, solution, formula]],
            run_time=1
        )
        
        final = self.show_equation(r"x = 1.43 \text{ or } x = 0.23", color=self.COLOR_ANSWER)
        final.scale(1.2)
        self.play(
            values.animate.move_to(final.get_center()),
            run_time=1.5
        )
        self.remove(values)
        self.play(Write(final), run_time=2)
        
        answer_box = self.highlight_box(final, color=self.COLOR_ANSWER)
        self.pause_for_voiceover(3)
        
        self.wait(2)


# ============================================================================
# SCENE 3: QUADRATIC INEQUALITIES
# ============================================================================

class QuadraticInequality(AlgebraLesson):
    def construct(self):
        # VOICEOVER: "Now let's learn how to solve quadratic inequalities."
        
        title = self.show_title("Quadratic Inequalities", "Finding intervals that satisfy the condition")
        self.play(title.animate.scale(0.7).to_edge(UP, buff=0.3), run_time=1.5)
        
        # Problem
        problem_text = Text("Solve for x:", font_size=self.FONT_STEP)
        problem_text.shift(UP*2.5)
        self.play(Write(problem_text), run_time=1.5)
        self.pause_for_voiceover(2)
        
        problem = self.show_equation(r"2x^2 - 7 \leq 5x", position=UP*1.5)
        self.play(Write(problem), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "Solve 2 x squared minus 7 is less than or equal to 5 x."
        
        # Step 1: Rearrange
        step1 = self.show_step("Step 1: Rearrange to standard form", position=UP*0.5)
        self.play(FadeIn(step1), run_time=1.5)
        self.pause_for_voiceover(2)
        
        rearranged = self.show_equation(r"2x^2 - 5x - 7 \leq 0", position=ORIGIN)
        self.play(Write(rearranged), run_time=2)
        self.pause_for_voiceover(3)
        
        self.play(FadeOut(step1), run_time=0.8)
        
        # Step 2: Solve equality
        step2 = self.show_step("Step 2: Solve 2x² - 5x - 7 = 0", position=UP*0.5)
        self.play(FadeIn(step2), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # VOICEOVER: "First solve the equation 2 x squared minus 5 x minus 7 equals zero."
        
        factored = self.show_equation(r"(2x - 7)(x + 1) = 0", position=ORIGIN)
        self.play(TransformMatchingTex(rearranged.copy(), factored), run_time=2)
        self.pause_for_voiceover(3)
        
        critical = VGroup(
            MathTex("x = \\frac{7}{2} = 3.5", font_size=32, color=YELLOW),
            MathTex("x = -1", font_size=32, color=YELLOW)
        ).arrange(RIGHT, buff=1.5).shift(DOWN*0.8)
        
        self.play(Write(critical), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "The critical values are x equals 3.5 and x equals negative 1."
        
        self.play(FadeOut(step2), run_time=0.8)
        
        # Step 3: Number line and testing
        self.play(
            *[FadeOut(mob) for mob in [problem, rearranged, factored]],
            run_time=1
        )
        
        step3 = self.show_step("Step 3: Test intervals", position=UP*2.5)
        step3.scale(0.9)
        self.play(FadeIn(step3), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # Create number line
        numberline = NumberLine(
            x_range=[-3, 5, 1],
            length=10,
            include_numbers=False,
            include_tip=True
        ).shift(UP*1.2)
        
        self.play(Create(numberline), run_time=2)
        
        # Mark critical points
        point1 = Dot(numberline.n2p(-1), color=RED, radius=0.1)
        point2 = Dot(numberline.n2p(3.5), color=RED, radius=0.1)
        label1 = MathTex("-1", font_size=28).next_to(point1, DOWN, buff=0.3)
        label2 = MathTex("3.5", font_size=28).next_to(point2, DOWN, buff=0.3)
        
        self.play(
            Create(point1), Create(point2),
            Write(label1), Write(label2),
            run_time=2
        )
        self.pause_for_voiceover(3)
        
        # Test regions
        test_regions = VGroup(
            Text("-", font_size=40, color=RED).move_to(numberline.n2p(-2.5)+UP*0.5),
            Text("+", font_size=40, color=GREEN).move_to(numberline.n2p(1)+UP*0.5),
            Text("-", font_size=40, color=RED).move_to(numberline.n2p(4.5)+UP*0.5)
        )
        
        # Show testing calculation
        test_point = Text("Test x = 0:", font_size=24).shift(DOWN*0.3)
        test_calc = MathTex(
            r"2(0)^2 - 5(0) - 7 = -7 < 0 \checkmark",
            font_size=28,
            color=GREEN
        ).shift(DOWN*1)
        
        self.play(Write(test_point), run_time=1.5)
        self.play(Write(test_calc), run_time=2)
        self.pause_for_voiceover(3)
        
        self.play(Write(test_regions[1]), run_time=1.5)
        self.pause_for_voiceover(2)
        
        self.play(FadeOut(test_point), FadeOut(test_calc), run_time=0.8)
        
        # Show other regions
        self.play(
            Write(test_regions[0]),
            Write(test_regions[2]),
            run_time=2
        )
        self.pause_for_voiceover(2)
        
        # VOICEOVER: "The expression is negative in the middle interval."
        
        # Highlight solution interval
        solution_line = Line(
            numberline.n2p(-1), numberline.n2p(3.5),
            color=self.COLOR_ANSWER, stroke_width=8
        ).shift(DOWN*0.1)
        
        self.play(Create(solution_line), run_time=2)
        self.pause_for_voiceover(3)
        
        self.play(FadeOut(step3), run_time=0.8)
        self.wait(1)
        
        # Final answer
        self.play(
            *[FadeOut(mob) for mob in [numberline, point1, point2, label1, label2,
                                       test_regions, solution_line, critical]],
            run_time=1
        )
        
        final = VGroup(
            MathTex(r"-1 \leq x \leq 3.5", font_size=48, color=self.COLOR_ANSWER),
            Text("or", font_size=32, color=WHITE),
            MathTex(r"x \in [-1; 3.5]", font_size=48, color=self.COLOR_ANSWER)
        ).arrange(DOWN, buff=0.5)
        
        self.play(Write(final), run_time=3)
        
        answer_box = self.highlight_box(final, color=self.COLOR_ANSWER)
        self.pause_for_voiceover(4)
        
        # VOICEOVER: "The solution is negative 1 less than or equal to x less than or equal to 3.5."
        
        self.wait(2)


# ============================================================================
# SCENE 4: EXPONENTIAL EQUATIONS
# ============================================================================

class ExponentialEquation(AlgebraLesson):
    def construct(self):
        # VOICEOVER: "Let's solve exponential equations using the same base strategy."
        
        title = self.show_title("Exponential Equations", "Using substitution and same base")
        self.play(title.animate.scale(0.7).to_edge(UP, buff=0.3), run_time=1.5)
        
        # Problem
        problem_text = Text("Solve for x:", font_size=self.FONT_STEP)
        problem_text.shift(UP*2.5)
        self.play(Write(problem_text), run_time=1.5)
        self.pause_for_voiceover(2)
        
        problem = self.show_equation(r"3^{2x} - 9 = 24 \cdot 3^x + 72", position=UP*1.5)
        self.play(Write(problem), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "Solve 3 to the power 2x minus 9 equals 24 times 3 to the x plus 72."
        
        # Step 1: Recognize pattern
        step1 = self.show_step("Recognize: 3²ˣ = (3ˣ)²", position=UP*0.3)
        self.play(FadeIn(step1), run_time=1.5)
        self.pause_for_voiceover(3)
        
        rewrite = self.show_equation(r"(3^x)^2 - 9 = 24 \cdot 3^x + 72", position=DOWN*0.3)
        self.play(Write(rewrite), run_time=2)
        self.pause_for_voiceover(3)
        
        self.play(FadeOut(step1), run_time=0.8)
        
        # Step 2: Substitution
        step2 = self.show_step("Let y = 3ˣ", position=UP*0.3, color=YELLOW)
        self.play(FadeIn(step2), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # VOICEOVER: "Let y equal 3 to the power x. This gives us a quadratic in y."
        
        substituted = self.show_equation(r"y^2 - 9 = 24y + 72", position=DOWN*0.3)
        self.play(Write(substituted), run_time=2)
        self.pause_for_voiceover(3)
        
        rearranged = self.show_equation(r"y^2 - 24y - 81 = 0", position=DOWN*1.2)
        self.play(Write(rearranged), run_time=2)
        self.pause_for_voiceover(3)
        
        self.play(FadeOut(step2), FadeOut(substituted), run_time=0.8)
        
        # Step 3: Solve quadratic
        step3 = self.show_step("Factor the quadratic:", position=UP*0.3)
        self.play(FadeIn(step3), run_time=1.5)
        self.pause_for_voiceover(2)
        
        factored = self.show_equation(r"(y - 27)(y + 3) = 0", position=ORIGIN)
        self.play(TransformMatchingTex(rearranged.copy(), factored), run_time=2)
        self.pause_for_voiceover(3)
        
        solutions_y = VGroup(
            MathTex("y = 27", font_size=36, color=YELLOW),
            Text("or", font_size=28, color=WHITE),
            MathTex("y = -3", font_size=36, color=RED)
        ).arrange(RIGHT, buff=0.5).shift(DOWN*1)
        
        self.play(Write(solutions_y), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "We get y equals 27 or y equals negative 3."
        
        self.play(FadeOut(step3), run_time=0.8)
        
        # Step 4: Substitute back
        step4 = self.show_step("Substitute back: y = 3ˣ", position=UP*0.3)
        self.play(FadeIn(step4), run_time=1.5)
        self.pause_for_voiceover(2)
        
        self.play(
            *[FadeOut(mob) for mob in [problem, rewrite, rearranged, factored]],
            run_time=1
        )
        
        sub_back = VGroup(
            MathTex("3^x = 27", font_size=36, color=YELLOW),
            Text("or", font_size=28, color=WHITE),
            MathTex("3^x = -3", font_size=36, color=RED)
        ).arrange(RIGHT, buff=0.5).shift(ORIGIN)
        
        self.play(TransformMatchingTex(solutions_y, sub_back), run_time=2)
        self.pause_for_voiceover(3)
        
        # Warning about negative
        warning = Text(
            "Reject! Exponential is always positive",
            font_size=24,
            color=RED
        ).next_to(sub_back[2], DOWN, buff=0.4)
        
        cross = Line(
            sub_back[2].get_corner(UL), sub_back[2].get_corner(DR),
            color=RED, stroke_width=4
        )
        
        self.play(Write(warning), Create(cross), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "We reject the negative value because exponentials are always positive."
        
        self.play(FadeOut(warning), FadeOut(cross), FadeOut(sub_back[1]), FadeOut(sub_back[2]), FadeOut(step4), run_time=1)
        
        # Solve valid equation
        step5 = self.show_step("Solve: 3ˣ = 27", position=UP*0.8)
        self.play(FadeIn(step5), run_time=1.5)
        self.pause_for_voiceover(2)
        
        express = self.show_equation(r"3^x = 3^3", position=ORIGIN)
        self.play(TransformMatchingTex(sub_back[0].copy(), express), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "27 equals 3 cubed, so x equals 3."
        
        self.play(FadeOut(step5), FadeOut(sub_back[0]), run_time=0.8)
        self.wait(1)
        
        # Final answer
        self.play(FadeOut(express), run_time=0.8)
        
        final = self.show_equation(r"x = 3", color=self.COLOR_ANSWER)
        final.scale(1.5)
        self.play(Write(final), run_time=2)
        
        answer_box = self.highlight_box(final, color=self.COLOR_ANSWER)
        self.pause_for_voiceover(3)
        
        self.wait(2)


# ============================================================================
# SCENE 5: SURD/RADICAL EQUATIONS
# ============================================================================

class SurdEquation(AlgebraLesson):
    def construct(self):
        # VOICEOVER: "Let's solve equations with square roots, also called surd equations."
        
        title = self.show_title("Surd Equations", "Solving equations with square roots")
        self.play(title.animate.scale(0.7).to_edge(UP, buff=0.3), run_time=1.5)
        
        # Problem
        problem_text = Text("Solve for x:", font_size=self.FONT_STEP)
        problem_text.shift(UP*2.5)
        self.play(Write(problem_text), run_time=1.5)
        self.pause_for_voiceover(2)
        
        problem = self.show_equation(r"\sqrt{x^2 + 14} = 3\sqrt{x}", position=UP*1.8)
        self.play(Write(problem), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "Solve the square root of x squared plus 14 equals 3 times the square root of x."
        
        # Step 1: Square both sides
        step1 = self.show_step("Step 1: Square both sides", position=UP*0.8)
        self.play(FadeIn(step1), run_time=1.5)
        self.pause_for_voiceover(2)
        
        squared_left = self.show_equation(r"(\sqrt{x^2 + 14})^2", position=ORIGIN+LEFT*2.5)
        equals = MathTex("=", font_size=40).move_to(ORIGIN)
        squared_right = self.show_equation(r"(3\sqrt{x})^2", position=ORIGIN+RIGHT*2.5)
        
        self.play(Write(squared_left), Write(equals), Write(squared_right), run_time=2)
        self.pause_for_voiceover(3)
        
        result = self.show_equation(r"x^2 + 14 = 9x", position=DOWN*0.8)
        self.play(Write(result), run_time=2)
        self.pause_for_voiceover(3)
        
        self.play(
            FadeOut(step1), FadeOut(squared_left), FadeOut(equals), FadeOut(squared_right),
            run_time=0.8
        )
        
        # Step 2: Rearrange and solve
        step2 = self.show_step("Step 2: Rearrange and solve", position=UP*0.8)
        self.play(FadeIn(step2), run_time=1.5)
        self.pause_for_voiceover(2)
        
        rearranged = self.show_equation(r"x^2 - 9x + 14 = 0", position=ORIGIN)
        self.play(TransformMatchingTex(result, rearranged), run_time=2)
        self.pause_for_voiceover(3)
        
        factored = self.show_equation(r"(x - 7)(x - 2) = 0", position=DOWN*0.8)
        self.play(Write(factored), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "This factors to x minus 7 times x minus 2 equals zero."
        
        solutions = VGroup(
            MathTex("x = 7", font_size=36, color=YELLOW),
            Text("or", font_size=28, color=WHITE),
            MathTex("x = 2", font_size=36, color=YELLOW)
        ).arrange(RIGHT, buff=0.5).shift(DOWN*1.8)
        
        self.play(Write(solutions), run_time=2)
        self.pause_for_voiceover(3)
        
        self.play(FadeOut(step2), run_time=0.8)
        
        # Step 3: CHECK solutions
        warning = Text(
            "⚠ MUST CHECK: Squaring can create false solutions!",
            font_size=26,
            color=self.COLOR_WARNING,
            weight=BOLD
        ).to_edge(UP, buff=1.2)
        
        self.play(Write(warning), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "Warning! We must check both solutions because squaring can create false solutions."
        
        self.play(
            *[FadeOut(mob) for mob in [problem, rearranged, factored]],
            run_time=1
        )
        
        # Check x = 7
        check1_title = Text("Check x = 7:", font_size=28, color=YELLOW).shift(UP*1.5)
        self.play(FadeOut(solutions), Write(check1_title), run_time=1.5)
        self.pause_for_voiceover(2)
        
        check1_lhs = MathTex(
            r"\text{LHS: } \sqrt{7^2 + 14} = \sqrt{63} = 3\sqrt{7}",
            font_size=32
        ).shift(UP*0.5)
        check1_rhs = MathTex(
            r"\text{RHS: } 3\sqrt{7}",
            font_size=32
        ).shift(DOWN*0.3)
        check1_result = MathTex(
            r"\text{LHS} = \text{RHS} \checkmark",
            font_size=32,
            color=GREEN
        ).shift(DOWN*1.2)
        
        self.play(Write(check1_lhs), run_time=2)
        self.pause_for_voiceover(3)
        self.play(Write(check1_rhs), run_time=2)
        self.pause_for_voiceover(2)
        self.play(Write(check1_result), run_time=1.5)
        self.pause_for_voiceover(2)
        
        self.play(
            *[FadeOut(mob) for mob in [check1_title, check1_lhs, check1_rhs, check1_result]],
            run_time=1
        )
        
        # Check x = 2
        check2_title = Text("Check x = 2:", font_size=28, color=YELLOW).shift(UP*1.5)
        self.play(Write(check2_title), run_time=1.5)
        self.pause_for_voiceover(2)
        
        check2_lhs = MathTex(
            r"\text{LHS: } \sqrt{2^2 + 14} = \sqrt{18} = 3\sqrt{2}",
            font_size=32
        ).shift(UP*0.5)
        check2_rhs = MathTex(
            r"\text{RHS: } 3\sqrt{2}",
            font_size=32
        ).shift(DOWN*0.3)
        check2_result = MathTex(
            r"\text{LHS} = \text{RHS} \checkmark",
            font_size=32,
            color=GREEN
        ).shift(DOWN*1.2)
        
        self.play(Write(check2_lhs), run_time=2)
        self.pause_for_voiceover(3)
        self.play(Write(check2_rhs), run_time=2)
        self.pause_for_voiceover(2)
        self.play(Write(check2_result), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # VOICEOVER: "Both solutions are valid!"
        
        self.play(
            *[FadeOut(mob) for mob in [check2_title, check2_lhs, check2_rhs, check2_result, warning]],
            run_time=1
        )
        self.wait(1)
        
        # Final answer
        final = self.show_equation(r"x = 2 \text{ or } x = 7", color=self.COLOR_ANSWER)
        final.scale(1.2)
        self.play(Write(final), run_time=2)
        
        answer_box = self.highlight_box(final, color=self.COLOR_ANSWER)
        self.pause_for_voiceover(3)
        
        self.wait(2)


# ============================================================================
# SCENE 6: SIMULTANEOUS EQUATIONS
# ============================================================================

class SimultaneousEquations(AlgebraLesson):
    def construct(self):
        # VOICEOVER: "Let's solve simultaneous equations where one is linear and one is non-linear."
        
        title = self.show_title("Simultaneous Equations", "One Linear + One Non-Linear")
        self.play(title.animate.scale(0.7).to_edge(UP, buff=0.3), run_time=1.5)
        
        # Problem
        problem_text = Text("Solve for x and y:", font_size=self.FONT_STEP)
        problem_text.shift(UP*2.5)
        self.play(Write(problem_text), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # Show both equations
        eq1 = self.show_equation(r"5x - y = 4", position=UP*1.8+LEFT*2)
        eq2 = self.show_equation(r"x^2 - x + y^2 = 4 - 3y", position=UP*1.8+RIGHT*2)
        
        self.play(Write(eq1), run_time=2)
        self.pause_for_voiceover(2)
        self.play(Write(eq2), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "We have 5x minus y equals 4, and x squared minus x plus y squared equals 4 minus 3y."
        
        # Step 1: Express y from linear equation
        step1 = self.show_step("Step 1: Express y from the linear equation", position=UP*0.5)
        self.play(FadeIn(step1), run_time=1.5)
        self.pause_for_voiceover(2)
        
        y_expr = self.show_equation(r"y = 5x - 4", color=self.COLOR_STEP, position=ORIGIN)
        self.play(Write(y_expr), run_time=2)
        self.pause_for_voiceover(3)
        
        # Highlight this for later
        box_y = self.highlight_box(y_expr, color=YELLOW)
        self.pause_for_voiceover(2)
        
        self.play(FadeOut(step1), FadeOut(box_y), run_time=0.8)
        
        # Step 2: Substitute
        step2 = self.show_step("Step 2: Substitute into the second equation", position=UP*0.5)
        self.play(FadeIn(step2), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # VOICEOVER: "Substitute y equals 5x minus 4 into the second equation."
        
        self.play(
            *[FadeOut(mob) for mob in [eq1, eq2]],
            run_time=0.8
        )
        
        substituted = self.show_equation(
            r"x^2 - x + (5x-4)^2 = 4 - 3(5x-4)",
            position=DOWN*0.5
        )
        self.play(Write(substituted), run_time=3)
        self.pause_for_voiceover(4)
        
        self.play(FadeOut(step2), run_time=0.8)
        
        # Step 3: Expand and simplify
        step3 = self.show_step("Step 3: Expand and simplify", position=UP*0.5)
        self.play(FadeIn(step3), run_time=1.5)
        self.pause_for_voiceover(2)
        
        expanded1 = self.show_equation(
            r"x^2 - x + 25x^2 - 40x + 16 = 4 - 15x + 12",
            position=ORIGIN
        )
        self.play(Write(expanded1), run_time=3)
        self.pause_for_voiceover(4)
        
        simplified = self.show_equation(
            r"26x^2 - 26x = 0",
            position=DOWN*0.8
        )
        self.play(Write(simplified), run_time=2)
        self.pause_for_voiceover(3)
        
        self.play(FadeOut(step3), FadeOut(substituted), FadeOut(expanded1), run_time=0.8)
        
        # Step 4: Solve for x
        step4 = self.show_step("Step 4: Factor and solve for x", position=UP*0.5)
        self.play(FadeIn(step4), run_time=1.5)
        self.pause_for_voiceover(2)
        
        factored = self.show_equation(r"26x(x - 1) = 0", position=ORIGIN)
        self.play(TransformMatchingTex(simplified.copy(), factored), run_time=2)
        self.pause_for_voiceover(3)
        
        x_solutions = VGroup(
            MathTex("x = 0", font_size=36, color=YELLOW),
            Text("or", font_size=28, color=WHITE),
            MathTex("x = 1", font_size=36, color=YELLOW)
        ).arrange(RIGHT, buff=0.5).shift(DOWN*0.8)
        
        self.play(Write(x_solutions), run_time=2)
        self.pause_for_voiceover(3)
        
        self.play(FadeOut(step4), run_time=0.8)
        
        # Step 5: Find y values
        step5 = self.show_step("Step 5: Find corresponding y values", position=UP*0.5)
        self.play(FadeIn(step5), run_time=1.5)
        self.pause_for_voiceover(2)
        
        self.play(*[FadeOut(mob) for mob in [simplified, factored]], run_time=0.8)
        
        # Show y = 5x - 4 again
        self.play(y_expr.animate.move_to(UP*0.8), run_time=1.5)
        
        # For x = 0
        calc1 = VGroup(
            MathTex(r"\text{For } x = 0:", font_size=32),
            MathTex(r"y = 5(0) - 4 = -4", font_size=32, color=self.COLOR_ANSWER)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).shift(LEFT*3+DOWN*0.5)
        
        self.play(Write(calc1), run_time=2)
        self.pause_for_voiceover(3)
        
        # For x = 1
        calc2 = VGroup(
            MathTex(r"\text{For } x = 1:", font_size=32),
            MathTex(r"y = 5(1) - 4 = 1", font_size=32, color=self.COLOR_ANSWER)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).shift(RIGHT*3+DOWN*0.5)
        
        self.play(Write(calc2), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "So we have two solution pairs: x equals 0, y equals negative 4; and x equals 1, y equals 1."
        
        self.play(FadeOut(step5), run_time=0.8)
        self.wait(1)
        
        # Final answer
        self.play(
            *[FadeOut(mob) for mob in [problem_text, y_expr, x_solutions, calc1, calc2]],
            run_time=1
        )
        
        final = VGroup(
            MathTex(r"(0; -4)", font_size=48, color=self.COLOR_ANSWER),
            Text("or", font_size=36, color=WHITE),
            MathTex(r"(1; 1)", font_size=48, color=self.COLOR_ANSWER)
        ).arrange(RIGHT, buff=0.8)
        
        self.play(Write(final), run_time=2)
        
        answer_box = self.highlight_box(final, color=self.COLOR_ANSWER)
        self.pause_for_voiceover(4)
        
        self.wait(2)


# ============================================================================
# SCENE 7: EXPONENT LAWS
# ============================================================================

class ExponentLaws(AlgebraLesson):
    def construct(self):
        # VOICEOVER: "Let's apply exponent laws to simplify complex expressions."
        
        title = self.show_title("Exponent Laws", "Simplifying with same base")
        self.play(title.animate.scale(0.7).to_edge(UP, buff=0.3), run_time=1.5)
        
        # Problem
        problem_text = Text("Find k:", font_size=self.FONT_STEP)
        problem_text.shift(UP*2.5)
        self.play(Write(problem_text), run_time=1.5)
        self.pause_for_voiceover(2)
        
        problem = self.show_equation(
            r"4^{24} + 8^{16} + 16^{12} + 64^8 = 2^k",
            position=UP*1.8
        )
        self.play(Write(problem), run_time=3)
        self.pause_for_voiceover(4)
        
        # VOICEOVER: "Find k if 4 to the 24, plus 8 to the 16, plus 16 to the 12, plus 64 to the 8, equals 2 to the k."
        
        # Show key insight
        insight = Text("Key: Express everything as powers of 2", font_size=28, color=YELLOW)
        insight.shift(UP*0.5)
        self.play(FadeIn(insight), run_time=2)
        self.pause_for_voiceover(3)
        
        # Show powers table
        powers_table = VGroup(
            MathTex(r"4 = 2^2", font_size=32),
            MathTex(r"8 = 2^3", font_size=32),
            MathTex(r"16 = 2^4", font_size=32),
            MathTex(r"64 = 2^6", font_size=32)
        ).arrange(RIGHT, buff=0.8).shift(ORIGIN)
        
        self.play(Write(powers_table), run_time=3)
        self.pause_for_voiceover(4)
        
        self.play(FadeOut(insight), run_time=0.8)
        
        # Step 1: Convert each term
        step1 = self.show_step("Step 1: Convert to base 2", position=UP*0.5)
        self.play(FadeIn(step1), run_time=1.5)
        self.pause_for_voiceover(2)
        
        self.play(FadeOut(powers_table), run_time=0.8)
        
        # Show conversions one by one
        conv1 = MathTex(r"4^{24} = (2^2)^{24} = 2^{48}", font_size=28, color=YELLOW)
        conv1.shift(UP*0.8+LEFT*3)
        self.play(Write(conv1), run_time=2)
        self.pause_for_voiceover(2)
        
        conv2 = MathTex(r"8^{16} = (2^3)^{16} = 2^{48}", font_size=28, color=YELLOW)
        conv2.shift(UP*0.8+RIGHT*3)
        self.play(Write(conv2), run_time=2)
        self.pause_for_voiceover(2)
        
        conv3 = MathTex(r"16^{12} = (2^4)^{12} = 2^{48}", font_size=28, color=YELLOW)
        conv3.shift(DOWN*0.5+LEFT*3)
        self.play(Write(conv3), run_time=2)
        self.pause_for_voiceover(2)
        
        conv4 = MathTex(r"64^8 = (2^6)^8 = 2^{48}", font_size=28, color=YELLOW)
        conv4.shift(DOWN*0.5+RIGHT*3)
        self.play(Write(conv4), run_time=2)
        self.pause_for_voiceover(2)
        
        # VOICEOVER: "Notice that all four terms equal 2 to the 48!"
        
        self.play(FadeOut(step1), run_time=0.8)
        
        # Step 2: Substitute
        step2 = self.show_step("Step 2: Substitute back", position=UP*0.5)
        self.play(FadeIn(step2), run_time=1.5)
        self.pause_for_voiceover(2)
        
        self.play(
            *[FadeOut(mob) for mob in [conv1, conv2, conv3, conv4, problem]],
            run_time=1
        )
        
        substituted = self.show_equation(
            r"2^{48} + 2^{48} + 2^{48} + 2^{48} = 2^k",
            position=UP*0.8
        )
        self.play(Write(substituted), run_time=3)
        self.pause_for_voiceover(4)
        
        self.play(FadeOut(step2), run_time=0.8)
        
        # Step 3: Add same powers
        step3 = self.show_step("Step 3: Add the terms", position=UP*0.5)
        self.play(FadeIn(step3), run_time=1.5)
        self.pause_for_voiceover(2)
        
        added = self.show_equation(r"4 \times 2^{48} = 2^k", position=ORIGIN)
        self.play(Write(added), run_time=2)
        self.pause_for_voiceover(3)
        
        self.play(FadeOut(step3), run_time=0.8)
        
        # Step 4: Express 4 as power of 2
        step4 = self.show_step("Step 4: Express 4 as 2²", position=UP*0.5)
        self.play(FadeIn(step4), run_time=1.5)
        self.pause_for_voiceover(2)
        
        final_expr = self.show_equation(r"2^2 \times 2^{48} = 2^k", position=DOWN*0.5)
        self.play(Write(final_expr), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "Using the law: 2 squared times 2 to the 48 equals 2 to the 50."
        
        simplified = self.show_equation(r"2^{50} = 2^k", position=DOWN*1.5)
        self.play(Write(simplified), run_time=2)
        self.pause_for_voiceover(3)
        
        self.play(FadeOut(step4), run_time=0.8)
        
        # Final answer
        self.play(
            *[FadeOut(mob) for mob in [problem_text, substituted, added, final_expr, simplified]],
            run_time=1
        )
        
        final = self.show_equation(r"k = 50", color=self.COLOR_ANSWER)
        final.scale(1.5)
        self.play(Write(final), run_time=2)
        
        answer_box = self.highlight_box(final, color=self.COLOR_ANSWER)
        self.pause_for_voiceover(3)
        
        self.wait(2)


# ============================================================================
# SCENE 8: DIFFERENCE OF SQUARES (BONUS)
# ============================================================================

class DifferenceOfSquares(AlgebraLesson):
    def construct(self):
        # VOICEOVER: "Here's a powerful factorization pattern: difference of squares."
        
        title = self.show_title("Difference of Squares", "a² - b² = (a - b)(a + b)")
        self.play(title.animate.scale(0.7).to_edge(UP, buff=0.3), run_time=1.5)
        
        # Show the pattern
        pattern_label = Text("The Pattern:", font_size=self.FONT_STEP)
        pattern_label.shift(UP*2)
        self.play(Write(pattern_label), run_time=1.5)
        self.pause_for_voiceover(2)
        
        pattern = self.show_equation(
            r"a^2 - b^2 = (a - b)(a + b)",
            color=self.COLOR_HIGHLIGHT,
            position=UP*1
        )
        self.play(Write(pattern), run_time=3)
        self.pause_for_voiceover(4)
        
        box = self.highlight_box(pattern, color=self.COLOR_HIGHLIGHT)
        self.pause_for_voiceover(2)
        
        self.play(FadeOut(box), FadeOut(pattern_label), run_time=1)
        
        # Example 1
        ex1_text = Text("Example 1:", font_size=self.FONT_STEP)
        ex1_text.shift(UP*2)
        self.play(
            Transform(title, ex1_text),
            pattern.animate.scale(0.5).to_edge(RIGHT).shift(UP*2),
            run_time=1.5
        )
        
        problem1 = self.show_equation(r"x^2 - 25", position=UP*0.8)
        self.play(Write(problem1), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "Factor x squared minus 25."
        
        # Recognize pattern
        recognize = VGroup(
            MathTex(r"a = x", font_size=32, color=YELLOW),
            MathTex(r"b = 5", font_size=32, color=YELLOW)
        ).arrange(RIGHT, buff=1.5).shift(ORIGIN)
        
        self.play(Write(recognize), run_time=2)
        self.pause_for_voiceover(3)
        
        # Apply pattern
        solution1 = self.show_equation(
            r"= (x - 5)(x + 5)",
            color=self.COLOR_ANSWER,
            position=DOWN*0.8
        )
        self.play(Write(solution1), run_time=2)
        self.pause_for_voiceover(3)
        
        self.wait(1)
        self.play(
            *[FadeOut(mob) for mob in [problem1, recognize, solution1]],
            run_time=1
        )
        
        # Example 2: More complex
        ex2_text = Text("Example 2:", font_size=self.FONT_STEP)
        ex2_text.shift(UP*2)
        self.play(Transform(title, ex2_text), run_time=1.5)
        
        problem2 = self.show_equation(r"9x^2 - 16y^2", position=UP*0.8)
        self.play(Write(problem2), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "Factor 9 x squared minus 16 y squared."
        
        recognize2 = VGroup(
            MathTex(r"a = 3x", font_size=32, color=YELLOW),
            MathTex(r"b = 4y", font_size=32, color=YELLOW)
        ).arrange(RIGHT, buff=1.5).shift(ORIGIN)
        
        self.play(Write(recognize2), run_time=2)
        self.pause_for_voiceover(3)
        
        solution2 = self.show_equation(
            r"= (3x - 4y)(3x + 4y)",
            color=self.COLOR_ANSWER,
            position=DOWN*0.8
        )
        self.play(Write(solution2), run_time=2)
        self.pause_for_voiceover(3)
        
        answer_box = self.highlight_box(solution2, color=self.COLOR_ANSWER)
        self.pause_for_voiceover(2)
        
        self.wait(2)


# ============================================================================
# ============================================================================
# SCENE 9: COMPLETING THE SQUARE (BONUS) - ENHANCED UI/UX
# ============================================================================

class CompletingTheSquare(AlgebraLesson):
    def construct(self):
        # Enhanced color palette for better visual hierarchy
        COLOR_PRIMARY = "#3498db"      # Blue
        COLOR_ACCENT = "#e74c3c"       # Red  
        COLOR_SUCCESS = "#2ecc71"      # Green
        COLOR_WARNING = "#f39c12"      # Orange
        COLOR_INFO = "#9b59b6"         # Purple
        COLOR_LIGHT = "#ecf0f1"        # Light gray
        COLOR_BG = "#1a1a2e"           # Dark blue background
        
        # Set background color
        self.camera.background_color = COLOR_BG
        
        # VOICEOVER: "Completing the square is a powerful technique for solving quadratics and has many applications in mathematics."
        
        # Animated title entrance
        title = self.show_title("Completing the Square", "Converting to perfect square form")
        self.play(
            title.animate.scale(0.7).to_edge(UP, buff=0.3),
            run_time=2,
            rate_func=smooth
        )
        self.wait(0.5)
        
        # ========================================================================
        # INTRODUCTION: Why this method?
        # ========================================================================
        
        intro_title = Text("Why Completing the Square?", font_size=36, color=COLOR_WARNING)
        intro_title.to_edge(UP, buff=1.2)
        self.play(
            Write(intro_title),
            run_time=1.8,
            rate_func=smooth
        )
        self.pause_for_voiceover(2)
        
        # Bullet points with staggered entrance - left aligned
        bullets = VGroup(
            VGroup(
                Dot(color=COLOR_SUCCESS, radius=0.08),
                Text("Works for ANY quadratic equation", font_size=26)
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Dot(color=COLOR_SUCCESS, radius=0.08),
                Text("Reveals vertex form of parabola", font_size=26)
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Dot(color=COLOR_SUCCESS, radius=0.08),
                Text("Foundation for quadratic formula", font_size=26)
            ).arrange(RIGHT, buff=0.3)
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        bullets.shift(LEFT*2)
        
        for i, bullet in enumerate(bullets):
            self.play(
                FadeIn(bullet, shift=RIGHT*0.5),
                run_time=1.2,
                rate_func=smooth
            )
            self.pause_for_voiceover(1.5)
        
        self.wait(1)
        self.play(
            FadeOut(intro_title, shift=UP*0.3),
            FadeOut(bullets, shift=DOWN*0.3),
            FadeOut(title),
            run_time=1.2
        )
        
        # ========================================================================
        # EXAMPLE 1: Standard case - CLEAN LAYOUT
        # ========================================================================
        
        # New clean title for example
        example1_title = Text("Example 1: Standard Form", font_size=40, color=COLOR_PRIMARY)
        example1_title.to_edge(UP, buff=0.4)
        self.play(Write(example1_title), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # Problem label and equation - properly spaced
        problem_text = Text("Solve:", font_size=32, color=COLOR_ACCENT)
        problem_text.shift(UP*2.5)
        
        problem = self.show_equation(r"x^2 + 6x + 5 = 0", position=UP*1.8)
        
        self.play(Write(problem_text), run_time=1)
        self.pause_for_voiceover(1)
        self.play(Write(problem), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "Let's solve x squared plus 6x plus 5 equals zero."
        
        # Clear divider
        divider = Line(LEFT*6.5, RIGHT*6.5, color=COLOR_LIGHT, stroke_width=1.5)
        divider.shift(UP*1.2)
        self.play(Create(divider), run_time=0.8)
        self.wait(0.5)
        
        # Step 1: Move constant - left aligned label, centered equation
        step1 = Text("Step 1: Move constant to right", font_size=26, color=COLOR_WARNING)
        step1.to_edge(LEFT, buff=0.5).shift(UP*0.7)
        self.play(FadeIn(step1, shift=RIGHT*0.3), run_time=1.5)
        self.pause_for_voiceover(2)
        
        moved = self.show_equation(r"x^2 + 6x = -5", position=ORIGIN)
        self.play(Write(moved), run_time=2)
        self.pause_for_voiceover(3)
        
        self.play(FadeOut(step1), run_time=0.8)
        
        # Step 2: Half coefficient, square it (with visual) - left aligned label
        step2 = Text("Step 2: Half of b, then square", font_size=26, color=COLOR_WARNING)
        step2.to_edge(LEFT, buff=0.5).shift(UP*0.7)
        self.play(FadeIn(step2, shift=RIGHT*0.3), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # Show the calculation visually - left aligned
        calc_half = VGroup(
            MathTex(r"\text{Coefficient: } b = 6", font_size=26),
            MathTex(r"\text{Half: } \frac{b}{2} = 3", font_size=26, color=YELLOW),
            MathTex(r"\text{Square: } 3^2 = 9", font_size=26, color=YELLOW)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        calc_half.to_edge(LEFT, buff=1).shift(DOWN*1.2)
        
        for line in calc_half:
            self.play(Write(line), run_time=1.5)
            self.pause_for_voiceover(2)
        
        # VOICEOVER: "Take half the coefficient of x, which is 3, and square it to get 9."
        
        self.play(FadeOut(step2), FadeOut(calc_half), run_time=0.8)
        
        # Step 3: Add to both sides - CLEAR previous equation first
        self.play(FadeOut(moved), run_time=0.6)
        
        step3 = Text("Step 3: Add 9 to both sides", font_size=26, color=COLOR_WARNING)
        step3.to_edge(LEFT, buff=0.5).shift(UP*0.7)
        self.play(FadeIn(step3, shift=RIGHT*0.3), run_time=1.5)
        self.pause_for_voiceover(2)
        
        added = self.show_equation(r"x^2 + 6x + 9 = -5 + 9", position=UP*0.2)
        self.play(Write(added), run_time=2)
        self.pause_for_voiceover(3)
        
        simplified_right = self.show_equation(r"x^2 + 6x + 9 = 4", position=DOWN*0.6)
        self.play(Write(simplified_right), run_time=2)
        self.pause_for_voiceover(2)
        
        self.play(FadeOut(step3), FadeOut(added), run_time=0.8)
        
        # Step 4: Factor left side - CLEAR previous equation first
        self.play(FadeOut(simplified_right), run_time=0.6)
        
        step4 = Text("Step 4: Factor as perfect square", font_size=26, color=COLOR_WARNING)
        step4.to_edge(LEFT, buff=0.5).shift(UP*0.7)
        self.play(FadeIn(step4, shift=RIGHT*0.3), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # Show the equation again then factor
        refactoring = self.show_equation(r"x^2 + 6x + 9 = 4", position=UP*0.3)
        self.play(Write(refactoring), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # Show factoring pattern - centered
        pattern_reminder = MathTex(r"x^2 + 6x + 9 = (x+3)^2", font_size=26, color=GREEN)
        pattern_reminder.shift(DOWN*0.5)
        self.play(Write(pattern_reminder), run_time=2)
        self.pause_for_voiceover(3)
        
        factored = self.show_equation(r"(x + 3)^2 = 4", position=DOWN*1.5)
        self.play(Write(factored), run_time=2)
        self.pause_for_voiceover(3)
        
        self.play(FadeOut(step4), FadeOut(pattern_reminder), FadeOut(refactoring), run_time=0.8)
        
        # Step 5: Square root both sides - CLEAR previous equation first
        self.play(FadeOut(factored), run_time=0.6)
        
        step5 = Text("Step 5: Square root both sides", font_size=26, color=COLOR_WARNING)
        step5.to_edge(LEFT, buff=0.5).shift(UP*0.7)
        self.play(FadeIn(step5, shift=RIGHT*0.3), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # Show equation again
        factored2 = self.show_equation(r"(x + 3)^2 = 4", position=UP*0.3)
        self.play(Write(factored2), run_time=1.5)
        self.pause_for_voiceover(1.5)
        
        sqrt_show = self.show_equation(r"\sqrt{(x + 3)^2} = \pm\sqrt{4}", position=ORIGIN)
        self.play(Write(sqrt_show), run_time=2)
        self.pause_for_voiceover(3)
        
        sqrt_both = self.show_equation(r"x + 3 = \pm 2", position=DOWN*0.9)
        self.play(Write(sqrt_both), run_time=2)
        self.pause_for_voiceover(3)
        
        self.play(FadeOut(step5), FadeOut(sqrt_show), FadeOut(factored2), run_time=0.8)
        
        # Step 6: Solve - CLEAR previous equation first
        self.play(FadeOut(sqrt_both), run_time=0.6)
        
        step6 = Text("Step 6: Solve for x", font_size=26, color=COLOR_WARNING)
        step6.to_edge(LEFT, buff=0.5).shift(UP*0.7)
        self.play(FadeIn(step6, shift=RIGHT*0.3), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # Show the equation we're solving
        solving = self.show_equation(r"x + 3 = \pm 2", position=UP*0.3)
        self.play(Write(solving), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # VOICEOVER: "So x equals negative 3 plus or minus 2, giving us two solutions."
        
        # Solutions - centered
        solutions = VGroup(
            MathTex(r"x = -3 + 2 = -1", font_size=34, color=self.COLOR_ANSWER),
            Text("or", font_size=26, color=WHITE),
            MathTex(r"x = -3 - 2 = -5", font_size=34, color=self.COLOR_ANSWER)
        ).arrange(DOWN, buff=0.4).shift(DOWN*1.5)
        
        self.play(Write(solutions), run_time=3)
        self.pause_for_voiceover(4)
        
        self.play(FadeOut(step6), FadeOut(solving), run_time=0.8)
        
        # Show final answer - clear everything first
        self.play(
            *[FadeOut(mob) for mob in [problem_text, problem, divider, solutions]],
            run_time=1
        )
        
        final = self.show_equation(r"x = -1 \text{ or } x = -5", color=self.COLOR_ANSWER)
        final.scale(1.2)
        self.play(Write(final), run_time=2)
        
        answer_box = self.highlight_box(final, color=self.COLOR_ANSWER)
        self.pause_for_voiceover(3)
        
        self.wait(1)
        
        # Clear for example 2
        self.play(
            *[FadeOut(mob) for mob in [example1_title, solutions, final, answer_box]],
            run_time=1.5
        )
        self.wait(1)
        
        # ========================================================================
        # EXAMPLE 2: With leading coefficient ≠ 1
        # ========================================================================
        
        # VOICEOVER: "Now let's try a harder example where the coefficient of x squared is not 1."
        
        example2_label = Text("Example 2: Leading Coefficient ≠ 1", font_size=self.FONT_STEP, color=YELLOW)
        example2_label.to_edge(UP, buff=1)
        self.play(Write(example2_label), run_time=1.5)
        self.pause_for_voiceover(2)
        
        problem2_text = Text("Solve for x:", font_size=self.FONT_STEP)
        problem2_text.shift(UP*2.5)
        self.play(Write(problem2_text), run_time=1.5)
        self.pause_for_voiceover(2)
        
        problem2 = self.show_equation(r"2x^2 + 12x + 10 = 0", position=UP*2)
        self.play(Write(problem2), run_time=2)
        self.pause_for_voiceover(3)
        
        # Key step: Divide by leading coefficient
        key_step = self.show_step("Key: First divide everything by 2", position=UP*0.8)
        self.play(FadeIn(key_step), run_time=1.5)
        self.pause_for_voiceover(3)
        
        divided = self.show_equation(r"x^2 + 6x + 5 = 0", position=UP*0.2)
        self.play(Write(divided), run_time=2)
        self.pause_for_voiceover(3)
        
        # Point out it's the same as Example 1
        notice = Text("Notice: This is Example 1!", font_size=28, color=GREEN)
        notice.shift(ORIGIN)
        self.play(FadeIn(notice), run_time=1.5)
        self.pause_for_voiceover(3)
        
        self.play(FadeOut(key_step), FadeOut(notice), run_time=1)
        
        # Fast-forward through solution
        fast_text = Text("Using the same method...", font_size=self.FONT_STEP)
        fast_text.shift(ORIGIN)
        self.play(FadeIn(fast_text), run_time=1.5)
        self.pause_for_voiceover(2)
        self.play(FadeOut(fast_text), run_time=1)
        
        # Show key steps quickly
        quick_step1 = self.show_equation(r"x^2 + 6x = -5", position=UP*0.5)
        self.play(Write(quick_step1), run_time=1.5)
        self.pause_for_voiceover(2)
        
        quick_step2 = self.show_equation(r"x^2 + 6x + 9 = 4", position=ORIGIN)
        self.play(Write(quick_step2), run_time=1.5)
        self.pause_for_voiceover(2)
        
        quick_step3 = self.show_equation(r"(x+3)^2 = 4", position=DOWN*0.5)
        self.play(Write(quick_step3), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # Same answer
        self.play(
            *[FadeOut(mob) for mob in [problem2_text, problem2, divided, quick_step1, quick_step2, quick_step3]],
            run_time=1
        )
        
        final2 = self.show_equation(r"x = -1 \text{ or } x = -5", color=self.COLOR_ANSWER)
        final2.scale(1.3)
        self.play(Write(final2), run_time=2)
        
        answer_box2 = self.highlight_box(final2, color=self.COLOR_ANSWER)
        self.pause_for_voiceover(3)
        
        self.wait(1)
        self.play(FadeOut(example2_label), FadeOut(final2), FadeOut(answer_box2), run_time=1.5)
        
        # ========================================================================
        # GENERAL PATTERN
        # ========================================================================
        
        # VOICEOVER: "Here's the general pattern you can memorize for completing the square."
        
        pattern_title = Text("General Pattern", font_size=36, color=YELLOW)
        pattern_title.to_edge(UP, buff=0.5)
        self.play(Write(pattern_title), run_time=2)
        self.pause_for_voiceover(2)
        
        # Show general form
        general = VGroup(
            MathTex(r"x^2 + bx + c = 0", font_size=36),
            MathTex(r"\Downarrow", font_size=36, color=YELLOW),
            MathTex(r"x^2 + bx = -c", font_size=36),
            MathTex(r"\Downarrow", font_size=36, color=YELLOW),
            MathTex(r"x^2 + bx + \left(\frac{b}{2}\right)^2 = -c + \left(\frac{b}{2}\right)^2", font_size=32),
            MathTex(r"\Downarrow", font_size=36, color=YELLOW),
            MathTex(r"\left(x + \frac{b}{2}\right)^2 = -c + \left(\frac{b}{2}\right)^2", font_size=32, color=GREEN)
        ).arrange(DOWN, buff=0.3)
        general.shift(DOWN*0.3)
        
        for line in general:
            self.play(Write(line), run_time=1.5)
            self.pause_for_voiceover(2)
        
        # Highlight the key formula
        key_box = self.highlight_box(general[-1], color=GREEN)
        self.pause_for_voiceover(4)
        
        # VOICEOVER: "This formula shows that for any quadratic, you can complete the square by adding the square of half the coefficient of x."
        
        self.wait(2)
        
        # Final summary
        self.play(FadeOut(general), FadeOut(key_box), run_time=1)
        
        summary_title = Text("Remember:", font_size=36, color=YELLOW)
        summary_title.to_edge(UP, buff=0.8)
        
        summary_points = VGroup(
            Text("1. If a ≠ 1, divide through by a first", font_size=28),
            Text("2. Move constant to right side", font_size=28),
            Text("3. Add (b/2)² to both sides", font_size=28),
            Text("4. Factor left side as perfect square", font_size=28),
            Text("5. Take square root and solve", font_size=28)
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        summary_points.shift(DOWN*0.5)
        
        self.play(Transform(pattern_title, summary_title), run_time=1.5)
        
        for point in summary_points:
            self.play(FadeIn(point, shift=RIGHT*0.3), run_time=1.2)
            self.pause_for_voiceover(2)
        
        self.pause_for_voiceover(3)
        self.wait(3)


# ============================================================================
# MAIN RENDERING (for testing individual scenes)
# ============================================================================

if __name__ == "__main__":
    # Render all scenes:
    # manim -pql algebra_lessons.py QuadraticFactorization
    # manim -pql algebra_lessons.py QuadraticFormula
    # manim -pql algebra_lessons.py QuadraticInequality
    # manim -pql algebra_lessons.py ExponentialEquation
    # manim -pql algebra_lessons.py SurdEquation
    # manim -pql algebra_lessons.py SimultaneousEquations
    # manim -pql algebra_lessons.py ExponentLaws
    # manim -pql algebra_lessons.py DifferenceOfSquares
    # manim -pql algebra_lessons.py CompletingTheSquare
    pass
