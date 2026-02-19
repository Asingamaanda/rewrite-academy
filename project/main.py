"""
Main entry point for Manim animations.

Run with:
    manim -pql main.py QuadraticReveal
    
Options:
    -p: preview (auto-play after rendering)
    -q: quality (l=low, m=medium, h=high, k=4k)
"""

from scenes.quadratic_scene import QuadraticReveal

# You can also define scenes directly here if preferred
# class MyScene(Scene):
#     def construct(self):
#         text = Text("Hello, Manim!")
#         self.play(Write(text))
#         self.wait()
