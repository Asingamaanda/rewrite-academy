from manim import *

class TitleCard(Scene):
    """Title card for the complete lesson"""
    def construct(self):
        # Main title
        main_title = Text("Grade 9 Mathematics", font_size=56, color=BLUE, weight=BOLD)
        main_title.to_edge(UP, buff=1)
        
        chapter = Text("Chapter 1", font_size=48, color=YELLOW)
        chapter.next_to(main_title, DOWN, buff=0.5)
        
        subtitle = Text("Whole Numbers", font_size=44, color=WHITE)
        subtitle.next_to(chapter, DOWN, buff=0.3)
        
        # Decorative elements
        line1 = Line(LEFT * 6, RIGHT * 6, color=BLUE)
        line1.next_to(main_title, DOWN, buff=0.2)
        
        line2 = Line(LEFT * 5, RIGHT * 5, color=YELLOW)
        line2.next_to(subtitle, DOWN, buff=0.5)
        
        self.play(
            Write(main_title),
            Create(line1),
            run_time=1.5
        )
        self.wait(0.5)
        
        self.play(Write(chapter), run_time=1)
        self.wait(0.3)
        
        self.play(
            Write(subtitle),
            Create(line2),
            run_time=1.5
        )
        self.wait(2)
        
        # Topics preview
        topics_title = Text("Topics Covered:", font_size=32, color=GREEN)
        topics_title.next_to(line2, DOWN, buff=0.8)
        
        topics = VGroup(
            Text("• Types of Numbers", font_size=24),
            Text("• Calculations with Whole Numbers", font_size=24),
            Text("• Multiples and Factors", font_size=24),
            Text("• Ratio, Rate, and Proportion", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        topics.next_to(topics_title, DOWN, buff=0.4)
        
        self.play(Write(topics_title))
        for topic in topics:
            self.play(Write(topic), run_time=0.6)
        
        self.wait(3)
        
        # Fade out
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class SectionCard(Scene):
    """Section divider cards"""
    def construct(self):
        # This will be customized for each section
        pass


class NumberTypesSectionCard(Scene):
    """Section 1: Number Types"""
    def construct(self):
        title = Text("Section 1", font_size=48, color=BLUE)
        title.to_edge(UP, buff=1.5)
        
        section_title = Text("Types of Numbers", font_size=56, color=YELLOW, weight=BOLD)
        section_title.next_to(title, DOWN, buff=0.8)
        
        topics = VGroup(
            Text("Natural Numbers", font_size=32),
            Text("Whole Numbers", font_size=32),
            Text("Integers", font_size=32),
            Text("Rational Numbers", font_size=32),
        ).arrange(DOWN, buff=0.4)
        topics.next_to(section_title, DOWN, buff=1)
        
        box = SurroundingRectangle(section_title, color=YELLOW, buff=0.3)
        
        self.play(Write(title))
        self.play(Write(section_title), Create(box))
        self.wait(0.5)
        
        for topic in topics:
            self.play(FadeIn(topic), run_time=0.5)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class CalculationsSectionCard(Scene):
    """Section 2: Calculations"""
    def construct(self):
        title = Text("Section 2", font_size=48, color=BLUE)
        title.to_edge(UP, buff=1.5)
        
        section_title = Text("Calculations", font_size=56, color=YELLOW, weight=BOLD)
        section_title.next_to(title, DOWN, buff=0.8)
        
        topics = VGroup(
            Text("Estimating & Rounding", font_size=32),
            Text("Addition in Columns", font_size=32),
            Text("Multiplication in Columns", font_size=32),
            Text("Long Division", font_size=32),
        ).arrange(DOWN, buff=0.4)
        topics.next_to(section_title, DOWN, buff=1)
        
        box = SurroundingRectangle(section_title, color=YELLOW, buff=0.3)
        
        self.play(Write(title))
        self.play(Write(section_title), Create(box))
        self.wait(0.5)
        
        for topic in topics:
            self.play(FadeIn(topic), run_time=0.5)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class MultiplesFactorsSectionCard(Scene):
    """Section 3: Multiples and Factors"""
    def construct(self):
        title = Text("Section 3", font_size=48, color=BLUE)
        title.to_edge(UP, buff=1.5)
        
        section_title = Text("Multiples & Factors", font_size=56, color=YELLOW, weight=BOLD)
        section_title.next_to(title, DOWN, buff=0.8)
        
        topics = VGroup(
            Text("Lowest Common Multiple (LCM)", font_size=32),
            Text("Highest Common Factor (HCF)", font_size=32),
        ).arrange(DOWN, buff=0.4)
        topics.next_to(section_title, DOWN, buff=1)
        
        box = SurroundingRectangle(section_title, color=YELLOW, buff=0.3)
        
        self.play(Write(title))
        self.play(Write(section_title), Create(box))
        self.wait(0.5)
        
        for topic in topics:
            self.play(FadeIn(topic), run_time=0.5)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class RatioRateSectionCard(Scene):
    """Section 4: Ratio, Rate, and Proportion"""
    def construct(self):
        title = Text("Section 4", font_size=48, color=BLUE)
        title.to_edge(UP, buff=1.5)
        
        section_title = Text("Ratio, Rate & Proportion", font_size=52, color=YELLOW, weight=BOLD)
        section_title.next_to(title, DOWN, buff=0.8)
        
        topics = VGroup(
            Text("Ratios in Recipes", font_size=32),
            Text("Speed, Distance, Time", font_size=32),
        ).arrange(DOWN, buff=0.4)
        topics.next_to(section_title, DOWN, buff=1)
        
        box = SurroundingRectangle(section_title, color=YELLOW, buff=0.3)
        
        self.play(Write(title))
        self.play(Write(section_title), Create(box))
        self.wait(0.5)
        
        for topic in topics:
            self.play(FadeIn(topic), run_time=0.5)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class EndCard(Scene):
    """End card with summary and next steps"""
    def construct(self):
        # Thank you message
        thanks = Text("Congratulations!", font_size=56, color=GREEN, weight=BOLD)
        thanks.shift(UP * 2)
        
        completed = Text("You've completed Chapter 1", font_size=36, color=YELLOW)
        completed.next_to(thanks, DOWN, buff=0.5)
        
        self.play(Write(thanks), run_time=1.5)
        self.wait(0.5)
        self.play(Write(completed))
        self.wait(2)
        
        self.play(FadeOut(thanks), FadeOut(completed))
        
        # What you learned
        learned_title = Text("What You Learned:", font_size=40, color=BLUE)
        learned_title.to_edge(UP, buff=1)
        
        skills = VGroup(
            Text("✓ Different types of numbers", font_size=28),
            Text("✓ Estimation and rounding techniques", font_size=28),
            Text("✓ Column arithmetic operations", font_size=28),
            Text("✓ Finding LCM and HCF", font_size=28),
            Text("✓ Solving ratio and rate problems", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        skills.next_to(learned_title, DOWN, buff=0.6)
        
        self.play(Write(learned_title))
        for skill in skills:
            self.play(Write(skill), run_time=0.7)
        
        self.wait(2)
        
        # Next chapter preview
        next_chapter = Text("Next: Chapter 2 - Integers", font_size=32, color=YELLOW)
        next_chapter.to_edge(DOWN, buff=1.5)
        
        self.play(FadeIn(next_chapter))
        self.wait(3)
        
        # Final fade
        self.play(*[FadeOut(mob) for mob in self.mobjects])
