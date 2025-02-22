from manim import *

class BufferComparison(Scene):
    def construct(self):
        # Colors
        CORAL_RED = "#FF6F61"
        BUFFER_BLUE = "#1E90FF"
        
        # Create title
        title = Text("Bhumi: Accelerated LLM Inference", color=CORAL_RED)
        title.to_edge(UP)
        self.play(Write(title))

        # Create system diagram
        # Server cluster (multiple LLM servers)
        server_cluster = VGroup()
        for i in range(3):
            server = VGroup(
                Rectangle(height=2, width=1.5),
                Text("LLM Server").scale(0.4),
                *[Rectangle(height=0.2, width=1, fill_opacity=1, color=GRAY).scale(0.8)
                  for _ in range(2)],
                Text("H100s", color=WHITE).scale(0.3)
            ).arrange(DOWN, buff=0.1)
            server_cluster.add(server)
        server_cluster.arrange(RIGHT, buff=0.3).shift(LEFT * 5)
        
        # Endpoint (e.g. API Gateway)
        endpoint = VGroup(
            Rectangle(height=1.5, width=2),
            Text("API Endpoint").scale(0.5)
        ).shift(RIGHT * 5)

        # Traditional vs Bhumi paths
        traditional_path = VGroup(
            Rectangle(height=1.2, width=6, color=BUFFER_BLUE).set_opacity(0.2),
            Text("Traditional Pipeline", color=BUFFER_BLUE).scale(0.6)
        ).shift(UP * 1.5)
        
        bhumi_path = VGroup(
            Rectangle(height=1.2, width=6, color=CORAL_RED).set_opacity(0.2),
            Text("Bhumi Pipeline", color=CORAL_RED).scale(0.6)
        ).shift(DOWN * 1.5)

        # Add buffer visualizations
        trad_buffer = VGroup(
            DashedVMobject(Rectangle(height=0.8, width=1.5, color=BUFFER_BLUE)),
            Text("Fixed Buffer", color=BUFFER_BLUE).scale(0.4)
        ).move_to(traditional_path)

        bhumi_buffer = VGroup(
            DashedVMobject(Rectangle(height=0.8, width=1.5, color=CORAL_RED)),
            Text("Dynamic Buffer", color=CORAL_RED).scale(0.4)
        ).move_to(bhumi_path)

        # Show system setup
        self.play(
            Create(server_cluster),
            Create(endpoint),
            Create(traditional_path),
            Create(bhumi_path),
            Create(trad_buffer),
            Create(bhumi_buffer)
        )
        self.wait()

        # Packet generation and flow
        def create_packet_stream(color, count, start_points):
            return VGroup(*[
                Dot(color=color, radius=0.08)
                .move_to(start_points[i % len(start_points)])
                for i in range(count)
            ])

        # Create packets for both paths
        server_points = [server.get_right() for server in server_cluster]
        traditional_packets = create_packet_stream(BUFFER_BLUE, 15, server_points)
        bhumi_packets = create_packet_stream(CORAL_RED, 15, server_points)

        # Animate traditional flow
        self.play(Write(Text("Traditional Flow", color=BUFFER_BLUE).scale(0.6).to_edge(UP + RIGHT)))
        
        buffer_point = trad_buffer.get_center()
        for i, packet in enumerate(traditional_packets):
            # Move to buffer
            self.play(
                packet.animate.move_to(buffer_point),
                run_time=0.3
            )
            if i < 10:  # Wait for buffer to fill
                self.wait(0.1)
            
        # Send batch to endpoint
        self.play(
            *[packet.animate.move_to(endpoint.get_left())
              for packet in traditional_packets],
            run_time=1
        )
        self.wait()

        # Clear traditional packets
        self.play(FadeOut(traditional_packets))
        
        # Dynamic buffer animation for Bhumi
        buffer_animations = []
        for w in [1.2, 2, 1.5, 1.8]:
            new_buffer = DashedVMobject(
                Rectangle(height=0.8, width=w, color=CORAL_RED)
            ).move_to(bhumi_buffer)
            buffer_animations.append(Transform(bhumi_buffer[0], new_buffer))

        # Animate Bhumi flow
        self.play(Write(Text("Bhumi Flow", color=CORAL_RED).scale(0.6).to_edge(UP + RIGHT)))
        
        # Parallel animations for dynamic buffer and packet flow
        for i, packet in enumerate(bhumi_packets):
            # Faster packet movement
            self.play(
                packet.animate.move_to(bhumi_buffer.get_center()),
                run_time=0.15
            )
            self.play(
                packet.animate.move_to(endpoint.get_left()),
                run_time=0.15
            )
            
            # Occasionally adjust buffer size
            if i % 4 == 0:
                self.play(buffer_animations[i // 4], run_time=0.3)

        # Show performance comparison
        metrics = VGroup(
            Text("Traditional TTFT: ~2.5s", color=BUFFER_BLUE).scale(0.5),
            Text("Bhumi TTFT: ~0.5s", color=CORAL_RED).scale(0.5),
            Text("5x Faster First Token", color=CORAL_RED).scale(0.6)
        ).arrange(DOWN, buff=0.3)
        metrics.to_edge(DOWN)
        
        self.play(Write(metrics))
        self.wait(2)

        # Add final explanation
        explanation = Text(
            "Bhumi's dynamic buffer sizing + Rust concurrency\n"
            "optimizes token delivery while maintaining throughput",
            color=WHITE
        ).scale(0.4)
        explanation.next_to(metrics, UP)
        self.play(Write(explanation))
        self.wait(2)

        # Cleanup
        self.play(*[FadeOut(mob) for mob in self.mobjects])

if __name__ == "__main__":
    with tempconfig({"quality": "high_quality", "preview": True}):
        scene = BufferComparison()
        scene.render() 