from manim import *

class LatencyImpactDemo(Scene):
    def construct(self):
        # Configure faster animations
        self.camera.background_color = "#111111"  # Darker background for better contrast
        
        # Colors
        CORAL_RED = "#FF6F61"
        BUFFER_BLUE = "#1E90FF"
        SUCCESS_GREEN = "#28A745"
        
        # Title with quick fade in
        title = Text("Impact of Latency on Agent Tasks", color=CORAL_RED, font="SF Pro Display")
        title.to_edge(UP)
        self.play(Write(title), run_time=0.5)

        # Create task pipeline visualization
        def create_task_box(text, color=WHITE):
            return VGroup(
                Rectangle(height=1, width=2, color=color, fill_opacity=0.1),
                Text(text, color=color, font="SF Pro Display").scale(0.4)
            ).arrange(DOWN, buff=0.1)

        # Create task sequence with modern tasks
        tasks = VGroup(
            create_task_box("LLM Query", BUFFER_BLUE),
            create_task_box("Process Response", BUFFER_BLUE),
            create_task_box("Generate Action", BUFFER_BLUE),
            create_task_box("Execute Task", BUFFER_BLUE),
        ).arrange(RIGHT, buff=1)
        
        # Animated arrows
        arrows = VGroup(*[
            Arrow(tasks[i].get_right(), tasks[i+1].get_left(), color=WHITE, 
                  max_tip_length_to_length_ratio=0.15, stroke_width=2)
            for i in range(len(tasks)-1)
        ])

        pipeline = VGroup(tasks, arrows)
        pipeline.next_to(title, DOWN, buff=1)

        # Quick creation of pipeline
        self.play(Create(pipeline), run_time=0.8)

        # Traditional approach - faster but still showing delay
        traditional_label = Text("Traditional Pipeline (High Latency)", 
                               color=BUFFER_BLUE, font="SF Pro Display").scale(0.6)
        traditional_label.next_to(pipeline, UP)
        self.play(Write(traditional_label), run_time=0.3)

        # Faster processing simulation
        completion_marks = []
        for i, task in enumerate(tasks):
            # Quick thinking animation
            thinking_dots = Text("...", font="SF Pro Display").next_to(task, DOWN)
            self.play(Write(thinking_dots), run_time=0.2)
            self.wait(0.2)  # Reduced wait time
            
            # Snappy completion
            completion = Text("✓", color=SUCCESS_GREEN, font="SF Pro Display").scale(0.8).next_to(task, RIGHT)
            completion_marks.append(completion)
            self.play(
                FadeOut(thinking_dots),
                Write(completion),
                run_time=0.2
            )

        # Quick time display
        total_time = Text("Total Time: 2.5s", color=BUFFER_BLUE, font="SF Pro Display").scale(0.6)
        total_time.next_to(pipeline, DOWN)
        self.play(Write(total_time), run_time=0.3)
        
        # Fast cleanup
        self.play(
            *[FadeOut(mob) for mob in [traditional_label, total_time]],
            *[FadeOut(mark) for mark in completion_marks],
            run_time=0.3
        )

        # Bhumi approach - even faster
        bhumi_label = Text("Bhumi Pipeline (Optimized Latency)", 
                         color=CORAL_RED, font="SF Pro Display").scale(0.6)
        bhumi_label.next_to(pipeline, UP)
        self.play(Write(bhumi_label), run_time=0.3)

        # Parallel processing animation
        all_thinking_dots = VGroup(*[
            Text("...", font="SF Pro Display").next_to(task, DOWN)
            for task in tasks
        ])
        
        # Super quick parallel processing
        self.play(Write(all_thinking_dots), run_time=0.2)
        self.wait(0.1)

        # Fast completion
        completions = VGroup(*[
            Text("✓", color=SUCCESS_GREEN, font="SF Pro Display").scale(0.8).next_to(task, RIGHT)
            for task in tasks
        ])
        
        self.play(
            FadeOut(all_thinking_dots),
            Write(completions),
            run_time=0.3
        )

        # Quick time display
        bhumi_time = Text("Total Time: 0.5s", color=CORAL_RED, font="SF Pro Display").scale(0.6)
        bhumi_time.next_to(pipeline, DOWN)
        self.play(Write(bhumi_time), run_time=0.3)

        # Snappy benefits display
        benefits = VGroup(
            Text("5x Faster Processing", color=CORAL_RED, font="SF Pro Display").scale(0.5),
            Text("Immediate Response", color=CORAL_RED, font="SF Pro Display").scale(0.5),
            Text("Optimized for Agents", color=CORAL_RED, font="SF Pro Display").scale(0.5)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        benefits.to_edge(DOWN)

        self.play(Write(benefits), run_time=0.5)

        # Quick final message
        final_msg = Text(
            "Bhumi: Accelerating AI Workflows",
            gradient=(BUFFER_BLUE, CORAL_RED),
            font="SF Pro Display"
        ).scale(0.7)
        final_msg.to_edge(DOWN)

        self.play(
            FadeOut(benefits),
            Write(final_msg),
            run_time=0.5
        )
        self.wait(0.5)

        # Fast cleanup
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.3)

if __name__ == "__main__":
    # Configure for high quality
    config.pixel_height = 1440  # 2K resolution
    config.pixel_width = 2560
    config.frame_rate = 60  # Higher frame rate
    
    with tempconfig({
        "quality": "production_quality",
        "preview": True,
        "disable_caching": True,  # For faster development
        "renderer": "opengl"  # Hardware acceleration
    }):
        scene = LatencyImpactDemo()
        scene.render() 