from manim import *

# ---------- GLOBAL DESIGN SYSTEM ----------

ARITH_COLOR = BLUE_C
GEO_COLOR = RED_C
SIGMA_COLOR = YELLOW_C
TEXT_COLOR = WHITE
HIGHLIGHT_COLOR = GREEN_C

BG_COLOR = "#0E1A25"

config.background_color = BG_COLOR


class BaseLesson(Scene):
    """Base class with reusable helper methods"""
    
    # Color scheme
    COLOR_BG = BG_COLOR
    COLOR_ARITH = ARITH_COLOR
    COLOR_GEO = GEO_COLOR
    COLOR_SIGMA = SIGMA_COLOR
    COLOR_TEXT = TEXT_COLOR
    COLOR_HIGHLIGHT = HIGHLIGHT_COLOR
    COLOR_WARNING = "#f39c12"
    COLOR_INFO = "#9b59b6"
    COLOR_LIGHT = "#ecf0f1"
    COLOR_ANSWER = HIGHLIGHT_COLOR
    
    FONT_TITLE = 48
    FONT_SUBTITLE = 36
    FONT_STEP = 28
    FONT_BODY = 24
    
    def construct(self):
        self.camera.background_color = self.COLOR_BG
    
    def lesson_title(self, text, color=WHITE):
        """Animated title that fades in and moves to top"""
        title = Text(text, font_size=self.FONT_TITLE, color=color)
        self.play(FadeIn(title, shift=UP), run_time=1.5)
        self.wait(1)
        self.play(title.animate.to_edge(UP, buff=0.8), run_time=1)
        return title
    
    def section_divider(self, text, color=None):
        """Temporary section divider"""
        if color is None:
            color = GREY_A
        divider = Text(text, font_size=self.FONT_SUBTITLE, color=color)
        self.play(FadeIn(divider), run_time=1)
        self.wait(1.5)
        self.play(FadeOut(divider), run_time=0.8)
    
    def show_equation(self, tex_string, position=ORIGIN, color=WHITE, font_size=36):
        """Helper to display mathematical equations"""
        eq = MathTex(tex_string, font_size=font_size, color=color)
        eq.move_to(position)
        return eq
    
    def show_step(self, step_text, position=ORIGIN, color=None, font_size=28):
        """Helper to display step labels"""
        if color is None:
            color = self.COLOR_WARNING
        step = Text(step_text, font_size=font_size, color=color)
        step.move_to(position)
        return step
    
    def highlight_box(self, mobject, color=None, buff=0.3):
        """Create a highlighted box around a mobject"""
        if color is None:
            color = self.COLOR_HIGHLIGHT
        box = SurroundingRectangle(mobject, color=color, buff=buff, corner_radius=0.1)
        self.play(Create(box), run_time=1)
        return box
    
    def pause_for_voiceover(self, duration=1):
        """Placeholder for voiceover timing"""
        self.wait(duration)


