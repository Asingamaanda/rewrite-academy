"""
Scene 1: Introduction to Limits
Demonstrates limits using algebraic simplification.
VOICEOVER: Use deep, slow, soothing voice throughout.
"""

from manim import *
from .base_lesson import CalculusLesson


class IntroductionToLimits(CalculusLesson):
    """
    Teaches the concept of limits using a classic example:
    lim(x→1) of (x² - 1)/(x - 1)
    """
    
    def construct(self):
        # VOICEOVER: "Welcome to our lesson on limits. Today we'll explore what happens 
        # when a function approaches a specific value."
        
        # Title
        title = self.show_title("Introduction to Limits", "Understanding Function Behavior")
        self.pause_for_voiceover(3)
        
        # Move title to top permanently
        self.play(title.animate.scale(0.7).to_edge(UP, buff=0.3), run_time=1)
        self.wait(1)
        
        # VOICEOVER: "Let's examine the function f of x equals x squared minus 1, 
        # divided by x minus 1."
        
        # Step 1: Show the function
        function_label = Text("Consider this function:", font_size=self.FONT_EXPLANATION)
        function_label.shift(UP*2.5)
        self.play(Write(function_label), run_time=1.5)
        self.pause_for_voiceover(2)
        
        function = MathTex(
            r"f(x) = \frac{x^2 - 1}{x - 1}",
            font_size=self.FONT_EQUATION,
            color=self.COLOR_FUNCTION
        ).shift(UP*1.5)
        
        self.play(Write(function), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "What happens when x approaches 1? Let's investigate."
        
        # Step 2: Show the limit question
        limit_question = MathTex(
            r"\lim_{x \to 1} \frac{x^2 - 1}{x - 1} = ?",
            font_size=self.FONT_EQUATION,
            color=self.COLOR_HIGHLIGHT
        ).shift(UP*0.3)
        
        self.play(Write(limit_question), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "If we substitute x equals 1 directly, we get 0 over 0, 
        # which is undefined. So we need a different approach."
        
        # Step 3: Show substitution problem
        problem_text = Text(
            "Direct substitution gives: 0/0 (undefined!)",
            font_size=self.FONT_EXPLANATION,
            color=RED
        ).shift(DOWN*0.5)
        
        self.play(FadeIn(problem_text), run_time=1.5)
        self.pause_for_voiceover(3)
        self.wait(1)
        
        # Clear explanation text
        self.play(FadeOut(problem_text), FadeOut(function_label), run_time=0.8)
        
        # VOICEOVER: "The solution is to factor the numerator and simplify."
        
        # Step 4: Show factorization
        factor_text = Text("Let's factor the numerator:", font_size=self.FONT_EXPLANATION)
        factor_text.shift(DOWN*0.5)
        self.play(Write(factor_text), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # Factored form
        factored = MathTex(
            r"f(x) = \frac{(x-1)(x+1)}{x - 1}",
            font_size=self.FONT_EQUATION,
            color=self.COLOR_FUNCTION
        ).shift(DOWN*1.5)
        
        self.play(Write(factored), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "Notice that x minus 1 appears in both the numerator and denominator."
        
        # Highlight cancellation
        box1 = SurroundingRectangle(factored[0][5:9], color=YELLOW)  # (x-1) in numerator
        box2 = SurroundingRectangle(factored[0][14:18], color=YELLOW)  # (x-1) in denominator
        
        self.play(Create(box1), Create(box2), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # VOICEOVER: "We can cancel these terms, as long as x is not equal to 1."
        
        cancel_note = Text(
            "Cancel (for x ≠ 1)",
            font_size=self.FONT_LABEL,
            color=YELLOW
        ).next_to(factored, RIGHT)
        
        self.play(Write(cancel_note), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # Step 5: Simplified form
        self.play(
            FadeOut(box1), FadeOut(box2), 
            FadeOut(cancel_note), FadeOut(factor_text),
            run_time=0.8
        )
        
        # VOICEOVER: "After cancellation, we're left with simply x plus 1."
        
        simplified = MathTex(
            r"f(x) = x + 1",
            font_size=self.FONT_EQUATION,
            color=self.COLOR_FUNCTION
        ).shift(DOWN*2.5)
        
        self.play(Write(simplified), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "Now we can safely substitute x equals 1."
        
        # Step 6: Calculate limit
        limit_calc = MathTex(
            r"\lim_{x \to 1} (x + 1) = 1 + 1 = 2",
            font_size=self.FONT_EQUATION,
            color=self.COLOR_DERIVATIVE
        ).shift(DOWN*3.5)
        
        self.play(Write(limit_calc), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "Therefore, the limit as x approaches 1 is equal to 2."
        
        # Final answer box
        final_answer = MathTex(
            r"\lim_{x \to 1} \frac{x^2 - 1}{x - 1} = 2",
            font_size=self.FONT_EQUATION + 4,
            color=self.COLOR_CONCLUSION
        )
        
        # Clear and show final answer
        self.wait(1)
        self.play(
            FadeOut(function),
            FadeOut(limit_question),
            FadeOut(factored),
            FadeOut(simplified),
            FadeOut(limit_calc),
            run_time=1
        )
        
        final_answer.move_to(ORIGIN)
        self.play(Write(final_answer), run_time=2.5)
        self.pause_for_voiceover(3)
        
        # Highlight the answer
        answer_box = self.highlight_box(final_answer, color=self.COLOR_CONCLUSION)
        self.pause_for_voiceover(2)
        
        # VOICEOVER: "This is the fundamental concept of limits. We found the value 
        # the function approaches, even though it's undefined at that exact point."
        
        key_concept = Text(
            "Key: Limits describe the value a function approaches,\nnot necessarily the value at that point.",
            font_size=self.FONT_EXPLANATION,
            color=WHITE,
            line_spacing=1.2
        ).to_edge(DOWN, buff=0.8)
        
        self.play(FadeIn(key_concept), run_time=2)
        self.pause_for_voiceover(4)
        
        # VOICEOVER: "Understanding limits is essential for calculus. Take your time 
        # to practice similar problems."
        
        self.wait(3)
        self.clear_all()
