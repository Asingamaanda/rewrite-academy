"""
Waves, Sound & Light - Visual Physics Lab
CAPS Grade 10/11 Core Content
Cinematic, Interactive, Conceptual
"""

from manim import *
import numpy as np

# ========== GLOBAL DESIGN SYSTEM ==========
config.background_color = "#0E1A25"

WAVE_COLOR = BLUE_C
SOUND_COLOR = GREEN_C
LIGHT_COLOR = YELLOW_C
ENERGY_COLOR = RED_C
TEXT_COLOR = WHITE
HIGHLIGHT_COLOR = "#FF6B6B"
INFO_COLOR = "#4ECDC4"


# ========== BASE CLASS ==========
class PhysicsLesson(Scene):
    """Base class for physics lessons with reusable methods"""
    
    COLOR_WAVE = WAVE_COLOR
    COLOR_SOUND = SOUND_COLOR
    COLOR_LIGHT = LIGHT_COLOR
    COLOR_ENERGY = ENERGY_COLOR
    COLOR_TEXT = TEXT_COLOR
    COLOR_HIGHLIGHT = HIGHLIGHT_COLOR
    COLOR_INFO = INFO_COLOR
    
    FONT_TITLE = 48
    FONT_SUBTITLE = 32
    FONT_BODY = 24
    FONT_SMALL = 20
    
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
    
    def highlight_box(self, mobject, color=None, buff=0.3):
        """Create highlighted box"""
        if color is None:
            color = self.COLOR_HIGHLIGHT
        box = SurroundingRectangle(mobject, color=color, buff=buff, corner_radius=0.1)
        self.play(Create(box), run_time=1)
        return box
    
    def ask_question(self, question_text, wait_time=4):
        """Interactive question pause"""
        question = Text(question_text, font_size=self.FONT_BODY, color=self.COLOR_INFO)
        question.shift(DOWN*2.5)
        self.play(FadeIn(question, shift=UP), run_time=1)
        self.wait(wait_time)
        self.play(FadeOut(question), run_time=0.8)


# ========== SCENE 1: INTRODUCTION ==========
class WavesIntro(PhysicsLesson):
    """Opening title scene"""
    
    def construct(self):
        # Main title
        title = Text("Waves, Sound & Light", font_size=60, color=self.COLOR_LIGHT)
        subtitle = Text("Physics is Motion in Patterns", font_size=32, color=self.COLOR_INFO)
        subtitle.next_to(title, DOWN, buff=0.5)
        
        self.play(FadeIn(title, shift=UP), run_time=1.5)
        self.play(FadeIn(subtitle), run_time=1)
        self.wait(1)
        
        # Create background wave animation
        wave_group = VGroup()
        for i in range(3):
            wave = FunctionGraph(
                lambda x: 0.3 * np.sin(x - i*0.5),
                x_range=[0, 2*PI],
                color=[self.COLOR_WAVE, self.COLOR_SOUND, self.COLOR_LIGHT][i]
            ).shift(DOWN*(1.5 + i*0.5))
            wave_group.add(wave)
        
        self.play(
            LaggedStart(*[Create(w) for w in wave_group], lag_ratio=0.3),
            run_time=2
        )
        self.wait(2)
        
        # Clear
        self.play(
            FadeOut(title, shift=UP),
            FadeOut(subtitle),
            FadeOut(wave_group),
            run_time=1.5
        )