class ArithmeticSequence(BaseLesson):
    """Arithmetic sequence: The Linear Machine"""
    
    def construct(self):
        super().construct()
        
        # Title with helper
        title = self.lesson_title("Arithmetic Sequences: The Linear Machine", self.COLOR_ARITH)
        
        # PART 1: The DNA - Constant Difference
        self.section_divider("The DNA: Constant Difference", self.COLOR_WARNING)
        
        terms = [2, 5, 8, 11, 14, "..."]
        term_mobs = VGroup(*[MathTex(str(t), font_size=36, color=self.COLOR_ARITH) for t in terms])
        term_mobs.arrange(RIGHT, buff=0.5).shift(UP*1.5)
        
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN) for t in term_mobs], lag_ratio=0.3), run_time=3)
        self.wait(1)
        
        # Show common difference
        arrows = VGroup()
        labels = VGroup()
        for i in range(len(terms) - 2):
            arrow = Arrow(term_mobs[i].get_right(), term_mobs[i+1].get_left(), buff=0.1, 
                         color=self.COLOR_HIGHLIGHT, stroke_width=3)
            label = MathTex("+3", font_size=20, color=self.COLOR_HIGHLIGHT).next_to(arrow, UP, buff=0.1)
            arrows.add(arrow)
            labels.add(label)
        
        self.play(LaggedStart(*[AnimationGroup(Create(a), Write(l)) for a, l in zip(arrows, labels)], lag_ratio=0.2), run_time=2.5)
        self.wait(1)
        
        # Emphasize d as DNA
        dna_text = Text("d = 3  (This is the DNA of the sequence)", font_size=24, color=self.COLOR_HIGHLIGHT)
        dna_text.shift(DOWN*0.5)
        self.play(Write(dna_text), run_time=2)
        self.wait(1)
        
        rule = Text("If d is constant → the sequence is LINEAR", font_size=22, color=self.COLOR_INFO)
        rule.shift(DOWN*1.2)
        self.play(FadeIn(rule, shift=UP), run_time=1.5)
        self.wait(1.5)
        
        self.play(FadeOut(term_mobs), FadeOut(arrows), FadeOut(labels), FadeOut(dna_text), FadeOut(rule), run_time=1)
        
        # PART 2: Linear Engine - Formula Connection
        self.section_divider("The Linear Engine", self.COLOR_WARNING)
        
        # Standard formula
        formula1 = MathTex(r"a_n = a_1 + (n-1)d", font_size=40, color=self.COLOR_ARITH).shift(UP*1.8)
        self.play(Write(formula1), run_time=2)
        self.wait(1)
        
        interpretation = VGroup(
            Text("starting value", font_size=22, color=self.COLOR_INFO),
            Text("+", font_size=22),
            Text("(steps taken)", font_size=22, color=self.COLOR_INFO),
            Text("×", font_size=22),
            Text("(step size)", font_size=22, color=self.COLOR_HIGHLIGHT)
        ).arrange(RIGHT, buff=0.3).shift(UP*0.9)
        
        self.play(Write(interpretation), run_time=2.5)
        self.wait(1.5)
        
        # Rewrite as linear function
        arrow_transform = Arrow(UP*0.3, DOWN*0.3, color=self.COLOR_WARNING)
        self.play(Create(arrow_transform), run_time=1)
        
        formula2 = MathTex(r"a_n = dn + (a_1 - d)", font_size=40, color=self.COLOR_ARITH).shift(DOWN*0.8)
        self.play(Write(formula2), run_time=2)
        self.wait(1)
        
        # Connect to y = mx + c
        linear_form = MathTex(r"y = mx + c", font_size=40, color=self.COLOR_HIGHLIGHT).shift(DOWN*1.8)
        connection = Text("This is a straight line!", font_size=24, color=self.COLOR_HIGHLIGHT).shift(DOWN*2.7)
        
        self.play(Write(linear_form), run_time=2)
        self.play(FadeIn(connection, shift=UP), run_time=1.5)
        self.wait(2)
        
        self.play(FadeOut(VGroup(formula1, interpretation, arrow_transform, formula2, linear_form, connection)), run_time=1)
        
        # PART 3: Geometric Interpretation
        self.section_divider("Geometric View", self.COLOR_WARNING)
        
        # Create axes
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 16, 2],
            x_length=5,
            y_length=4,
            axis_config={"color": GREY_A, "include_tip": True},
            tips=True
        ).shift(DOWN*0.5)
        
        axes_labels = axes.get_axis_labels(x_label="n", y_label="a_n")
        self.play(Create(axes), Write(axes_labels), run_time=2)
        self.wait(0.5)
        
        # Plot points for sequence 2, 5, 8, 11, 14
        points_data = [(1, 2), (2, 5), (3, 8), (4, 11), (5, 14)]
        dots = VGroup(*[Dot(axes.coords_to_point(n, val), color=self.COLOR_ARITH) for n, val in points_data])
        
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.3), run_time=2)
        self.wait(1)
        
        # Draw line through points
        line = axes.plot(lambda x: 3*x - 1, x_range=[0.8, 5.2], color=self.COLOR_HIGHLIGHT, stroke_width=3)
        self.play(Create(line), run_time=2)
        self.wait(1)
        
        insight = Text("Discrete sampling of a continuous line", font_size=22, color=self.COLOR_INFO)
        insight.to_edge(UP, buff=1.5)
        self.play(Write(insight), run_time=2)
        self.wait(2)
        
        self.play(FadeOut(VGroup(axes, axes_labels, dots, line, insight)), run_time=1)
        
        # PART 4: Behavior Analysis
        self.section_divider("Behavior Analysis", self.COLOR_WARNING)
        
        behaviors = VGroup(
            VGroup(
                Text("d > 0  →", font_size=24, color=self.COLOR_HIGHLIGHT),
                Text("Increasing", font_size=24, color=self.COLOR_INFO)
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("d < 0  →", font_size=24, color=RED),
                Text("Decreasing", font_size=24, color=self.COLOR_INFO)
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("d = 0  →", font_size=24, color=GREY_B),
                Text("Constant", font_size=24, color=self.COLOR_INFO)
            ).arrange(RIGHT, buff=0.3)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).shift(UP*0.8)
        
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT) for b in behaviors], lag_ratio=0.4), run_time=3)
        self.wait(2)
        
        # Example: decreasing sequence
        example_desc = Text("Example: d = -2 (Linear Decay)", font_size=24, color=RED).shift(DOWN*0.8)
        self.play(Write(example_desc), run_time=1.5)
        
        dec_seq = MathTex(r"15, 13, 11, 9, 7, ...", font_size=32, color=RED).shift(DOWN*1.5)
        self.play(Write(dec_seq), run_time=2)
        self.wait(2)
        
        self.play(FadeOut(VGroup(behaviors, example_desc, dec_seq)), run_time=1)
        
        # PART 5: Finding nth Term - Structural Thinking
        self.section_divider("Finding nth Term", self.COLOR_WARNING)
        
        problem_text = Text("Find n when sequence reaches -121:", font_size=26, color=self.COLOR_WARNING)
        problem_text.to_edge(UP, buff=1.5)
        self.play(Write(problem_text), run_time=1.5)
        self.wait(0.5)
        
        seq_given = MathTex(r"15, 13, 11, 9, ..., -121", font_size=32, color=self.COLOR_ARITH).shift(UP*1.5)
        self.play(Write(seq_given), run_time=2)
        self.wait(1)
        
        # Given values
        given_vals = VGroup(
            MathTex(r"a_1 = 15", font_size=26),
            MathTex(r"d = -2", font_size=26),
            MathTex(r"a_n = -121", font_size=26)
        ).arrange(RIGHT, buff=1).shift(UP*0.6)
        self.play(Write(given_vals), run_time=2)
        self.wait(1)
        
        # Solution steps
        steps = [
            (r"-121 = 15 + (n-1)(-2)", 26),
            (r"-121 = 15 - 2(n-1)", 26),
            (r"-136 = -2(n-1)", 26),
            (r"68 = n - 1", 26),
            (r"n = 69", 32)
        ]
        
        pos = DOWN*0.2
        for i, (step_text, size) in enumerate(steps):
            is_answer = (i == len(steps) - 1)
            color = self.COLOR_ANSWER if is_answer else WHITE
            step = MathTex(step_text, font_size=size, color=color).shift(pos)
            self.play(Write(step), run_time=1.5)
            self.wait(1)
            if not is_answer:
                self.play(FadeOut(step), run_time=0.5)
        
        box = self.highlight_box(step, color=self.COLOR_ANSWER)
        
        conclusion = Text("The sequence reaches -121 at the 69th step", font_size=20, color=self.COLOR_INFO)
        conclusion.shift(DOWN*1.5)
        self.play(FadeIn(conclusion, shift=UP), run_time=1.5)
        self.wait(3)


