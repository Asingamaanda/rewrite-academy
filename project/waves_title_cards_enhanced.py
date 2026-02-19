"""
Enhanced Professional Title Cards for Waves Physics Lesson
Grade 10/11 CAPS Curriculum - With detailed subtopics and transitions
"""

from manim import *

# ========== DESIGN SYSTEM ==========
config.background_color = "#0E1A25"

WAVE_COLOR = BLUE_C
SOUND_COLOR = GREEN_C
LIGHT_COLOR = YELLOW_C
ACCENT_COLOR = "#FF6B6B"
INFO_COLOR = "#4ECDC4"


# ========== MAIN TITLE CARD ==========
class WavesTitleCard(Scene):
    """Opening title card for the complete lesson"""
    
    def construct(self):
        # Background gradient effect
        background_rect = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color=BLUE_E,
            fill_opacity=0.1,
            stroke_width=0
        )
        self.add(background_rect)
        
        # Main title
        title = Text(
            "Waves, Sound & Light",
            font_size=64,
            color=WHITE,
            weight=BOLD
        )
        
        # Subtitle
        subtitle = Text(
            "Physics of Wave Motion",
            font_size=36,
            color=INFO_COLOR
        )
        subtitle.next_to(title, DOWN, buff=0.5)
        
        # Grade level
        grade = Text(
            "Grade 10/11 • CAPS Curriculum",
            font_size=24,
            color=GREY_A
        )
        grade.to_edge(DOWN, buff=1)
        
        # Decorative wave
        wave_path = ParametricFunction(
            lambda t: np.array([t, 0.3*np.sin(3*t), 0]),
            t_range=[-7, 7],
            color=WAVE_COLOR,
            stroke_width=4
        )
        wave_path.shift(UP*2.5)
        
        # Animation sequence
        self.play(Create(wave_path), run_time=2)
        self.play(FadeIn(title, shift=UP), run_time=1.5)
        self.play(Write(subtitle), run_time=1)
        self.wait(1)
        self.play(FadeIn(grade, shift=UP), run_time=0.8)
        self.wait(2)
        
        # Fade out
        self.play(
            FadeOut(VGroup(title, subtitle, grade, wave_path, background_rect)),
            run_time=1
        )


# ========== SECTION 1: WAVE TYPES ==========
class WaveTypesSectionCard(Scene):
    """Section divider with detailed learning objectives and subtopics"""
    
    def construct(self):
        section_num = Text("SECTION 1", font_size=28, color=GREY_B, weight=BOLD)
        section_num.to_edge(UP, buff=0.8)
        
        section_title = Text("Types of Waves", font_size=56, color=WAVE_COLOR, weight=BOLD)
        section_title.next_to(section_num, DOWN, buff=0.5)
        
        # Learning objectives
        obj_title = Text("Learning Objectives:", font_size=24, color=INFO_COLOR, weight=BOLD)
        obj_title.next_to(section_title, DOWN, buff=0.8)
        
        objectives = VGroup(
            Text("• Understand two main wave types", font_size=20, color=WHITE),
            Text("• Identify direction of energy transfer", font_size=20, color=WHITE),
            Text("• Compare motion patterns", font_size=20, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        objectives.next_to(obj_title, DOWN, buff=0.3, aligned_edge=LEFT)
        
        # Topics covered
        topics_title = Text("Topics Covered:", font_size=24, color=ACCENT_COLOR, weight=BOLD)
        topics_title.next_to(objectives, DOWN, buff=0.6)
        
        topics = VGroup(
            Text("1.1  Transverse Waves → perpendicular motion", font_size=22, color=WAVE_COLOR),
            Text("1.2  Longitudinal Waves → parallel motion", font_size=22, color=WAVE_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        topics.next_to(topics_title, DOWN, buff=0.3, aligned_edge=LEFT)
        
        line = Line(LEFT*5, RIGHT*5, color=WAVE_COLOR, stroke_width=3)
        line.next_to(section_num, DOWN, buff=0.2)
        
        # Animation
        self.play(Write(section_num), Create(line), run_time=0.8)
        self.play(FadeIn(section_title, scale=0.8), run_time=1)
        self.wait(0.5)
        self.play(Write(obj_title), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(obj, shift=RIGHT*0.3) for obj in objectives], lag_ratio=0.3), run_time=1.5)
        self.wait(0.8)
        self.play(Write(topics_title), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(topic, shift=RIGHT*0.3) for topic in topics], lag_ratio=0.4), run_time=1.2)
        self.wait(2.5)
        
        self.play(FadeOut(VGroup(section_num, section_title, obj_title, objectives, topics_title, topics, line)), run_time=1)


