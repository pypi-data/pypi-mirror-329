from manim import *

class BufferOptimizationScene(Scene):
    def construct(self):
        # Title
        title = Text("Bhumi: Dynamic Buffer Optimization", font_size=40)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))
        
        # Setup two buffer systems
        fixed_label = Text("Traditional Fixed Buffer", font_size=24).shift(LEFT * 4 + UP * 2)
        bhumi_label = Text("Bhumi Dynamic Buffer", font_size=24).shift(RIGHT * 4 + UP * 2)
        
        # Buffers as rectangles
        fixed_buffer = Rectangle(width=4, height=1, color=BLUE, fill_opacity=0.2).shift(LEFT * 4)
        bhumi_buffer = Rectangle(width=4, height=1, color=GREEN, fill_opacity=0.2).shift(RIGHT * 4)
        
        self.play(Write(fixed_label), Write(bhumi_label))
        self.play(Create(fixed_buffer), Create(bhumi_buffer))
        
        # Data dots (representing packets)
        def create_data_dots(n, color=YELLOW):
            return [Dot(radius=0.1, color=color).shift(LEFT * 6 + UP * (i * 0.2 - (n-1) * 0.1)) for i in range(n)]
        
        data_dots_fixed = create_data_dots(10)
        data_dots_bhumi = create_data_dots(10)
        
        # Animate data flowing into buffers
        self.play(*[dot.animate.shift(RIGHT * 2) for dot in data_dots_fixed + data_dots_bhumi], run_time=1)
        
        # Fixed buffer overflows
        overflow_label = Text("Overflow!", font_size=20, color=RED).next_to(fixed_buffer, UP)
        for i, dot in enumerate(data_dots_fixed):
            if i < 5:  # Only 5 fit in fixed buffer
                self.play(dot.animate.move_to(fixed_buffer.get_center() + (i - 2) * RIGHT * 0.8), run_time=0.2)
            else:
                self.play(dot.animate.shift(UP * 0.5), FadeIn(overflow_label), run_time=0.2)
        
        # Bhumi buffer adjusts size
        sizing_label = Text("Dynamic Sizing", font_size=20, color=GREEN).next_to(bhumi_buffer, UP)
        self.play(bhumi_buffer.animate.scale_to_fit_height(1.5), FadeIn(sizing_label), run_time=1)
        for i, dot in enumerate(data_dots_bhumi):
            self.play(dot.animate.move_to(bhumi_buffer.get_center() + (i - 4.5) * RIGHT * 0.8), run_time=0.2)
        
        # First packet race
        first_packet_fixed = Dot(color=ORANGE).move_to(fixed_buffer.get_right() + RIGHT * 0.5)
        first_packet_bhumi = Dot(color=ORANGE).move_to(bhumi_buffer.get_right() + RIGHT * 0.5)
        client_line = Line(RIGHT * 4, RIGHT * 6, color=WHITE).shift(DOWN * 2)
        client_label = Text("Client", font_size=20).next_to(client_line, RIGHT)
        
        ttft_label_fixed = Text("TTFT: Slower", font_size=20).next_to(fixed_label, DOWN * 4)
        ttft_label_bhumi = Text("TTFT: Faster!", font_size=20, color=GREEN).next_to(bhumi_label, DOWN * 4)
        
        self.play(Create(first_packet_fixed), Create(first_packet_bhumi), Create(client_line), Write(client_label))
        self.play(
            first_packet_fixed.animate.move_to(client_line.get_end()).shift(UP * 0.2),
            run_time=2,
            rate_func=linear
        )
        self.play(
            first_packet_bhumi.animate.move_to(client_line.get_end()).shift(DOWN * 0.2),
            run_time=1,  # Bhumi is faster
            rate_func=linear
        )
        self.play(Write(ttft_label_fixed), Write(ttft_label_bhumi))
        
        # Concurrency hint (arrows showing parallel processing)
        concurrency_label = Text("Rust Concurrency", font_size=20, color=GREEN).next_to(bhumi_buffer, DOWN)
        arrows = VGroup(*[Arrow(bhumi_buffer.get_bottom() + RIGHT * i - RIGHT * 2, 
                               bhumi_buffer.get_bottom() + RIGHT * i - RIGHT * 2 + DOWN * 0.5, 
                               color=GREEN) for i in range(5)])
        self.play(FadeIn(concurrency_label), Create(arrows))
        
        # Final fade out
        self.wait(2)
        self.play(FadeOut(Group(*self.mobjects)))

# Run this with: manim -pqh bhumi_buffer_animation.py BufferOptimizationScene