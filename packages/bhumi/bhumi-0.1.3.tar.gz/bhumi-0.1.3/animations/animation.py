from manim import *

class StreamingComparison(Scene):
    def construct(self):
        # Scene 1: Introduction to Streaming and Buffers
        self.play_intro()

        # Scene 2: Problems with Fixed Buffer Sizes
        self.play_fixed_buffer_problems()

        # Scene 3: Introduction to MAP-Elites
        self.play_map_elites_intro()

        # Scene 4 & 5: Split-Screen Comparison
        self.play_comparison()

        # Scene 6: Conclusion
        self.play_conclusion()

    def play_intro(self):
        # Elements
        cloud = Circle(radius=0.5, fill_color=GREY, fill_opacity=0.5).to_edge(LEFT)
        buffer = Rectangle(width=2, height=0.5, fill_opacity=0.3, fill_color=BLUE).shift(LEFT * 2)
        player = Rectangle(width=1, height=1, fill_opacity=0.3, fill_color=GREEN).shift(RIGHT * 2)
        arrow1 = Arrow(cloud.get_right(), buffer.get_left(), buff=0.1)
        arrow2 = Arrow(buffer.get_right(), player.get_left(), buff=0.1)
        label = Text("Buffers store data for smooth playback", font_size=24).to_edge(UP)

        # Animation
        self.play(FadeIn(cloud), FadeIn(buffer), FadeIn(player), Create(arrow1), Create(arrow2))
        packets = [Square(0.2, fill_color=YELLOW, fill_opacity=1) for _ in range(3)]
        for i, pkt in enumerate(packets):
            pkt.move_to(cloud.get_center())
            self.play(pkt.animate.move_to(buffer.get_center()), run_time=0.5)
            self.play(pkt.animate.move_to(player.get_center()), run_time=0.5)
            self.play(FadeOut(pkt))
        self.play(Write(label))
        self.wait(1)
        self.play(FadeOut(cloud, buffer, player, arrow1, arrow2, label))

    def play_fixed_buffer_problems(self):
        # Setup
        small_buffer = Rectangle(width=1, height=0.5, fill_opacity=0.3, fill_color=BLUE).shift(LEFT * 3 + UP * 2)
        large_buffer = Rectangle(width=3, height=0.5, fill_opacity=0.3, fill_color=BLUE).shift(RIGHT * 3 + UP * 2)
        small_label = Text("Small Buffer", font_size=20).next_to(small_buffer, UP)
        large_label = Text("Large Buffer", font_size=20).next_to(large_buffer, UP)
        small_play = Triangle(fill_color=GREEN, fill_opacity=1).scale(0.2).next_to(small_buffer, DOWN)
        large_play = Triangle(fill_color=GREEN, fill_opacity=1).scale(0.2).next_to(large_buffer, DOWN)

        # Network speed graph
        axes = Axes(x_range=[0, 6, 1], y_range=[0, 3, 1], axis_config={"font_size": 20}).to_edge(DOWN)
        network_speed = [2, 2, 0.5, 0.5, 2, 2]
        graph = axes.plot(lambda t: network_speed[min(int(t), len(network_speed) - 1)], color=YELLOW)

        self.play(Create(axes), Create(small_buffer), Create(large_buffer), Write(small_label), Write(large_label),
                  FadeIn(small_play), FadeIn(large_play))

        # Buffer levels
        small_fill = Rectangle(width=1, height=0.5, fill_color=BLUE, fill_opacity=0.8).align_to(small_buffer, DOWN + LEFT)
        large_fill = Rectangle(width=3, height=0.5, fill_color=BLUE, fill_opacity=0.8).align_to(large_buffer, DOWN + LEFT)
        small_level, large_level = 1, 3  # Starting full

        self.add(small_fill, large_fill)
        self.play(Create(graph), run_time=2)

        # Simulate
        for t in range(6):
            speed = network_speed[t]
            small_level += (speed - 1) * 0.5  # Playback rate = 1
            large_level += (speed - 1) * 0.5
            small_level = max(0, min(1, small_level))
            large_level = max(0, min(3, large_level))

            if small_level <= 0:
                small_play.become(Square(0.2, fill_color=RED, fill_opacity=1).move_to(small_play.get_center()))
            else:
                small_play.become(Triangle(fill_color=GREEN, fill_opacity=1).scale(0.2).move_to(small_play.get_center()))

            self.play(small_fill.animate.stretch_to_fit_width(small_level).align_to(small_buffer, LEFT),
                      large_fill.animate.stretch_to_fit_width(large_level).align_to(large_buffer, LEFT),
                      run_time=0.5)

        self.wait(1)
        self.play(FadeOut(axes, graph, small_buffer, large_buffer, small_fill, large_fill, small_label, large_label,
                          small_play, large_play))

    def play_map_elites_intro(self):
        # MAP-Elites Grid
        grid = VGroup(*[Square(side_length=1, fill_opacity=0.2, fill_color=GREY).move_to([i-1, j-1, 0])
                        for i in range(3) for j in range(3)]).shift(UP * 1.5)
        labels = VGroup(
            Text("Low Q", font_size=16).move_to(grid[0].get_center()),
            Text("Med Q", font_size=16).move_to(grid[1].get_center()),
            Text("High Q", font_size=16).move_to(grid[2].get_center()),
        )
        title = Text("MAP-Elites Archive", font_size=24).next_to(grid, UP)
        desc = Text("Optimizes strategies for conditions", font_size=20).next_to(grid, DOWN)

        self.play(Create(grid), Write(title))
        self.play(FadeIn(labels))
        for i in range(3):
            self.play(grid[i].animate.set_fill(YELLOW, opacity=0.5), run_time=0.3)
        self.play(Write(desc))
        self.wait(1)
        self.play(FadeOut(grid, labels, title, desc))

    def play_comparison(self):
        # Setup split screen
        fixed_title = Text("Fixed Buffer", font_size=24).shift(LEFT * 4 + UP * 3)
        elites_title = Text("MAP-Elites", font_size=24).shift(RIGHT * 4 + UP * 3)
        fixed_buffer = Rectangle(width=2, height=0.5, fill_opacity=0.3, fill_color=BLUE).shift(LEFT * 4)
        elites_buffer = Rectangle(width=2, height=0.5, fill_opacity=0.3, fill_color=BLUE).shift(RIGHT * 4)
        fixed_fill = Rectangle(width=2, height=0.5, fill_color=BLUE, fill_opacity=0.8).align_to(fixed_buffer, DOWN + LEFT)
        elites_fill = Rectangle(width=2, height=0.5, fill_color=BLUE, fill_opacity=0.8).align_to(elites_buffer, DOWN + LEFT)
        fixed_play = Triangle(fill_color=GREEN, fill_opacity=1).scale(0.2).next_to(fixed_buffer, DOWN)
        elites_play = Triangle(fill_color=GREEN, fill_opacity=1).scale(0.2).next_to(elites_buffer, DOWN)
        elites_grid = VGroup(*[Square(side_length=0.5, fill_opacity=0.2, fill_color=GREY).move_to([i*0.6-0.3, j*0.6-0.3, 0])
                              for i in range(3) for j in range(1)]).shift(RIGHT * 4 + DOWN * 1.5)
        grid_labels = VGroup(Text("L", font_size=12).move_to(elites_grid[0].get_center()),
                             Text("M", font_size=12).move_to(elites_grid[1].get_center()),
                             Text("H", font_size=12).move_to(elites_grid[2].get_center()))
        fixed_counter = Text("Buffering: 0s", font_size=20).next_to(fixed_title, DOWN)
        elites_counter = Text("Buffering: 0s", font_size=20).next_to(elites_title, DOWN)

        # Network speed
        axes = Axes(x_range=[0, 6, 1], y_range=[0, 3, 1], axis_config={"font_size": 20}).to_edge(DOWN)
        network_speed = [2, 2, 0.5, 0.5, 2, 2]
        graph = axes.plot(lambda t: network_speed[min(int(t), len(network_speed) - 1)], color=YELLOW)

        self.play(Write(fixed_title), Write(elites_title), Create(fixed_buffer), Create(elites_buffer),
                  FadeIn(fixed_fill), FadeIn(elites_fill), FadeIn(fixed_play), FadeIn(elites_play),
                  Create(elites_grid), FadeIn(grid_labels), Write(fixed_counter), Write(elites_counter),
                  Create(axes))

        # Simulation
        fixed_level, elites_level = 2, 2
        self.fixed_buffering, self.elites_buffering = 0, 0  # Store as instance variables
        playback_rates = [0.5, 1, 2]  # Low, Medium, High quality

        for t in range(6):
            speed = network_speed[t]
            fixed_rate = 1  # Fixed at medium quality
            elites_rate = min([r for r in playback_rates if r <= speed], default=0.5)  # Adaptive

            fixed_level += (speed - fixed_rate) * 0.5
            elites_level += (speed - elites_rate) * 0.5
            fixed_level = max(0, min(2, fixed_level))
            elites_level = max(0, min(2, elites_level))

            if fixed_level <= 0:
                fixed_play.become(Square(0.2, fill_color=RED, fill_opacity=1).move_to(fixed_play.get_center()))
                self.fixed_buffering += 0.5
                fixed_counter.become(Text(f"Buffering: {int(self.fixed_buffering)}s", font_size=20).next_to(fixed_title, DOWN))
            else:
                fixed_play.become(Triangle(fill_color=GREEN, fill_opacity=1).scale(0.2).move_to(fixed_play.get_center()))

            elites_play.become(Triangle(fill_color=GREEN, fill_opacity=1).scale(0.2).move_to(elites_play.get_center()))
            elites_grid.set_opacity(0.2)
            elites_grid[playback_rates.index(elites_rate)].set_fill(YELLOW, opacity=0.5)

            self.play(fixed_fill.animate.stretch_to_fit_width(fixed_level).align_to(fixed_buffer, LEFT),
                      elites_fill.animate.stretch_to_fit_width(elites_level).align_to(elites_buffer, LEFT),
                      Create(graph, run_time=0.5 if t == 0 else 0), run_time=0.5)

        self.wait(1)
        self.fixed_group = VGroup(fixed_title, fixed_buffer, fixed_fill, fixed_play, fixed_counter)
        self.elites_group = VGroup(elites_title, elites_buffer, elites_fill, elites_play, elites_counter, elites_grid, grid_labels)
        self.axes_group = VGroup(axes, graph)

    def play_conclusion(self):
        # Metrics
        buffering_chart = BarChart(
            values=[self.fixed_buffering, self.elites_buffering],  # Use stored variables directly
            bar_names=["Fixed", "MAP-Elites"],
            y_range=[0, 5, 1],
            y_axis_config={"font_size": 20},
            bar_colors=[RED, GREEN]
        ).scale(0.8).shift(DOWN * 1.5)
        chart_label = Text("Total Buffering Time (s)", font_size=24).next_to(buffering_chart, UP)

        self.play(FadeOut(self.fixed_group, self.elites_group, self.axes_group),
                  Create(buffering_chart), Write(chart_label))
        self.wait(1)
        conclusion = Text("MAP-Elites optimizes streaming", font_size=36).shift(UP * 2)
        self.play(Write(conclusion))
        self.wait(2)

if __name__ == "__main__":
    # Run with: manim -pql animation.py StreamingComparison
    pass