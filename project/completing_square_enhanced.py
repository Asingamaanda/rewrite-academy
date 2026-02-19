"""
Enhanced UI/UX Version of Completing the Square
================================================
This standalone version demonstrates modern animation design principles:
- Visual hierarchy with color-coded elements
- Smooth transitions and timing
- Clear layout with visual separators
- Progressive disclosure of information
- Emphasis through highlighting and movement
"""

from manim import *

class CompletingTheSquareEnhanced(Scene):
    # Enhanced color palette
    COLOR_PRIMARY = "#3498db"      # Blue
    COLOR_ACCENT = "#e74c3c"       # Red  
    COLOR_SUCCESS = "#2ecc71"      # Green
    COLOR_WARNING = "#f39c12"      # Orange
    COLOR_INFO = "#9b59b6"         # Purple
    COLOR_LIGHT = "#bdc3c7"        # Light gray
    COLOR_DARK_BG = "#2c3e50"      # Dark background
    
    def construct(self):
        # ====================================================================
        # ANIMATED TITLE WITH MODERN DESIGN
        # ====================================================================
        
        # Background gradient effect
        title_bg = Rectangle(
            width=14, height=1.2,
            fill_color=self.COLOR_PRIMARY,
            fill_opacity=0.15,
            stroke_width=0
        ).to_edge(UP, buff=0.2)
        
        main_title = Text("Completing the Square", font_size=48, color=self.COLOR_PRIMARY, weight=BOLD)
        subtitle = Text("Converting to Perfect Square Form", font_size=24, color=self.COLOR_LIGHT)
        
        title_group = VGroup(main_title, subtitle).arrange(DOWN, buff=0.2)
        title_group.move_to(title_bg.get_center())
        
        self.play(
            FadeIn(title_bg, scale=1.1),
            run_time=1
        )
        self.play(
            Write(main_title),
            run_time=1.5,
            rate_func=smooth
        )
        self.play(
            FadeIn(subtitle, shift=UP*0.2),
            run_time=1
        )
        
        self.play(
            title_group.animate.scale(0.6).to_edge(UP, buff=0.3),
            title_bg.animate.scale(0.6).to_edge(UP, buff=0.3),
            run_time=1.5,
            rate_func=smooth
        )
        self.wait(0.5)
        
        # ====================================================================
        # INTRODUCTION SECTION WITH BULLET ANIMATIONS
        # ====================================================================
        
        intro_title = Text("Why Use This Method?", font_size=36, color=self.COLOR_WARNING)
        intro_title.shift(UP*2.2)
        
        self.play(
            DrawBorderThenFill(intro_title),
            run_time=1.5
        )
        self.wait(1)
        
        # Animated bullet points with icons
        bullets = VGroup()
        bullet_data = [
            ("✓", "Works for ANY quadratic equation", self.COLOR_SUCCESS),
            ("♦", "Reveals vertex form of parabola", self.COLOR_INFO),
            ("★", "Foundation for quadratic formula", self.COLOR_WARNING)
        ]
        
        for icon, text, color in bullet_data:
            bullet_icon = Text(icon, font_size=32, color=color)
            bullet_text = Text(text, font_size=26)
            bullet_item = VGroup(bullet_icon, bullet_text).arrange(RIGHT, buff=0.4)
            bullets.add(bullet_item)
        
        bullets.arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        bullets.shift(UP*0.2)
        
        for i, bullet in enumerate(bullets):
            self.play(
                FadeIn(bullet[0], scale=2),
                run_time=0.5
            )
            self.play(
                Write(bullet[1]),
                run_time=1
            )
            self.wait(0.8)
        
        self.wait(1.5)
        self.play(
            FadeOut(intro_title, shift=UP*0.5),
            FadeOut(bullets, shift=DOWN*0.5),
            run_time=1.5
        )
        
        # ====================================================================
        # EXAMPLE 1: ENHANCED LAYOUT
        # ====================================================================
        
        # Section header with styled background
        example_header_bg = RoundedRectangle(
            width=14, height=0.9,
            fill_color=self.COLOR_PRIMARY,
            fill_opacity=0.2,
            stroke_color=self.COLOR_PRIMARY,
            stroke_width=2,
            corner_radius=0.1
        ).to_edge(UP, buff=1.1)
        
        example_label = Text("Example 1: Standard Form", font_size=34, color=self.COLOR_PRIMARY, weight=BOLD)
        example_label.move_to(example_header_bg.get_center())
        
        self.play(
            DrawBorderThenFill(example_header_bg),
            Write(example_label),
            run_time=1.5
        )
        self.wait(1)
        
        # Problem presentation in styled frame
        problem_container = VGroup()
        
        problem_label = Text("Solve:", font_size=30, color=self.COLOR_ACCENT, weight=BOLD)
        problem_label.shift(UP*2.3+LEFT*4.5)
        
        problem_eq = MathTex(r"x^2 + 6x + 5 = 0", font_size=48, color=WHITE)
        problem_eq.shift(UP*2.3+RIGHT*0.5)
        
        problem_box = SurroundingRectangle(
            problem_eq,
            color=self.COLOR_ACCENT,
            buff=0.25,
            stroke_width=3
        )
        
        self.play(
            FadeIn(problem_label, shift=RIGHT*0.3),
            run_time=1
        )
        self.play(
            Create(problem_box),
            run_time=1
        )
        self.play(
            Write(problem_eq),
            run_time=2
        )
        self.wait(1.5)
        
        # Horizontal divider
        divider = Line(
            start=LEFT*7, end=RIGHT*7,
            color=self.COLOR_LIGHT,
            stroke_width=1.5
        ).shift(UP*1.4)
        
        self.play(
            Create(divider),
            run_time=1
        )
        
        # ====================================================================
        # STEP 1: MOVE CONSTANT (Enhanced visual flow)
        # ====================================================================
        
        # Step indicator with circular number badge
        step1_badge = VGroup(
            Circle(radius=0.3, color=self.COLOR_WARNING, fill_opacity=1, stroke_width=0),
            Text("1", font_size=28, color=WHITE, weight=BOLD)
        )
        step1_badge[1].move_to(step1_badge[0].get_center())
        
        step1_text = Text("Move constant to right side", font_size=28, color=self.COLOR_WARNING)
        step1_header = VGroup(step1_badge, step1_text).arrange(RIGHT, buff=0.5)
        step1_header.shift(UP*0.7+LEFT*2)
        
        self.play(
            GrowFromCenter(step1_badge),
            run_time=0.6
        )
        self.play(
            Write(step1_text),
            run_time=1.2
        )
        self.wait(1)
        
        # Show transformation with color coding
        moved_eq = MathTex(
            r"x^2 + 6x", r"=", r"-5",
            font_size=44
        )
        moved_eq[0].set_color(BLUE)
        moved_eq[2].set_color(self.COLOR_ACCENT)
        moved_eq.shift(DOWN*0.2)
        
        self.play(
            TransformMatchingTex(problem_eq.copy(), moved_eq),
            run_time=2,
            rate_func=smooth
        )
        self.wait(1)
        
        # Highlight the moved constant
        const_highlight = SurroundingRectangle(
            moved_eq[2],
            color=self.COLOR_SUCCESS,
            buff=0.12,
            stroke_width=3
        )
        
        self.play(
            Create(const_highlight),
            Flash(moved_eq[2], color=self.COLOR_SUCCESS, flash_radius=0.5),
            run_time=1
        )
        self.wait(1)
        
        self.play(
            FadeOut(const_highlight),
            FadeOut(step1_header),
            run_time=0.8
        )
        
        # ====================================================================
        # STEP 2: CALCULATE (b/2)² (Visual diagram)
        # ====================================================================
        
        step2_badge = VGroup(
            Circle(radius=0.3, color=self.COLOR_WARNING, fill_opacity=1, stroke_width=0),
            Text("2", font_size=28, color=WHITE, weight=BOLD)
        )
        step2_badge[1].move_to(step2_badge[0].get_center())
        
        step2_text = Text("Calculate (b/2)²", font_size=28, color=self.COLOR_WARNING)
        step2_header = VGroup(step2_badge, step2_text).arrange(RIGHT, buff=0.5)
        step2_header.shift(UP*0.7+LEFT*2)
        
        self.play(
            GrowFromCenter(step2_badge),
            Write(step2_text),
            run_time=1.5
        )
        self.wait(1)
        
        # Calculation box with visual flow
        calc_container = RoundedRectangle(
            width=6.5, height=3,
            stroke_color=self.COLOR_INFO,
            stroke_width=3,
            fill_color=self.COLOR_INFO,
            fill_opacity=0.08,
            corner_radius=0.15
        ).shift(RIGHT*3.5+DOWN*0.8)
        
        calc_title = Text("Calculation:", font_size=24, color=self.COLOR_INFO, weight=BOLD)
        calc_title.next_to(calc_container, UP, buff=0.2)
        
        self.play(
            DrawBorderThenFill(calc_container),
            Write(calc_title),
            run_time=1.2
        )
        
        # Step-by-step calculation with arrows
        calc_step1 = MathTex(r"b = 6", font_size=36, color=WHITE)
        calc_step1.shift(RIGHT*3.5+UP*0.3)
        
        arrow1 = MathTex(r"\Downarrow", font_size=32, color=self.COLOR_WARNING)
        arrow1.shift(RIGHT*3.5+DOWN*0.3)
        
        calc_step2 = MathTex(r"\frac{b}{2} = \frac{6}{2} = 3", font_size=36, color=self.COLOR_WARNING)
        calc_step2.shift(RIGHT*3.5+DOWN*0.8)
        
        arrow2 = MathTex(r"\Downarrow", font_size=32, color=self.COLOR_SUCCESS)
        arrow2.shift(RIGHT*3.5+DOWN*1.4)
        
        calc_step3 = MathTex(r"\left(\frac{b}{2}\right)^2 = 3^2 = 9", font_size=36, color=self.COLOR_SUCCESS)
        calc_step3.shift(RIGHT*3.5+DOWN*1.9)
        
        # Animate each step
        self.play(Write(calc_step1), run_time=1.5)
        self.wait(0.8)
        
        self.play(GrowFromPoint(arrow1, arrow1.get_top()), run_time=0.6)
        
        self.play(Write(calc_step2), run_time=1.5)
        self.wait(0.8)
        
        self.play(GrowFromPoint(arrow2, arrow2.get_top()), run_time=0.6)
        
        self.play(Write(calc_step3), run_time=1.5)
        self.wait(1)
        
        # Emphasize the result "9"
        result_box = SurroundingRectangle(
            calc_step3[-1],
            color=self.COLOR_SUCCESS,
            buff=0.15,
            stroke_width=4
        )
        
        self.play(
            Create(result_box),
            Circumscribe(calc_step3[-1], color=self.COLOR_SUCCESS, fade_out=True),
            run_time=1.5
        )
        self.wait(1.5)
        
        self.play(
            FadeOut(VGroup(calc_container, calc_title, calc_step1, arrow1, calc_step2, arrow2, calc_step3, result_box)),
            FadeOut(step2_header),
            run_time=1.2
        )
        
        # ====================================================================
        # STEP 3: ADD 9 TO BOTH SIDES (Animated balance)
        # ====================================================================
        
        step3_badge = VGroup(
            Circle(radius=0.3, color=self.COLOR_WARNING, fill_opacity=1, stroke_width=0),
            Text("3", font_size=28, color=WHITE, weight=BOLD)
        )
        step3_badge[1].move_to(step3_badge[0].get_center())
        
        step3_text = Text("Add 9 to both sides", font_size=28, color=self.COLOR_WARNING)
        step3_header = VGroup(step3_badge, step3_text).arrange(RIGHT, buff=0.5)
        step3_header.shift(UP*0.7+LEFT*2)
        
        self.play(
            GrowFromCenter(step3_badge),
            Write(step3_text),
            run_time=1.5
        )
        self.wait(1)
        
        # Show +9 appearing simultaneously on both sides
        plus_nine_left = MathTex(r"+ 9", font_size=40, color=self.COLOR_SUCCESS)
        plus_nine_left.next_to(moved_eq[0], RIGHT, buff=0.15)
        
        plus_nine_right = MathTex(r"+ 9", font_size=40, color=self.COLOR_SUCCESS)
        plus_nine_right.next_to(moved_eq[2], RIGHT, buff=0.15)
        
        self.play(
            FadeIn(plus_nine_left, scale=1.8),
            FadeIn(plus_nine_right, scale=1.8),
            run_time=1.5
        )
        self.wait(1)
        
        # Transform to combined equation
        combined_eq = MathTex(
            r"x^2 + 6x + 9", r"=", r"-5 + 9",
            font_size=44
        )
        combined_eq[0].set_color(BLUE)
        combined_eq[2].set_color(self.COLOR_INFO)
        combined_eq.shift(DOWN*1.3)
        
        self.play(
            FadeOut(moved_eq),
            FadeOut(plus_nine_left),
            FadeOut(plus_nine_right),
            Write(combined_eq),
            run_time=2
        )
        self.wait(1)
        
        # Simplify right side
        simplified_eq = MathTex(
            r"x^2 + 6x + 9", r"=", r"4",
            font_size=44
        )
        simplified_eq[0].set_color(BLUE)
        simplified_eq[2].set_color(self.COLOR_ACCENT)
        simplified_eq.shift(DOWN*2.2)
        
        self.play(
            Write(simplified_eq),
            run_time=1.5
        )
        self.wait(1)
        
        self.play(
            FadeOut(step3_header),
            FadeOut(combined_eq),
            run_time=0.8
        )
        
        # ====================================================================
        # STEP 4: FACTOR AS PERFECT SQUARE (Pattern recognition)
        # ====================================================================
        
        step4_badge = VGroup(
            Circle(radius=0.3, color=self.COLOR_WARNING, fill_opacity=1, stroke_width=0),
            Text("4", font_size=28, color=WHITE, weight=BOLD)
        )
        step4_badge[1].move_to(step4_badge[0].get_center())
        
        step4_text = Text("Factor as perfect square", font_size=28, color=self.COLOR_WARNING)
        step4_header = VGroup(step4_badge, step4_text).arrange(RIGHT, buff=0.5)
        step4_header.shift(UP*0.7+LEFT*2)
        
        self.play(
            GrowFromCenter(step4_badge),
            Write(step4_text),
            run_time=1.5
        )
        self.wait(1)
        
        # Show pattern with visual connection
        pattern_container = RoundedRectangle(
            width=8, height=1.3,
            stroke_color=self.COLOR_SUCCESS,
            stroke_width=2,
            fill_color=self.COLOR_SUCCESS,
            fill_opacity=0.1,
            corner_radius=0.1
        ).shift(RIGHT*2.5+DOWN*0.5)
        
        pattern_eq = MathTex(
            r"x^2 + 6x + 9 = (x+3)^2",
            font_size=36,
            color=self.COLOR_SUCCESS
        )
        pattern_eq.move_to(pattern_container.get_center())
        
        self.play(
            DrawBorderThenFill(pattern_container),
            run_time=1
        )
        self.play(
            Write(pattern_eq),
            run_time=2
        )
        self.wait(1.5)
        
        # Transform to factored form
        factored_eq = MathTex(
            r"(x + 3)^2", r"=", r"4",
            font_size=52
        )
        factored_eq[0].set_color(self.COLOR_PRIMARY)
        factored_eq[2].set_color(self.COLOR_ACCENT)
        factored_eq.shift(DOWN*3.2)
        
        self.play(
            TransformMatchingTex(simplified_eq.copy(), factored_eq),
            run_time=2,
            rate_func=smooth
        )
        self.wait(1)
        
        # Emphasize the perfect square
        perfect_square_box = SurroundingRectangle(
            factored_eq[0],
            color=self.COLOR_SUCCESS,
            buff=0.15,
            stroke_width=4
        )
        
        self.play(
            Create(perfect_square_box),
            run_time=1
        )
        self.wait(1.5)
        
        self.play(
            FadeOut(step4_header),
            FadeOut(pattern_container),
            FadeOut(pattern_eq),
            FadeOut(simplified_eq),
            FadeOut(perfect_square_box),
            run_time=1
        )
        
        # ====================================================================
        # STEP 5: SQUARE ROOT (Visual representation)
        # ====================================================================
        
        step5_badge = VGroup(
            Circle(radius=0.3, color=self.COLOR_WARNING, fill_opacity=1, stroke_width=0),
            Text("5", font_size=28, color=WHITE, weight=BOLD)
        )
        step5_badge[1].move_to(step5_badge[0].get_center())
        
        step5_text = Text("Take square root of both sides", font_size=28, color=self.COLOR_WARNING)
        step5_header = VGroup(step5_badge, step5_text).arrange(RIGHT, buff=0.5)
        step5_header.shift(UP*0.7+LEFT*1.5)
        
        self.play(
            GrowFromCenter(step5_badge),
            Write(step5_text),
            run_time=1.5
        )
        self.wait(1)
        
        # Show square root operation
        sqrt_eq = MathTex(
            r"\sqrt{(x + 3)^2} = \pm\sqrt{4}",
            font_size=42,
            color=self.COLOR_INFO
        )
        sqrt_eq.shift(DOWN*1.8)
        
        self.play(
            Write(sqrt_eq),
            run_time=2
        )
        self.wait(1.5)
        
        # Simplify
        simplified_sqrt = MathTex(
            r"x + 3 = \pm 2",
            font_size=48,
            color=self.COLOR_PRIMARY
        )
        simplified_sqrt.shift(DOWN*3.5)
        
        self.play(
            TransformMatchingTex(sqrt_eq.copy(), simplified_sqrt),
            run_time=2
        )
        self.wait(1.5)
        
        self.play(
            FadeOut(step5_header),
            FadeOut(sqrt_eq),
            FadeOut(factored_eq),
            run_time=1
        )
        
        # ====================================================================
        # STEP 6: FINAL SOLUTIONS (Split view with visual divider)
        # ====================================================================
        
        step6_badge = VGroup(
            Circle(radius=0.3, color=self.COLOR_WARNING, fill_opacity=1, stroke_width=0),
            Text("6", font_size=28, color=WHITE, weight=BOLD)
        )
        step6_badge[1].move_to(step6_badge[0].get_center())
        
        step6_text = Text("Solve for x", font_size=28, color=self.COLOR_WARNING)
        step6_header = VGroup(step6_badge, step6_text).arrange(RIGHT, buff=0.5)
        step6_header.shift(UP*0.7+LEFT*2)
        
        self.play(
            GrowFromCenter(step6_badge),
            Write(step6_text),
            run_time=1.5
        )
        self.wait(1)
        
        # Vertical divider for split cases
        vertical_divider = Line(
            start=UP*3, end=DOWN*3.5,
            color=self.COLOR_LIGHT,
            stroke_width=2
        )
        
        self.play(
            Create(vertical_divider),
            run_time=1
        )
        
        # LEFT CASE: x = -3 + 2
        case1_bg = RoundedRectangle(
            width=5.5, height=2.5,
            stroke_color=self.COLOR_SUCCESS,
            stroke_width=2,
            fill_color=self.COLOR_SUCCESS,
            fill_opacity=0.05,
            corner_radius=0.1
        ).shift(LEFT*3.5+DOWN*2)
        
        case1_label = Text("Case 1: +2", font_size=28, color=self.COLOR_SUCCESS, weight=BOLD)
        case1_label.shift(LEFT*3.5+DOWN*0.8)
        
        case1_calc = MathTex(r"x = -3 + 2", font_size=38, color=WHITE)
        case1_calc.shift(LEFT*3.5+DOWN*1.8)
        
        case1_arrow = MathTex(r"\Downarrow", font_size=28, color=self.COLOR_SUCCESS)
        case1_arrow.shift(LEFT*3.5+DOWN*2.5)
        
        case1_answer = MathTex(r"x = -1", font_size=48, color=self.COLOR_ACCENT, weight=BOLD)
        case1_answer.shift(LEFT*3.5+DOWN*3.2)
        
        # RIGHT CASE: x = -3 - 2
        case2_bg = RoundedRectangle(
            width=5.5, height=2.5,
            stroke_color=self.COLOR_SUCCESS,
            stroke_width=2,
            fill_color=self.COLOR_SUCCESS,
            fill_opacity=0.05,
            corner_radius=0.1
        ).shift(RIGHT*3.5+DOWN*2)
        
        case2_label = Text("Case 2: -2", font_size=28, color=self.COLOR_SUCCESS, weight=BOLD)
        case2_label.shift(RIGHT*3.5+DOWN*0.8)
        
        case2_calc = MathTex(r"x = -3 - 2", font_size=38, color=WHITE)
        case2_calc.shift(RIGHT*3.5+DOWN*1.8)
        
        case2_arrow = MathTex(r"\Downarrow", font_size=28, color=self.COLOR_SUCCESS)
        case2_arrow.shift(RIGHT*3.5+DOWN*2.5)
        
        case2_answer = MathTex(r"x = -5", font_size=48, color=self.COLOR_ACCENT, weight=BOLD)
        case2_answer.shift(RIGHT*3.5+DOWN*3.2)
        
        # Animate both cases
        self.play(
            DrawBorderThenFill(case1_bg),
            DrawBorderThenFill(case2_bg),
            run_time=1.2
        )
        
        self.play(
            Write(case1_label),
            Write(case2_label),
            run_time=1.2
        )
        self.wait(0.8)
        
        self.play(
            Write(case1_calc),
            Write(case2_calc),
            run_time=2
        )
        self.wait(1)
        
        self.play(
            GrowFromPoint(case1_arrow, case1_arrow.get_top()),
            GrowFromPoint(case2_arrow, case2_arrow.get_top()),
            run_time=0.8
        )
        
        self.play(
            Write(case1_answer),
            Write(case2_answer),
            run_time=2
        )
        self.wait(1)
        
        # Highlight final answers
        answer_box1 = SurroundingRectangle(
            case1_answer,
            color=self.COLOR_SUCCESS,
            buff=0.2,
            stroke_width=4
        )
        
        answer_box2 = SurroundingRectangle(
            case2_answer,
            color=self.COLOR_SUCCESS,
            buff=0.2,
            stroke_width=4
        )
        
        self.play(
            Create(answer_box1),
            Create(answer_box2),
            Flash(case1_answer, color=self.COLOR_SUCCESS),
            Flash(case2_answer, color=self.COLOR_SUCCESS),
            run_time=1.5
        )
        self.wait(3)
        
        # Final fade out
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )
        self.wait(1)
