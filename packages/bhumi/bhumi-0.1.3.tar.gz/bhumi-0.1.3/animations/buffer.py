from manim import *

class BufferSizeComparison(Scene):
    def construct(self):
        # Title
        title = Text("Buffer Size and Efficiency", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Labels for buffer sizes
        small_buffer_label = Text("16 KB Buffer", font_size=24).to_edge(LEFT)
        optimal_buffer_label = Text("128 KB Buffer", font_size=24)
        large_buffer_label = Text("512 KB Buffer", font_size=24).to_edge(RIGHT)

        self.play(
            Write(small_buffer_label),
            Write(optimal_buffer_label),
            Write(large_buffer_label),
        )

        # Create buffer rectangles
        small_buffer = Rectangle(width=2, height=1, color=BLUE).next_to(small_buffer_label, DOWN)
        optimal_buffer = Rectangle(width=4, height=1, color=GREEN).next_to(optimal_buffer_label, DOWN)
        large_buffer = Rectangle(width=6, height=1, color=RED).next_to(large_buffer_label, DOWN)

        self.play(Create(small_buffer), Create(optimal_buffer), Create(large_buffer))

        # Data packets filling buffers
        small_data = [Circle(radius=0.15, color=BLUE).move_to(small_buffer.get_left() + RIGHT * (0.3 * i)) for i in range(5)]
        optimal_data = [Circle(radius=0.15, color=GREEN).move_to(optimal_buffer.get_left() + RIGHT * (0.4 * i)) for i in range(10)]
        large_data = [Circle(radius=0.15, color=RED).move_to(large_buffer.get_left() + RIGHT * (0.6 * i)) for i in range(15)]

        # Animate data filling the buffers
        self.play(*[FadeIn(packet) for packet in small_data], run_time=1)
        self.play(*[FadeIn(packet) for packet in optimal_data], run_time=1.5)
        self.play(*[FadeIn(packet) for packet in large_data], run_time=2)

        # Simulate sending data
        small_send = Text("Sending...", font_size=20, color=BLUE).next_to(small_buffer, DOWN)
        optimal_send = Text("Sending...", font_size=20, color=GREEN).next_to(optimal_buffer, DOWN)
        large_send = Text("Sending...", font_size=20, color=RED).next_to(large_buffer, DOWN)

        self.play(FadeIn(small_send))
        self.wait(0.5)
        self.play(FadeOut(*small_data), FadeOut(small_send))

        self.play(FadeIn(optimal_send))
        self.wait(1)
        self.play(FadeOut(*optimal_data), FadeOut(optimal_send))

        self.play(FadeIn(large_send))
        self.wait(2)
        self.play(FadeOut(*large_data), FadeOut(large_send))

        # Conclusion
        conclusion = Text("128 KB is the optimal buffer size!\nLess overhead, faster processing.", font_size=24).to_edge(DOWN)
        self.play(Write(conclusion))

        self.wait(2)