class GeometricSequence(BaseLesson):
    """Geometric sequence: The Exponential Machine"""
    
    def construct(self):
        super().construct()
        
        # Title
        title = self.lesson_title("Geometric Sequences: The Exponential Machine", self.COLOR_GEO)
        
        # PART 1: The Growth Factor
        self.section_divider("The Growth Factor", self.COLOR_WARNING)
        
        terms = [3, 6, 12, 24, 48, "..."]
        term_mobs = VGroup(*[MathTex(str(t), font_size=36, color=self.COLOR_GEO) for t in terms])
        term_mobs.arrange(RIGHT, buff=0.5).shift(UP*1.5)
        
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN) for t in term_mobs], lag_ratio=0.3), run_time=3)
        self.wait(1)
        
        # Show multiplication
        arrows = VGroup()
        labels = VGroup()
        for i in range(len(terms) - 2):
            arrow = Arrow(term_mobs[i].get_bottom(), term_mobs[i+1].get_bottom(), buff=0.15,
                         color=self.COLOR_HIGHLIGHT, stroke_width=3)
            label = Text("×2", font_size=20, color=self.COLOR_HIGHLIGHT).next_to(arrow, DOWN, buff=0.1)
            arrows.add(arrow)
            labels.add(label)
        
        self.play(LaggedStart(*[AnimationGroup(Create(a), Write(l)) for a, l in zip(arrows, labels)], lag_ratio=0.2), run_time=2.5)
        self.wait(1)
        
        ratio_text = Text("r = 2  (This is MULTIPLICATIVE growth)", font_size=24, color=self.COLOR_HIGHLIGHT)
        ratio_text.shift(DOWN*0.5)
        self.play(Write(ratio_text), run_time=2)
        self.wait(1)
        
        self.play(FadeOut(term_mobs), FadeOut(arrows), FadeOut(labels), FadeOut(ratio_text), run_time=1)
        
        # PART 2: Exponential Formula Connection
        self.section_divider("The Exponential Engine", self.COLOR_WARNING)
        
        formula1 = MathTex(r"a_n = a_1 \times r^{n-1}", font_size=40, color=self.COLOR_GEO).shift(UP*1.5)
        self.play(Write(formula1), run_time=2)
        self.wait(1)
        
        expo_form = MathTex(r"a_n = \frac{a_1}{r} \times r^n", font_size=40, color=self.COLOR_GEO).shift(UP*0.5)
        self.play(Write(expo_form), run_time=2)
        self.wait(1)
        
        connection = Text("This is an EXPONENTIAL function!", font_size=26, color=self.COLOR_HIGHLIGHT).shift(DOWN*0.5)
        self.play(FadeIn(connection, shift=UP), run_time=1.5)
        
        comparison = Text("Arithmetic: linear (additive) | Geometric: exponential (multiplicative)",
                         font_size=20, color=self.COLOR_INFO).shift(DOWN*1.2)
        self.play(Write(comparison), run_time=2)
        self.wait(2)
        
        self.play(FadeOut(VGroup(formula1, expo_form, connection, comparison)), run_time=1)
        
        # PART 3: Behavior Analysis
        self.section_divider("Behavior Analysis", self.COLOR_WARNING)
        
        behaviors = VGroup(
            VGroup(Text("r > 1  →", font_size=24, color=self.COLOR_HIGHLIGHT),
                   Text("Explosive Growth", font_size=24, color=self.COLOR_INFO)).arrange(RIGHT, buff=0.3),
            VGroup(Text("0 < r < 1  →", font_size=24, color=ORANGE),
                   Text("Exponential Decay", font_size=24, color=self.COLOR_INFO)).arrange(RIGHT, buff=0.3),
            VGroup(Text("r < 0  →", font_size=24, color=PURPLE),
                   Text("Oscillating", font_size=24, color=self.COLOR_INFO)).arrange(RIGHT, buff=0.3)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).shift(UP*0.5)
        
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT) for b in behaviors], lag_ratio=0.4), run_time=3)
        self.wait(2)
        
        # Decay Example
        decay_ex = Text("Example: r = 0.5 (Halving - Radioactive Decay)", font_size=22, color=ORANGE).shift(DOWN*1)
        decay_seq = MathTex(r"100, 50, 25, 12.5, 6.25, ...", font_size=28, color=ORANGE).shift(DOWN*1.7)
        self.play(Write(decay_ex), run_time=1.5)
        self.play(Write(decay_seq), run_time=2)
        self.wait(2)
        
        self.play(FadeOut(VGroup(behaviors, decay_ex, decay_seq)), run_time=1)
        
        # PART 4: Real Applications
        self.section_divider("Real-World Applications", self.COLOR_WARNING)
        
        applications = VGroup(
            Text("• Compound Interest (money doubles)", font_size=22, color=self.COLOR_INFO),
            Text("• Population Growth (bacteria multiply)", font_size=22, color=self.COLOR_INFO),
            Text("• Radioactive Decay (half-life)", font_size=22, color=ORANGE),
            Text("• Viral Spread (exponential infection)", font_size=22, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(UP*0.3)
        
        self.play(LaggedStart(*[FadeIn(app, shift=RIGHT) for app in applications], lag_ratio=0.3), run_time=3)
        self.wait(3)
        
        self.play(FadeOut(applications), run_time=1)
        
        # PART 5: Example Problem
        self.section_divider("Example: Find 6th Term", self.COLOR_WARNING)
        
        problem = Text("Sequence: 3, 6, 12, 24, 48, ...", font_size=26, color=self.COLOR_GEO).shift(UP*1.8)
        self.play(Write(problem), run_time=1.5)
        self.wait(0.5)
        
        given = VGroup(
            MathTex(r"a_1 = 3", font_size=26),
            MathTex(r"r = 2", font_size=26),
            MathTex(r"n = 6", font_size=26)
        ).arrange(RIGHT, buff=1).shift(UP*0.8)
        self.play(Write(given), run_time=2)
        self.wait(1)
        
        steps = [
            (r"a_6 = 3 \times 2^{6-1}", 26),
            (r"a_6 = 3 \times 2^5", 26),
            (r"a_6 = 3 \times 32", 26),
            (r"a_6 = 96", 32)
        ]
        
        pos = DOWN*0.2
        for i, (step_text, size) in enumerate(steps):
            is_answer = (i == len(steps) - 1)
            color = self.COLOR_ANSWER if is_answer else WHITE
            step = MathTex(step_text, font_size=size, color=color).shift(pos)
            self.play(Write(step), run_time=1.5)
            self.wait(1)
            if not is_answer:
                self.play(FadeOut(step), run_time=0.5)
        
        box = self.highlight_box(step, color=self.COLOR_ANSWER)
        self.wait(3)


class ArithmeticSeries(BaseLesson):
    """Arithmetic series: Gauss's Insight"""
    
    def construct(self):
        super().construct()
        
        # Title
        title = self.lesson_title("Arithmetic Series: Gauss's Insight", self.COLOR_ARITH)
        
        # PART 1: The Pairing Trick
        self.section_divider("The Pairing Trick", self.COLOR_WARNING)
        
        story = Text("Young Gauss: Sum 1 + 2 + 3 + ... + 100 = ?", font_size=24, color=self.COLOR_INFO)
        story.shift(UP*1.5)
        self.play(Write(story), run_time=2)
        self.wait(1)
        
        # Show forward and backward
        forward = MathTex(r"S = 1 + 2 + 3 + ... + 98 + 99 + 100", font_size=26).shift(UP*0.5)
        backward = MathTex(r"S = 100 + 99 + 98 + ... + 3 + 2 + 1", font_size=26).shift(DOWN*0.2)
        
        self.play(Write(forward), run_time=2)
        self.wait(0.5)
        self.play(Write(backward), run_time=2)
        self.wait(1)
        
        # Add them
        line = Line(backward.get_left() + LEFT*0.3, backward.get_right() + RIGHT*0.3, color=self.COLOR_HIGHLIGHT)
        line.next_to(backward, DOWN, buff=0.15)
        self.play(Create(line), run_time=1)
        
        sum_result = MathTex(r"2S = 101 + 101 + 101 + ... + 101 + 101 + 101", font_size=26, color=self.COLOR_HIGHLIGHT)
        sum_result.next_to(line, DOWN, buff=0.3)
        self.play(Write(sum_result), run_time=2)
        self.wait(1)
        
        insight = MathTex(r"2S = 100 \times 101", font_size=30, color=self.COLOR_HIGHLIGHT).shift(DOWN*2)
        final = MathTex(r"S = \frac{100 \times 101}{2} = 5050", font_size=32, color=self.COLOR_ANSWER).shift(DOWN*2.7)
        
        self.play(Write(insight), run_time=1.5)
        self.wait(0.5)
        self.play(Write(final), run_time=1.5)
        box = self.highlight_box(final, color=self.COLOR_ANSWER)
        self.wait(2)
        
        self.play(FadeOut(VGroup(story, forward, backward, line, sum_result, insight, final, box)), run_time=1)
        
        # PART 2: General Formula
        self.section_divider("General Formula", self.COLOR_WARNING)
        
        explanation = Text("Pairing first + last, second + second-last, ...", font_size=22, color=self.COLOR_INFO)
        explanation.shift(UP*1.8)
        self.play(Write(explanation), run_time=2)
        self.wait(1)
        
        formula1 = MathTex(r"S_n = \frac{n}{2}(a_1 + a_n)", font_size=40, color=self.COLOR_ARITH).shift(UP*0.6)
        self.play(Write(formula1), run_time=2)
        self.wait(1)
        
        interpretation = VGroup(
            Text("number of pairs", font_size=20, color=self.COLOR_INFO),
            Text("×", font_size=20),
            Text("(first + last)", font_size=20, color=self.COLOR_HIGHLIGHT)
        ).arrange(RIGHT, buff=0.2).shift(DOWN*0.1)
        self.play(Write(interpretation), run_time=2)
        self.wait(1.5)
        
        # Alternative form
        alt_text = Text("Alternative (when last term unknown):", font_size=22, color=self.COLOR_WARNING).shift(DOWN*1)
        formula2 = MathTex(r"S_n = \frac{n}{2}[2a_1 + (n-1)d]", font_size=36, color=self.COLOR_ARITH).shift(DOWN*1.8)
        
        self.play(Write(alt_text), run_time=1.5)
        self.play(Write(formula2), run_time=2)
        self.wait(2)
        
        self.play(FadeOut(VGroup(explanation, formula1, interpretation, alt_text, formula2)), run_time=1)
        
        # PART 3: Geometric Interpretation (Trapezoid)
        self.section_divider("Trapezoid Area View", self.COLOR_WARNING)
        
        trap_text = Text("Sum = Area under discrete steps = Trapezoid area", font_size=22, color=self.COLOR_INFO)
        trap_text.shift(UP*2)
        self.play(Write(trap_text), run_time=2)
        self.wait(1)
        
        trap_formula = MathTex(r"\text{Area} = \frac{\text{width} \times (\text{base}_1 + \text{base}_2)}{2}",
                              font_size=28, color=self.COLOR_HIGHLIGHT).shift(UP*1)
        self.play(Write(trap_formula), run_time=2)
        self.wait(1)
        
        connection_text = Text("This is discrete INTEGRATION!", font_size=26, color=self.COLOR_SIGMA)
        connection_text.shift(ORIGIN)
        self.play(FadeIn(connection_text, shift=UP), run_time=1.5)
        
        calculus_note = Text("(Preview of calculus: integrating linear functions)", font_size=18, color=self.COLOR_LIGHT)
        calculus_note.shift(DOWN*0.8)
        self.play(Write(calculus_note), run_time=1.5)
        self.wait(2)
        
        self.play(FadeOut(VGroup(trap_text, trap_formula, connection_text, calculus_note)), run_time=1)
        
        # PART 4: Example
        self.section_divider("Example Problem", self.COLOR_WARNING)
        
        # Example problem
        problem = Text("Find the sum of first 20 terms:", font_size=28, color=self.COLOR_WARNING)
        problem.to_edge(UP, buff=1.5)
        self.play(Write(problem), run_time=1.5)
        self.pause_for_voiceover(2)
        
        sequence = MathTex(r"3 + 7 + 11 + 15 + ...", font_size=32)
        sequence.shift(UP*1.8)
        self.play(Write(sequence), run_time=2)
        self.pause_for_voiceover(2)
        
        # Given information
        given_title = Text("Given:", font_size=24, color=self.COLOR_INFO)
        given_title.shift(UP*0.8)
        self.play(Write(given_title), run_time=1)
        self.pause_for_voiceover(1)
        
        given = VGroup(
            MathTex(r"a_1 = 3", font_size=26),
            MathTex(r"d = 4", font_size=26),
            MathTex(r"n = 20", font_size=26)
        ).arrange(RIGHT, buff=1)
        given.shift(UP*0.3)
        self.play(Write(given), run_time=2)
        self.pause_for_voiceover(2)
        
        # Solution
        sol_title = Text("Solution:", font_size=24, color=self.COLOR_WARNING)
        sol_title.shift(DOWN*0.5)
        self.play(Write(sol_title), run_time=1)
        self.pause_for_voiceover(1)
        
        step1 = MathTex(r"S_{20} = \frac{20}{2}[2(3) + (20-1)(4)]", font_size=28)
        step1.shift(DOWN*1.1)
        self.play(Write(step1), run_time=2)
        self.pause_for_voiceover(2)
        
        self.play(FadeOut(step1), run_time=0.6)
        
        step2 = MathTex(r"S_{20} = 10[6 + 19 \times 4]", font_size=28)
        step2.shift(DOWN*1.1)
        self.play(Write(step2), run_time=1.5)
        self.pause_for_voiceover(2)
        
        self.play(FadeOut(step2), run_time=0.6)
        
        step3 = MathTex(r"S_{20} = 10[6 + 76]", font_size=28)
        step3.shift(DOWN*1.1)
        self.play(Write(step3), run_time=1.5)
        self.pause_for_voiceover(2)
        
        self.play(FadeOut(step3), run_time=0.6)
        
        step4 = MathTex(r"S_{20} = 10 \times 82", font_size=28)
        step4.shift(DOWN*1.1)
        self.play(Write(step4), run_time=1.5)
        self.pause_for_voiceover(2)
        
        self.play(FadeOut(step4), run_time=0.6)
        
        answer = MathTex(r"S_{20} = 820", font_size=36, color=self.COLOR_ANSWER)
        answer.shift(DOWN*1.1)
        self.play(Write(answer), run_time=2)
        answer_box = self.highlight_box(answer, color=self.COLOR_ANSWER)
        self.pause_for_voiceover(3)
        
        self.wait(2)


class GeometricSeries(BaseLesson):
    """Geometric series: Convergence and Limits"""
    
    def construct(self):
        super().construct()
        
        # Title
        title = self.lesson_title("Geometric Series: Convergence & Limits", self.COLOR_GEO)
        
        # PART 1: Finite Series Formula
        self.section_divider("Finite Series Formula", self.COLOR_WARNING)
        
        explanation = Text("Adding terms: a₁ + a₁r + a₁r² + ... + a₁r⁽ⁿ⁻¹⁾", font_size=22, color=self.COLOR_INFO)
        explanation.shift(UP*1.5)
        self.play(Write(explanation), run_time=2)
        self.wait(1)
        
        formula = MathTex(r"S_n = a_1 \frac{r^n - 1}{r - 1}", font_size=40, color=self.COLOR_GEO).shift(UP*0.5)
        self.play(Write(formula), run_time=2)
        self.wait(1)
        
        condition = Text("(when r ≠ 1)", font_size=20, color=self.COLOR_LIGHT).shift(DOWN*0.3)
        self.play(FadeIn(condition), run_time=1)
        self.wait(1.5)
        
        self.play(FadeOut(VGroup(explanation, formula, condition)), run_time=1)
        
        # PART 2: The Convergence Question
        self.section_divider("Infinite Series: Does it Converge?", self.COLOR_WARNING)
        
        question = Text("What happens when n → ∞?", font_size=26, color=self.COLOR_SIGMA)
        question.shift(UP*1.8)
        self.play(Write(question), run_time=1.5)
        self.wait(1)
        
        cases = VGroup(
            VGroup(Text("|r| < 1:", font_size=24, color=self.COLOR_HIGHLIGHT),
                   Text("Converges to finite value", font_size=22, color=self.COLOR_INFO)).arrange(RIGHT, buff=0.4),
            VGroup(Text("|r| ≥ 1:", font_size=24, color=RED),
                   Text("Diverges to infinity", font_size=22, color=RED)).arrange(RIGHT, buff=0.4)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).shift(UP*0.5)
        
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT) for c in cases], lag_ratio=0.4), run_time=2.5)
        self.wait(2)
        
        # Critical insight
        insight = Text("This is your first encounter with LIMITS!", font_size=24, color=self.COLOR_SIGMA)
        insight.shift(DOWN*0.8)
        self.play(FadeIn(insight, shift=UP), run_time=1.5)
        self.wait(2)
        
        self.play(FadeOut(VGroup(question, cases, insight)), run_time=1)
        
        # PART 3: The Infinite Formula Derivation
        self.section_divider("Infinite Series (|r| < 1)", self.COLOR_WARNING)
        
        deriv1 = MathTex(r"S_\infty = \lim_{n \to \infty} a_1 \frac{r^n - 1}{r - 1}", font_size=30)
        deriv1.shift(UP*1.5)
        self.play(Write(deriv1), run_time=2)
        self.wait(1)
        
        deriv2 = Text("When |r| < 1, as n → ∞, rⁿ → 0", font_size=22, color=self.COLOR_INFO)
        deriv2.shift(UP*0.6)
        self.play(Write(deriv2), run_time=2)
        self.wait(1)
        
        deriv3 = MathTex(r"S_\infty = a_1 \frac{0 - 1}{r - 1} = \frac{-a_1}{r - 1}", font_size=30)
        deriv3.shift(ORIGIN)
        self.play(Write(deriv3), run_time=2)
        self.wait(1)
        
        final_formula = MathTex(r"S_\infty = \frac{a_1}{1 - r}", font_size=42, color=self.COLOR_ANSWER)
        final_formula.shift(DOWN*1.2)
        self.play(Write(final_formula), run_time=2)
        box = self.highlight_box(final_formula, color=self.COLOR_ANSWER)
        self.wait(2)
        
        self.play(FadeOut(VGroup(deriv1, deriv2, deriv3, final_formula, box)), run_time=1)
        
        # PART 4: Zeno's Paradox
        self.section_divider("Zeno's Paradox", self.COLOR_WARNING)
        
        zeno_text = Text("Walk half the distance, then half again, forever...", font_size=22, color=self.COLOR_INFO)
        zeno_text.shift(UP*1.5)
        self.play(Write(zeno_text), run_time=2)
        self.wait(1)
        
        zeno_series = MathTex(r"S = 1 + \frac{1}{2} + \frac{1}{4} + \frac{1}{8} + \frac{1}{16} + ...",
                             font_size=28).shift(UP*0.6)
        self.play(Write(zeno_series), run_time=2)
        self.wait(1)
        
        zeno_vals = MathTex(r"a_1 = 1, \quad r = \frac{1}{2}", font_size=26).shift(DOWN*0.2)
        self.play(Write(zeno_vals), run_time=1.5)
        self.wait(1)
        
        zeno_calc = MathTex(r"S_\infty = \frac{1}{1 - \frac{1}{2}} = \frac{1}{\frac{1}{2}} = 2",
                           font_size=32, color=self.COLOR_ANSWER).shift(DOWN*1.2)
        self.play(Write(zeno_calc), run_time=2)
        self.wait(1)
        
        zeno_conclusion = Text("You DO reach the destination!", font_size=24, color=self.COLOR_HIGHLIGHT)
        zeno_conclusion.shift(DOWN*2.2)
        self.play(FadeIn(zeno_conclusion, shift=UP), run_time=1.5)
        self.wait(2)
        
        self.play(FadeOut(VGroup(zeno_text, zeno_series, zeno_vals, zeno_calc, zeno_conclusion)), run_time=1)
        
        # PART 5: Example Problem
        self.section_divider("Example: Finite Series", self.COLOR_WARNING)
        
        problem = Text("Find the sum of first 5 terms:", font_size=26, color=self.COLOR_WARNING)
        problem.to_edge(UP, buff=1.5)
        self.play(Write(problem), run_time=1.5)
        self.wait(0.5)
        
        sequence = MathTex(r"4 + 12 + 36 + 108 + ...", font_size=32).shift(UP*1.8)
        self.play(Write(sequence), run_time=2)
        self.wait(1)
        
        given = VGroup(
            MathTex(r"a_1 = 4", font_size=26),
            MathTex(r"r = 3", font_size=26),
            MathTex(r"n = 5", font_size=26)
        ).arrange(RIGHT, buff=1).shift(UP*0.8)
        self.play(Write(given), run_time=2)
        self.wait(1)
        
        steps = [
            (r"S_5 = 4 \frac{3^5 - 1}{3 - 1}", 26),
            (r"S_5 = 4 \frac{243 - 1}{2}", 26),
            (r"S_5 = 4 \times \frac{242}{2}", 26),
            (r"S_5 = 4 \times 121", 26),
            (r"S_5 = 484", 32)
        ]
        
        pos = DOWN*0.2
        for i, (step_text, size) in enumerate(steps):
            is_answer = (i == len(steps) - 1)
            color = self.COLOR_ANSWER if is_answer else WHITE
            step = MathTex(step_text, font_size=size, color=color).shift(pos)
            self.play(Write(step), run_time=1.5)
            self.wait(1)
            if not is_answer:
                self.play(FadeOut(step), run_time=0.5)
        
        box = self.highlight_box(step, color=self.COLOR_ANSWER)
        self.wait(3)


