from manim import *

class WholeNumbersIntro(Scene):
    """Introduction to Whole Numbers - Chapter 1"""
    def construct(self):
        # Title
        title = Text("Chapter 1: Whole Numbers", font_size=48, color=BLUE)
        self.play(Write(title))
        self.wait(2)
        self.play(title.animate.to_edge(UP))
        
        # Definition
        definition = Text("Whole Numbers: 0, 1, 2, 3, 4, 5, ...", font_size=36)
        self.play(Write(definition))
        self.wait(2)
        
        # Number line
        self.play(FadeOut(definition))
        number_line = NumberLine(
            x_range=[0, 10, 1],
            length=10,
            include_numbers=True,
            include_tip=True
        )
        self.play(Create(number_line))
        self.wait(2)
        
        self.play(FadeOut(number_line), FadeOut(title))


class PropertiesOfNumbers(Scene):
    """Properties of whole numbers"""
    def construct(self):
        title = Text("Properties of Numbers", font_size=42, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # Commutative Property
        comm_title = Text("1. Commutative Property", font_size=32, color=YELLOW)
        comm_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(comm_title))
        
        # Addition
        add_eq1 = MathTex("3 + 5 = 8", font_size=40)
        add_eq2 = MathTex("5 + 3 = 8", font_size=40)
        add_eq1.next_to(comm_title, DOWN, buff=0.5).shift(LEFT * 2)
        add_eq2.next_to(add_eq1, RIGHT, buff=1)
        
        self.play(Write(add_eq1))
        self.wait()
        self.play(Write(add_eq2))
        self.wait()
        
        # Highlight equality
        arrow = MathTex(r"\Rightarrow", font_size=50, color=GREEN)
        arrow.move_to((add_eq1.get_center() + add_eq2.get_center()) / 2)
        self.play(FadeIn(arrow))
        self.wait()
        
        # Multiplication
        mult_eq1 = MathTex("4 \\times 6 = 24", font_size=40)
        mult_eq2 = MathTex("6 \\times 4 = 24", font_size=40)
        mult_eq1.next_to(add_eq1, DOWN, buff=0.8).align_to(add_eq1, LEFT)
        mult_eq2.next_to(mult_eq1, RIGHT, buff=1)
        
        arrow2 = MathTex(r"\Rightarrow", font_size=50, color=GREEN)
        arrow2.move_to((mult_eq1.get_center() + mult_eq2.get_center()) / 2)
        
        self.play(Write(mult_eq1), Write(mult_eq2), FadeIn(arrow2))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        # Associative Property
        assoc_title = Text("2. Associative Property", font_size=32, color=YELLOW)
        assoc_title.to_edge(UP, buff=1)
        self.play(Write(assoc_title))
        
        assoc1 = MathTex("(2 + 3) + 4 = 5 + 4 = 9", font_size=40)
        assoc2 = MathTex("2 + (3 + 4) = 2 + 7 = 9", font_size=40)
        assoc1.next_to(assoc_title, DOWN, buff=0.5)
        assoc2.next_to(assoc1, DOWN, buff=0.5)
        
        self.play(Write(assoc1))
        self.wait()
        self.play(Write(assoc2))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        # Distributive Property
        dist_title = Text("3. Distributive Property", font_size=32, color=YELLOW)
        dist_title.to_edge(UP, buff=1)
        self.play(Write(dist_title))
        
        dist1 = MathTex("3 \\times (4 + 5)", font_size=40)
        dist2 = MathTex("= 3 \\times 4 + 3 \\times 5", font_size=40)
        dist3 = MathTex("= 12 + 15 = 27", font_size=40)
        
        dist1.next_to(dist_title, DOWN, buff=0.5)
        dist2.next_to(dist1, DOWN, buff=0.3)
        dist3.next_to(dist2, DOWN, buff=0.3)
        
        self.play(Write(dist1))
        self.wait()
        self.play(Write(dist2))
        self.wait()
        self.play(Write(dist3))
        self.wait(2)