# ========== TRANSITION: TRANSVERSE TO LONGITUDINAL ==========
class TransitionToLongitudinal(Scene):
    """Clear transition between wave types"""
    
    def construct(self):
        prev_topic = Text("Transverse Waves ✓", font_size=32, color=GREY_B)
        prev_topic.to_edge(UP, buff=2)
        
        arrow = Arrow(start=UP*0.5, end=DOWN*0.5, color=WAVE_COLOR, stroke_width=6, max_tip_length_to_length_ratio=0.3)
        
        next_topic = Text("Next: Longitudinal Waves", font_size=40, color=WAVE_COLOR, weight=BOLD)
        next_topic.to_edge(DOWN, buff=2)
        
        difference = Text("Motion changes from ⊥ to ∥", font_size=28, color=INFO_COLOR, slant=ITALIC)
        difference.next_to(arrow, RIGHT, buff=1)
        
        self.play(FadeIn(prev_topic, shift=DOWN), run_time=0.8)
        self.play(GrowArrow(arrow), run_time=1)
        self.play(FadeIn(difference, shift=LEFT), run_time=0.8)
        self.play(Write(next_topic), run_time=1)
        self.wait(1.5)
        self.play(FadeOut(VGroup(prev_topic, arrow, next_topic, difference)), run_time=0.8)


# ========== KEY CONCEPT CARD ==========
class KeyConceptWaveEquation(Scene):
    """Highlight key concept before wave equation section"""
    
    def construct(self):
        label = Text("KEY CONCEPT", font_size=28, color=ACCENT_COLOR, weight=BOLD)
        label.to_edge(UP, buff=1.5)
        
        concept_text = Text(
            "All waves follow the same\nmathematical relationship",
            font_size=36,
            color=WHITE,
            line_spacing=1.3
        )
        
        box = SurroundingRectangle(concept_text, color=INFO_COLOR, buff=0.5, corner_radius=0.2, stroke_width=4)
        concept_group = VGroup(box, concept_text)
        
        preview = MathTex("v = f\\lambda", font_size=56, color=INFO_COLOR)
        preview.next_to(concept_group, DOWN, buff=0.8)
        
        self.play(Write(label), run_time=0.8)
        self.play(Create(box), FadeIn(concept_text, scale=0.9), run_time=1.2)
        self.wait(1)
        self.play(Write(preview), run_time=1.2)
        self.wait(2)
        self.play(FadeOut(VGroup(label, concept_group, preview)), run_time=0.8)


