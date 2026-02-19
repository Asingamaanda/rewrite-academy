"""
Grade 12 Calculus - Complete Course
Main entry point for all calculus lessons.
"""

from project.scenes.limits import IntroductionToLimits
from project.scenes.derivative_definition import DerivativeDefinition
from project.scenes.power_rule import PowerRule
from project.scenes.turning_points import TurningPoints


# All scenes are imported and ready to render
# Use the scene class names when running manim commands

# RENDERING INSTRUCTIONS:
# Navigate to class directory, then run:
#
# Scene 1: .venv/Scripts/manim.exe -pql project/calculus_main.py IntroductionToLimits
# Scene 2: .venv/Scripts/manim.exe -pql project/calculus_main.py DerivativeDefinition
# Scene 3: .venv/Scripts/manim.exe -pql project/calculus_main.py PowerRule
# Scene 4: .venv/Scripts/manim.exe -pql project/calculus_main.py TurningPoints
#
# Quality: -ql (low/test), -qm (medium), -qh (high), -qk (4K)