class MultiplesAndFactors(Scene):
    """Multiples and Factors visualization"""
    def construct(self):
        title = Text("Multiples and Factors", font_size=42, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # Multiples
        mult_title = Text("Multiples of 3:", font_size=36, color=YELLOW)
        mult_title.next_to(title, DOWN, buff=0.5).to_edge(LEFT)
        self.play(Write(mult_title))
        
        multiples = VGroup(*[
            MathTex(f"{i} \\times 3 = {i*3}", font_size=32)
            for i in range(1, 6)
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        multiples.next_to(mult_title, DOWN, buff=0.3).shift(RIGHT)
        
        for mult in multiples:
            self.play(Write(mult), run_time=0.5)
        self.wait(2)
        
        # Highlight the multiples
        mult_nums = Text("Multiples: 3, 6, 9, 12, 15, ...", font_size=30, color=GREEN)
        mult_nums.next_to(multiples, DOWN, buff=0.5)
        self.play(Write(mult_nums))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in [mult_title, multiples, mult_nums]])
        
        # Factors
        factor_title = Text("Factors of 12:", font_size=36, color=YELLOW)
        factor_title.next_to(title, DOWN, buff=0.5).to_edge(LEFT)
        self.play(Write(factor_title))
        
        factor_pairs = VGroup(
            MathTex("1 \\times 12 = 12", font_size=32),
            MathTex("2 \\times 6 = 12", font_size=32),
            MathTex("3 \\times 4 = 12", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        factor_pairs.next_to(factor_title, DOWN, buff=0.3).shift(RIGHT)
        
        for pair in factor_pairs:
            self.play(Write(pair), run_time=0.7)
        self.wait()
        
        factors_list = Text("Factors: 1, 2, 3, 4, 6, 12", font_size=30, color=GREEN)
        factors_list.next_to(factor_pairs, DOWN, buff=0.5)
        self.play(Write(factors_list))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class PrimeFactorization(Scene):
    """Prime factorization using factor trees"""
    def construct(self):
        title = Text("Prime Factorization", font_size=42, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        subtitle = Text("Finding prime factors of 24", font_size=32, color=YELLOW)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(Write(subtitle))
        self.wait()
        
        # Create factor tree
        num_24 = MathTex("24", font_size=48, color=WHITE)
        num_24.shift(UP * 1.5)
        self.play(Write(num_24))
        
        # First split
        line1 = Line(num_24.get_bottom(), num_24.get_bottom() + DOWN * 0.5 + LEFT * 1)
        line2 = Line(num_24.get_bottom(), num_24.get_bottom() + DOWN * 0.5 + RIGHT * 1)
        num_2_1 = MathTex("2", font_size=40, color=GREEN)
        num_12 = MathTex("12", font_size=40)
        num_2_1.move_to(line1.get_end() + DOWN * 0.3)
        num_12.move_to(line2.get_end() + DOWN * 0.3)
        
        self.play(Create(line1), Create(line2))
        self.play(Write(num_2_1), Write(num_12))
        self.wait()
        
        # Split 12
        line3 = Line(num_12.get_bottom(), num_12.get_bottom() + DOWN * 0.5 + LEFT * 0.5)
        line4 = Line(num_12.get_bottom(), num_12.get_bottom() + DOWN * 0.5 + RIGHT * 0.5)
        num_2_2 = MathTex("2", font_size=40, color=GREEN)
        num_6 = MathTex("6", font_size=40)
        num_2_2.move_to(line3.get_end() + DOWN * 0.3)
        num_6.move_to(line4.get_end() + DOWN * 0.3)
        
        self.play(Create(line3), Create(line4))
        self.play(Write(num_2_2), Write(num_6))
        self.wait()
        
        # Split 6
        line5 = Line(num_6.get_bottom(), num_6.get_bottom() + DOWN * 0.5 + LEFT * 0.5)
        line6 = Line(num_6.get_bottom(), num_6.get_bottom() + DOWN * 0.5 + RIGHT * 0.5)
        num_2_3 = MathTex("2", font_size=40, color=GREEN)
        num_3 = MathTex("3", font_size=40, color=GREEN)
        num_2_3.move_to(line5.get_end() + DOWN * 0.3)
        num_3.move_to(line6.get_end() + DOWN * 0.3)
        
        self.play(Create(line5), Create(line6))
        self.play(Write(num_2_3), Write(num_3))
        self.wait(2)
        
        # Show result
        result = MathTex("24 = 2 \\times 2 \\times 2 \\times 3 = 2^3 \\times 3", 
                        font_size=36, color=YELLOW)
        result.to_edge(DOWN, buff=1)
        self.play(Write(result))
        self.wait(3)


class RatioAndProportion(Scene):
    """Ratio, Rate, and Proportion problems"""
    def construct(self):
        title = Text("Ratio, Rate & Proportion", font_size=42, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # Ratio example
        ratio_title = Text("Ratio Example:", font_size=32, color=YELLOW)
        ratio_title.next_to(title, DOWN, buff=0.5).to_edge(LEFT)
        self.play(Write(ratio_title))
        
        problem = Text("Mix red and blue paint in ratio 3:2", font_size=28)
        problem.next_to(ratio_title, DOWN, buff=0.3)
        self.play(Write(problem))
        self.wait()
        
        # Visual representation
        red_rect = Rectangle(width=3, height=0.5, color=RED, fill_opacity=0.7)
        blue_rect = Rectangle(width=2, height=0.5, color=BLUE, fill_opacity=0.7)
        red_rect.next_to(problem, DOWN, buff=0.5).shift(LEFT * 1.5)
        blue_rect.next_to(red_rect, RIGHT, buff=0.5)
        
        red_label = Text("3 parts", font_size=24).next_to(red_rect, DOWN)
        blue_label = Text("2 parts", font_size=24).next_to(blue_rect, DOWN)
        
        self.play(Create(red_rect), Create(blue_rect))
        self.play(Write(red_label), Write(blue_label))
        self.wait(2)
        
        # Calculation
        calc = MathTex(r"\text{If we need 10L total:}", font_size=28)
        calc.next_to(blue_label, DOWN, buff=0.5).shift(LEFT * 2)
        
        calc2 = MathTex(r"\text{Red} = \frac{3}{5} \times 10 = 6\text{L}", font_size=28)
        calc3 = MathTex(r"\text{Blue} = \frac{2}{5} \times 10 = 4\text{L}", font_size=28)
        calc2.next_to(calc, DOWN, buff=0.3, aligned_edge=LEFT)
        calc3.next_to(calc2, DOWN, buff=0.3, aligned_edge=LEFT)
        
        self.play(Write(calc))
        self.wait()
        self.play(Write(calc2))
        self.wait()
        self.play(Write(calc3))
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class RateProblems(Scene):
    """Rate problems - speed, distance, time"""
    def construct(self):
        title = Text("Rate Problems", font_size=42, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # Speed problem
        problem = Text("A car travels 240 km in 3 hours", font_size=32, color=YELLOW)
        problem.next_to(title, DOWN, buff=0.5)
        self.play(Write(problem))
        self.wait()
        
        question = Text("What is the speed?", font_size=28)
        question.next_to(problem, DOWN, buff=0.3)
        self.play(Write(question))
        self.wait()
        
        # Formula
        formula = MathTex(r"\text{Speed} = \frac{\text{Distance}}{\text{Time}}", font_size=36)
        formula.next_to(question, DOWN, buff=0.7)
        self.play(Write(formula))
        self.wait()
        
        # Calculation
        calc1 = MathTex(r"\text{Speed} = \frac{240 \text{ km}}{3 \text{ hours}}", font_size=36)
        calc1.next_to(formula, DOWN, buff=0.5)
        self.play(Write(calc1))
        self.wait()
        
        calc2 = MathTex(r"\text{Speed} = 80 \text{ km/h}", font_size=40, color=GREEN)
        calc2.next_to(calc1, DOWN, buff=0.5)
        self.play(Write(calc2))
        self.wait(2)
        
        # Highlight answer
        box = SurroundingRectangle(calc2, color=YELLOW, buff=0.2)
        self.play(Create(box))
        self.wait(2)


class FinancialProblems(Scene):
    """Financial context problems - percentage, interest, discounts"""
    def construct(self):
        title = Text("Financial Problems", font_size=42, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # Discount problem
        prob_title = Text("Discount Problem", font_size=32, color=YELLOW)
        prob_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(prob_title))
        
        problem = Text("A shirt costs R200. It's on sale for 25% off.", font_size=28)
        problem.next_to(prob_title, DOWN, buff=0.4)
        self.play(Write(problem))
        self.wait()
        
        question = Text("What is the sale price?", font_size=26)
        question.next_to(problem, DOWN, buff=0.3)
        self.play(Write(question))
        self.wait()
        
        # Solution
        step1 = MathTex(r"\text{Discount} = 25\% \text{ of } R200", font_size=32)
        step1.next_to(question, DOWN, buff=0.6)
        self.play(Write(step1))
        self.wait()
        
        step2 = MathTex(r"= \frac{25}{100} \times 200 = R50", font_size=32)
        step2.next_to(step1, DOWN, buff=0.3)
        self.play(Write(step2))
        self.wait()
        
        step3 = MathTex(r"\text{Sale Price} = R200 - R50 = R150", font_size=36, color=GREEN)
        step3.next_to(step2, DOWN, buff=0.5)
        self.play(Write(step3))
        self.wait(2)
        
        box = SurroundingRectangle(step3, color=YELLOW, buff=0.2)
        self.play(Create(box))
        self.wait(2)


class SimpleInterest(Scene):
    """Simple Interest calculation"""
    def construct(self):
        title = Text("Simple Interest", font_size=42, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # Formula
        formula_title = Text("Formula:", font_size=32, color=YELLOW)
        formula_title.next_to(title, DOWN, buff=0.5).to_edge(LEFT)
        self.play(Write(formula_title))
        
        formula = MathTex(r"I = \frac{P \times R \times T}{100}", font_size=40)
        formula.next_to(formula_title, DOWN, buff=0.4)
        self.play(Write(formula))
        self.wait()
        
        # Legend
        legend = VGroup(
            MathTex(r"I = \text{Interest}", font_size=28),
            MathTex(r"P = \text{Principal (initial amount)}", font_size=28),
            MathTex(r"R = \text{Rate (\% per year)}", font_size=28),
            MathTex(r"T = \text{Time (years)}", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend.next_to(formula, DOWN, buff=0.5)
        
        for item in legend:
            self.play(Write(item), run_time=0.7)
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        # Example problem
        title2 = Text("Example:", font_size=36, color=YELLOW)
        title2.to_edge(UP, buff=1)
        self.play(Write(title2))
        
        problem = Text("Invest R5000 at 6% per year for 3 years", font_size=30)
        problem.next_to(title2, DOWN, buff=0.4)
        self.play(Write(problem))
        self.wait()
        
        # Solution
        given = VGroup(
            MathTex(r"P = R5000", font_size=32),
            MathTex(r"R = 6\%", font_size=32),
            MathTex(r"T = 3 \text{ years}", font_size=32)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        given.next_to(problem, DOWN, buff=0.5).shift(LEFT * 2)
        
        for item in given:
            self.play(Write(item), run_time=0.6)
        self.wait()
        
        calc = MathTex(r"I = \frac{5000 \times 6 \times 3}{100}", font_size=36)
        calc.next_to(given, DOWN, buff=0.7).shift(RIGHT)
        self.play(Write(calc))
        self.wait()
        
        result1 = MathTex(r"I = \frac{90000}{100} = R900", font_size=36)
        result1.next_to(calc, DOWN, buff=0.4)
        self.play(Write(result1))
        self.wait()
        
        total = MathTex(r"\text{Total Amount} = R5000 + R900 = R5900", 
                       font_size=38, color=GREEN)
        total.next_to(result1, DOWN, buff=0.6)
        self.play(Write(total))
        self.wait(2)
        
        box = SurroundingRectangle(total, color=YELLOW, buff=0.2)
        self.play(Create(box))
        self.wait(3)


class ChapterSummary(Scene):
    """Summary of Chapter 1"""
    def construct(self):
        title = Text("Chapter 1 Summary", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        summary_items = VGroup(
            Text("✓ Properties: Commutative, Associative, Distributive", font_size=26),
            Text("✓ Multiples and Factors", font_size=26),
            Text("✓ Prime Factorization", font_size=26),
            Text("✓ Ratio, Rate, and Proportion", font_size=26),
            Text("✓ Financial Problems: Discounts & Interest", font_size=26)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        summary_items.next_to(title, DOWN, buff=1)
        
        for item in summary_items:
            self.play(Write(item), run_time=0.8)
            self.wait(0.5)
        
        self.wait(2)
        
        # Closing message
        closing = Text("Practice makes perfect!", font_size=36, color=YELLOW)
        closing.to_edge(DOWN, buff=1)
        self.play(Write(closing))
        self.wait(3)
