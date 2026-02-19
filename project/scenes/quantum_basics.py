from manim import *
import numpy as np


class QuantumForDummies(Scene):
    def construct(self):
        # ===== INTRO =====
        title = Text("Quantum Physics for Dummies", font_size=56, color=BLUE)
        subtitle = Text("The Weird Rules of the Very Small", font_size=32, color=GRAY)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title), run_time=2)
        self.play(FadeIn(subtitle), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # ===== CONCEPT 1: Wave-Particle Duality =====
        concept1_title = Text("Concept 1: Wave-Particle Duality", font_size=40, color=YELLOW)
        concept1_title.to_edge(UP)
        self.play(Write(concept1_title), run_time=2)
        self.wait(1)
        
        # Classical particle
        particle_label = Text("Classical Particle:", font_size=28).to_edge(LEFT).shift(UP*2)
        particle = Dot(color=RED, radius=0.15).move_to(LEFT*4)
        
        self.play(Write(particle_label), FadeIn(particle), run_time=1.5)
        self.play(particle.animate.shift(RIGHT*8), run_time=3, rate_func=linear)
        self.wait(1)
        
        # Wave nature
        wave_label = Text("Quantum Particle (acts like a wave too!):", font_size=28)
        wave_label.to_edge(LEFT).shift(DOWN*0.5)
        
        self.play(Write(wave_label), run_time=1.5)
        
        axes = Axes(
            x_range=[0, 8, 1],
            y_range=[-2, 2, 1],
            x_length=8,
            y_length=2,
            axis_config={"include_tip": False, "include_numbers": False},
        ).shift(DOWN*2)
        
        wave = axes.plot(lambda x: np.sin(2*PI*x), color=BLUE)
        
        self.play(Create(axes), run_time=1)
        self.play(Create(wave), run_time=2)
        self.wait(2)
        
        key_point1 = Text("Key: Light & matter are BOTH!", font_size=30, color=GREEN)
        key_point1.to_edge(DOWN)
        self.play(Write(key_point1), run_time=2)
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
        
        # ===== CONCEPT 2: Superposition =====
        concept2_title = Text("Concept 2: Superposition", font_size=40, color=PURPLE)
        concept2_title.to_edge(UP)
        self.play(Write(concept2_title), run_time=2)
        self.wait(1)
        
        explanation = Text(
            "A quantum particle can be in multiple states\nAT THE SAME TIME...until you measure it!",
            font_size=30,
            color=WHITE
        ).shift(UP*1.5)
        
        self.play(Write(explanation), run_time=3)
        self.wait(2)
        
        # Coin analogy
        coin_text = Text("Like a coin spinning in the air:", font_size=28).shift(UP*0.5)
        self.play(Write(coin_text), run_time=1.5)
        
        # Spinning state
        coin = Circle(radius=0.5, color=YELLOW, fill_opacity=0.5).shift(DOWN*0.5)
        heads_label = Text("Heads", font_size=20, color=GREEN).move_to(coin.get_center())
        tails_label = Text("Tails", font_size=20, color=RED).move_to(coin.get_center())
        both_label = Text("BOTH!", font_size=24, color=ORANGE).move_to(coin.get_center())
        
        self.play(Create(coin), Write(both_label), run_time=1.5)
        self.wait(1)
        
        superposition_text = Text("(Superposition State)", font_size=24, color=ORANGE)
        superposition_text.next_to(coin, DOWN)
        self.play(Write(superposition_text), run_time=1.5)
        self.wait(2)
        
        # Measurement
        measure_text = Text("When you MEASURE:", font_size=28, color=RED)
        measure_text.to_edge(DOWN).shift(UP*1.5)
        self.play(Write(measure_text), run_time=1.5)
        self.wait(1)
        
        self.play(FadeOut(both_label), FadeOut(superposition_text), run_time=0.5)
        self.play(Write(heads_label), coin.animate.set_color(GREEN), run_time=1)
        
        collapsed_text = Text("It 'collapses' to ONE state", font_size=24, color=GREEN)
        collapsed_text.to_edge(DOWN)
        self.play(Write(collapsed_text), run_time=1.5)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
        
        # ===== CONCEPT 3: Uncertainty Principle =====
        concept3_title = Text("Concept 3: Uncertainty Principle", font_size=40, color=RED)
        concept3_title.to_edge(UP)
        self.play(Write(concept3_title), run_time=2)
        self.wait(1)
        
        heisenberg = Text("Heisenberg's Famous Rule:", font_size=32, color=BLUE)
        heisenberg.shift(UP*2)
        self.play(Write(heisenberg), run_time=2)
        self.wait(1)
        
        uncertainty_eq = MathTex(
            r"\Delta x \cdot \Delta p \geq \frac{\hbar}{2}",
            font_size=60,
            color=YELLOW
        ).shift(UP*0.5)
        
        self.play(Write(uncertainty_eq), run_time=2)
        self.wait(2)
        
        explanation_parts = VGroup(
            Text("Δx = uncertainty in position", font_size=26, color=GREEN),
            Text("Δp = uncertainty in momentum", font_size=26, color=GREEN),
            Text("ℏ = reduced Planck constant", font_size=26, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(DOWN*1.2)
        
        for part in explanation_parts:
            self.play(Write(part), run_time=1.5)
            self.wait(0.8)
        
        simple_text = Text(
            "In plain English:\nYou CANNOT know BOTH position AND momentum\nof a particle with perfect precision!",
            font_size=28,
            color=ORANGE,
            line_spacing=1.2
        ).to_edge(DOWN).shift(UP*0.5)
        
        self.play(Write(simple_text), run_time=3)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
        
        # ===== CONCEPT 4: Probability Wave =====
        concept4_title = Text("Concept 4: Probability Waves", font_size=40, color=TEAL)
        concept4_title.to_edge(UP)
        self.play(Write(concept4_title), run_time=2)
        self.wait(1)
        
        psi_text = Text("The Wave Function Ψ (Psi):", font_size=32, color=BLUE)
        psi_text.shift(UP*2.5)
        self.play(Write(psi_text), run_time=1.5)
        self.wait(1)
        
        # Probability wave
        axes_prob = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 1.5, 0.5],
            x_length=10,
            y_length=3,
            axis_config={"include_tip": True, "include_numbers": False},
        ).shift(DOWN*0.5)
        
        x_label = axes_prob.get_x_axis_label("Position", edge=RIGHT, direction=RIGHT)
        y_label = axes_prob.get_y_axis_label("Probability", edge=UP, direction=UP)
        
        # Gaussian probability distribution
        prob_wave = axes_prob.plot(
            lambda x: 1.2 * np.exp(-x**2/2),
            color=BLUE,
            x_range=[-4, 4]
        )
        
        self.play(Create(axes_prob), Write(x_label), Write(y_label), run_time=2)
        self.play(Create(prob_wave), run_time=2)
        self.wait(2)
        
        # Show particles appearing
        particles = VGroup(*[
            Dot(axes_prob.c2p(np.random.normal(0, 1), 0), color=RED, radius=0.05)
            for _ in range(50)
        ])
        
        measurement_text = Text("When measured, particle appears at:", font_size=26)
        measurement_text.to_edge(DOWN).shift(UP*0.5)
        self.play(Write(measurement_text), run_time=1.5)
        
        self.play(FadeIn(particles, lag_ratio=0.02), run_time=3)
        self.wait(2)
        
        highlight_text = Text(
            "Higher wave = Higher probability of finding particle there",
            font_size=24,
            color=YELLOW
        ).to_edge(DOWN)
        self.play(Write(highlight_text), run_time=2)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
        
        # ===== CONCEPT 5: Energy Levels =====
        concept5_title = Text("Concept 5: Quantized Energy", font_size=40, color=GREEN)
        concept5_title.to_edge(UP)
        self.play(Write(concept5_title), run_time=2)
        self.wait(1)
        
        quantized_text = Text(
            "Energy comes in discrete 'packets' (quanta)",
            font_size=30
        ).shift(UP*2.5)
        self.play(Write(quantized_text), run_time=2)
        self.wait(1)
        
        # Energy levels diagram
        levels = VGroup()
        level_values = [0.5, 1.5, 2.7, 4.1, 5.6]
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE]
        
        for i, (val, col) in enumerate(zip(level_values, colors)):
            line = Line(LEFT*3, RIGHT*3, color=col, stroke_width=4)
            line.shift(UP*(val-3))
            label = MathTex(f"E_{i+1}", color=col, font_size=36).next_to(line, LEFT)
            levels.add(VGroup(line, label))
        
        self.play(Create(levels), run_time=3, lag_ratio=0.3)
        self.wait(2)
        
        # Electron jumping
        electron = Dot(color=WHITE, radius=0.12).move_to(levels[0][0].get_center())
        electron_label = Text("electron", font_size=20).next_to(electron, DOWN, buff=0.1)
        
        self.play(FadeIn(electron), Write(electron_label), run_time=1)
        self.wait(1)
        
        jump_text = Text("Electrons jump between levels", font_size=28, color=YELLOW)
        jump_text.to_edge(DOWN).shift(UP*1)
        self.play(Write(jump_text), run_time=1.5)
        
        # Show quantum jump
        for i in [1, 3, 2, 4, 0]:
            self.play(
                electron.animate.move_to(levels[i][0].get_center()),
                electron_label.animate.next_to(levels[i][0].get_center(), DOWN, buff=0.1),
                run_time=0.8
            )
            self.wait(0.5)
        
        no_between = Text(
            "They NEVER exist between levels!\n(That's the 'quantum' in quantum physics)",
            font_size=26,
            color=RED,
            line_spacing=1.1
        ).to_edge(DOWN)
        self.play(FadeOut(jump_text), run_time=0.3)
        self.play(Write(no_between), run_time=2)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
        
        # ===== CONCEPT 6: Double Slit Experiment =====
        concept6_title = Text("Concept 6: Double Slit Experiment", font_size=38, color=ORANGE)
        concept6_title.to_edge(UP)
        self.play(Write(concept6_title), run_time=2)
        self.wait(1)
        
        subtitle6 = Text("The experiment that breaks your brain", font_size=26, color=GRAY)
        subtitle6.next_to(concept6_title, DOWN)
        self.play(Write(subtitle6), run_time=1.5)
        self.wait(1)
        
        # Setup
        barrier = Rectangle(height=4, width=0.2, color=WHITE, fill_opacity=1)
        barrier.shift(LEFT*2)
        
        slit1 = Line(LEFT*2 + UP*0.3, LEFT*2 + UP*1.5, color=BLACK, stroke_width=8)
        slit2 = Line(LEFT*2 + DOWN*0.3, LEFT*2 + DOWN*1.5, color=BLACK, stroke_width=8)
        
        screen = Rectangle(height=4, width=0.15, color=GRAY, fill_opacity=0.5)
        screen.shift(RIGHT*3)
        
        self.play(Create(barrier), Create(slit1), Create(slit2), Create(screen), run_time=2)
        self.wait(1)
        
        # Source
        source = Dot(LEFT*5, color=YELLOW, radius=0.15)
        source_label = Text("particle\nsource", font_size=18).next_to(source, DOWN)
        self.play(FadeIn(source), Write(source_label), run_time=1)
        self.wait(1)
        
        # Particle going through
        particle_exp = Dot(color=RED, radius=0.1).move_to(source.get_center())
        
        self.play(FadeIn(particle_exp), run_time=0.5)
        self.play(particle_exp.animate.move_to(LEFT*2), run_time=1)
        self.play(particle_exp.animate.move_to(screen.get_center() + UP*0.5), run_time=1)
        
        # Pattern on screen
        pattern_text = Text("Interference Pattern!", font_size=32, color=GREEN)
        pattern_text.to_edge(DOWN).shift(UP*1.5)
        
        # Create interference pattern
        pattern_lines = VGroup(*[
            Line(screen.get_center() + UP*y, screen.get_center() + UP*y + RIGHT*0.1,
                 stroke_width=6, color=GREEN).set_opacity(np.cos(y*2)**2)
            for y in np.linspace(-1.5, 1.5, 30)
        ])
        
        self.play(Create(pattern_lines), run_time=2)
        self.play(Write(pattern_text), run_time=1.5)
        self.wait(2)
        
        mind_blow = Text(
            "The particle goes through BOTH slits\nand interferes with ITSELF!",
            font_size=28,
            color=YELLOW,
            line_spacing=1.2
        ).to_edge(DOWN)
        
        self.play(FadeOut(pattern_text), run_time=0.3)
        self.play(Write(mind_blow), run_time=2)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
        
        # ===== FINALE =====
        finale_title = Text("Quantum Physics in a Nutshell", font_size=48, color=GOLD)
        finale_title.shift(UP*2.5)
        self.play(Write(finale_title), run_time=2)
        self.wait(1)
        
        summary = VGroup(
            Text("1. Things are waves AND particles", font_size=26, color=BLUE),
            Text("2. Multiple states at once (superposition)", font_size=26, color=PURPLE),
            Text("3. Can't know everything (uncertainty)", font_size=26, color=RED),
            Text("4. It's all probabilities", font_size=26, color=TEAL),
            Text("5. Energy is quantized (discrete)", font_size=26, color=GREEN),
            Text("6. Observation changes reality", font_size=26, color=ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(DOWN*0.5)
        
        for item in summary:
            self.play(Write(item), run_time=1.5)
            self.wait(0.8)
        
        self.wait(2)
        
        final_quote = Text(
            '"If you think you understand quantum mechanics,\nyou don\'t understand quantum mechanics."\n— Richard Feynman',
            font_size=24,
            color=GRAY,
            line_spacing=1.1,
            slant=ITALIC
        ).to_edge(DOWN, buff=0.5)
        
        self.play(FadeIn(final_quote), run_time=2)
        self.wait(4)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=2)
