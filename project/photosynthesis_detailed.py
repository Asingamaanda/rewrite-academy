from manim import *

class PhotosynthesisDetailed(Scene):
    """Base class for detailed photosynthesis animations"""
    
    # Color scheme
    COLOR_BG = "#1a1a2e"
    COLOR_PRIMARY = "#3498db"
    COLOR_ACCENT = "#e74c3c"
    COLOR_SUCCESS = "#2ecc71"
    COLOR_WARNING = "#f39c12"
    COLOR_INFO = "#9b59b6"
    COLOR_LIGHT = "#ecf0f1"
    COLOR_PLANT = "#27ae60"
    COLOR_SUN = "#f1c40f"
    COLOR_WATER = "#3498db"
    COLOR_CO2 = "#95a5a6"
    COLOR_O2 = "#e8f8f5"
    COLOR_GLUCOSE = "#e67e22"
    COLOR_ATP = "#e74c3c"
    COLOR_NADPH = "#9b59b6"
    
    FONT_TITLE = 44
    FONT_SUBTITLE = 32
    FONT_STEP = 28
    FONT_BODY = 24
    
    def construct(self):
        self.camera.background_color = self.COLOR_BG
    
    def create_table(self, headers, rows, title=None):
        """Create a formatted table"""
        # Table title
        if title:
            table_title = Text(title, font_size=28, color=self.COLOR_WARNING)
            table_title.to_edge(UP, buff=0.5)
        
        # Create header
        header_cells = VGroup(*[
            Text(h, font_size=22, color=self.COLOR_INFO, weight=BOLD)
            for h in headers
        ]).arrange(RIGHT, buff=1.5)
        
        # Create rows
        row_groups = []
        for row in rows:
            row_cells = VGroup(*[
                Text(str(cell), font_size=20, color=WHITE)
                for cell in row
            ]).arrange(RIGHT, buff=1.5)
            
            # Align with headers
            for i, cell in enumerate(row_cells):
                cell.align_to(header_cells[i], LEFT)
            
            row_groups.append(row_cells)
        
        # Arrange all rows
        all_rows = VGroup(header_cells, *row_groups).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        
        # Add horizontal lines
        lines = VGroup()
        line_under_header = Line(
            header_cells.get_left() + LEFT*0.3,
            header_cells.get_right() + RIGHT*0.3,
            color=self.COLOR_INFO
        ).next_to(header_cells, DOWN, buff=0.2)
        lines.add(line_under_header)
        
        table = VGroup(all_rows, lines)
        
        if title:
            table.add(table_title)
            table.arrange(DOWN, buff=0.5)
        
        return table


