"""
Scene 3: The Power Rule
Demonstrates the pattern and formula for differentiating power functions.
VOICEOVER: Use deep, slow, soothing voice throughout.
"""

from manim import *
from .base_lesson import CalculusLesson


class PowerRule(CalculusLesson):
    """
    Teaches the power rule for differentiation:
    If f(x) = x^n, then f'(x) = n·x^(n-1)
    
    Shows pattern recognition and visual transformation.
    """
    
    def construct(self):
        # VOICEOVER: "Now that we understand what derivatives mean, let's learn 
        # a powerful shortcut: the power rule."
        
        # Title
        title = self.show_title(
            "The Power Rule",
            "A Shortcut for Derivatives"
        )
        self.pause_for_voiceover(3)
        
        self.play(title.animate.scale(0.7).to_edge(UP, buff=0.3), run_time=1)
        self.wait(1)
        
        # VOICEOVER: "The power rule is one of the most useful tools in calculus. 
        # Let's discover the pattern."
        
        # Step 1: Show the general rule
        rule_label = Text("The Rule:", font_size=self.FONT_SUBTITLE, color=self.COLOR_HIGHLIGHT)
        rule_label.shift(UP*2.5)
        self.play(Write(rule_label), run_time=1.5)
        self.pause_for_voiceover(2)
        
        general_rule = MathTex(
            r"\text{If } f(x) = x^n \text{, then } f'(x) = n \cdot x^{n-1}",
            font_size=self.FONT_EQUATION,
            color=self.COLOR_DERIVATIVE
        ).shift(UP*1.5)
        
        self.play(Write(general_rule), run_time=2.5)
        self.pause_for_voiceover(4)
        
        # Highlight the rule
        rule_box = self.highlight_box(general_rule, color=self.COLOR_DERIVATIVE)
        self.pause_for_voiceover(2)
        
        self.play(FadeOut(rule_box), run_time=0.5)
        
        # VOICEOVER: "Let's see this pattern in action with specific examples."
        
        # Step 2: Show pattern with examples
        self.play(
            FadeOut(rule_label),
            general_rule.animate.scale(0.7).to_corner(UL).shift(DOWN*0.8),
            run_time=1
        )
        
        pattern_title = Text("Pattern Recognition:", font_size=self.FONT_SUBTITLE)
        pattern_title.shift(UP*2.2)
        self.play(Write(pattern_title), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # VOICEOVER: "Example 1: x to the power of 1."
        
        # Example 1: x^1 → 1
        ex1_function = MathTex(r"f(x) = x^1 = x", font_size=36, color=self.COLOR_FUNCTION)
        ex1_function.shift(UP*1)
        self.play(Write(ex1_function), run_time=2)
        self.pause_for_voiceover(3)
        
        # Show transformation
        arrow1 = Arrow(LEFT, RIGHT, color=YELLOW).next_to(ex1_function, DOWN, buff=0.3)
        self.play(GrowArrow(arrow1), run_time=1)
        
        # VOICEOVER: "Bring down the exponent 1, then reduce the power by 1. 
        # This gives us 1 times x to the power of 0, which equals 1."
        
        ex1_derivative = MathTex(r"f'(x) = 1 \cdot x^0 = 1", font_size=36, color=self.COLOR_DERIVATIVE)
        ex1_derivative.next_to(arrow1, DOWN, buff=0.3)
        self.play(Write(ex1_derivative), run_time=2)
        self.pause_for_voiceover(4)
        
        self.wait(2)
        
        # Move to side
        example1_group = VGroup(ex1_function, arrow1, ex1_derivative)
        self.play(example1_group.animate.scale(0.7).to_edge(LEFT).shift(DOWN*0.5), run_time=1)
        
        # VOICEOVER: "Example 2: x squared."
        
        # Example 2: x^2 → 2x
        ex2_function = MathTex(r"f(x) = x^2", font_size=36, color=self.COLOR_FUNCTION)
        ex2_function.shift(UP*1)
        self.play(Write(ex2_function), run_time=2)
        self.pause_for_voiceover(2)
        
        arrow2 = Arrow(LEFT, RIGHT, color=YELLOW).next_to(ex2_function, DOWN, buff=0.3)
        self.play(GrowArrow(arrow2), run_time=1)
        
        # VOICEOVER: "Bring down 2, reduce the power by 1. We get 2x to the power of 1, 
        # which is simply 2x."
        
        ex2_derivative = MathTex(r"f'(x) = 2 \cdot x^1 = 2x", font_size=36, color=self.COLOR_DERIVATIVE)
        ex2_derivative.next_to(arrow2, DOWN, buff=0.3)
        self.play(Write(ex2_derivative), run_time=2)
        self.pause_for_voiceover(4)
        
        self.wait(2)
        
        # Move to side
        example2_group = VGroup(ex2_function, arrow2, ex2_derivative)
        self.play(example2_group.animate.scale(0.7).to_edge(RIGHT).shift(DOWN*0.5), run_time=1)
        
        # VOICEOVER: "Example 3: x cubed."
        
        # Example 3: x^3 → 3x^2
        ex3_function = MathTex(r"f(x) = x^3", font_size=36, color=self.COLOR_FUNCTION)
        ex3_function.shift(UP*1)
        self.play(Write(ex3_function), run_time=2)
        self.pause_for_voiceover(2)
        
        arrow3 = Arrow(LEFT, RIGHT, color=YELLOW).next_to(ex3_function, DOWN, buff=0.3)
        self.play(GrowArrow(arrow3), run_time=1)
        
        # VOICEOVER: "Following the pattern: bring down 3, reduce the power. 
        # This gives us 3x squared."
        
        ex3_derivative = MathTex(r"f'(x) = 3 \cdot x^2 = 3x^2", font_size=36, color=self.COLOR_DERIVATIVE)
        ex3_derivative.next_to(arrow3, DOWN, buff=0.3)
        self.play(Write(ex3_derivative), run_time=2)
        self.pause_for_voiceover(4)
        
        self.wait(2)
        
        # VOICEOVER: "Do you see the pattern? The exponent becomes the coefficient, 
        # and the new exponent is one less."
        
        # Step 3: Highlight the pattern
        self.play(
            FadeOut(example1_group),
            FadeOut(example2_group),
            VGroup(ex3_function, arrow3, ex3_derivative).animate.move_to(ORIGIN),
            run_time=1
        )
        
        pattern_explanation = VGroup(
            Text("Notice the pattern:", font_size=self.FONT_EXPLANATION, color=YELLOW),
            Text("1. Bring the exponent down (multiply)", font_size=self.FONT_LABEL, color=WHITE),
            Text("2. Reduce the exponent by 1", font_size=self.FONT_LABEL, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(DOWN*2)
        
        for line in pattern_explanation:
            self.play(FadeIn(line), run_time=1.5)
            self.pause_for_voiceover(2)
        
        self.wait(2)
        
        # Clear for comprehensive example
        self.play(*[FadeOut(mob) for mob in [
            ex3_function, arrow3, ex3_derivative, pattern_explanation, pattern_title
        ]], run_time=1)
        
        # VOICEOVER: "Let's try a more complex example to solidify your understanding."
        
        # Step 4: Comprehensive example
        comp_title = Text("Complete Example:", font_size=self.FONT_SUBTITLE, color=self.COLOR_HIGHLIGHT)
        comp_title.shift(UP*2.5)
        self.play(Write(comp_title), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # Given function
        given_function = MathTex(r"f(x) = 5x^4", font_size=self.FONT_EQUATION, color=self.COLOR_FUNCTION)
        given_function.shift(UP*1.3)
        self.play(Write(given_function), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "For f of x equals 5x to the fourth, we apply the power rule."
        
        # Step-by-step breakdown
        step1 = Text("Step 1: Multiply by the exponent (4)", font_size=self.FONT_LABEL)
        step1.shift(UP*0.2)
        self.play(FadeIn(step1), run_time=1.5)
        self.pause_for_voiceover(3)
        
        intermediate1 = MathTex(r"= 4 \cdot 5x^4", font_size=32, color=YELLOW)
        intermediate1.next_to(step1, DOWN, buff=0.3)
        self.play(Write(intermediate1), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # VOICEOVER: "Step 2: Reduce the exponent by 1."
        
        step2 = Text("Step 2: Reduce the exponent by 1", font_size=self.FONT_LABEL)
        step2.next_to(intermediate1, DOWN, buff=0.5)
        self.play(FadeIn(step2), run_time=1.5)
        self.pause_for_voiceover(3)
        
        intermediate2 = MathTex(r"= 4 \cdot 5x^{4-1}", font_size=32, color=YELLOW)
        intermediate2.next_to(step2, DOWN, buff=0.3)
        self.play(Write(intermediate2), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # VOICEOVER: "Step 3: Simplify."
        
        step3 = Text("Step 3: Simplify", font_size=self.FONT_LABEL)
        step3.next_to(intermediate2, DOWN, buff=0.5)
        self.play(FadeIn(step3), run_time=1.5)
        self.pause_for_voiceover(2)
        
        final_answer = MathTex(r"f'(x) = 20x^3", font_size=self.FONT_EQUATION, color=self.COLOR_CONCLUSION)
        final_answer.next_to(step3, DOWN, buff=0.4)
        self.play(Write(final_answer), run_time=2)
        self.pause_for_voiceover(3)
        
        # Highlight final answer
        answer_box = self.highlight_box(final_answer, color=self.COLOR_CONCLUSION)
        self.pause_for_voiceover(2)
        
        # VOICEOVER: "Therefore, the derivative of 5x to the fourth is 20x cubed."
        
        self.wait(3)
        
        # Clear all
        self.clear_all()
        
        # VOICEOVER: "The power rule works for any real number exponent, 
        # making it incredibly powerful and efficient."
        
        # Final summary
        summary_title = Text("Power Rule Summary", font_size=self.FONT_TITLE, color=self.COLOR_HIGHLIGHT)
        summary_title.shift(UP*2.5)
        self.play(Write(summary_title), run_time=2)
        self.pause_for_voiceover(2)
        
        formula_box = MathTex(
            r"\frac{d}{dx}(x^n) = n \cdot x^{n-1}",
            font_size=50,
            color=self.COLOR_DERIVATIVE
        ).shift(UP*1)
        
        self.play(Write(formula_box), run_time=2.5)
        self.pause_for_voiceover(3)
        
        summary_box = self.highlight_box(formula_box, color=self.COLOR_DERIVATIVE)
        self.pause_for_voiceover(2)
        
        key_points = VGroup(
            Text("✓ Works for any power of x", font_size=self.FONT_LABEL, color=GREEN),
            Text("✓ Multiply by exponent, then reduce exponent by 1", font_size=self.FONT_LABEL, color=GREEN),
            Text("✓ Constants multiply through", font_size=self.FONT_LABEL, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(DOWN*1.2)
        
        for point in key_points:
            self.play(FadeIn(point), run_time=1.5)
            self.pause_for_voiceover(2.5)
        
        # VOICEOVER: "Practice this rule until it becomes second nature. 
        # It's the backbone of differentiation."
        
        self.wait(4)
        self.clear_all()
