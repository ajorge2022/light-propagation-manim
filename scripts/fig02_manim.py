"""FIGURE 02 -- LAW OF REFLECTION

Faithful animated treatment of Figure 2 in
'Light Propagation for Undergraduates' (A. W. Romero Jorge et al.).

Manim Community Edition (tested for Python syntax, intended for v0.19+).
Render in HD:
    manim -pqh figura_02_manim.py Figura02Reflexion
Render quickly:
    manim -pql figura_02_manim.py Figura02Reflexion

Physics:
    theta_incident = theta_reflected, both measured from the surface normal.
    An ideal flat mirror and specular reflection are assumed.

The supplementary MP4 preview uses a separate OpenCV renderer because the
Manim package was unavailable in the authoring environment.
"""

from manim import *
import numpy as np

# Palette shared with Fig. 01
BG = "#0C1524"
PANEL = "#122236"
BORDER = "#2A4058"
WHITE = "#F0F7FF"
DIM = "#A2B3C7"
CYAN = "#58DDF7"
GOLD = "#FFC478"
MINT = "#61E8B0"
PURPLE = "#8795E5"


class Figura02Reflexion(Scene):
    """Animate the incidence angle and the specularly reflected ray."""

    def construct(self):
        self.camera.background_color = BG
        theta = ValueTracker(40 * DEGREES)
        phase = ValueTracker(0.0)
        incoming_progress = ValueTracker(0.0)
        outgoing_progress = ValueTracker(0.0)

        # Consistent 16:9 composition; scene coordinates assume 14.22 x 8.
        hit = np.array([0.0, -1.08, 0.0])
        ray_height = 2.30
        mirror_y = hit[1] - 0.12

        def endpoints():
            """The normal is vertical; theta is measured from this normal."""
            a = theta.get_value()
            lateral = ray_height * np.tan(a)
            source = hit + np.array([-lateral, ray_height, 0.0])
            target = hit + np.array([lateral, ray_height, 0.0])
            return source, target

        header = Text(
            "FIGURE 02   /   CLASSICAL WAVE OPTICS",
            font="Lato", font_size=19, color=GOLD,
        ).to_corner(UL, buff=0.5)
        title = Text(
            "LAW OF REFLECTION", font="Lato", font_size=34,
            weight=BOLD, color=WHITE,
        ).next_to(header, DOWN, aligned_edge=LEFT, buff=0.13)
        subtitle = Text(
            "The incident and reflected rays make equal angles with the normal.",
            font="Lato", font_size=19, color=DIM,
        ).next_to(title, DOWN, aligned_edge=LEFT, buff=0.10)
        divider = Line(
            [-6.56, 2.14, 0], [6.56, 2.14, 0],
            color=BORDER, stroke_width=1.4,
        )
        stage = RoundedRectangle(
            width=13.15, height=4.05, corner_radius=0.16,
            stroke_color=BORDER, stroke_width=1.3,
            fill_color=PANEL, fill_opacity=1,
        ).move_to([0, 0.03, 0])
        footer = RoundedRectangle(
            width=13.15, height=1.28, corner_radius=0.16,
            stroke_color=BORDER, stroke_width=1.3,
            fill_color=PANEL, fill_opacity=1,
        ).move_to([0, -3.00, 0])

        mirror_shadow = Rectangle(
            width=11.9, height=0.17,
            stroke_width=0, fill_color="#090F1C", fill_opacity=.55,
        ).move_to([0, mirror_y - .07, 0])
        mirror = Rectangle(
            width=11.9, height=0.20,
            stroke_width=1.2, stroke_color=PURPLE,
            fill_color="#435379", fill_opacity=1,
        ).move_to([0, mirror_y, 0])
        mirror_top = Line(
            [-5.94, hit[1], 0], [5.94, hit[1], 0],
            stroke_width=3.5, color="#A5B7EF",
        )
        mirror_label = Text(
            "MIRROR", font="Lato", font_size=17,
            color=DIM,
        ).move_to([0, -1.60, 0])
        normal = DashedLine(
            hit, hit + UP * 2.90,
            dash_length=.15, dashed_ratio=.57,
            color=WHITE, stroke_width=2.0,
        )
        normal_label = Text(
            "NORMAL", font="Lato", font_size=17, color=DIM,
        ).move_to([0.0, 1.72, 0])
        incidence = Dot(point=hit, radius=.078, color=WHITE)

        def vector_ray(direction, progress):
            """Extend the incident or reflected ray during its entrance."""
            source, target = endpoints()
            if direction == "incoming":
                start, end = source, hit
            else:
                start, end = hit, target
            p = np.clip(progress.get_value(), .001, 1.0)
            end_now = start + p * (end - start)
            # Use a Line plus explicit tip: stable during continuous redraw.
            shaft = Line(start, end_now, color=CYAN if direction == "incoming" else GOLD,
                         stroke_width=5.0)
            if p >= .12:
                u = (end_now - start) / np.linalg.norm(end_now - start)
                tip = Triangle(
                    color=CYAN if direction == "incoming" else GOLD,
                    fill_opacity=1, stroke_width=0,
                ).scale(.105).rotate(np.arctan2(u[1], u[0]) - PI / 2)
                tip.move_to(end_now - .02*u)
                return VGroup(shaft, tip)
            return VGroup(shaft)

        ray_in = always_redraw(lambda: vector_ray("incoming", incoming_progress))
        ray_out = always_redraw(lambda: vector_ray("outgoing", outgoing_progress))

        def angular_sector(a1, a2, color):
            """Polygon wedge avoids ambiguity about Angle quadrant conventions."""
            angles = np.linspace(a1, a2, 30)
            radius = 1.04
            pts = [hit] + [
                hit + radius * np.array([np.cos(a), np.sin(a), 0])
                for a in angles
            ]
            sector = Polygon(*pts, color=color, stroke_width=0,
                             fill_color=color, fill_opacity=.12)
            arc = Arc(radius=radius, start_angle=a1, angle=a2-a1,
                      arc_center=hit, color=color, stroke_width=2.6)
            return VGroup(sector, arc)

        left_sector = always_redraw(
            lambda: angular_sector(PI/2, PI/2+theta.get_value(), MINT)
        )
        right_sector = always_redraw(
            lambda: angular_sector(PI/2-theta.get_value(), PI/2, GOLD)
        )

        def label_polar(text, sign, color):
            a = PI/2 + sign*theta.get_value()/2
            return MathTex(text, font_size=37, color=color).move_to(
                hit + 1.47*np.array([np.cos(a), np.sin(a), 0])
            )

        # Create Tex only once and update its position, avoiding a new SVG per frame.
        theta_i = MathTex(r"\theta_i", font_size=37, color=MINT)
        theta_r = MathTex(r"\theta_r", font_size=37, color=GOLD)
        theta_i.add_updater(lambda m: m.move_to(
            hit + 1.47*np.array([
                np.cos(PI/2 + theta.get_value()/2),
                np.sin(PI/2 + theta.get_value()/2), 0,
            ])
        ))
        theta_r.add_updater(lambda m: m.move_to(
            hit + 1.47*np.array([
                np.cos(PI/2 - theta.get_value()/2),
                np.sin(PI/2 - theta.get_value()/2), 0,
            ])
        ))

        source_label = Text(
            "INCIDENT RAY", font="Lato", font_size=17, color=CYAN,
        ).move_to([-4.42, 1.64, 0])
        reflected_label = Text(
            "REFLECTED RAY", font="Lato", font_size=17, color=GOLD,
        ).move_to([4.42, 1.64, 0])

        def wavefronts(incoming):
            """Small transverse marks move in the direction of propagation."""
            source, target = endpoints()
            start, end = (source, hit) if incoming else (hit, target)
            u = (end - start) / np.linalg.norm(end - start)
            transverse = np.array([-u[1], u[0], 0.0])
            L = np.linalg.norm(end - start)
            waves = VGroup()
            for i in range(6):
                d = (i * .63 + phase.get_value() * .63) % L
                center = start + d*u
                waves.add(Line(
                    center - .14*transverse, center + .14*transverse,
                    color=CYAN if incoming else GOLD,
                    stroke_width=2.0, stroke_opacity=.75,
                ))
            return waves

        wave_in = always_redraw(lambda: wavefronts(True))
        wave_out = always_redraw(lambda: wavefronts(False))

        equation = MathTex(r"\boxed{\theta_i = \theta_r}",
                           font_size=52, color=WHITE).move_to([-3.45, -3.00, 0])
        left_live = MathTex(r"\theta_i=", font_size=33,
                            color=MINT).move_to([.96, -2.80, 0])
        right_live = MathTex(r"\theta_r=", font_size=33,
                             color=GOLD).move_to([3.97, -2.80, 0])
        val_i = always_redraw(lambda: DecimalNumber(
            theta.get_value() / DEGREES, num_decimal_places=0,
            font_size=36, color=WHITE,
        ).move_to([2.10, -2.80, 0]))
        val_r = always_redraw(lambda: DecimalNumber(
            theta.get_value() / DEGREES, num_decimal_places=0,
            font_size=36, color=WHITE,
        ).move_to([5.10, -2.80, 0]))
        degree_i = MathTex(r"{}^\circ", color=DIM, font_size=28).move_to([2.45, -2.70, 0])
        degree_r = MathTex(r"{}^\circ", color=DIM, font_size=28).move_to([5.45, -2.70, 0])
        footer_note = Text("Angles are measured from the surface normal.",
                           font="Lato", font_size=15,
                           color=DIM).move_to([3.02, -3.30, 0])

        self.play(FadeIn(stage), FadeIn(footer),
                  FadeIn(header, shift=UP*.12), Write(title),
                  FadeIn(subtitle), Create(divider), run_time=1.6)
        self.play(FadeIn(mirror_shadow), FadeIn(mirror),
                  Create(mirror_top), FadeIn(mirror_label),
                  Create(normal), FadeIn(normal_label),
                  FadeIn(incidence), run_time=1.2)
        self.add(ray_in)
        self.play(incoming_progress.animate.set_value(1),
                  FadeIn(source_label), run_time=1.6, rate_func=linear)
        self.add(ray_out)
        self.play(outgoing_progress.animate.set_value(1),
                  FadeIn(reflected_label), run_time=1.5, rate_func=linear)
        # Only reveal the sectors once both rays are established.
        self.play(FadeIn(left_sector), FadeIn(right_sector),
                  FadeIn(theta_i), FadeIn(theta_r),
                  FadeIn(equation), run_time=1.2)
        self.add(wave_in, wave_out)
        self.play(FadeIn(left_live), FadeIn(right_live),
                  FadeIn(val_i), FadeIn(val_r),
                  FadeIn(degree_i), FadeIn(degree_r),
                  FadeIn(footer_note), run_time=.7)
        # Three continuously varying angles: both rays obey the same theta.
        self.play(theta.animate.set_value(62*DEGREES),
                  phase.animate.set_value(3.0), run_time=2.6,
                  rate_func=smooth)
        self.play(theta.animate.set_value(23*DEGREES),
                  phase.animate.set_value(7.5), run_time=3.1,
                  rate_func=smooth)
        self.play(theta.animate.set_value(45*DEGREES),
                  phase.animate.set_value(10.5), run_time=2.5,
                  rate_func=smooth)
        self.wait(1.2)