class SigmaNotation(BaseLesson):
    """Sigma (summation) notation"""
    
    def construct(self):
        super().construct()
        
        # Title with helper
        title = self.lesson_title("Sigma Notation (Σ)", self.COLOR_SIGMA)
        
        # Introduction
        intro = Text("A shorthand way to write series", font_size=self.FONT_SUBTITLE, color=self.COLOR_LIGHT)
        intro.shift(UP*2.2)
        self.play(FadeIn(intro), run_time=1.5)
        self.wait(1)
        
        # Sigma notation with labeled components
        sigma = MathTex(r"\sum_{i=1}^{n} a_i", font_size=60, color=self.COLOR_SIGMA).shift(UP*0.8)
        self.play(Write(sigma), run_time=2.5)
        self.wait(1)
        
        # Component labels with arrows
        labels_data = [
            ("Upper limit (last term)", UP, 0.8, RIGHT*0.5, self.COLOR_SIGMA, "top"),
            ("Lower limit (first term)", DOWN, 1, RIGHT*0.5, self.COLOR_ARITH, "bottom"),
            ("General term", RIGHT, 0, (1.5, 0, 0), self.COLOR_HIGHLIGHT, "right")
        ]
        
        labels = VGroup()
        arrows = VGroup()
        
        for text, direction, buff_val, shift_val, color, anchor in labels_data:
            label = Text(text, font_size=20, color=color)
            label.next_to(sigma, direction, buff=buff_val).shift(shift_val)
            
            if anchor == "top":
                arrow = Arrow(label.get_top(), sigma.get_top() + RIGHT*0.3, color=color, buff=0.1, stroke_width=2)
            elif anchor == "bottom":
                arrow = Arrow(label.get_top(), sigma.get_bottom() + RIGHT*0.3, color=color, buff=0.1, stroke_width=2)
            else:  # right
                arrow = Arrow(label.get_left(), sigma.get_right(), color=color, buff=0.1, stroke_width=2)
            
            labels.add(label)
            arrows.add(arrow)
        
        self.play(LaggedStart(*[AnimationGroup(Write(l), Create(a)) for l, a in zip(labels, arrows)], lag_ratio=0.4), run_time=3)
        self.wait(1.5)
        
        # Clear labels
        self.play(FadeOut(labels), FadeOut(arrows), run_time=1)
        
        # Expanded meaning
        meaning = MathTex(r"= a_1 + a_2 + a_3 + ... + a_n", font_size=32).shift(DOWN*0.8)
        self.play(Write(meaning), run_time=2)
        self.wait(1.5)
        
        # Clear for examples
        self.play(FadeOut(intro), FadeOut(sigma), FadeOut(meaning), run_time=1.5)
        
        # Example 1 with section divider
        self.section_divider("Example 1", self.COLOR_WARNING)
        
        ex1 = MathTex(r"\sum_{k=1}^{5} (2k + 1)", font_size=40, color=self.COLOR_SIGMA).shift(UP*1)
        self.play(Write(ex1), run_time=2)
        self.wait(1)
        
        # Show steps for example 1
        steps1 = [
            r"= (2 \cdot 1 + 1) + (2 \cdot 2 + 1) + (2 \cdot 3 + 1) + (2 \cdot 4 + 1) + (2 \cdot 5 + 1)",
            r"= 3 + 5 + 7 + 9 + 11",
            r"= 35"
        ]
        
        for i, step in enumerate(steps1):
            size = 22 if i == 0 else (28 if i == 1 else 32)
            color = self.COLOR_ANSWER if i == 2 else WHITE
            step_tex = MathTex(step, font_size=size, color=color).shift(UP*0.1)
            self.play(Write(step_tex), run_time=2 if i < 2 else 1.5)
            self.wait(1.5 if i < 2 else 1)
            if i < 2:
                self.play(FadeOut(step_tex), run_time=0.6)
        
        self.wait(1)
        self.play(FadeOut(ex1), FadeOut(step_tex), run_time=1)
        
        # Example 2 with section divider
        self.section_divider("Example 2", self.COLOR_WARNING)
        
        ex2 = MathTex(r"\sum_{n=1}^{4} 3^n", font_size=40, color=self.COLOR_SIGMA).shift(UP*1)
        self.play(Write(ex2), run_time=2)
        self.wait(1)
        
        # Show steps for example 2
        steps2 = [
            r"= 3^1 + 3^2 + 3^3 + 3^4",
            r"= 3 + 9 + 27 + 81",
            r"= 120"
        ]
        
        for i, step in enumerate(steps2):
            color = self.COLOR_ANSWER if i == 2 else WHITE
            step_tex = MathTex(step, font_size=28 if i < 2 else 32, color=color).shift(UP*0.1)
            self.play(Write(step_tex), run_time=2 if i < 2 else 1.5)
            self.wait(1.5 if i < 2 else 1)
            if i < 2:
                self.play(FadeOut(step_tex), run_time=0.6)
        
        box = self.highlight_box(step_tex, color=self.COLOR_ANSWER)
        self.wait(2)


