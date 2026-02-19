"""
Scene 4: Finding Turning Points
Demonstrates how to find maxima and minima using derivatives.
VOICEOVER: Use deep, slow, soothing voice throughout.
"""

from manim import *
from .base_lesson import CalculusLesson
import numpy as np


class TurningPoints(CalculusLesson):
    """
    Teaches how to find turning points (maxima and minima) by:
    - Finding where f'(x) = 0
    - Identifying the nature of turning points
    - Visual representation on a cubic function
    """
    
    def construct(self):
        # VOICEOVER: "In this final lesson, we'll discover how derivatives help us 
        # find the peaks and valleys of a function: the turning points."
        
        # Title
        title = self.show_title(
            "Finding Turning Points",
            "Maxima and Minima Using Derivatives"
        )
        self.pause_for_voiceover(4)
        
        self.play(title.animate.scale(0.7).to_edge(UP, buff=0.3), run_time=1)
        self.wait(1)
        
        # VOICEOVER: "A turning point occurs where the tangent line is horizontal. 
        # This means the derivative equals zero."
        
        # Step 1: Show key concept
        concept = Text(
            "Key Idea: At turning points, the slope is zero",
            font_size=self.FONT_EXPLANATION,
            color=self.COLOR_HIGHLIGHT
        ).shift(UP*2.5)
        
        self.play(Write(concept), run_time=2)
        self.pause_for_voiceover(4)
        
        concept_formula = MathTex(
            r"f'(x) = 0",
            font_size=self.FONT_EQUATION,
            color=self.COLOR_DERIVATIVE
        ).shift(UP*1.5)
        
        self.play(Write(concept_formula), run_time=2)
        self.pause_for_voiceover(3)
        
        self.wait(1)
        self.play(
            FadeOut(concept),
            concept_formula.animate.scale(0.7).to_corner(UL).shift(DOWN*0.8),
            run_time=1
        )
        
        # VOICEOVER: "Let's work through a complete example. Consider the cubic function 
        # f of x equals x cubed minus 6x squared plus 9x plus 1."
        
        # Step 2: Show the example function
        example_title = Text("Example:", font_size=self.FONT_SUBTITLE)
        example_title.shift(UP*2.3)
        self.play(Write(example_title), run_time=1.5)
        self.pause_for_voiceover(2)
        
        function = MathTex(
            r"f(x) = x^3 - 6x^2 + 9x + 1",
            font_size=self.FONT_EQUATION,
            color=self.COLOR_FUNCTION
        ).shift(UP*1.5)
        
        self.play(Write(function), run_time=2.5)
        self.pause_for_voiceover(4)
        
        # Step 3: Visualize the function first
        # VOICEOVER: "Let's first see what this function looks like."
        
        axes = Axes(
            x_range=[-0.5, 4.5, 1],
            y_range=[-2, 6, 2],
            x_length=7,
            y_length=4,
            axis_config={"include_numbers": True, "font_size": 20},
        ).shift(DOWN*1.2)
        
        axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        
        # The cubic function
        graph = axes.plot(
            lambda x: x**3 - 6*x**2 + 9*x + 1,
            color=self.COLOR_FUNCTION,
            x_range=[0, 4]
        )
        
        self.play(
            function.animate.scale(0.75).next_to(axes, RIGHT).shift(UP*2),
            example_title.animate.scale(0.8).next_to(axes, RIGHT).shift(UP*2.8),
            run_time=1
        )
        
        self.play(Create(axes), Write(axes_labels), run_time=2)
        self.pause_for_voiceover(2)
        
        self.play(Create(graph), run_time=2.5)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "Notice the curve has a maximum point and a minimum point. 
        # Let's find them mathematically."
        
        self.wait(2)
        
        # Step 4: Find the derivative
        # VOICEOVER: "Step 1: Find the derivative using the power rule."
        
        step1_text = Text("Step 1: Find f'(x)", font_size=self.FONT_LABEL, color=YELLOW)
        step1_text.next_to(function, DOWN, buff=0.4, aligned_edge=LEFT)
        self.play(Write(step1_text), run_time=1.5)
        self.pause_for_voiceover(3)
        
        derivative = MathTex(
            r"f'(x) = 3x^2 - 12x + 9",
            font_size=30,
            color=self.COLOR_DERIVATIVE
        ).next_to(step1_text, DOWN, buff=0.2, aligned_edge=LEFT)
        
        self.play(Write(derivative), run_time=2)
        self.pause_for_voiceover(4)
        
        # VOICEOVER: "Step 2: Set the derivative equal to zero and solve for x."
        
        step2_text = Text("Step 2: Set f'(x) = 0", font_size=self.FONT_LABEL, color=YELLOW)
        step2_text.next_to(derivative, DOWN, buff=0.4, aligned_edge=LEFT)
        self.play(Write(step2_text), run_time=1.5)
        self.pause_for_voiceover(3)
        
        equation_to_solve = MathTex(
            r"3x^2 - 12x + 9 = 0",
            font_size=30,
            color=WHITE
        ).next_to(step2_text, DOWN, buff=0.2, aligned_edge=LEFT)
        
        self.play(Write(equation_to_solve), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "We can factor out 3 to simplify."
        
        factored = MathTex(
            r"3(x^2 - 4x + 3) = 0",
            font_size=30,
            color=WHITE
        ).next_to(equation_to_solve, DOWN, buff=0.2, aligned_edge=LEFT)
        
        self.play(Write(factored), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "Now factor the quadratic expression."
        
        factored2 = MathTex(
            r"3(x - 1)(x - 3) = 0",
            font_size=30,
            color=WHITE
        ).next_to(factored, DOWN, buff=0.2, aligned_edge=LEFT)
        
        self.play(Write(factored2), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "Therefore, x equals 1 or x equals 3."
        
        solutions = MathTex(
            r"x = 1 \text{ or } x = 3",
            font_size=32,
            color=self.COLOR_CONCLUSION
        ).next_to(factored2, DOWN, buff=0.3, aligned_edge=LEFT)
        
        self.play(Write(solutions), run_time=2)
        self.pause_for_voiceover(3)
        
        solution_box = SurroundingRectangle(solutions, color=self.COLOR_CONCLUSION, buff=0.15)
        self.play(Create(solution_box), run_time=1)
        self.pause_for_voiceover(2)
        
        # VOICEOVER: "These x-values are where our turning points occur. 
        # Let's mark them on the graph."
        
        # Step 5: Mark the turning points on the graph
        self.wait(1)
        
        # Calculate y-values
        y1 = 1**3 - 6*(1**2) + 9*1 + 1  # x=1: y=5
        y2 = 3**3 - 6*(3**2) + 9*3 + 1  # x=3: y=1
        
        point1 = axes.c2p(1, y1)
        point2 = axes.c2p(3, y2)
        
        # Maximum at (1, 5)
        dot1 = Dot(point1, color=RED, radius=0.1)
        label1 = MathTex("(1, 5)", font_size=24, color=RED).next_to(dot1, UP, buff=0.15)
        max_label = Text("Maximum", font_size=20, color=RED).next_to(label1, UP, buff=0.1)
        
        self.play(FadeIn(dot1), Write(label1), run_time=1.5)
        self.pause_for_voiceover(2)
        
        self.play(Write(max_label), run_time=1)
        self.pause_for_voiceover(2)
        
        # Minimum at (3, 1)
        dot2 = Dot(point2, color=GREEN, radius=0.1)
        label2 = MathTex("(3, 1)", font_size=24, color=GREEN).next_to(dot2, DOWN, buff=0.15)
        min_label = Text("Minimum", font_size=20, color=GREEN).next_to(label2, DOWN, buff=0.1)
        
        self.play(FadeIn(dot2), Write(label2), run_time=1.5)
        self.pause_for_voiceover(2)
        
        self.play(Write(min_label), run_time=1)
        self.pause_for_voiceover(2)
        
        # VOICEOVER: "At x equals 1, we have a maximum with a value of 5. 
        # At x equals 3, we have a minimum with a value of 1."
        
        # Draw horizontal tangent lines to emphasize slope = 0
        tangent1 = Line(
            axes.c2p(0.5, y1),
            axes.c2p(1.5, y1),
            color=YELLOW,
            stroke_width=3
        )
        
        tangent2 = Line(
            axes.c2p(2.5, y2),
            axes.c2p(3.5, y2),
            color=YELLOW,
            stroke_width=3
        )
        
        self.play(Create(tangent1), Create(tangent2), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "Notice the tangent lines are perfectly horizontal at these points, 
        # confirming that the slope, or derivative, is zero."
        
        slope_note = Text(
            "Horizontal tangents → f'(x) = 0",
            font_size=self.FONT_LABEL,
            color=YELLOW
        ).to_edge(DOWN, buff=0.5)
        
        self.play(FadeIn(slope_note), run_time=1.5)
        self.pause_for_voiceover(3)
        
        self.wait(3)
        
        # Clear for summary
        self.clear_all()
        
        # VOICEOVER: "Let's summarize the complete process for finding turning points."
        
        # Summary
        summary_title = Text(
            "Finding Turning Points: Complete Method",
            font_size=self.FONT_TITLE,
            color=self.COLOR_HIGHLIGHT
        )
        summary_title.to_edge(UP, buff=0.5)
        self.play(Write(summary_title), run_time=2)
        self.pause_for_voiceover(3)
        
        steps = VGroup(
            Text("1. Find the derivative f'(x)", font_size=self.FONT_EXPLANATION, color=WHITE),
            Text("2. Set f'(x) = 0 and solve for x", font_size=self.FONT_EXPLANATION, color=WHITE),
            Text("3. Substitute x-values into f(x) to find y-coordinates", font_size=self.FONT_EXPLANATION, color=WHITE),
            Text("4. Identify maximum vs minimum", font_size=self.FONT_EXPLANATION, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).shift(UP*0.5)
        
        for i, step in enumerate(steps):
            self.play(FadeIn(step), run_time=1.8)
            self.pause_for_voiceover(3)
        
        # VOICEOVER: "Follow these four steps, and you'll be able to find any turning point. 
        # This skill is essential for optimization problems in calculus."
        
        # Additional note
        note = Text(
            "Note: Use the second derivative test or a table\nto determine if points are maxima or minima",
            font_size=self.FONT_LABEL,
            color=GRAY,
            line_spacing=1.2
        ).to_edge(DOWN, buff=0.8)
        
        self.play(FadeIn(note), run_time=2)
        self.pause_for_voiceover(4)
        
        # VOICEOVER: "With practice, finding turning points will become second nature. 
        # Keep working through problems, and you'll master this concept."
        
        self.wait(4)
        self.clear_all()
        
        # Final message
        final_message = Text(
            "You've completed the Grade 12 Calculus essentials!\nPractice these concepts daily for exam success.",
            font_size=self.FONT_SUBTITLE,
            color=self.COLOR_HIGHLIGHT,
            line_spacing=1.3
        )
        
        self.play(FadeIn(final_message), run_time=2)
        self.pause_for_voiceover(4)
        
        # VOICEOVER: "Congratulations! You've learned the fundamental concepts of calculus. 
        # Practice these techniques regularly, and you'll excel in your exams. Good luck!"
        
        self.wait(4)
