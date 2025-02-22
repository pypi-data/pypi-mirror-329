from manim import *

class StreamingConcurrencyDemo(Scene):
    def clear_scene(self):
        """Helper to clear current scene"""
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.3)

    def construct(self):
        # Setup
        self.camera.background_color = "#111111"
        CORAL_RED = "#FF6F61"
        BUFFER_BLUE = "#1E90FF"
        RUST_COLOR = "#DEA584"
        
        # Use a more common font
        FONT = "Arial" # or "Helvetica" or None for default
        
        # Slide 1: Introduction
        title = Text("Bhumi: Streaming Architecture", 
                    color=CORAL_RED, font=FONT).scale(1.2)
        subtitle = Text("Accelerating LLM Inference", 
                       color=WHITE, font=FONT).scale(0.6)
        VGroup(title, subtitle).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        
        self.play(Write(title), run_time=0.5)
        self.play(FadeIn(subtitle), run_time=0.3)
        self.wait(0.5)
        self.clear_scene()

        # Slide 2: System Components
        components_title = Text("System Architecture", 
                              color=CORAL_RED, font=FONT).scale(0.8)
        components_title.to_edge(UP)
        self.play(Write(components_title))

        # Create and position components
        def create_server(name, color):
            return VGroup(
                Rectangle(height=2, width=1.5, color=color, fill_opacity=0.1),
                Text(name, font=FONT, color=color).scale(0.4)
            ).arrange(DOWN, buff=0.1)

        llm = create_server("LLM Server", WHITE)
        bhumi = create_server("Bhumi\nRust Workers", RUST_COLOR)
        client = create_server("Client", WHITE)
        
        components = VGroup(llm, bhumi, client).arrange(RIGHT, buff=4)
        components.next_to(components_title, DOWN, buff=1)
        
        self.play(Create(components))

        # Create and show workers
        workers = VGroup(*[
            Rectangle(height=0.3, width=1.2, color=CORAL_RED, fill_opacity=0.2)
            for _ in range(4)
        ]).arrange(DOWN, buff=0.1)
        workers.move_to(bhumi)
        
        worker_labels = VGroup(*[
            Text(f"Worker {i}", color=CORAL_RED, font=FONT).scale(0.25)
            .move_to(worker)
            for i, worker in enumerate(workers)
        ])

        self.play(Create(workers), Write(worker_labels))
        self.wait(0.5)
        self.clear_scene()

        # Slide 3: Traditional Approach
        trad_title = Text("Traditional Approach: Batch Processing", 
                         color=BUFFER_BLUE, font=FONT).scale(0.8)
        trad_title.to_edge(UP)
        self.play(Write(trad_title))

        # Recreate minimal components for traditional flow
        components_simple = VGroup(
            llm.copy(), client.copy()
        ).arrange(RIGHT, buff=6)
        components_simple.next_to(trad_title, DOWN, buff=1)
        self.play(Create(components_simple))

        def create_chunk(text, color):
            return VGroup(
                Rectangle(height=0.3, width=0.8, color=color, fill_opacity=0.2),
                Text(text, color=color, font=FONT).scale(0.25)
            ).arrange(buff=0.1)

        # Show traditional batch processing
        chunks = VGroup(*[
            create_chunk(f"Chunk {i}", BUFFER_BLUE)
            for i in range(5)
        ]).arrange(RIGHT, buff=0.1)
        chunks.next_to(components_simple[0], RIGHT, buff=1)

        for chunk in chunks:
            self.play(Create(chunk), run_time=0.2)
        self.wait(0.3)
        
        self.play(
            chunks.animate.next_to(components_simple[1], LEFT, buff=1),
            run_time=0.5
        )
        self.wait(0.3)
        self.clear_scene()

        # Slide 4: Bhumi Approach
        bhumi_title = Text("Bhumi: Concurrent Streaming", 
                          color=CORAL_RED, font=FONT).scale(0.8)
        bhumi_title.to_edge(UP)
        self.play(Write(bhumi_title))

        # Recreate components with workers
        components_full = VGroup(llm.copy(), bhumi.copy(), client.copy())
        components_full.arrange(RIGHT, buff=4)
        components_full.next_to(bhumi_title, DOWN, buff=1)
        
        workers_copy = workers.copy()
        workers_copy.move_to(components_full[1])
        worker_labels_copy = worker_labels.copy()
        worker_labels_copy.move_to(components_full[1])
        
        self.play(
            Create(components_full),
            Create(workers_copy),
            Write(worker_labels_copy)
        )

        # Show streaming process
        for i in range(5):
            # Create chunk
            chunk = create_chunk(f"Chunk {i}", CORAL_RED)
            chunk.next_to(components_full[0], RIGHT, buff=1)
            self.play(Create(chunk), run_time=0.15)
            
            # Process through worker
            worker = workers_copy[i % len(workers_copy)]
            self.play(
                chunk.animate.move_to(worker),
                worker.animate.set_fill(opacity=0.4),
                run_time=0.15
            )
            
            # Send to client and cleanup
            self.play(
                chunk.animate.next_to(components_full[2], LEFT, buff=1),
                worker.animate.set_fill(opacity=0.2),
                run_time=0.15
            )
            self.play(FadeOut(chunk), run_time=0.1)

        # Slide 5: Benefits
        benefits_title = Text("Performance Benefits", 
                            color=CORAL_RED, font=FONT).scale(0.8)
        benefits = VGroup(
            Text("• 5x Faster TTFT", color=CORAL_RED, font=FONT).scale(0.6),
            Text("• 2x Higher Throughput", color=CORAL_RED, font=FONT).scale(0.6),
            Text("• Immediate Chunk Delivery", color=CORAL_RED, font=FONT).scale(0.6),
            Text("• Optimized Memory Usage", color=CORAL_RED, font=FONT).scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        final_group = VGroup(benefits_title, benefits).arrange(DOWN, buff=0.5)
        final_group.move_to(ORIGIN)
        
        self.play(
            FadeOut(components_full),
            FadeOut(workers_copy),
            FadeOut(worker_labels_copy),
            FadeOut(bhumi_title),
            run_time=0.3
        )
        self.play(Write(final_group), run_time=0.8)
        self.wait(0.5)

if __name__ == "__main__":
    config.pixel_height = 1440
    config.pixel_width = 2560
    config.frame_rate = 60
    
    with tempconfig({
        "quality": "production_quality",
        "preview": True,
        "disable_caching": True,
        "renderer": "opengl"
    }):
        scene = StreamingConcurrencyDemo()
        scene.render() 