# ========== SCENE 2: TRANSVERSE WAVES ==========
class TransverseWave(PhysicsLesson):
    """Interactive transverse wave visualization"""
    
    def construct(self):
        title = self.lesson_title("Transverse Wave", self.COLOR_WAVE)
        
        # Definition
        definition = Text("Oscillation ⊥ perpendicular to direction of travel",
                         font_size=self.FONT_BODY, color=self.COLOR_INFO)
        definition.shift(UP*2)
        self.play(FadeIn(definition), run_time=1.5)
        self.wait(1)
        
        # Create axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=4,
            axis_config={"color": GREY_A, "include_tip": True}
        ).shift(DOWN*0.5)
        
        self.play(Create(axes), run_time=1.5)
        
        # Animated wave propagation
        wave = always_redraw(lambda: axes.plot(
            lambda x: np.sin(x - self.time * 2),
            color=self.COLOR_WAVE,
            stroke_width=4
        ))
        
        self.add(wave)
        self.wait(3)
        
        # Add particle tracker
        particle = Dot(color=self.COLOR_HIGHLIGHT).move_to(axes.c2p(5, 0))
        self.play(FadeIn(particle, scale=0.5))
        
        # Animate particle moving up and down
        def update_particle(mob):
            x = 5
            y = np.sin(x - self.time * 2)
            mob.move_to(axes.c2p(x, y))
        
        particle.add_updater(update_particle)
        self.wait(3)
        particle.clear_updaters()
        
        # Labels
        direction_label = VGroup(
            Text("Particle Motion", font_size=self.FONT_SMALL, color=self.COLOR_HIGHLIGHT),
            Arrow(UP*0.5, DOWN*0.5, color=self.COLOR_HIGHLIGHT, stroke_width=3)
        ).arrange(RIGHT, buff=0.3).next_to(particle, RIGHT, buff=1)
        
        wave_direction = VGroup(
            Text("Wave Motion", font_size=self.FONT_SMALL, color=self.COLOR_WAVE),
            Arrow(LEFT*0.5, RIGHT*0.5, color=self.COLOR_WAVE, stroke_width=3)
        ).arrange(RIGHT, buff=0.3).shift(DOWN*2.5)
        
        self.play(
            FadeIn(direction_label, shift=LEFT),
            FadeIn(wave_direction, shift=UP),
            run_time=1.5
        )
        self.wait(2)
        
        # Examples
        examples = Text("Examples: Light, water ripples, string vibrations",
                       font_size=self.FONT_SMALL, color=self.COLOR_INFO)
        examples.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(examples, shift=UP), run_time=1)
        self.wait(2)
        
        # Clear
        self.remove(wave)
        self.play(
            FadeOut(VGroup(definition, axes, particle, direction_label, wave_direction, examples)),
            run_time=1
        )


# ========== SCENE 3: LONGITUDINAL WAVES ==========
class LongitudinalWave(PhysicsLesson):
    """Compression and rarefaction visualization"""
    
    def construct(self):
        title = self.lesson_title("Longitudinal Wave", self.COLOR_SOUND)
        
        # Definition
        definition = Text("Oscillation ∥ parallel to direction of travel",
                         font_size=self.FONT_BODY, color=self.COLOR_INFO)
        definition.shift(UP*2)
        self.play(FadeIn(definition), run_time=1.5)
        self.wait(1)
        
        # Create particles
        num_particles = 30
        dots = VGroup()
        
        for i in range(num_particles):
            dot = Dot(
                point=[i * 0.4 - 6, 0, 0],
                color=self.COLOR_SOUND,
                radius=0.08
            )
            dots.add(dot)
        
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.05), run_time=2)
        self.wait(0.5)
        
        # Compression/rarefaction animation
        def compress(mob, dt):
            for i, d in enumerate(mob):
                base_x = i * 0.4 - 6
                # Create compression zones
                shift = 0.15 * np.sin(i * 0.4 - self.time * 3)
                d.move_to([base_x + shift, 0, 0])
        
        dots.add_updater(compress)
        
        # Add labels during animation
        self.wait(1)
        
        compression_label = Text("Compression", font_size=self.FONT_SMALL, color=self.COLOR_HIGHLIGHT)
        compression_label.shift(UP*1.5 + LEFT*2)
        
        rarefaction_label = Text("Rarefaction", font_size=self.FONT_SMALL, color=BLUE)
        rarefaction_label.shift(UP*1.5 + RIGHT*2)
        
        self.play(
            FadeIn(compression_label, shift=DOWN),
            FadeIn(rarefaction_label, shift=DOWN),
            run_time=1
        )
        
        self.wait(4)
        
        dots.clear_updaters()
        
        # Direction arrow
        direction = VGroup(
            Text("Wave Direction", font_size=self.FONT_SMALL, color=self.COLOR_SOUND),
            Arrow(LEFT*1.5, RIGHT*1.5, color=self.COLOR_SOUND, stroke_width=4)
        ).arrange(DOWN, buff=0.3).shift(DOWN*1.8)
        
        self.play(FadeIn(direction, shift=UP), run_time=1)
        self.wait(1)
        
        # Examples
        examples = Text("Examples: Sound waves, seismic P-waves, spring coils",
                       font_size=self.FONT_SMALL, color=self.COLOR_INFO)
        examples.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(examples, shift=UP), run_time=1)
        self.wait(2)
        
        # Clear
        self.play(
            FadeOut(VGroup(definition, dots, compression_label, rarefaction_label, direction, examples)),
            run_time=1
        )