# ========== SECTION 2: WAVE EQUATION ==========
class WaveEquationSectionCard(Scene):
    """Detailed wave equation section with variable explanations"""
    
    def construct(self):
        section_num = Text("SECTION 2", font_size=28, color=GREY_B, weight=BOLD)
        section_num.to_edge(UP, buff=0.8)
        
        section_title = Text("Wave Properties & Mathematics", font_size=48, color=INFO_COLOR, weight=BOLD)
        section_title.next_to(section_num, DOWN, buff=0.5)
        
        eq_label = Text("Universal Wave Equation:", font_size=24, color=ACCENT_COLOR)
        eq_label.next_to(section_title, DOWN, buff=0.8)
        
        equation = MathTex("v = f\\lambda", font_size=72, color=WHITE)
        equation.next_to(eq_label, DOWN, buff=0.5)
        
        # Detailed explanations
        explanations = VGroup(
            VGroup(
                MathTex("v", font_size=32, color=INFO_COLOR),
                Text("= velocity (m/s)", font_size=20, color=GREY_A),
                Text("How fast the wave moves", font_size=18, color=GREY_B, slant=ITALIC)
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                MathTex("f", font_size=32, color=INFO_COLOR),
                Text("= frequency (Hz)", font_size=20, color=GREY_A),
                Text("Oscillations per second", font_size=18, color=GREY_B, slant=ITALIC)
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                MathTex("\\lambda", font_size=32, color=INFO_COLOR),
                Text("= wavelength (m)", font_size=20, color=GREY_A),
                Text("Distance between peaks", font_size=18, color=GREY_B, slant=ITALIC)
            ).arrange(RIGHT, buff=0.3)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        explanations.next_to(equation, DOWN, buff=0.7)
        
        line = Line(LEFT*5, RIGHT*5, color=INFO_COLOR, stroke_width=3)
        line.next_to(section_num, DOWN, buff=0.2)
        
        self.play(Write(section_num), Create(line), run_time=0.8)
        self.play(FadeIn(section_title, scale=0.9), run_time=1)
        self.wait(0.5)
        self.play(Write(eq_label), run_time=0.6)
        self.play(Write(equation), run_time=1.5)
        self.wait(0.8)
        self.play(LaggedStart(*[FadeIn(exp, shift=UP) for exp in explanations], lag_ratio=0.4), run_time=2)
        self.wait(2.5)
        
        self.play(FadeOut(VGroup(section_num, section_title, eq_label, equation, explanations, line)), run_time=1)


# ========== DID YOU KNOW CARD ==========
class DidYouKnowSound(Scene):
    """Fun fact before sound section"""
    
    def construct(self):
        label = Text("DID YOU KNOW?", font_size=32, color=SOUND_COLOR, weight=BOLD)
        label.to_edge(UP, buff=1.5)
        
        fact = Text("Sound travels faster in water\nthan in air!", font_size=40, color=WHITE, line_spacing=1.3)
        
        detail = Text("Water: ~1,480 m/s  |  Air: ~340 m/s", font_size=24, color=INFO_COLOR)
        detail.next_to(fact, DOWN, buff=0.8)
        
        explanation = Text("Denser medium = faster sound", font_size=22, color=GREY_A, slant=ITALIC)
        explanation.next_to(detail, DOWN, buff=0.5)
        
        self.play(Write(label), run_time=0.8)
        self.wait(0.3)
        self.play(FadeIn(fact, scale=1.1), run_time=1.2)
        self.wait(0.8)
        self.play(Write(detail), run_time=1)
        self.play(FadeIn(explanation, shift=UP), run_time=0.8)
        self.wait(2.5)
        self.play(FadeOut(VGroup(label, fact, detail, explanation)), run_time=0.8)


# ========== SECTION 3: SOUND WAVES ==========
class SoundSectionCard(Scene):
    """Comprehensive sound waves section"""
    
    def construct(self):
        section_num = Text("SECTION 3", font_size=28, color=GREY_B, weight=BOLD)
        section_num.to_edge(UP, buff=0.8)
        
        section_title = Text("Sound Waves", font_size=56, color=SOUND_COLOR, weight=BOLD)
        section_title.next_to(section_num, DOWN, buff=0.5)
        
        speed_label = Text("Speed in Air (20°C):", font_size=24, color=INFO_COLOR)
        speed_label.next_to(section_title, DOWN, buff=0.7)
        
        speed = Text("340 m/s", font_size=56, color=WHITE, weight=BOLD)
        speed.next_to(speed_label, DOWN, buff=0.3)
        
        char_title = Text("Key Characteristics:", font_size=22, color=ACCENT_COLOR, weight=BOLD)
        char_title.next_to(speed, DOWN, buff=0.8)
        
        characteristics = VGroup(
            Text("Type: Longitudinal mechanical wave", font_size=20, color=GREY_A),
            Text("Medium: Requires matter (solid/liquid/gas)", font_size=20, color=GREY_A),
            Text("Speed varies with: Temperature & density", font_size=20, color=GREY_A)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        characteristics.next_to(char_title, DOWN, buff=0.3, aligned_edge=LEFT)
        
        subtopic = Text("3.1  Echo & Speed Calculation", font_size=22, color=SOUND_COLOR, slant=ITALIC)
        subtopic.to_edge(DOWN, buff=1)
        
        line = Line(LEFT*5, RIGHT*5, color=SOUND_COLOR, stroke_width=3)
        line.next_to(section_num, DOWN, buff=0.2)
        
        self.play(Write(section_num), Create(line), run_time=0.8)
        self.play(FadeIn(section_title, scale=0.9), run_time=1)
        self.wait(0.5)
        self.play(Write(speed_label), run_time=0.6)
        self.play(FadeIn(speed, scale=1.2), run_time=1)
        self.wait(0.8)
        self.play(Write(char_title), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(char, shift=RIGHT*0.3) for char in characteristics], lag_ratio=0.3), run_time=1.5)
        self.wait(0.8)
        self.play(FadeIn(subtopic, shift=UP), run_time=0.8)
        self.wait(2)
        
        self.play(FadeOut(VGroup(section_num, section_title, speed_label, speed, char_title, characteristics, subtopic, line)), run_time=1)


