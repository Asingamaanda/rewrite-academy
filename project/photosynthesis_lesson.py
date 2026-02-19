from manim import *

class PhotosynthesisLesson(Scene):
    """Base class for photosynthesis animations with consistent styling"""
    
    # Color scheme
    COLOR_BG = "#1a1a2e"
    COLOR_PRIMARY = "#3498db"    # Blue
    COLOR_ACCENT = "#e74c3c"     # Red
    COLOR_SUCCESS = "#2ecc71"    # Green
    COLOR_WARNING = "#f39c12"    # Orange
    COLOR_INFO = "#9b59b6"       # Purple
    COLOR_LIGHT = "#ecf0f1"      # Light gray
    COLOR_PLANT = "#27ae60"      # Plant green
    COLOR_SUN = "#f1c40f"        # Sun yellow
    COLOR_WATER = "#3498db"      # Water blue
    COLOR_CO2 = "#95a5a6"        # CO2 gray
    COLOR_O2 = "#e8f8f5"         # O2 light blue
    
    FONT_TITLE = 44
    FONT_SUBTITLE = 32
    FONT_STEP = 28
    FONT_BODY = 24
    
    def construct(self):
        self.camera.background_color = self.COLOR_BG
    
    def show_equation(self, tex_string, position=ORIGIN, color=WHITE, font_size=36):
        """Helper to display mathematical equations"""
        eq = MathTex(tex_string, font_size=font_size, color=color)
        eq.move_to(position)
        return eq
    
    def show_text(self, text_string, position=ORIGIN, color=WHITE, font_size=28):
        """Helper to display text"""
        txt = Text(text_string, font_size=font_size, color=color)
        txt.move_to(position)
        return txt
    
    def highlight_box(self, mobject, color=YELLOW, buff=0.3):
        """Create a highlighted box around a mobject"""
        box = SurroundingRectangle(mobject, color=color, buff=buff, corner_radius=0.1)
        self.play(Create(box), run_time=1)
        return box
    
    def pause_for_voiceover(self, duration=1):
        """Placeholder for voiceover timing"""
        self.wait(duration)