class ChloroplastStructure(PhotosynthesisDetailed):
    """Detailed chloroplast structure with labels"""
    
    def construct(self):
        super().construct()
        
        title = Text("Chloroplast Structure", font_size=self.FONT_TITLE, color=self.COLOR_PLANT)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2)
        self.wait(1)
        
        # Draw chloroplast structure
        # Outer membrane
        outer_membrane = Ellipse(width=6, height=3, color=self.COLOR_PLANT, stroke_width=3)
        outer_membrane.shift(LEFT*0.5)
        
        # Inner membrane
        inner_membrane = Ellipse(width=5.6, height=2.7, color=self.COLOR_SUCCESS, stroke_width=2)
        inner_membrane.shift(LEFT*0.5)
        
        # Thylakoids (disc-like structures)
        thylakoid_stacks = VGroup()
        for x_pos in [-2, 0, 1.5]:
            stack = VGroup(*[
                Ellipse(width=0.8, height=0.15, color=self.COLOR_SUN, fill_opacity=0.6, stroke_width=1.5)
                .shift(LEFT*0.5 + RIGHT*x_pos + UP*0.08*i)
                for i in range(5)
            ])
            thylakoid_stacks.add(stack)
        
        # Stroma (fluid)
        stroma_label_pos = RIGHT*2 + DOWN*0.5
        
        self.play(Create(outer_membrane), run_time=2)
        self.wait(0.5)
        
        self.play(Create(inner_membrane), run_time=1.5)
        self.wait(0.5)
        
        self.play(Create(thylakoid_stacks), run_time=2)
        self.wait(1)
        
        # Labels with arrows
        outer_label = Text("Outer Membrane", font_size=20, color=self.COLOR_PLANT)
        outer_label.to_edge(LEFT, buff=0.5).shift(UP*1.5)
        outer_arrow = Arrow(outer_label.get_right(), outer_membrane.get_left() + UP*1, 
                           color=self.COLOR_PLANT, buff=0.1, stroke_width=2)
        
        inner_label = Text("Inner Membrane", font_size=20, color=self.COLOR_SUCCESS)
        inner_label.to_edge(LEFT, buff=0.5).shift(UP*0.5)
        inner_arrow = Arrow(inner_label.get_right(), inner_membrane.get_left() + UP*0.5,
                           color=self.COLOR_SUCCESS, buff=0.1, stroke_width=2)
        
        thylakoid_label = Text("Thylakoid\n(Stacked = Granum)", font_size=20, color=self.COLOR_SUN, line_spacing=0.8)
        thylakoid_label.to_edge(RIGHT, buff=0.5).shift(UP*1)
        thylakoid_arrow = Arrow(thylakoid_label.get_left(), thylakoid_stacks[1].get_right(),
                               color=self.COLOR_SUN, buff=0.1, stroke_width=2)
        
        stroma_label = Text("Stroma\n(Fluid)", font_size=20, color=self.COLOR_INFO, line_spacing=0.8)
        stroma_label.to_edge(RIGHT, buff=0.5).shift(DOWN*0.5)
        stroma_arrow = Arrow(stroma_label.get_left(), stroma_label_pos,
                            color=self.COLOR_INFO, buff=0.1, stroke_width=2)
        
        self.play(
            Write(outer_label), Create(outer_arrow),
            run_time=1.5
        )
        self.wait(1)
        
        self.play(
            Write(inner_label), Create(inner_arrow),
            run_time=1.5
        )
        self.wait(1)
        
        self.play(
            Write(thylakoid_label), Create(thylakoid_arrow),
            run_time=1.5
        )
        self.wait(1)
        
        self.play(
            Write(stroma_label), Create(stroma_arrow),
            run_time=1.5
        )
        self.wait(2)
        
        # Add location labels for stages
        stage1_box = Text("STAGE 1\n(Light Reactions)\nOccur HERE", 
                         font_size=18, color=YELLOW, line_spacing=0.7)
        stage1_box.next_to(thylakoid_stacks[2], DOWN, buff=0.3).shift(RIGHT*0.5)
        stage1_arrow = Arrow(stage1_box.get_top(), thylakoid_stacks[2].get_bottom(),
                            color=YELLOW, buff=0.05, stroke_width=3)
        
        stage2_box = Text("STAGE 2\n(Calvin Cycle)\nOccurs HERE",
                         font_size=18, color=self.COLOR_SUCCESS, line_spacing=0.7)
        stage2_box.shift(LEFT*2.5 + DOWN*1)
        stage2_arrow = Arrow(stage2_box.get_top(), stroma_label_pos,
                            color=self.COLOR_SUCCESS, buff=0.05, stroke_width=3)
        
        self.play(Write(stage1_box), Create(stage1_arrow), run_time=2)
        self.wait(2)
        
        self.play(Write(stage2_box), Create(stage2_arrow), run_time=2)
        self.wait(3)