# ========== SCENE 4: WAVE EQUATION ==========
class WaveEquation(PhysicsLesson):
    """Universal wave equation with visual derivation"""
    
    def construct(self):
        title = self.lesson_title("The Universal Wave Equation", self.COLOR_HIGHLIGHT)
        
        # The equation
        self.section_divider("The Master Formula", self.COLOR_INFO)
        
        formula = MathTex("v = f \\lambda", font_size=70, color=self.COLOR_WAVE)
        self.play(Write(formula), run_time=2)
        self.wait(1)
        
        # Label components
        labels = VGroup(
            MathTex("v", " = ", "\\text{speed (m/s)}", font_size=28).set_color_by_tex("speed", self.COLOR_INFO),
            MathTex("f", " = ", "\\text{frequency (Hz)}", font_size=28).set_color_by_tex("frequency", self.COLOR_SOUND),
            MathTex("\\lambda", " = ", "\\text{wavelength (m)}", font_size=28).set_color_by_tex("wavelength", self.COLOR_LIGHT)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(DOWN*1.5)
        
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT) for l in labels], lag_ratio=0.3), run_time=2)
        self.wait(2)
        
        self.play(FadeOut(VGroup(formula, labels)), run_time=1)
        
        # Visual interpretation
        self.section_divider("Visual Interpretation", self.COLOR_INFO)
        
        interpretation = Text("How many wavelengths pass per second?",
                             font_size=self.FONT_BODY, color=self.COLOR_INFO)
        interpretation.shift(UP*2)
        self.play(Write(interpretation), run_time=2)
        self.wait(1)
        
        # Show 3 wavelengths
        wavelengths = VGroup()
        for i in range(3):
            wave_segment = FunctionGraph(
                lambda x, offset=i: 0.5 * np.sin(x),
                x_range=[i*2*PI, (i+1)*2*PI],
                color=self.COLOR_WAVE
            ).shift(LEFT*3 + DOWN*0.5)
            wavelengths.add(wave_segment)
        
        self.play(LaggedStart(*[Create(w) for w in wavelengths], lag_ratio=0.3), run_time=2)
        
        # Wavelength label
        lambda_arrow = DoubleArrow(
            wavelengths[0].get_left(),
            wavelengths[0].get_right(),
            color=self.COLOR_LIGHT,
            buff=0.1
        ).shift(DOWN*1)
        
        lambda_label = MathTex("\\lambda", font_size=36, color=self.COLOR_LIGHT)
        lambda_label.next_to(lambda_arrow, DOWN)
        
        self.play(Create(lambda_arrow), Write(lambda_label), run_time=1.5)
        self.wait(1)
        
        # Frequency explanation
        freq_text = MathTex("f = 3 \\text{ Hz}", font_size=32, color=self.COLOR_SOUND)
        freq_text.shift(DOWN*2.8)
        freq_explain = Text("(3 waves pass per second)", font_size=self.FONT_SMALL, color=self.COLOR_INFO)
        freq_explain.next_to(freq_text, DOWN, buff=0.3)
        
        self.play(Write(freq_text), FadeIn(freq_explain), run_time=1.5)
        self.wait(2)
        
        # Conclusion
        self.play(
            FadeOut(VGroup(interpretation, wavelengths, lambda_arrow, lambda_label, freq_text, freq_explain)),
            run_time=1
        )
        
        # Final formula with insight
        final_formula = MathTex("v = f \\lambda", font_size=80, color=self.COLOR_HIGHLIGHT)
        insight = Text("Speed = (cycles/second) × (distance/cycle)",
                      font_size=self.FONT_BODY, color=self.COLOR_INFO)
        insight.next_to(final_formula, DOWN, buff=0.8)
        
        self.play(Write(final_formula), run_time=2)
        self.play(FadeIn(insight, shift=UP), run_time=1.5)
        self.wait(3)