class SummaryTable(BaseLesson):
    """Summary comparison table"""
    
    def construct(self):
        super().construct()
        
        # Title
        title = Text("Sequences & Series Summary", font_size=self.FONT_TITLE, color=self.COLOR_WARNING)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2)
        self.pause_for_voiceover(2)
        
        # Table headers with LaggedStart
        headers = VGroup(
            Text("Type", font_size=24, color=self.COLOR_INFO, weight=BOLD),
            Text("Arithmetic", font_size=24, color=self.COLOR_ARITH, weight=BOLD),
            Text("Geometric", font_size=24, color=self.COLOR_GEO, weight=BOLD)
        ).arrange(RIGHT, buff=1.8)
        headers.shift(UP*2.2)
        
        self.play(LaggedStart(*[Write(h) for h in headers], lag_ratio=0.4), run_time=2.5)
        self.pause_for_voiceover(2)
        
        # Underline
        line = Line(headers.get_left() + LEFT*0.3, headers.get_right() + RIGHT*0.3,
                   color=self.COLOR_INFO)
        line.next_to(headers, DOWN, buff=0.15)
        self.play(Create(line), run_time=1)
        self.wait(0.5)
        
        # Row 1: Pattern
        row1 = VGroup(
            Text("Pattern", font_size=20, color=self.COLOR_TEXT),
            Text("Add constant (d)", font_size=19, color=self.COLOR_ARITH),
            Text("Multiply by constant (r)", font_size=19, color=self.COLOR_GEO)
        ).arrange(RIGHT, buff=1.5)
        for i, cell in enumerate(row1):
            cell.align_to(headers[i], LEFT)
        row1.shift(UP*1.5)
        
        # Row 2: nth term
        row2 = VGroup(
            Text("nth Term", font_size=20, color=self.COLOR_TEXT),
            MathTex(r"a_n = a_1 + (n-1)d", font_size=19, color=self.COLOR_ARITH),
            MathTex(r"a_n = a_1 r^{n-1}", font_size=19, color=self.COLOR_GEO)
        ).arrange(RIGHT, buff=1.2)
        for i, cell in enumerate(row2):
            cell.align_to(headers[i], LEFT)
        row2.shift(UP*0.8)
        
        # Row 3: Sum (finite)
        row3_label = Text("Sum (n terms)", font_size=20, color=self.COLOR_TEXT)
        row3_label.align_to(headers[0], LEFT).shift(UP*0.1)
        
        row3_arith = MathTex(r"S_n = \frac{n}{2}(a_1 + a_n)", font_size=18, color=self.COLOR_ARITH)
        row3_arith.align_to(headers[1], LEFT).shift(UP*0.1)
        
        row3_geom = MathTex(r"S_n = a_1\frac{r^n - 1}{r - 1}", font_size=18, color=self.COLOR_GEO)
        row3_geom.align_to(headers[2], LEFT).shift(UP*0.1)
        
        row3 = VGroup(row3_label, row3_arith, row3_geom)
        
        # Row 4: Example
        row4 = VGroup(
            Text("Example", font_size=20, color=self.COLOR_TEXT),
            Text("2, 5, 8, 11, ...", font_size=19, color=self.COLOR_ARITH),
            Text("3, 6, 12, 24, ...", font_size=19, color=self.COLOR_GEO)
        ).arrange(RIGHT, buff=1.5)
        for i, cell in enumerate(row4):
            cell.align_to(headers[i], LEFT)
        row4.shift(DOWN*0.6)
        
        # Row 5: Common value
        row5 = VGroup(
            Text("Common value", font_size=20, color=self.COLOR_TEXT),
            Text("d = 3", font_size=19, color=self.COLOR_HIGHLIGHT),
            Text("r = 2", font_size=19, color=self.COLOR_HIGHLIGHT)
        ).arrange(RIGHT, buff=1.8)
        for i, cell in enumerate(row5):
            cell.align_to(headers[i], LEFT)
        row5.shift(DOWN*1.2)
        
        # Animate all rows with LaggedStart
        all_table_rows = [row1, row2, row3, row4, row5]
        self.play(LaggedStart(*[FadeIn(row, shift=DOWN*0.2) for row in all_table_rows], lag_ratio=0.3), run_time=5)
        self.pause_for_voiceover(3)
        
        self.wait(2)
        
        # Key formulas box
        key_title = Text("Key Sigma Notation:", font_size=24, color=self.COLOR_SIGMA, weight=BOLD)
        key_title.shift(DOWN*2.2)
        
        sigma_formula = MathTex(r"\sum_{i=1}^{n} a_i = a_1 + a_2 + ... + a_n",
                               font_size=24)
        sigma_formula.shift(DOWN*2.8)
        
        formula_box = SurroundingRectangle(
            VGroup(key_title, sigma_formula),
            color=self.COLOR_SIGMA,
            buff=0.3,
            corner_radius=0.1
        )
        
        self.play(Write(key_title), run_time=1.5)
        self.play(Write(sigma_formula), run_time=2)
        self.play(Create(formula_box), run_time=1)
        self.pause_for_voiceover(3)
        
        self.wait(3)