class LightReactionsDetailed(PhotosynthesisDetailed):
    """Detailed breakdown of light-dependent reactions"""
    
    def construct(self):
        super().construct()
        
        title = Text("Light Reactions - Detailed", font_size=self.FONT_TITLE, color=self.COLOR_SUN)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2)
        self.wait(1)
        
        # Location reminder
        location = Text("Location: Thylakoid Membranes", font_size=24, color=self.COLOR_INFO)
        location.shift(UP*2.5)
        self.play(FadeIn(location), run_time=1.5)
        self.wait(1)
        
        # Step-by-step equations
        subtitle = Text("Step-by-Step Process:", font_size=28, color=self.COLOR_WARNING)
        subtitle.shift(UP*1.8)
        self.play(Write(subtitle), run_time=1.5)
        self.wait(1)
        
        # Step 1
        step1_label = Text("Step 1: Light Absorption", font_size=24, color=self.COLOR_SUN)
        step1_label.to_edge(LEFT, buff=0.5).shift(UP*1)
        self.play(FadeIn(step1_label, shift=RIGHT*0.3), run_time=1.5)
        self.wait(1)
        
        step1_eq = MathTex(r"\text{Chlorophyll} + \text{Light Energy} \rightarrow \text{Excited Electrons}",
                          font_size=24)
        step1_eq.next_to(step1_label, DOWN, buff=0.3).shift(RIGHT*0.5)
        self.play(Write(step1_eq), run_time=2)
        self.wait(2)
        
        # Step 2
        step2_label = Text("Step 2: Water Splitting (Photolysis)", font_size=24, color=self.COLOR_WATER)
        step2_label.to_edge(LEFT, buff=0.5).shift(UP*0.1)
        self.play(FadeIn(step2_label, shift=RIGHT*0.3), run_time=1.5)
        self.wait(1)
        
        step2_eq = MathTex(r"2\text{H}_2\text{O} \rightarrow 4\text{H}^+ + 4\text{e}^- + \text{O}_2",
                          font_size=24)
        step2_eq.next_to(step2_label, DOWN, buff=0.3).shift(RIGHT*0.5)
        
        # Color parts
        step2_eq[0][0:4].set_color(self.COLOR_WATER)  # H2O
        step2_eq[0][-2:].set_color(self.COLOR_O2)      # O2
        
        self.play(Write(step2_eq), run_time=2)
        self.wait(2)
        
        oxygen_note = Text("(This is the oxygen we breathe!)", font_size=18, color=self.COLOR_O2)
        oxygen_note.next_to(step2_eq, DOWN, buff=0.2).shift(RIGHT*2)
        self.play(FadeIn(oxygen_note), run_time=1)
        self.wait(2)
        
        # Step 3
        self.play(FadeOut(step1_label), FadeOut(step1_eq), run_time=0.8)
        
        step3_label = Text("Step 3: ATP Production", font_size=24, color=self.COLOR_ATP)
        step3_label.to_edge(LEFT, buff=0.5).shift(DOWN*1)
        self.play(FadeIn(step3_label, shift=RIGHT*0.3), run_time=1.5)
        self.wait(1)
        
        step3_eq = MathTex(r"\text{ADP} + \text{P}_i + \text{Energy} \rightarrow \text{ATP}",
                          font_size=24, color=self.COLOR_ATP)
        step3_eq.next_to(step3_label, DOWN, buff=0.3).shift(RIGHT*0.5)
        self.play(Write(step3_eq), run_time=2)
        self.wait(1)
        
        atp_note = Text("(ATP = Energy currency of cells)", font_size=18, color=YELLOW)
        atp_note.next_to(step3_eq, DOWN, buff=0.2).shift(RIGHT*1.5)
        self.play(FadeIn(atp_note), run_time=1)
        self.wait(2)
        
        # Step 4
        self.play(
            FadeOut(step2_label), FadeOut(step2_eq), FadeOut(oxygen_note),
            run_time=0.8
        )
        
        step4_label = Text("Step 4: NADPH Production", font_size=24, color=self.COLOR_NADPH)
        step4_label.to_edge(LEFT, buff=0.5).shift(DOWN*2)
        self.play(FadeIn(step4_label, shift=RIGHT*0.3), run_time=1.5)
        self.wait(1)
        
        step4_eq = MathTex(r"\text{NADP}^+ + 2\text{e}^- + \text{H}^+ \rightarrow \text{NADPH}",
                          font_size=24, color=self.COLOR_NADPH)
        step4_eq.next_to(step4_label, DOWN, buff=0.3).shift(RIGHT*0.5)
        self.play(Write(step4_eq), run_time=2)
        self.wait(1)
        
        nadph_note = Text("(NADPH = Electron carrier)", font_size=18, color=self.COLOR_INFO)
        nadph_note.next_to(step4_eq, DOWN, buff=0.2).shift(RIGHT*1.5)
        self.play(FadeIn(nadph_note), run_time=1)
        self.wait(2)
        
        # Clear all
        self.play(
            *[FadeOut(mob) for mob in [location, subtitle, step3_label, step3_eq, atp_note,
                                        step4_label, step4_eq, nadph_note]],
            run_time=1.5
        )
        
        # Summary equation
        summary_title = Text("Overall Light Reactions:", font_size=28, color=self.COLOR_WARNING)
        summary_title.shift(UP*1.5)
        self.play(Write(summary_title), run_time=1.5)
        self.wait(1)
        
        overall_eq = MathTex(
            r"2\text{H}_2\text{O} + 2\text{NADP}^+ + 3\text{ADP} + 3\text{P}_i + \text{light}",
            r"\rightarrow",
            r"\text{O}_2 + 2\text{NADPH} + 3\text{ATP}",
            font_size=26
        ).arrange(DOWN, buff=0.3)
        overall_eq.shift(UP*0.3)
        
        overall_eq[0][0:4].set_color(self.COLOR_WATER)       # H2O
        overall_eq[2][0:2].set_color(self.COLOR_O2)          # O2
        overall_eq[2][3:9].set_color(self.COLOR_NADPH)       # NADPH
        overall_eq[2][10:13].set_color(self.COLOR_ATP)       # ATP
        
        self.play(Write(overall_eq), run_time=3)
        self.wait(2)
        
        # Products box
        products_title = Text("Products (Used in Stage 2):", font_size=24, color=self.COLOR_SUCCESS)
        products_title.shift(DOWN*1.3)
        self.play(Write(products_title), run_time=1.5)
        self.wait(1)
        
        products = VGroup(
            Text("• ATP (energy)", font_size=22, color=self.COLOR_ATP),
            Text("• NADPH (electrons)", font_size=22, color=self.COLOR_NADPH),
            Text("• O₂ (byproduct - released)", font_size=22, color=self.COLOR_O2)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        products.shift(DOWN*2.3 + LEFT*1.5)
        
        for product in products:
            self.play(FadeIn(product, shift=RIGHT*0.3), run_time=1)
            self.wait(1.5)
        
        self.wait(3)


class CalvinCycleDetailed(PhotosynthesisDetailed):
    """Detailed breakdown of Calvin Cycle (Dark Reactions)"""
    
    def construct(self):
        super().construct()
        
        title = Text("Calvin Cycle - Detailed", font_size=self.FONT_TITLE, color=self.COLOR_SUCCESS)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2)
        self.wait(1)
        
        # Location reminder
        location = Text("Location: Stroma (fluid of chloroplast)", font_size=24, color=self.COLOR_INFO)
        location.shift(UP*2.5)
        self.play(FadeIn(location), run_time=1.5)
        self.wait(1)
        
        # Important note
        note = Text("Does NOT directly need light\n(But needs ATP & NADPH from Light Reactions)",
                   font_size=22, color=YELLOW, line_spacing=0.9)
        note.shift(UP*1.7)
        self.play(FadeIn(note), run_time=2)
        self.wait(2)
        
        self.play(FadeOut(note), run_time=0.8)
        
        # Three phases
        phases_title = Text("Three Phases:", font_size=28, color=self.COLOR_WARNING)
        phases_title.shift(UP*1.8)
        self.play(Write(phases_title), run_time=1.5)
        self.wait(1)
        
        # Phase 1: Carbon Fixation
        phase1_title = Text("Phase 1: Carbon Fixation", font_size=26, color=self.COLOR_CO2)
        phase1_title.to_edge(LEFT, buff=0.5).shift(UP*1)
        self.play(FadeIn(phase1_title, shift=RIGHT*0.3), run_time=1.5)
        self.wait(1)
        
        phase1_desc = VGroup(
            Text("• CO₂ from air enters cycle", font_size=20),
            Text("• Combines with RuBP (5-carbon)", font_size=20),
            Text("• Forms 2 molecules of 3-PGA (3-carbon each)", font_size=20)
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        phase1_desc.next_to(phase1_title, DOWN, buff=0.3).shift(RIGHT*0.3)
        
        for line in phase1_desc:
            self.play(FadeIn(line, shift=RIGHT*0.2), run_time=1)
            self.wait(1.5)
        
        phase1_eq = MathTex(
            r"3\text{CO}_2 + 3\text{RuBP} \rightarrow 6 \text{ 3-PGA}",
            font_size=22
        )
        phase1_eq.next_to(phase1_desc, DOWN, buff=0.4).shift(RIGHT*1)
        phase1_eq[0][0:4].set_color(self.COLOR_CO2)
        self.play(Write(phase1_eq), run_time=2)
        self.wait(2)
        
        # Phase 2: Reduction
        self.play(FadeOut(phase1_desc), FadeOut(phase1_eq), run_time=0.8)
        
        phase2_title = Text("Phase 2: Reduction", font_size=26, color=self.COLOR_NADPH)
        phase2_title.to_edge(LEFT, buff=0.5).shift(DOWN*0.3)
        self.play(FadeIn(phase2_title, shift=RIGHT*0.3), run_time=1.5)
        self.wait(1)
        
        phase2_desc = VGroup(
            Text("• ATP provides energy", font_size=20, color=self.COLOR_ATP),
            Text("• NADPH provides electrons", font_size=20, color=self.COLOR_NADPH),
            Text("• 3-PGA reduced to G3P (sugar)", font_size=20)
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        phase2_desc.next_to(phase2_title, DOWN, buff=0.3).shift(RIGHT*0.3)
        
        for line in phase2_desc:
            self.play(FadeIn(line, shift=RIGHT*0.2), run_time=1)
            self.wait(1.5)
        
        phase2_eq = MathTex(
            r"6\text{ 3-PGA} + 6\text{ATP} + 6\text{NADPH} \rightarrow 6\text{ G3P}",
            font_size=20
        )
        phase2_eq.next_to(phase2_desc, DOWN, buff=0.4).shift(RIGHT*0.5)
        self.play(Write(phase2_eq), run_time=2)
        self.wait(2)
        
        # Phase 3: Regeneration
        self.play(FadeOut(phase1_title), FadeOut(phase2_desc), FadeOut(phase2_eq), run_time=0.8)
        
        phase3_title = Text("Phase 3: Regeneration", font_size=26, color=self.COLOR_SUCCESS)
        phase3_title.to_edge(LEFT, buff=0.5).shift(DOWN*1.7)
        self.play(FadeIn(phase3_title, shift=RIGHT*0.3), run_time=1.5)
        self.wait(1)
        
        phase3_desc = VGroup(
            Text("• 5 out of 6 G3P molecules recycled", font_size=20),
            Text("• ATP used to regenerate RuBP", font_size=20, color=self.COLOR_ATP),
            Text("• 1 G3P exits to make glucose!", font_size=20, color=self.COLOR_GLUCOSE)
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        phase3_desc.next_to(phase3_title, DOWN, buff=0.3).shift(RIGHT*0.3)
        
        for line in phase3_desc:
            self.play(FadeIn(line, shift=RIGHT*0.2), run_time=1)
            self.wait(1.5)
        
        phase3_eq = MathTex(
            r"5\text{ G3P} + 3\text{ATP} \rightarrow 3\text{RuBP}",
            font_size=22
        )
        phase3_eq.next_to(phase3_desc, DOWN, buff=0.4).shift(RIGHT*1)
        self.play(Write(phase3_eq), run_time=2)
        self.wait(2)
        
        # Clear all
        self.play(
            *[FadeOut(mob) for mob in [location, phases_title, phase2_title, phase3_title,
                                        phase3_desc, phase3_eq]],
            run_time=1.5
        )
        
        # Overall equation
        overall_title = Text("Overall Calvin Cycle (for 1 glucose):", font_size=28, color=self.COLOR_WARNING)
        overall_title.shift(UP*1.8)
        self.play(Write(overall_title), run_time=1.5)
        self.wait(1)
        
        overall_eq = MathTex(
            r"6\text{CO}_2 + 18\text{ATP} + 12\text{NADPH}",
            r"\rightarrow",
            r"\text{C}_6\text{H}_{12}\text{O}_6 + 18\text{ADP} + 12\text{NADP}^+",
            font_size=24
        ).arrange(DOWN, buff=0.4)
        overall_eq.shift(UP*0.5)
        
        overall_eq[0][0:4].set_color(self.COLOR_CO2)
        overall_eq[0][5:10].set_color(self.COLOR_ATP)
        overall_eq[0][11:].set_color(self.COLOR_NADPH)
        overall_eq[2][0:11].set_color(self.COLOR_GLUCOSE)
        
        self.play(Write(overall_eq), run_time=3)
        self.wait(2)
        
        # Key point
        key_point = Text("It takes 6 turns of the cycle to make 1 glucose!",
                        font_size=26, color=YELLOW)
        key_point.shift(DOWN*1.5)
        self.play(Write(key_point), run_time=2)
        
        box = SurroundingRectangle(key_point, color=YELLOW, buff=0.2, corner_radius=0.1)
        self.play(Create(box), run_time=1)
        self.wait(3)


class ComparisonTable(PhotosynthesisDetailed):
    """Comparison table of Light vs Dark Reactions"""
    
    def construct(self):
        super().construct()
        
        title = Text("Light vs Dark Reactions", font_size=self.FONT_TITLE, color=self.COLOR_PLANT)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2)
        self.wait(1)
        
        # Create comparison table
        table_title = Text("Detailed Comparison", font_size=28, color=self.COLOR_WARNING)
        table_title.shift(UP*2.5)
        self.play(Write(table_title), run_time=1.5)
        self.wait(1)
        
        # Table headers
        headers = VGroup(
            Text("Feature", font_size=22, color=self.COLOR_INFO, weight=BOLD),
            Text("Light Reactions", font_size=22, color=self.COLOR_SUN, weight=BOLD),
            Text("Dark Reactions (Calvin)", font_size=22, color=self.COLOR_SUCCESS, weight=BOLD)
        ).arrange(RIGHT, buff=1.2)
        headers.shift(UP*1.7)
        
        self.play(Write(headers), run_time=2)
        self.wait(1)
        
        # Underline
        line = Line(headers.get_left() + LEFT*0.3, headers.get_right() + RIGHT*0.3,
                   color=self.COLOR_INFO)
        line.next_to(headers, DOWN, buff=0.15)
        self.play(Create(line), run_time=1)
        self.wait(0.5)
        
        # Table rows data
        rows_data = [
            ("Location", "Thylakoid membrane", "Stroma"),
            ("Light needed?", "YES - directly", "NO - indirectly"),
            ("Main input", "H₂O + Light", "CO₂"),
            ("Main output", "O₂ + ATP + NADPH", "Glucose"),
            ("Energy form", "Captures light → ATP", "Uses ATP"),
            ("Process type", "Photolysis", "Carbon fixation")
        ]
        
        # Create rows
        all_rows = VGroup()
        y_position = 1.2
        
        for row_data in rows_data:
            row = VGroup(
                Text(row_data[0], font_size=19, color=WHITE),
                Text(row_data[1], font_size=18, color=self.COLOR_SUN),
                Text(row_data[2], font_size=18, color=self.COLOR_SUCCESS)
            ).arrange(RIGHT, buff=1.2)
            
            # Align with headers
            for i, cell in enumerate(row):
                cell.align_to(headers[i], LEFT)
            
            row.shift(UP*y_position)
            all_rows.add(row)
            y_position -= 0.55
        
        # Animate rows one by one
        for row in all_rows:
            self.play(FadeIn(row, shift=DOWN*0.2), run_time=1)
            self.wait(1)
        
        self.wait(2)
        
        # Add summary box
        summary_box = VGroup(
            Text("KEY INSIGHT:", font_size=24, color=YELLOW, weight=BOLD),
            Text("These two stages work together!", font_size=22),
            Text("Light reactions provide energy (ATP & NADPH)", font_size=19, color=self.COLOR_SUN),
            Text("for the Calvin cycle to make glucose", font_size=19, color=self.COLOR_SUCCESS)
        ).arrange(DOWN, buff=0.3)
        summary_box.shift(DOWN*2.7)
        
        box_rect = SurroundingRectangle(summary_box, color=YELLOW, buff=0.3, corner_radius=0.1)
        
        self.play(FadeIn(summary_box), Create(box_rect), run_time=2)
        self.wait(4)


class EnergyFlowDiagram(PhotosynthesisDetailed):
    """Energy flow diagram through photosynthesis"""
    
    def construct(self):
        super().construct()
        
        title = Text("Energy Flow in Photosynthesis", font_size=self.FONT_TITLE, color=self.COLOR_PLANT)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2)
        self.wait(1)
        
        # Sun
        sun = Circle(radius=0.5, color=self.COLOR_SUN, fill_opacity=0.8)
        sun.shift(LEFT*5 + UP*1.5)
        sun_rays = VGroup(*[
            Line(sun.get_center(), sun.get_center() + 0.7*np.array([np.cos(angle), np.sin(angle), 0]),
                 color=self.COLOR_SUN)
            for angle in np.linspace(0, 2*np.pi, 12, endpoint=False)
        ])
        sun_label = Text("Sun\n(Light Energy)", font_size=18, color=self.COLOR_SUN, line_spacing=0.7)
        sun_label.next_to(sun, DOWN, buff=0.3)
        
        self.play(Create(sun), Create(sun_rays), Write(sun_label), run_time=2)
        self.wait(1)
        
        # Arrow to chlorophyll
        arrow1 = Arrow(sun.get_right() + RIGHT*0.3, LEFT*2.5 + UP*1.5,
                      color=YELLOW, buff=0.1, stroke_width=4)
        arrow1_label = Text("Light absorbed", font_size=16, color=YELLOW)
        arrow1_label.next_to(arrow1, UP, buff=0.1)
        
        self.play(Create(arrow1), Write(arrow1_label), run_time=1.5)
        self.wait(1)
        
        # Chlorophyll
        chlorophyll_box = RoundedRectangle(width=2.5, height=1.2, color=self.COLOR_PLANT,
                                           fill_opacity=0.3, corner_radius=0.1)
        chlorophyll_box.shift(LEFT*1.2 + UP*1.5)
        chlorophyll_label = Text("Chlorophyll\n(Light Reactions)", font_size=18,
                                color=self.COLOR_PLANT, line_spacing=0.7)
        chlorophyll_label.move_to(chlorophyll_box)
        
        self.play(Create(chlorophyll_box), Write(chlorophyll_label), run_time=2)
        self.wait(1)
        
        # Products of light reactions
        products_box = RoundedRectangle(width=2.5, height=1.5, color=self.COLOR_ATP,
                                       fill_opacity=0.2, corner_radius=0.1)
        products_box.shift(RIGHT*2 + UP*1.5)
        products_label = VGroup(
            Text("ATP", font_size=20, color=self.COLOR_ATP, weight=BOLD),
            Text("+", font_size=18),
            Text("NADPH", font_size=20, color=self.COLOR_NADPH, weight=BOLD)
        ).arrange(DOWN, buff=0.2)
        products_label.move_to(products_box)
        
        arrow2 = Arrow(chlorophyll_box.get_right(), products_box.get_left(),
                      color=self.COLOR_ATP, buff=0.1, stroke_width=4)
        arrow2_label = Text("Produces", font_size=16, color=WHITE)
        arrow2_label.next_to(arrow2, UP, buff=0.1)
        
        self.play(Create(arrow2), Write(arrow2_label), run_time=1.5)
        self.play(Create(products_box), Write(products_label), run_time=2)
        self.wait(1)
        
        # Arrow down to Calvin Cycle
        arrow3 = Arrow(products_box.get_bottom(), products_box.get_bottom() + DOWN*1.5,
                      color=self.COLOR_SUCCESS, buff=0.1, stroke_width=4)
        arrow3_label = Text("Powers", font_size=16, color=self.COLOR_SUCCESS)
        arrow3_label.next_to(arrow3, RIGHT, buff=0.2)
        
        self.play(Create(arrow3), Write(arrow3_label), run_time=1.5)
        self.wait(1)
        
        # Calvin Cycle
        calvin_box = RoundedRectangle(width=3, height=1.5, color=self.COLOR_SUCCESS,
                                     fill_opacity=0.3, corner_radius=0.1)
        calvin_box.shift(RIGHT*2 + DOWN*1.2)
        calvin_label = VGroup(
            Text("Calvin Cycle", font_size=20, color=self.COLOR_SUCCESS, weight=BOLD),
            Text("(Dark Reactions)", font_size=16, color=WHITE)
        ).arrange(DOWN, buff=0.15)
        calvin_label.move_to(calvin_box)
        
        self.play(Create(calvin_box), Write(calvin_label), run_time=2)
        self.wait(1)
        
        # CO2 input
        co2_label = Text("CO₂", font_size=20, color=self.COLOR_CO2, weight=BOLD)
        co2_label.shift(LEFT*1.5 + DOWN*1.2)
        arrow_co2 = Arrow(co2_label.get_right(), calvin_box.get_left(),
                         color=self.COLOR_CO2, buff=0.1, stroke_width=3)
        
        self.play(Write(co2_label), Create(arrow_co2), run_time=1.5)
        self.wait(1)
        
        # Glucose output
        arrow4 = Arrow(calvin_box.get_bottom(), calvin_box.get_bottom() + DOWN*1.3,
                      color=self.COLOR_GLUCOSE, buff=0.1, stroke_width=4)
        arrow4_label = Text("Produces", font_size=16, color=WHITE)
        arrow4_label.next_to(arrow4, RIGHT, buff=0.2)
        
        self.play(Create(arrow4), Write(arrow4_label), run_time=1.5)
        self.wait(1)
        
        # Glucose
        glucose_box = RoundedRectangle(width=2.5, height=1, color=self.COLOR_GLUCOSE,
                                      fill_opacity=0.4, corner_radius=0.1)
        glucose_box.shift(RIGHT*2 + DOWN*3.2)
        glucose_label = VGroup(
            Text("GLUCOSE", font_size=22, color=self.COLOR_GLUCOSE, weight=BOLD),
            MathTex(r"\text{C}_6\text{H}_{12}\text{O}_6", font_size=18, color=WHITE)
        ).arrange(DOWN, buff=0.15)
        glucose_label.move_to(glucose_box)
        
        self.play(Create(glucose_box), Write(glucose_label), run_time=2)
        self.wait(2)
        
        # O2 byproduct
        o2_arrow = Arrow(chlorophyll_box.get_left() + DOWN*0.3, LEFT*3.5 + DOWN*0.5,
                        color=self.COLOR_O2, buff=0.1, stroke_width=3)
        o2_label = Text("O₂\n(Released)", font_size=18, color=self.COLOR_O2, line_spacing=0.7)
        o2_label.shift(LEFT*4.5 + DOWN*0.5)
        
        self.play(Create(o2_arrow), Write(o2_label), run_time=1.5)
        self.wait(2)
        
        # Summary equation at bottom
        summary = MathTex(
            r"6\text{CO}_2 + 6\text{H}_2\text{O} + \text{Light} \rightarrow \text{C}_6\text{H}_{12}\text{O}_6 + 6\text{O}_2",
            font_size=24
        )
        summary.to_edge(DOWN, buff=0.3).shift(LEFT*1)
        summary_box_rect = SurroundingRectangle(summary, color=YELLOW, buff=0.2, corner_radius=0.1)
        
        self.play(Write(summary), Create(summary_box_rect), run_time=2)
        self.wait(4)


class GlucoseProduction(PhotosynthesisDetailed):
    """Detailed glucose production mathematics"""
    
    def construct(self):
        super().construct()
        
        title = Text("Making One Glucose Molecule", font_size=self.FONT_TITLE, color=self.COLOR_GLUCOSE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2)
        self.wait(1)
        
        subtitle = Text("The Numbers Behind It", font_size=28, color=self.COLOR_INFO)
        subtitle.shift(UP*2.5)
        self.play(FadeIn(subtitle), run_time=1.5)
        self.wait(1)
        
        # Glucose structure
        glucose_formula = MathTex(r"\text{C}_6\text{H}_{12}\text{O}_6", font_size=48, color=self.COLOR_GLUCOSE)
        glucose_formula.shift(UP*1.6)
        glucose_name = Text("Glucose (a simple sugar)", font_size=22, color=WHITE)
        glucose_name.next_to(glucose_formula, DOWN, buff=0.3)
        
        self.play(Write(glucose_formula), run_time=2)
        self.play(FadeIn(glucose_name), run_time=1)
        self.wait(2)
        
        # Break down what's needed
        needed_title = Text("To make 1 glucose, you need:", font_size=26, color=self.COLOR_WARNING)
        needed_title.shift(UP*0.3)
        self.play(Write(needed_title), run_time=1.5)
        self.wait(1)
        
        needed_list = VGroup(
            Text("• 6 CO₂ molecules (carbon source)", font_size=22, color=self.COLOR_CO2),
            Text("• 12 H₂O molecules (for electrons)", font_size=22, color=self.COLOR_WATER),
            Text("• 18 ATP molecules (energy)", font_size=22, color=self.COLOR_ATP),
            Text("• 12 NADPH molecules (electrons)", font_size=22, color=self.COLOR_NADPH),
            Text("• Light energy (to power it all)", font_size=22, color=self.COLOR_SUN)
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        needed_list.shift(DOWN*1.2 + LEFT*1.5)
        
        for item in needed_list:
            self.play(FadeIn(item, shift=RIGHT*0.3), run_time=1)
            self.wait(1.5)
        
        self.wait(2)
        
        # Clear for detailed math
        self.play(
            FadeOut(glucose_formula), FadeOut(glucose_name),
            FadeOut(needed_title), FadeOut(needed_list),
            run_time=1.5
        )
        
        # Calvin Cycle turns needed
        cycles_title = Text("Calvin Cycle Turns", font_size=28, color=self.COLOR_SUCCESS)
        cycles_title.shift(UP*1.8)
        self.play(Write(cycles_title), run_time=1.5)
        self.wait(1)
        
        cycle_explanation = VGroup(
            Text("Each turn of Calvin Cycle:", font_size=24, color=WHITE),
            Text("• Fixes 1 CO₂", font_size=22, color=self.COLOR_CO2),
            Text("• Produces 1 G3P (3-carbon sugar)", font_size=22, color=self.COLOR_SUCCESS),
            Text("", font_size=22),  # spacer
            Text("To make glucose (6-carbon):", font_size=24, color=YELLOW),
            Text("• Need TWO G3P molecules", font_size=22),
            Text("• So cycle must turn 6 times!", font_size=22, color=self.COLOR_GLUCOSE)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        cycle_explanation.shift(UP*0.3 + LEFT*1.5)
        
        for line in cycle_explanation:
            if line.text != "":
                self.play(FadeIn(line, shift=RIGHT*0.3), run_time=1)
                self.wait(1.5)
        
        self.wait(2)
        
        # Calculation box
        calc_box = VGroup(
            Text("Quick Math:", font_size=24, color=self.COLOR_WARNING, weight=BOLD),
            MathTex(r"2 \text{ G3P} = 1 \text{ glucose}", font_size=22),
            MathTex(r"6 \text{ turns} = 6 \text{ G3P total}", font_size=22),
            MathTex(r"6 \text{ G3P} - 2 \text{ G3P (for glucose)} = 4 \text{ G3P}", font_size=20),
            Text("(4 G3P recycled to continue cycle)", font_size=18, color=self.COLOR_INFO)
        ).arrange(DOWN, buff=0.3)
        calc_box.shift(DOWN*2)
        
        calc_rect = SurroundingRectangle(calc_box, color=self.COLOR_WARNING, buff=0.3, corner_radius=0.1)
        
        self.play(Create(calc_rect), run_time=1)
        for line in calc_box:
            self.play(Write(line), run_time=1.5)
            self.wait(1)
        
        self.wait(3)
        
        # Clear everything
        self.play(*[FadeOut(mob) for mob in self.mobjects if mob != title], run_time=1.5)
        
        # Final summary table
        summary_title = Text("Complete Requirements Table", font_size=28, color=self.COLOR_WARNING)
        summary_title.shift(UP*2.3)
        self.play(Write(summary_title), run_time=1.5)
        self.wait(1)
        
        # Create table
        table_data = [
            ["Molecule", "Amount Needed", "Purpose"],
            ["CO₂", "6", "Carbon source"],
            ["H₂O", "12", "Source of electrons & H⁺"],
            ["ATP", "18", "Energy"],
            ["NADPH", "12", "Electron carrier"],
            ["Light", "Continuous", "Initial energy input"]
        ]
        
        # Create table manually for better control
        rows = VGroup()
        for i, row_data in enumerate(table_data):
            row = VGroup(*[
                Text(str(cell), font_size=20 if i == 0 else 18,
                    color=self.COLOR_INFO if i == 0 else WHITE,
                    weight=BOLD if i == 0 else NORMAL)
                for cell in row_data
            ]).arrange(RIGHT, buff=1.8)
            rows.add(row)
        
        # Align columns
        for row in rows[1:]:
            for i, cell in enumerate(row):
                cell.align_to(rows[0][i], LEFT)
        
        rows.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        rows.shift(UP*0.2)
        
        # Header line
        header_line = Line(
            rows[0].get_left() + LEFT*0.3,
            rows[0].get_right() + RIGHT*0.3,
            color=self.COLOR_INFO
        )
        header_line.next_to(rows[0], DOWN, buff=0.2)
        
        self.play(Write(rows[0]), Create(header_line), run_time=2)
        self.wait(1)
        
        for row in rows[1:]:
            self.play(FadeIn(row, shift=DOWN*0.2), run_time=1)
            self.wait(1)
        
        # Final product
        product_text = Text("PRODUCES: 1 Glucose (C₆H₁₂O₆) + 6 O₂",
                          font_size=26, color=self.COLOR_GLUCOSE, weight=BOLD)
        product_text.shift(DOWN*2.3)
        product_box = SurroundingRectangle(product_text, color=self.COLOR_GLUCOSE, buff=0.3, corner_radius=0.1)
        
        self.play(Write(product_text), Create(product_box), run_time=2)
        self.wait(4)