class IntroToPhotosynthesis(PhotosynthesisLesson):
    """Introduction to photosynthesis - what it is and why it matters"""
    
    def construct(self):
        super().construct()
        
        # Title
        title = Text("Photosynthesis", font_size=self.FONT_TITLE, color=self.COLOR_PLANT)
        title.to_edge(UP, buff=0.8)
        self.play(Write(title), run_time=2)
        self.pause_for_voiceover(2)
        
        # Subtitle
        subtitle = Text("How Plants Make Food", font_size=self.FONT_SUBTITLE, color=self.COLOR_LIGHT)
        subtitle.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(subtitle), run_time=1.5)
        self.pause_for_voiceover(2)
        
        self.wait(1)
        self.play(FadeOut(subtitle), run_time=0.8)
        
        # Definition
        definition_title = Text("What is Photosynthesis?", font_size=self.FONT_SUBTITLE, color=self.COLOR_WARNING)
        definition_title.shift(UP*2)
        self.play(Write(definition_title), run_time=1.5)
        self.pause_for_voiceover(2)
        
        definition = VGroup(
            Text("Photosynthesis is the process by which", font_size=self.FONT_BODY),
            Text("green plants use sunlight to make", font_size=self.FONT_BODY),
            Text("their own food from carbon dioxide", font_size=self.FONT_BODY),
            Text("and water.", font_size=self.FONT_BODY)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        definition.shift(UP*0.3)
        
        for line in definition:
            self.play(FadeIn(line, shift=RIGHT*0.3), run_time=1)
            self.pause_for_voiceover(1.5)
        
        self.wait(1)
        
        # Clear for word origin
        self.play(FadeOut(definition), run_time=0.8)
        
        # Word breakdown
        word_title = Text("Breaking Down the Word:", font_size=self.FONT_STEP, color=self.COLOR_INFO)
        word_title.shift(UP*1.5)
        self.play(Write(word_title), run_time=1.5)
        self.pause_for_voiceover(2)
        
        photo_part = Text("Photo", font_size=36, color=self.COLOR_SUN)
        photo_part.shift(LEFT*3 + UP*0.3)
        photo_meaning = Text("= Light", font_size=28, color=self.COLOR_LIGHT)
        photo_meaning.next_to(photo_part, DOWN, buff=0.3)
        
        synthesis_part = Text("Synthesis", font_size=36, color=self.COLOR_SUCCESS)
        synthesis_part.shift(RIGHT*2.5 + UP*0.3)
        synthesis_meaning = Text("= To make", font_size=28, color=self.COLOR_LIGHT)
        synthesis_meaning.next_to(synthesis_part, DOWN, buff=0.3)
        
        self.play(
            FadeIn(photo_part, shift=DOWN*0.3),
            FadeIn(synthesis_part, shift=DOWN*0.3),
            run_time=1.5
        )
        self.pause_for_voiceover(2)
        
        self.play(
            Write(photo_meaning),
            Write(synthesis_meaning),
            run_time=1.5
        )
        self.pause_for_voiceover(2)
        
        conclusion = Text("Making things using light!", font_size=32, color=YELLOW)
        conclusion.shift(DOWN*1.5)
        self.play(Write(conclusion), run_time=2)
        self.pause_for_voiceover(3)
        
        self.wait(1)
        
        # Clear everything
        self.play(
            *[FadeOut(mob) for mob in [title, definition_title, word_title, photo_part, 
                                        photo_meaning, synthesis_part, synthesis_meaning, conclusion]],
            run_time=1.5
        )
        
        # Why is it important?
        importance_title = Text("Why Is Photosynthesis Important?", font_size=self.FONT_SUBTITLE, color=self.COLOR_WARNING)
        importance_title.to_edge(UP, buff=1)
        self.play(Write(importance_title), run_time=2)
        self.pause_for_voiceover(2)
        
        reasons = VGroup(
            Text("1. Produces oxygen we breathe", font_size=self.FONT_STEP, color=self.COLOR_O2),
            Text("2. Creates food for plants", font_size=self.FONT_STEP, color=self.COLOR_PLANT),
            Text("3. Foundation of food chains", font_size=self.FONT_STEP, color=self.COLOR_WARNING),
            Text("4. Removes CO₂ from atmosphere", font_size=self.FONT_STEP, color=self.COLOR_CO2)
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        reasons.shift(DOWN*0.5 + LEFT*1)
        
        for reason in reasons:
            self.play(FadeIn(reason, shift=RIGHT*0.3), run_time=1.2)
            self.pause_for_voiceover(2.5)
        
        self.wait(2)
        
        # Final message
        self.play(FadeOut(reasons), run_time=1)
        
        final = Text("Without photosynthesis,\nlife on Earth would not exist!", 
                    font_size=32, color=YELLOW, line_spacing=1.5)
        final.shift(ORIGIN)
        self.play(Write(final), run_time=2.5)
        self.pause_for_voiceover(4)
        
        self.wait(2)


class PhotosynthesisEquation(PhotosynthesisLesson):
    """The chemical equation of photosynthesis"""
    
    def construct(self):
        super().construct()
        
        # Title
        title = Text("The Photosynthesis Equation", font_size=self.FONT_TITLE, color=self.COLOR_PLANT)
        title.to_edge(UP, buff=0.8)
        self.play(Write(title), run_time=2)
        self.pause_for_voiceover(2)
        
        # Show the equation
        equation_title = Text("Chemical Equation:", font_size=self.FONT_SUBTITLE, color=self.COLOR_INFO)
        equation_title.shift(UP*2)
        self.play(FadeIn(equation_title), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # Full equation
        equation = MathTex(
            r"6\text{CO}_2", r"+", r"6\text{H}_2\text{O}", r"+", 
            r"\text{light energy}", r"\rightarrow",
            r"\text{C}_6\text{H}_{12}\text{O}_6", r"+", r"6\text{O}_2",
            font_size=32
        )
        equation.shift(UP*0.8)
        
        # Color code the equation
        equation[0].set_color(self.COLOR_CO2)      # CO2
        equation[2].set_color(self.COLOR_WATER)    # H2O
        equation[4].set_color(self.COLOR_SUN)      # light energy
        equation[6].set_color(self.COLOR_SUCCESS)  # C6H12O6 (glucose)
        equation[8].set_color(self.COLOR_O2)       # O2
        
        self.play(Write(equation), run_time=3)
        self.pause_for_voiceover(3)
        
        self.wait(1)
        
        # Labels below
        co2_label = Text("Carbon Dioxide", font_size=20, color=self.COLOR_CO2)
        co2_label.next_to(equation[0], DOWN, buff=0.8)
        
        water_label = Text("Water", font_size=20, color=self.COLOR_WATER)
        water_label.next_to(equation[2], DOWN, buff=0.8)
        
        light_label = Text("Sunlight", font_size=20, color=self.COLOR_SUN)
        light_label.next_to(equation[4], DOWN, buff=0.8)
        
        glucose_label = Text("Glucose (Sugar)", font_size=20, color=self.COLOR_SUCCESS)
        glucose_label.next_to(equation[6], DOWN, buff=0.8)
        
        oxygen_label = Text("Oxygen", font_size=20, color=self.COLOR_O2)
        oxygen_label.next_to(equation[8], DOWN, buff=0.8)
        
        self.play(
            Write(co2_label),
            Write(water_label),
            Write(light_label),
            run_time=2
        )
        self.pause_for_voiceover(3)
        
        self.play(
            Write(glucose_label),
            Write(oxygen_label),
            run_time=2
        )
        self.pause_for_voiceover(3)
        
        self.wait(1)
        
        # Clear labels
        self.play(
            FadeOut(co2_label), FadeOut(water_label), FadeOut(light_label),
            FadeOut(glucose_label), FadeOut(oxygen_label),
            run_time=0.8
        )
        
        # Word equation
        word_eq_title = Text("In Words:", font_size=self.FONT_STEP, color=self.COLOR_WARNING)
        word_eq_title.shift(DOWN*1)
        self.play(Write(word_eq_title), run_time=1.5)
        self.pause_for_voiceover(2)
        
        word_equation = VGroup(
            Text("Carbon Dioxide + Water + Light Energy", font_size=24),
            MathTex(r"\Downarrow", font_size=32, color=YELLOW),
            Text("Glucose + Oxygen", font_size=24)
        ).arrange(DOWN, buff=0.3)
        word_equation.shift(DOWN*2.3)
        
        for part in word_equation:
            self.play(Write(part), run_time=1.5)
            self.pause_for_voiceover(2)
        
        self.wait(2)
        
        # Clear for summary
        self.play(
            FadeOut(equation_title), FadeOut(word_eq_title), FadeOut(word_equation),
            run_time=1
        )
        
        # What goes in, what comes out
        summary_title = Text("Inputs and Outputs", font_size=self.FONT_SUBTITLE, color=self.COLOR_INFO)
        summary_title.shift(UP*1.5)
        self.play(Transform(equation, summary_title), run_time=1.5)
        self.pause_for_voiceover(2)
        
        inputs = VGroup(
            Text("INPUTS:", font_size=28, color=self.COLOR_WARNING),
            Text("• Carbon Dioxide (CO₂)", font_size=24),
            Text("• Water (H₂O)", font_size=24),
            Text("• Light Energy", font_size=24)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        inputs.shift(LEFT*3 + DOWN*0.3)
        
        outputs = VGroup(
            Text("OUTPUTS:", font_size=28, color=self.COLOR_SUCCESS),
            Text("• Glucose (C₆H₁₂O₆)", font_size=24),
            Text("• Oxygen (O₂)", font_size=24)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        outputs.shift(RIGHT*2.5 + DOWN*0.3)
        
        self.play(FadeIn(inputs, shift=RIGHT*0.3), run_time=2)
        self.pause_for_voiceover(3)
        
        self.play(FadeIn(outputs, shift=LEFT*0.3), run_time=2)
        self.pause_for_voiceover(3)
        
        self.wait(2)


class WhereItHappens(PhotosynthesisLesson):
    """Where photosynthesis occurs - chloroplasts and chlorophyll"""
    
    def construct(self):
        super().construct()
        
        # Title
        title = Text("Where Does Photosynthesis Happen?", font_size=self.FONT_TITLE, color=self.COLOR_PLANT)
        title.to_edge(UP, buff=0.8)
        self.play(Write(title), run_time=2)
        self.pause_for_voiceover(2)
        
        # Location hierarchy
        location1 = Text("In green plants", font_size=self.FONT_SUBTITLE, color=self.COLOR_PLANT)
        location1.shift(UP*1.8)
        self.play(FadeIn(location1), run_time=1.5)
        self.pause_for_voiceover(2)
        
        arrow1 = MathTex(r"\Downarrow", font_size=40, color=YELLOW)
        arrow1.shift(UP*0.8)
        self.play(Write(arrow1), run_time=1)
        
        location2 = Text("In plant cells", font_size=self.FONT_SUBTITLE, color=self.COLOR_INFO)
        location2.shift(UP*0.2)
        self.play(FadeIn(location2), run_time=1.5)
        self.pause_for_voiceover(2)
        
        arrow2 = MathTex(r"\Downarrow", font_size=40, color=YELLOW)
        arrow2.shift(DOWN*0.8)
        self.play(Write(arrow2), run_time=1)
        
        location3 = Text("In CHLOROPLASTS", font_size=self.FONT_SUBTITLE, color=self.COLOR_SUCCESS)
        location3.shift(DOWN*1.4)
        self.play(FadeIn(location3), run_time=1.5)
        box = self.highlight_box(location3, color=self.COLOR_SUCCESS)
        self.pause_for_voiceover(3)
        
        self.wait(1)
        
        # Clear for chloroplast info
        self.play(
            FadeOut(location1), FadeOut(arrow1), FadeOut(location2), 
            FadeOut(arrow2), FadeOut(location3), FadeOut(box),
            run_time=1.5
        )
        
        # Chloroplast information
        chloroplast_title = Text("Chloroplasts", font_size=self.FONT_SUBTITLE, color=self.COLOR_SUCCESS)
        chloroplast_title.shift(UP*2.2)
        self.play(Write(chloroplast_title), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # Simple chloroplast representation
        chloroplast = Ellipse(width=3, height=1.5, color=self.COLOR_PLANT, fill_opacity=0.3)
        chloroplast.shift(UP*0.5)
        
        # Internal membranes (simplified)
        membranes = VGroup(*[
            Line(LEFT*1.3, RIGHT*1.3, color=self.COLOR_SUCCESS).shift(UP*0.5 + UP*i*0.3)
            for i in range(-1, 2)
        ])
        
        self.play(Create(chloroplast), run_time=2)
        self.play(Create(membranes), run_time=2)
        self.pause_for_voiceover(3)
        
        # Facts about chloroplasts
        facts = VGroup(
            Text("• Green organelles in plant cells", font_size=22),
            Text("• Contain chlorophyll (green pigment)", font_size=22),
            Text("• Capture light energy from sun", font_size=22)
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        facts.shift(DOWN*1.8 + LEFT*2)
        
        for fact in facts:
            self.play(FadeIn(fact, shift=RIGHT*0.3), run_time=1.2)
            self.pause_for_voiceover(2.5)
        
        self.wait(2)
        
        # Clear for chlorophyll
        self.play(
            FadeOut(chloroplast), FadeOut(membranes), FadeOut(facts),
            run_time=1
        )
        
        chlorophyll_title = Text("Chlorophyll", font_size=self.FONT_SUBTITLE, color=self.COLOR_PLANT)
        chlorophyll_title.shift(UP*1.5)
        self.play(Transform(chloroplast_title, chlorophyll_title), run_time=1.5)
        self.pause_for_voiceover(2)
        
        chlorophyll_info = VGroup(
            Text("Chlorophyll is the green pigment", font_size=self.FONT_BODY),
            Text("that absorbs light energy.", font_size=self.FONT_BODY),
        ).arrange(DOWN, buff=0.3)
        chlorophyll_info.shift(UP*0.3)
        
        for line in chlorophyll_info:
            self.play(FadeIn(line), run_time=1.5)
            self.pause_for_voiceover(2)
        
        self.wait(1)
        
        # Why green?
        why_green = Text("Why are plants green?", font_size=28, color=self.COLOR_WARNING)
        why_green.shift(DOWN*1)
        self.play(Write(why_green), run_time=1.5)
        self.pause_for_voiceover(2)
        
        answer = VGroup(
            Text("Chlorophyll absorbs red and blue light,", font_size=24),
            Text("but reflects green light back to our eyes!", font_size=24, color=self.COLOR_PLANT)
        ).arrange(DOWN, buff=0.3)
        answer.shift(DOWN*2.2)
        
        for line in answer:
            self.play(FadeIn(line, shift=UP*0.2), run_time=1.5)
            self.pause_for_voiceover(2.5)
        
        self.wait(3)


class TwoStages(PhotosynthesisLesson):
    """The two stages of photosynthesis"""
    
    def construct(self):
        super().construct()
        
        # Title
        title = Text("Two Stages of Photosynthesis", font_size=self.FONT_TITLE, color=self.COLOR_PLANT)
        title.to_edge(UP, buff=0.8)
        self.play(Write(title), run_time=2)
        self.pause_for_voiceover(2)
        
        # Introduction
        intro = Text("Photosynthesis happens in TWO stages:", font_size=self.FONT_SUBTITLE, color=self.COLOR_INFO)
        intro.shift(UP*2)
        self.play(FadeIn(intro), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # Stage 1
        stage1_title = Text("Stage 1: Light-Dependent Reactions", font_size=32, color=self.COLOR_SUN)
        stage1_title.shift(UP*0.8)
        self.play(Write(stage1_title), run_time=2)
        self.pause_for_voiceover(2)
        
        stage1_subtitle = Text("(Happens in the light)", font_size=24, color=self.COLOR_LIGHT)
        stage1_subtitle.next_to(stage1_title, DOWN, buff=0.3)
        self.play(FadeIn(stage1_subtitle), run_time=1)
        self.pause_for_voiceover(2)
        
        stage1_points = VGroup(
            Text("• Requires sunlight", font_size=22),
            Text("• Water is split (H₂O → H + O)", font_size=22),
            Text("• Oxygen is released", font_size=22, color=self.COLOR_O2),
            Text("• Energy is captured and stored", font_size=22, color=YELLOW)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        stage1_points.shift(DOWN*1.2 + LEFT*1.5)
        
        for point in stage1_points:
            self.play(FadeIn(point, shift=RIGHT*0.3), run_time=1)
            self.pause_for_voiceover(2)
        
        self.wait(2)
        
        # Clear for Stage 2
        self.play(
            FadeOut(stage1_title), FadeOut(stage1_subtitle), FadeOut(stage1_points),
            run_time=1.5
        )
        
        # Stage 2
        stage2_title = Text("Stage 2: Light-Independent Reactions", font_size=32, color=self.COLOR_SUCCESS)
        stage2_title.shift(UP*0.8)
        self.play(Write(stage2_title), run_time=2)
        self.pause_for_voiceover(2)
        
        stage2_subtitle = Text("(Calvin Cycle - Can happen in dark)", font_size=24, color=self.COLOR_LIGHT)
        stage2_subtitle.next_to(stage2_title, DOWN, buff=0.3)
        self.play(FadeIn(stage2_subtitle), run_time=1)
        self.pause_for_voiceover(2)
        
        stage2_points = VGroup(
            Text("• Does NOT require sunlight", font_size=22),
            Text("• Uses CO₂ from air", font_size=22, color=self.COLOR_CO2),
            Text("• Uses energy from Stage 1", font_size=22, color=YELLOW),
            Text("• Produces glucose (sugar)", font_size=22, color=self.COLOR_SUCCESS)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        stage2_points.shift(DOWN*1.2 + LEFT*1.5)
        
        for point in stage2_points:
            self.play(FadeIn(point, shift=RIGHT*0.3), run_time=1)
            self.pause_for_voiceover(2)
        
        self.wait(2)
        
        # Clear for summary
        self.play(
            FadeOut(intro), FadeOut(stage2_title), FadeOut(stage2_subtitle), FadeOut(stage2_points),
            run_time=1.5
        )
        
        # Summary diagram
        summary_title = Text("The Complete Process", font_size=self.FONT_SUBTITLE, color=self.COLOR_WARNING)
        summary_title.shift(UP*2.2)
        self.play(Write(summary_title), run_time=1.5)
        self.pause_for_voiceover(2)
        
        # Stage 1 box
        stage1_box = VGroup(
            Text("STAGE 1", font_size=24, color=self.COLOR_SUN),
            Text("Light Reactions", font_size=20),
            Line(LEFT*1.5, RIGHT*1.5, color=self.COLOR_SUN),
            Text("H₂O → O₂", font_size=20, color=self.COLOR_O2),
            Text("Captures Energy", font_size=18, color=YELLOW)
        ).arrange(DOWN, buff=0.25)
        stage1_box.shift(LEFT*3.5 + UP*0.3)
        
        # Arrow
        arrow = Arrow(LEFT*1.5, RIGHT*1.5, color=YELLOW, buff=0.3)
        arrow.shift(UP*0.3)
        
        # Stage 2 box
        stage2_box = VGroup(
            Text("STAGE 2", font_size=24, color=self.COLOR_SUCCESS),
            Text("Calvin Cycle", font_size=20),
            Line(LEFT*1.5, RIGHT*1.5, color=self.COLOR_SUCCESS),
            Text("CO₂ → Glucose", font_size=20, color=self.COLOR_SUCCESS),
            Text("Makes Food", font_size=18, color=self.COLOR_PLANT)
        ).arrange(DOWN, buff=0.25)
        stage2_box.shift(RIGHT*3.5 + UP*0.3)
        
        self.play(FadeIn(stage1_box, shift=RIGHT*0.5), run_time=2)
        self.pause_for_voiceover(2)
        
        self.play(Create(arrow), run_time=1.5)
        self.pause_for_voiceover(1)
        
        self.play(FadeIn(stage2_box, shift=LEFT*0.5), run_time=2)
        self.pause_for_voiceover(2)
        
        # Key point
        key_point = Text("Energy from Stage 1 powers Stage 2!", 
                        font_size=26, color=YELLOW)
        key_point.shift(DOWN*2)
        self.play(Write(key_point), run_time=2)
        box = self.highlight_box(key_point, color=YELLOW)
        self.pause_for_voiceover(4)
        
        self.wait(3)


class PhotosynthesisSummary(PhotosynthesisLesson):
    """Summary of photosynthesis"""
    
    def construct(self):
        super().construct()
        
        # Title
        title = Text("Photosynthesis Summary", font_size=self.FONT_TITLE, color=self.COLOR_PLANT)
        title.to_edge(UP, buff=0.8)
        self.play(Write(title), run_time=2)
        self.pause_for_voiceover(2)
        
        # Key points
        summary_title = Text("Key Points to Remember:", font_size=self.FONT_SUBTITLE, color=self.COLOR_WARNING)
        summary_title.shift(UP*2.2)
        self.play(Write(summary_title), run_time=1.5)
        self.pause_for_voiceover(2)
        
        points = VGroup(
            Text("1. Plants use sunlight to make food", font_size=26),
            Text("2. Takes place in chloroplasts", font_size=26),
            Text("3. Chlorophyll captures light energy", font_size=26),
            Text("4. Inputs: CO₂, H₂O, and light", font_size=26),
            Text("5. Outputs: Glucose and O₂", font_size=26),
            Text("6. Two stages: Light and Dark reactions", font_size=26),
            Text("7. Oxygen we breathe comes from this!", font_size=26, color=self.COLOR_O2)
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        points.shift(DOWN*0.5 + LEFT*1.5)
        
        for i, point in enumerate(points):
            self.play(FadeIn(point, shift=RIGHT*0.3), run_time=1)
            self.pause_for_voiceover(2.5)
        
        self.wait(2)
        
        # Clear for equation reminder
        self.play(FadeOut(points), run_time=1)
        
        equation_reminder = Text("The Equation:", font_size=28, color=self.COLOR_INFO)
        equation_reminder.shift(UP*0.8)
        self.play(Write(equation_reminder), run_time=1.5)
        self.pause_for_voiceover(2)
        
        final_equation = MathTex(
            r"6\text{CO}_2 + 6\text{H}_2\text{O} + \text{light} \rightarrow \text{C}_6\text{H}_{12}\text{O}_6 + 6\text{O}_2",
            font_size=28
        )
        final_equation.shift(DOWN*0.2)
        self.play(Write(final_equation), run_time=3)
        box = self.highlight_box(final_equation, color=self.COLOR_PLANT)
        self.pause_for_voiceover(4)
        
        self.wait(1)
        
        # Final message
        final_message = Text("Photosynthesis = Life on Earth!", 
                           font_size=36, color=YELLOW)
        final_message.shift(DOWN*2)
        self.play(Write(final_message), run_time=2)
        self.pause_for_voiceover(4)
        
        self.wait(3)
