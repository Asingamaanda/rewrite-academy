"""
Base class for all Grade 12 Calculus lessons.
Provides consistent styling and helper methods.
"""

from manim import *


class CalculusLesson(Scene):
    """
    Reusable base class for Grade 12 Calculus animations.
    Maintains consistent visual style across all lessons.
    """
    
    # Color scheme
    COLOR_FUNCTION = BLUE
    COLOR_DERIVATIVE = YELLOW
    COLOR_CONCLUSION = RED
    COLOR_HIGHLIGHT = GREEN
    COLOR_TITLE = WHITE
    
    # Font sizes
    FONT_TITLE = 44
    FONT_SUBTITLE = 32
    FONT_EQUATION = 40
    FONT_EXPLANATION = 28
    FONT_LABEL = 24
    
    def show_title(self, title_text, subtitle_text=None):
        """
        Display lesson title with optional subtitle.
        
        Args:
            title_text: Main title
            subtitle_text: Optional subtitle
        """
        title = Text(title_text, font_size=self.FONT_TITLE, color=self.COLOR_TITLE)
        title.to_edge(UP, buff=0.5)
        
        if subtitle_text:
            subtitle = Text(subtitle_text, font_size=self.FONT_SUBTITLE, color=GRAY)
            subtitle.next_to(title, DOWN)
            
            self.play(Write(title), run_time=2)
            self.wait(1)  # VOICEOVER: Title narration
            self.play(FadeIn(subtitle), run_time=1.5)
            self.wait(2)  # VOICEOVER: Subtitle narration
            
            return VGroup(title, subtitle)
        else:
            self.play(Write(title), run_time=2)
            self.wait(2)  # VOICEOVER: Title narration
            return title
    
    def show_equation(self, latex_str, color=None, position=ORIGIN):
        """
        Display a mathematical equation clearly.
        
        Args:
            latex_str: LaTeX string for the equation
            color: Color of the equation (default: COLOR_EQUATION blue)
            position: Position on screen
        """
        if color is None:
            color = self.COLOR_FUNCTION
            
        equation = MathTex(latex_str, font_size=self.FONT_EQUATION, color=color)
        equation.move_to(position)
        
        self.play(Write(equation), run_time=2)
        self.wait(2)  # VOICEOVER: Equation explanation
        
        return equation
    
    def show_explanation(self, text, position=DOWN*2.5, color=WHITE):
        """
        Display explanatory text.
        
        Args:
            text: Explanation text
            position: Position on screen
            color: Text color
        """
        explanation = Text(text, font_size=self.FONT_EXPLANATION, color=color)
        explanation.move_to(position)
        
        self.play(FadeIn(explanation), run_time=1.5)
        self.wait(2)  # VOICEOVER: Explanation narration
        
        return explanation
    
    def highlight_box(self, mobject, color=YELLOW):
        """
        Draw a box around important content.
        
        Args:
            mobject: Object to highlight
            color: Box color
        """
        box = SurroundingRectangle(mobject, color=color, buff=0.2)
        self.play(Create(box), run_time=1)
        self.wait(1)
        return box
    
    def pause_for_voiceover(self, duration=2):
        """
        Pause for voiceover narration.
        
        Args:
            duration: Seconds to wait
        """
        self.wait(duration)
    
    def clear_all(self):
        """Clear all objects from the scene."""
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