# ========== SCENE 5: SPEED OF SOUND ==========
class SoundSpeed(PhysicsLesson):
    """Echo demonstration and speed calculation"""
    
    def construct(self):
        title = self.lesson_title("Speed of Sound", self.COLOR_SOUND)
        
        # Echo experiment
        self.section_divider("Echo Experiment", self.COLOR_INFO)
        
        # Setup
        wall = Line(UP*2.5, DOWN*2.5, color=GREY_A, stroke_width=8)
        wall.shift(RIGHT*4)
        
        # Use simple circle to represent person
        person = Circle(radius=0.3, color=self.COLOR_SOUND, fill_opacity=0.5).shift(LEFT*4)
        
        distance_line = DashedLine(person.get_right(), wall.get_left(), color=self.COLOR_INFO)
        distance_label = MathTex("d", font_size=32, color=self.COLOR_INFO)
        distance_label.next_to(distance_line, UP)
        
        self.play(Create(wall), FadeIn(person), run_time=1)
        self.play(Create(distance_line), Write(distance_label), run_time=1)
        self.wait(1)
        
        # Sound wave going
        wave_out = Circle(radius=0.1, color=self.COLOR_SOUND, stroke_width=6)
        wave_out.move_to(person.get_center())
        
        self.play(
            wave_out.animate.scale(40).move_to(wall.get_center()).set_opacity(0),
            run_time=2
        )
        
        # Clap sound text
        clap_text = Text("CLAP!", font_size=24, color=self.COLOR_HIGHLIGHT)
        clap_text.next_to(person, UP)
        self.add(clap_text)
        self.wait(0.2)
        self.remove(clap_text)
        
        # Sound wave returning
        wave_back = Circle(radius=0.1, color=self.COLOR_HIGHLIGHT, stroke_width=6)
        wave_back.move_to(wall.get_center())
        
        self.play(
            wave_back.animate.scale(40).move_to(person.get_center()).set_opacity(0),
            run_time=2
        )
        
        # Echo text
        echo_text = Text("echo", font_size=24, color=self.COLOR_HIGHLIGHT)
        echo_text.next_to(person, UP)
        self.add(echo_text)
        self.wait(0.5)
        self.remove(echo_text)
        
        self.wait(0.5)
        
        # Calculation
        calc_title = Text("Calculation:", font_size=28, color=self.COLOR_INFO)
        calc_title.to_edge(UP, buff=1.5).shift(RIGHT*2)
        
        calc_steps = VGroup(
            MathTex("\\text{Total distance} = 2d", font_size=24),
            MathTex("v = \\frac{2d}{t}", font_size=24, color=self.COLOR_SOUND),
            MathTex("v \\approx 340 \\text{ m/s (in air)}", font_size=24, color=self.COLOR_HIGHLIGHT)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        calc_steps.next_to(calc_title, DOWN, aligned_edge=LEFT, buff=0.5)
        
        self.play(Write(calc_title), run_time=1)
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT) for s in calc_steps], lag_ratio=0.4), run_time=2)
        self.wait(2)
        
        # Factors affecting speed
        self.play(
            FadeOut(VGroup(wall, person, distance_line, distance_label, calc_title, calc_steps)),
            run_time=1
        )
        
        factors_title = Text("Speed depends on:", font_size=32, color=self.COLOR_INFO)
        factors_title.shift(UP*1.5)
        
        factors = VGroup(
            Text("• Medium (solid > liquid > gas)", font_size=24, color=self.COLOR_SOUND),
            Text("• Temperature (higher T → faster)", font_size=24, color=self.COLOR_SOUND),
            Text("• Pressure (minimal effect in gases)", font_size=24, color=self.COLOR_SOUND)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        
        self.play(Write(factors_title), run_time=1)
        self.play(LaggedStart(*[FadeIn(f, shift=RIGHT) for f in factors], lag_ratio=0.3), run_time=2)
        self.wait(3)


# ========== SCENE 6: ELECTROMAGNETIC WAVES ==========
class EMWave(ThreeDScene):
    """3D electromagnetic wave visualization"""
    
    COLOR_LIGHT = YELLOW_C
    COLOR_INFO = "#4ECDC4"
    FONT_TITLE = 48
    
    def construct(self):
        title = Text("Electromagnetic Wave", font_size=self.FONT_TITLE, color=self.COLOR_LIGHT)
        title.to_edge(UP)
        self.add(title)
        
        # Set 3D camera
        axes = ThreeDAxes(
            x_range=[-1, 8, 1],
            y_range=[-2, 2, 1],
            z_range=[-2, 2, 1],
            x_length=8,
            y_length=4,
            z_length=4
        )
        
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        self.add(axes)
        self.wait(0.5)
        
        # Electric field (oscillates in y-direction)
        e_wave = ParametricFunction(
            lambda t: np.array([t, np.sin(t), 0]),
            t_range=[0, 6*PI],
            color=self.COLOR_LIGHT,
            stroke_width=6
        )
        
        # Magnetic field (oscillates in z-direction)
        b_wave = ParametricFunction(
            lambda t: np.array([t, 0, np.sin(t)]),
            t_range=[0, 6*PI],
            color=BLUE,
            stroke_width=6
        )
        
        # Labels
        e_label = Text("Electric Field", font_size=20, color=self.COLOR_LIGHT)
        e_label.to_corner(UL).shift(DOWN*1.5)
        
        b_label = Text("Magnetic Field", font_size=20, color=BLUE)
        b_label.next_to(e_label, DOWN, aligned_edge=LEFT)
        
        # Animate waves
        self.play(Create(e_wave), run_time=3)
        self.add_fixed_in_frame_mobjects(e_label)
        self.play(FadeIn(e_label))
        
        self.play(Create(b_wave), run_time=3)
        self.add_fixed_in_frame_mobjects(b_label)
        self.play(FadeIn(b_label))
        
        self.wait(1)
        
        # Rotate camera
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        
        self.wait(1)
        
        # Key facts
        facts = Text("• No medium needed\n• Speed = c = 3×10⁸ m/s\n• Perpendicular oscillations",
                    font_size=20, color=self.COLOR_INFO, line_spacing=1.5)
        facts.to_corner(UR)
        self.add_fixed_in_frame_mobjects(facts)
        self.play(FadeIn(facts, shift=LEFT))
        
        self.wait(3)


# ========== SCENE 7: PHOTON ENERGY ==========
class PhotonEnergy(PhysicsLesson):
    """Quantum energy of photons"""
    
    def construct(self):
        title = self.lesson_title("Energy of a Photon", self.COLOR_ENERGY)
        
        # Quantum leap
        self.section_divider("The Quantum Leap", self.COLOR_INFO)
        
        # Formula
        formula = MathTex("E = hf", font_size=80, color=self.COLOR_ENERGY)
        self.play(Write(formula), run_time=2)
        self.wait(1)
        
        # Components
        components = VGroup(
            MathTex("E", " = ", "\\text{Energy (J)}", font_size=28).set_color_by_tex("Energy", self.COLOR_ENERGY),
            MathTex("h", " = ", "6.63 \\times 10^{-34} \\text{ J·s}", font_size=28).set_color_by_tex("6.63", self.COLOR_INFO),
            MathTex("f", " = ", "\\text{Frequency (Hz)}", font_size=28).set_color_by_tex("Frequency", self.COLOR_LIGHT)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(DOWN*1.5)
        
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT) for c in components], lag_ratio=0.3), run_time=2)
        self.wait(2)
        
        self.play(FadeOut(VGroup(formula, components)), run_time=1)
        
        # Visual spectrum
        self.section_divider("The Electromagnetic Spectrum", self.COLOR_INFO)
        
        spectrum = VGroup()
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        names = ["Radio", "Microwave", "Infrared", "Visible", "UV", "X-ray", "Gamma"]
        
        # Frequency arrow
        freq_arrow = Arrow(LEFT*5, RIGHT*5, color=self.COLOR_LIGHT, stroke_width=6)
        freq_arrow.shift(UP*1)
        
        freq_label = Text("Increasing Frequency →", font_size=24, color=self.COLOR_LIGHT)
        freq_label.next_to(freq_arrow, UP)
        
        energy_label = Text("Increasing Energy →", font_size=24, color=self.COLOR_ENERGY)
        energy_label.next_to(freq_arrow, DOWN)
        
        self.play(Create(freq_arrow), run_time=1.5)
        self.play(Write(freq_label), Write(energy_label), run_time=1.5)
        self.wait(1)
        
        # Show visible spectrum
        visible = Rectangle(height=0.8, width=2, color=WHITE, stroke_width=3)
        visible.shift(DOWN*1)
        
        for i, color in enumerate(colors):
            segment = Rectangle(height=0.8, width=2/6, fill_color=color, fill_opacity=0.8, stroke_width=0)
            segment.move_to(visible.get_left() + RIGHT*(i+0.5)*(2/6))
            spectrum.add(segment)
        
        spectrum.shift(DOWN*1)
        
        self.play(FadeIn(spectrum), Create(visible), run_time=2)
        
        visible_label = Text("Visible Light", font_size=20, color=WHITE)
        visible_label.next_to(visible, DOWN)
        self.play(Write(visible_label), run_time=1)
        self.wait(2)
        
        # Interactive question
        self.play(FadeOut(VGroup(freq_arrow, freq_label, energy_label, spectrum, visible, visible_label)), run_time=1)
        
        self.ask_question("If frequency doubles, what happens to energy?", wait_time=3)
        
        answer = Text("Energy DOUBLES too! (E = hf)", font_size=32, color=self.COLOR_ENERGY)
        self.play(FadeIn(answer, shift=UP), run_time=1.5)
        box = self.highlight_box(answer, color=self.COLOR_ENERGY)
        self.wait(3)