# ========== TRANSITION: SOUND TO LIGHT ==========
class TransitionToLight(Scene):
    """Compare and transition from sound to light"""
    
    def construct(self):
        sound_side = VGroup(
            Text("Sound Waves", font_size=32, color=SOUND_COLOR, weight=BOLD),
            Text("• Mechanical", font_size=20, color=GREY_A),
            Text("• Needs medium", font_size=20, color=GREY_A),
            Text("• 340 m/s", font_size=20, color=GREY_A)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        sound_side.shift(LEFT*3)
        
        vs_text = Text("VS", font_size=40, color=WHITE, weight=BOLD)
        
        light_side = VGroup(
            Text("Light Waves", font_size=32, color=LIGHT_COLOR, weight=BOLD),
            Text("• Electromagnetic", font_size=20, color=GREY_A),
            Text("• No medium needed!", font_size=20, color=GREY_A),
            MathTex("3 \\times 10^8 \\text{ m/s}", font_size=20, color=GREY_A)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        light_side.shift(RIGHT*3)
        
        self.play(FadeIn(sound_side, shift=RIGHT), run_time=1)
        self.wait(0.5)
        self.play(Write(vs_text), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(light_side, shift=LEFT), run_time=1)
        self.wait(2.5)
        self.play(FadeOut(VGroup(sound_side, vs_text, light_side)), run_time=0.8)


# ========== SECTION 4: LIGHT & ENERGY ==========
class LightEnergySectionCard(Scene):
    """Detailed light and energy section with subtopics"""
    
    def construct(self):
        section_num = Text("SECTION 4", font_size=28, color=GREY_B, weight=BOLD)
        section_num.to_edge(UP, buff=0.8)
        
        section_title = Text("Light & Electromagnetic Energy", font_size=48, color=LIGHT_COLOR, weight=BOLD)
        section_title.next_to(section_num, DOWN, buff=0.5)
        
        # Subtopic 4.1
        subtopic1_num = Text("4.1", font_size=22, color=ACCENT_COLOR, weight=BOLD)
        subtopic1_num.next_to(section_title, DOWN, buff=0.8).shift(LEFT*5)
        
        subtopic1_title = Text("Electromagnetic Waves", font_size=28, color=WHITE, weight=BOLD)
        subtopic1_title.next_to(subtopic1_num, RIGHT, buff=0.3)
        
        em_details = VGroup(
            Text("• No medium required (travel through vacuum)", font_size=18, color=GREY_A),
            Text("• Electric & magnetic fields oscillate perpendicular", font_size=18, color=GREY_A),
            MathTex("c = 3 \\times 10^8 \\text{ m/s (speed of light)}", font_size=22, color=INFO_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        em_details.next_to(subtopic1_title, DOWN, buff=0.3, aligned_edge=LEFT).shift(RIGHT*0.5)
        
        # Subtopic 4.2
        subtopic2_num = Text("4.2", font_size=22, color=ACCENT_COLOR, weight=BOLD)
        subtopic2_num.next_to(em_details, DOWN, buff=0.6).align_to(subtopic1_num, LEFT)
        
        subtopic2_title = Text("Quantum Energy of Light", font_size=28, color=WHITE, weight=BOLD)
        subtopic2_title.next_to(subtopic2_num, RIGHT, buff=0.3)
        
        energy_details = VGroup(
            Text("• Light exists as quantized packets (photons)", font_size=18, color=GREY_A),
            MathTex("E = hf", font_size=32, color=ACCENT_COLOR),
            Text("where h = Planck's constant", font_size=16, color=GREY_B, slant=ITALIC)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        energy_details.next_to(subtopic2_title, DOWN, buff=0.3, aligned_edge=LEFT).shift(RIGHT*0.5)
        
        line = Line(LEFT*5, RIGHT*5, color=LIGHT_COLOR, stroke_width=3)
        line.next_to(section_num, DOWN, buff=0.2)
        
        self.play(Write(section_num), Create(line), run_time=0.8)
        self.play(FadeIn(section_title, scale=0.9), run_time=1)
        self.wait(0.5)
        
        # Subtopic 4.1
        self.play(Write(subtopic1_num), FadeIn(subtopic1_title, shift=RIGHT*0.3), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(detail, shift=RIGHT*0.2) for detail in em_details], lag_ratio=0.3), run_time=1.5)
        self.wait(1)
        
        # Subtopic 4.2
        self.play(Write(subtopic2_num), FadeIn(subtopic2_title, shift=RIGHT*0.3), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(detail, shift=RIGHT*0.2) for detail in energy_details], lag_ratio=0.3), run_time=1.5)
        self.wait(2.5)
        
        all_objects = VGroup(
            section_num, section_title, line,
            subtopic1_num, subtopic1_title, em_details,
            subtopic2_num, subtopic2_title, energy_details
        )
        self.play(FadeOut(all_objects), run_time=1)


# ========== END CARD ==========
class WavesEndCard(Scene):
    """Closing card with summary"""
    
    def construct(self):
        title = Text("Lesson Complete!", font_size=56, color=WHITE, weight=BOLD)
        
        summary = Text(
            "You've learned about wave motion,\nsound, light, and energy",
            font_size=28,
            color=INFO_COLOR,
            line_spacing=1.2
        )
        summary.next_to(title, DOWN, buff=1)
        
        takeaways = VGroup(
            Text("✓ Transverse & Longitudinal Waves", font_size=24, color=WAVE_COLOR),
            Text("✓ Wave Equation: v = fλ", font_size=24, color=INFO_COLOR),
            Text("✓ Sound Speed: 340 m/s", font_size=24, color=SOUND_COLOR),
            Text("✓ Light Speed: 3×10⁸ m/s", font_size=24, color=LIGHT_COLOR),
            Text("✓ Photon Energy: E = hf", font_size=24, color=ACCENT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        takeaways.to_edge(DOWN, buff=1.5)
        
        wave = ParametricFunction(
            lambda t: np.array([t, 0.2*np.sin(4*t), 0]),
            t_range=[-6, 6],
            color=WAVE_COLOR,
            stroke_width=3
        )
        wave.next_to(summary, DOWN, buff=0.8)
        
        self.play(FadeIn(title, scale=0.8), run_time=1.5)
        self.play(Write(summary), run_time=1.5)
        self.play(Create(wave), run_time=2)
        self.play(LaggedStart(*[FadeIn(item, shift=RIGHT*0.5) for item in takeaways], lag_ratio=0.2), run_time=2.5)
        self.wait(3)
        
        self.play(FadeOut(VGroup(title, summary, wave, takeaways)), run_time=2)
