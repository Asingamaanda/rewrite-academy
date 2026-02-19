from manim import *

class QuadraticReveal(Scene):
    def construct(self):
        # ===== INTRO =====
        title = Text("Complete Guide to Parabolas", font_size=52, color=BLUE)
        subtitle = Text("All Forms & Transformations", font_size=32, color=GRAY)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title), run_time=2)
        self.play(FadeIn(subtitle), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # ===== SCENARIO 1: Basic Parabola =====
        scene1_title = Text("Scenario 1: The Basic Parabola", font_size=36)
        scene1_title.to_edge(UP)
        self.play(Write(scene1_title), run_time=1.5)
        self.wait(1)
        
        axes1 = Axes(
            x_range=[-5, 5, 1],
            y_range=[-1, 10, 1],
            axis_config={"include_numbers": True, "font_size": 24},
        ).scale(0.7)
        
        labels1 = axes1.get_axis_labels(x_label="x", y_label="y")
        
        graph1 = axes1.plot(lambda x: x**2, color=BLUE, x_range=[-3, 3])
        eq1 = MathTex("f(x) = x^2", color=BLUE).to_corner(UR)
        
        self.play(Create(axes1), Write(labels1), run_time=2)
        self.play(Create(graph1), Write(eq1), run_time=2)
        self.wait(2)
        
        # Highlight key features
        vertex_dot = Dot(axes1.c2p(0, 0), color=RED, radius=0.1)
        vertex_label = Text("Vertex (0, 0)", font_size=24, color=RED).next_to(vertex_dot, DOWN)
        
        self.play(FadeIn(vertex_dot), Write(vertex_label), run_time=1.5)
        self.wait(2)
        
        aos_line = DashedLine(axes1.c2p(0, -1), axes1.c2p(0, 10), color=YELLOW)
        aos_label = Text("Axis of Symmetry: x = 0", font_size=24, color=YELLOW).to_edge(LEFT).shift(UP*2)
        
        self.play(Create(aos_line), Write(aos_label), run_time=1.5)
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in [scene1_title, axes1, labels1, graph1, eq1, vertex_dot, vertex_label, aos_line, aos_label]], run_time=1)
        
        # ===== SCENARIO 2: Opening Direction =====
        scene2_title = Text("Scenario 2: Opening Up vs Down", font_size=36)
        scene2_title.to_edge(UP)
        self.play(Write(scene2_title), run_time=1.5)
        self.wait(1)
        
        axes2 = Axes(
            x_range=[-4, 4, 1],
            y_range=[-10, 10, 2],
            axis_config={"include_numbers": True, "font_size": 20},
        ).scale(0.65)
        
        labels2 = axes2.get_axis_labels(x_label="x", y_label="y")
        
        # Positive a (opens up)
        graph_up = axes2.plot(lambda x: x**2, color=GREEN, x_range=[-3, 3])
        eq_up = MathTex("f(x) = x^2", color=GREEN, font_size=36).to_corner(UL)
        eq_up_note = Text("a > 0 → Opens Up", font_size=24, color=GREEN).next_to(eq_up, DOWN, aligned_edge=LEFT)
        
        self.play(Create(axes2), Write(labels2), run_time=1.5)
        self.play(Create(graph_up), Write(eq_up), run_time=1.5)
        self.play(Write(eq_up_note), run_time=1)
        self.wait(2)
        
        # Negative a (opens down)
        graph_down = axes2.plot(lambda x: -x**2, color=RED, x_range=[-3, 3])
        eq_down = MathTex("g(x) = -x^2", color=RED, font_size=36).to_corner(UR)
        eq_down_note = Text("a < 0 → Opens Down", font_size=24, color=RED).next_to(eq_down, DOWN, aligned_edge=RIGHT)
        
        self.play(Create(graph_down), Write(eq_down), run_time=1.5)
        self.play(Write(eq_down_note), run_time=1)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in [scene2_title, axes2, labels2, graph_up, graph_down, eq_up, eq_down, eq_up_note, eq_down_note]], run_time=1)
        
        # ===== SCENARIO 3: Width Variation =====
        scene3_title = Text("Scenario 3: Narrow vs Wide", font_size=36)
        scene3_title.to_edge(UP)
        self.play(Write(scene3_title), run_time=1.5)
        self.wait(1)
        
        axes3 = Axes(
            x_range=[-5, 5, 1],
            y_range=[-1, 12, 2],
            axis_config={"include_numbers": True, "font_size": 20},
        ).scale(0.65)
        
        labels3 = axes3.get_axis_labels(x_label="x", y_label="y")
        self.play(Create(axes3), Write(labels3), run_time=1.5)
        
        # Wide parabola
        graph_wide = axes3.plot(lambda x: 0.5 * x**2, color=BLUE, x_range=[-4, 4])
        eq_wide = MathTex("f(x) = 0.5x^2", color=BLUE, font_size=32).to_corner(UL)
        wide_note = Text("|a| < 1 → Wide", font_size=24, color=BLUE).next_to(eq_wide, DOWN, aligned_edge=LEFT)
        
        self.play(Create(graph_wide), Write(eq_wide), run_time=1.5)
        self.play(Write(wide_note), run_time=1)
        self.wait(2)
        
        # Standard
        graph_standard = axes3.plot(lambda x: x**2, color=YELLOW, x_range=[-3.5, 3.5])
        eq_standard = MathTex("g(x) = x^2", color=YELLOW, font_size=32).move_to(RIGHT*3 + UP*2.5)
        standard_note = Text("|a| = 1", font_size=24, color=YELLOW).next_to(eq_standard, DOWN)
        
        self.play(Create(graph_standard), Write(eq_standard), run_time=1.5)
        self.play(Write(standard_note), run_time=1)
        self.wait(2)
        
        # Narrow parabola
        graph_narrow = axes3.plot(lambda x: 2 * x**2, color=RED, x_range=[-2.5, 2.5])
        eq_narrow = MathTex("h(x) = 2x^2", color=RED, font_size=32).to_corner(UR)
        narrow_note = Text("|a| > 1 → Narrow", font_size=24, color=RED).next_to(eq_narrow, DOWN, aligned_edge=RIGHT)
        
        self.play(Create(graph_narrow), Write(eq_narrow), run_time=1.5)
        self.play(Write(narrow_note), run_time=1)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in [scene3_title, axes3, labels3, graph_wide, graph_standard, graph_narrow, 
                                              eq_wide, eq_standard, eq_narrow, wide_note, standard_note, narrow_note]], run_time=1)
        
        # ===== SCENARIO 4: Vertical Shifts =====
        scene4_title = Text("Scenario 4: Vertical Shifts", font_size=36)
        scene4_title.to_edge(UP)
        self.play(Write(scene4_title), run_time=1.5)
        self.wait(1)
        
        axes4 = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 10, 2],
            axis_config={"include_numbers": True, "font_size": 20},
        ).scale(0.7)
        
        labels4 = axes4.get_axis_labels(x_label="x", y_label="y")
        self.play(Create(axes4), Write(labels4), run_time=1.5)
        
        # Original
        graph_original = axes4.plot(lambda x: x**2, color=BLUE, x_range=[-3, 3])
        eq_original = MathTex("f(x) = x^2", color=BLUE, font_size=32).to_corner(UL)
        
        self.play(Create(graph_original), Write(eq_original), run_time=1.5)
        self.wait(1.5)
        
        # Shift up
        graph_up_shift = axes4.plot(lambda x: x**2 + 3, color=GREEN, x_range=[-3, 3])
        eq_up_shift = MathTex("g(x) = x^2 + 3", color=GREEN, font_size=32).next_to(eq_original, DOWN, aligned_edge=LEFT)
        shift_up_note = Text("Shift up 3 units", font_size=22, color=GREEN).next_to(eq_up_shift, DOWN, aligned_edge=LEFT)
        
        self.play(Transform(graph_original.copy(), graph_up_shift), run_time=2)
        self.play(Write(eq_up_shift), Write(shift_up_note), run_time=1.5)
        self.wait(2)
        
        # Shift down
        graph_down_shift = axes4.plot(lambda x: x**2 - 2, color=RED, x_range=[-3, 3])
        eq_down_shift = MathTex("h(x) = x^2 - 2", color=RED, font_size=32).to_corner(UR)
        shift_down_note = Text("Shift down 2 units", font_size=22, color=RED).next_to(eq_down_shift, DOWN, aligned_edge=RIGHT)
        
        self.play(Create(graph_up_shift), run_time=0.5)
        self.play(Transform(graph_original.copy(), graph_down_shift), run_time=2)
        self.play(Write(eq_down_shift), Write(shift_down_note), run_time=1.5)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in [scene4_title, axes4, labels4, graph_original, graph_up_shift, graph_down_shift,
                                              eq_original, eq_up_shift, eq_down_shift, shift_up_note, shift_down_note]], run_time=1)
        
        # ===== SCENARIO 5: Horizontal Shifts =====
        scene5_title = Text("Scenario 5: Horizontal Shifts", font_size=36)
        scene5_title.to_edge(UP)
        self.play(Write(scene5_title), run_time=1.5)
        self.wait(1)
        
        axes5 = Axes(
            x_range=[-6, 6, 1],
            y_range=[-1, 10, 2],
            axis_config={"include_numbers": True, "font_size": 20},
        ).scale(0.65)
        
        labels5 = axes5.get_axis_labels(x_label="x", y_label="y")
        self.play(Create(axes5), Write(labels5), run_time=1.5)
        
        # Original
        graph5_original = axes5.plot(lambda x: x**2, color=BLUE, x_range=[-3, 3])
        eq5_original = MathTex("f(x) = x^2", color=BLUE, font_size=32).to_corner(UL)
        
        self.play(Create(graph5_original), Write(eq5_original), run_time=1.5)
        self.wait(1.5)
        
        # Shift right
        graph_right = axes5.plot(lambda x: (x-2)**2, color=GREEN, x_range=[-1, 5])
        eq_right = MathTex("g(x) = (x-2)^2", color=GREEN, font_size=32).next_to(eq5_original, DOWN, aligned_edge=LEFT)
        right_note = Text("Shift right 2 units", font_size=22, color=GREEN).next_to(eq_right, DOWN, aligned_edge=LEFT)
        
        self.play(Create(graph_right), run_time=2)
        self.play(Write(eq_right), Write(right_note), run_time=1.5)
        self.wait(2)
        
        # Shift left
        graph_left = axes5.plot(lambda x: (x+2)**2, color=RED, x_range=[-5, 1])
        eq_left = MathTex("h(x) = (x+2)^2", color=RED, font_size=32).to_corner(UR)
        left_note = Text("Shift left 2 units", font_size=22, color=RED).next_to(eq_left, DOWN, aligned_edge=RIGHT)
        
        self.play(Create(graph_left), run_time=2)
        self.play(Write(eq_left), Write(left_note), run_time=1.5)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in [scene5_title, axes5, labels5, graph5_original, graph_right, graph_left,
                                              eq5_original, eq_right, eq_left, right_note, left_note]], run_time=1)
        
        # ===== SCENARIO 6: Vertex Form =====
        scene6_title = Text("Scenario 6: Vertex Form", font_size=36)
        scene6_title.to_edge(UP)
        self.play(Write(scene6_title), run_time=1.5)
        self.wait(1)
        
        vertex_form = MathTex("f(x) = a(x-h)^2 + k", font_size=48)
        vertex_form.move_to(UP*1.5)
        
        self.play(Write(vertex_form), run_time=2)
        self.wait(1)
        
        explanation = VGroup(
            Text("h = horizontal shift", font_size=28, color=BLUE),
            Text("k = vertical shift", font_size=28, color=GREEN),
            Text("a = width & direction", font_size=28, color=RED),
            Text("Vertex at (h, k)", font_size=28, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(vertex_form, DOWN, buff=0.8)
        
        self.play(Write(explanation[0]), run_time=1.5)
        self.wait(1)
        self.play(Write(explanation[1]), run_time=1.5)
        self.wait(1)
        self.play(Write(explanation[2]), run_time=1.5)
        self.wait(1)
        self.play(Write(explanation[3]), run_time=1.5)
        self.wait(2)
        
        # Example
        example = MathTex("f(x) = 2(x-1)^2 + 3", font_size=42, color=ORANGE).to_edge(DOWN, buff=1)
        example_note = Text("Vertex: (1, 3), Opens up, Narrow", font_size=26, color=ORANGE).next_to(example, DOWN)
        
        self.play(Write(example), run_time=1.5)
        self.play(Write(example_note), run_time=1.5)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in [scene6_title, vertex_form, explanation, example, example_note]], run_time=1)
        
        # ===== FINALE: All Together =====
        finale_title = Text("All Scenarios Combined", font_size=40, color=GOLD)
        finale_title.to_edge(UP)
        self.play(Write(finale_title), run_time=2)
        self.wait(1)
        
        axes_final = Axes(
            x_range=[-5, 5, 1],
            y_range=[-8, 12, 2],
            axis_config={"include_numbers": True, "font_size": 18},
        ).scale(0.7)
        
        labels_final = axes_final.get_axis_labels(x_label="x", y_label="y")
        self.play(Create(axes_final), Write(labels_final), run_time=1.5)
        
        # Multiple parabolas
        graphs_final = VGroup(
            axes_final.plot(lambda x: x**2, color=BLUE, x_range=[-3, 3]),
            axes_final.plot(lambda x: -0.5*x**2 + 5, color=RED, x_range=[-4, 4]),
            axes_final.plot(lambda x: (x-2)**2 - 3, color=GREEN, x_range=[-1, 5]),
            axes_final.plot(lambda x: -2*(x+1.5)**2 + 8, color=PURPLE, x_range=[-3.5, 0.5]),
        )
        
        for graph in graphs_final:
            self.play(Create(graph), run_time=1.5)
            self.wait(0.5)
        
        self.wait(2)
        
        final_message = Text("Master all scenarios to master parabolas!", font_size=32, color=GOLD)
        final_message.to_edge(DOWN)
        
        self.play(Write(final_message), run_time=2)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=2)