# ========== SCENE 8: FINAL SUMMARY ==========
class WavesSummary(PhysicsLesson):
    """Visual recap of all concepts"""
    
    def construct(self):
        title = Text("Physics of Waves: Summary", font_size=self.FONT_TITLE, color=self.COLOR_HIGHLIGHT)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title, shift=DOWN), run_time=1.5)
        self.wait(1)
        
        # Create summary cards
        cards = VGroup(
            VGroup(
                Text("Transverse", font_size=24, color=self.COLOR_WAVE),
                Text("⊥ motion", font_size=18)
            ).arrange(DOWN, buff=0.2),
            
            VGroup(
                Text("Longitudinal", font_size=24, color=self.COLOR_SOUND),
                Text("∥ motion", font_size=18)
            ).arrange(DOWN, buff=0.2),
            
            VGroup(
                MathTex("v = f\\lambda", font_size=28, color=self.COLOR_WAVE),
                Text("Universal", font_size=18)
            ).arrange(DOWN, buff=0.2),
            
            VGroup(
                Text("Sound", font_size=24, color=self.COLOR_SOUND),
                Text("340 m/s", font_size=18)
            ).arrange(DOWN, buff=0.2),
            
            VGroup(
                Text("Light (EM)", font_size=24, color=self.COLOR_LIGHT),
                MathTex("3 \\times 10^8", font_size=18)
            ).arrange(DOWN, buff=0.2),
            
            VGroup(
                MathTex("E = hf", font_size=28, color=self.COLOR_ENERGY),
                Text("Quantum", font_size=18)
            ).arrange(DOWN, buff=0.2)
        )
        
        # Arrange in grid
        cards.arrange_in_grid(rows=2, cols=3, buff=0.8)
        
        # Add boxes around cards
        boxes = VGroup()
        for card in cards:
            box = SurroundingRectangle(card, color=self.COLOR_INFO, buff=0.3, corner_radius=0.1)
            boxes.add(box)
        
        self.play(
            LaggedStart(*[AnimationGroup(Create(b), FadeIn(c, scale=0.8)) 
                         for b, c in zip(boxes, cards)], lag_ratio=0.2),
            run_time=4
        )
        self.wait(2)
        
        # Final message
        final_msg = Text("Waves carry energy and information through space and time",
                        font_size=28, color=self.COLOR_HIGHLIGHT)
        final_msg.to_edge(DOWN, buff=0.5)
        
        self.play(FadeIn(final_msg, shift=UP), run_time=2)
        self.wait(3)
        
        # Fadeout all
        self.play(
            FadeOut(VGroup(title, cards, boxes, final_msg)),
            run_time=2
        )
