"""
Scene 2: Derivative from First Principles
Shows the definition of a derivative with visual secant-to-tangent animation.
VOICEOVER: Use deep, slow, soothing voice throughout.
"""

from manim import *
from .base_lesson import CalculusLesson


class DerivativeDefinition(CalculusLesson):
    """
    Teaches derivatives from first principles using:
    - The formal definition
    - Visual demonstration with secant lines becoming tangent
    - ValueTracker for smooth h → 0 animation
    """
    
    def construct(self):
        # VOICEOVER: "In this lesson, we'll discover what a derivative truly means, 
        # starting from first principles."
        
        # Title
        title = self.show_title(
            "Derivative from First Principles",
            "The Foundation of Calculus"
        )
        self.pause_for_voiceover(3)
        
        self.play(title.animate.scale(0.7).to_edge(UP, buff=0.3), run_time=1)
        self.wait(1)
        
        # VOICEOVER: "The derivative measures how fast a function is changing. 
        # Let's see the formal definition."
        
        # Step 1: Show the definition
        definition_label = Text(
            "Definition of the Derivative:",
            font_size=self.FONT_EXPLANATION,
            color=self.COLOR_HIGHLIGHT
        ).shift(UP*2.5)
        
        self.play(Write(definition_label), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # The derivative formula
        derivative_formula = MathTex(
            r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}",
            font_size=self.FONT_EQUATION,
            color=self.COLOR_DERIVATIVE
        ).shift(UP*1.5)
        
        self.play(Write(derivative_formula), run_time=2.5)
        self.pause_for_voiceover(4)
        
        # VOICEOVER: "This formula finds the slope of the tangent line at any point. 
        # Let's visualize what this means."
        
        explanation = Text(
            "This measures the instantaneous rate of change",
            font_size=self.FONT_EXPLANATION,
            color=WHITE
        ).shift(UP*0.5)
        
        self.play(FadeIn(explanation), run_time=1.5)
        self.pause_for_voiceover(3)
        self.wait(1)
        
        # Clear text, keep title and formula at top
        self.play(
            FadeOut(definition_label),
            FadeOut(explanation),
            derivative_formula.animate.scale(0.8).to_corner(UL).shift(DOWN*0.8),
            run_time=1
        )
        
        # VOICEOVER: "Let's use a simple parabola, f of x equals x squared, 
        # to see this in action."
        
        # Step 2: Create axes and function
        axes = Axes(
            x_range=[-1, 4, 1],
            y_range=[-1, 10, 2],
            x_length=6,
            y_length=4.5,
            axis_config={"include_numbers": True, "font_size": 20},
        ).shift(DOWN*0.8)
        
        axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        
        # Function: f(x) = x^2
        graph = axes.plot(lambda x: x**2, color=self.COLOR_FUNCTION, x_range=[-0.5, 3.5])
        graph_label = MathTex("f(x) = x^2", font_size=28, color=self.COLOR_FUNCTION)
        graph_label.next_to(axes, RIGHT).shift(UP*1.5)
        
        self.play(Create(axes), Write(axes_labels), run_time=2)
        self.pause_for_voiceover(2)
        
        self.play(Create(graph), Write(graph_label), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "We'll choose a point on the curve. Let's use x equals 2."
        
        # Step 3: Mark the point x
        x_val = 2
        point_x = axes.c2p(x_val, x_val**2)
        dot_x = Dot(point_x, color=RED, radius=0.08)
        label_x = MathTex("(x, f(x))", font_size=24, color=RED).next_to(dot_x, UP+RIGHT, buff=0.15)
        
        self.play(FadeIn(dot_x), Write(label_x), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # VOICEOVER: "Now, we pick another point, a distance h away. This gives us 
        # x plus h."
        
        # Step 4: Create ValueTracker for h
        h_tracker = ValueTracker(1.5)  # Start with h = 1.5
        
        # Point at x+h
        dot_xh = always_redraw(lambda: Dot(
            axes.c2p(x_val + h_tracker.get_value(), (x_val + h_tracker.get_value())**2),
            color=GREEN,
            radius=0.08
        ))
        
        label_xh = always_redraw(lambda: MathTex(
            "(x+h, f(x+h))",
            font_size=24,
            color=GREEN
        ).next_to(dot_xh, UP+LEFT, buff=0.15))
        
        self.play(FadeIn(dot_xh), Write(label_xh), run_time=1.5)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "The line connecting these two points is called a secant line."
        
        # Step 5: Draw secant line
        secant_line = always_redraw(lambda: Line(
            axes.c2p(x_val, x_val**2),
            axes.c2p(x_val + h_tracker.get_value(), (x_val + h_tracker.get_value())**2),
            color=YELLOW,
            stroke_width=3
        ))
        
        secant_label = Text("Secant Line", font_size=24, color=YELLOW)
        secant_label.to_edge(RIGHT).shift(DOWN*0.5)
        
        self.play(Create(secant_line), FadeIn(secant_label), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "The slope of this secant line is f of x plus h, minus f of x, 
        # all divided by h."
        
        slope_formula = MathTex(
            r"\text{Slope} = \frac{f(x+h) - f(x)}{h}",
            font_size=30,
            color=YELLOW
        ).to_edge(RIGHT).shift(DOWN*1.5)
        
        self.play(Write(slope_formula), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "Now watch carefully. As h gets smaller and smaller, approaching zero, 
        # the secant line becomes the tangent line."
        
        # Step 6: Animate h → 0
        self.wait(1)
        
        # Change label to tangent when close enough
        def update_label():
            if h_tracker.get_value() < 0.3:
                secant_label.become(Text("Tangent Line", font_size=24, color=YELLOW).to_edge(RIGHT).shift(DOWN*0.5))
        
        self.play(
            h_tracker.animate.set_value(0.05),
            run_time=6,
            rate_func=smooth
        )
        
        # Update label
        tangent_label = Text("Tangent Line!", font_size=24, color=self.COLOR_DERIVATIVE)
        tangent_label.to_edge(RIGHT).shift(DOWN*0.5)
        self.play(Transform(secant_label, tangent_label), run_time=1)
        
        self.pause_for_voiceover(4)
        
        # VOICEOVER: "This tangent line's slope is the derivative at x equals 2."
        
        # Step 7: Show the result
        # For f(x) = x^2, f'(x) = 2x, so f'(2) = 4
        result = MathTex(
            r"f'(2) = 4",
            font_size=self.FONT_EQUATION,
            color=self.COLOR_CONCLUSION
        ).to_edge(RIGHT).shift(DOWN*2.5)
        
        result_box = SurroundingRectangle(result, color=self.COLOR_CONCLUSION, buff=0.2)
        
        self.play(Write(result), Create(result_box), run_time=2)
        self.pause_for_voiceover(3)
        
        # VOICEOVER: "The slope of the tangent line at x equals 2 is exactly 4. 
        # This is the derivative at that point."
        
        self.wait(2)
        
        # Step 8: Summary
        self.play(
            FadeOut(axes), FadeOut(axes_labels), FadeOut(graph), FadeOut(graph_label),
            FadeOut(dot_x), FadeOut(dot_xh), FadeOut(label_x), FadeOut(label_xh),
            FadeOut(secant_line), FadeOut(secant_label), FadeOut(slope_formula),
            FadeOut(result), FadeOut(result_box),
            run_time=1
        )
        
        # VOICEOVER: "Let's review the concept one more time."
        
        summary_title = Text("Key Concept:", font_size=self.FONT_SUBTITLE, color=self.COLOR_HIGHLIGHT)
        summary_title.shift(UP*2)
        self.play(Write(summary_title), run_time=1.5)
        self.pause_for_voiceover(2)
        
        summary_points = VGroup(
            Text("• h represents a small change in x", font_size=self.FONT_EXPLANATION),
            Text("• As h → 0, secant becomes tangent", font_size=self.FONT_EXPLANATION),
            Text("• The derivative is the slope of the tangent", font_size=self.FONT_EXPLANATION),
            Text("• It measures instantaneous rate of change", font_size=self.FONT_EXPLANATION),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(DOWN*0.3)
        
        for point in summary_points:
            self.play(FadeIn(point), run_time=1.5)
            self.pause_for_voiceover(3)
        
        # VOICEOVER: "This is the foundation of differential calculus. Practice visualizing 
        # this process with different functions."
        
        self.wait(3)
        self.clear_all()
