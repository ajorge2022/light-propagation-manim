"""FIGURE 03 — REFRACTION AND SNELL'S LAW

Animated interpretation of Figure 3 (p. 3) of
'Light Propagation for Undergraduates' by A. W. Romero Jorge et al.

Manim Community Edition 0.19+ (Python syntax checked).

Render:
    manim -pqh figura_03_manim.py Figura03Refraccion

The figure depicts an ideal planar, stationary interface between two
transparent, homogeneous, isotropic, nonmagnetic media, with n1=1.0
(air) and n2=1.5 (glass). Angles are measured from the normal:

    n1 sin(theta_i) = n2 sin(theta_t).

The incident ray bends toward the normal in the denser medium;
its wavelength becomes shorter, while its frequency is unchanged.
Only the incident and refracted rays are shown, as in the original
Figure 3. The small reflection at a real interface is not drawn.
"""

from manim import *
import numpy as np

BG = "#0C1524"
PANEL = "#122236"
BORDER = "#2A4058"
WHITE_SOFT = "#F0F7FF"
DIM = "#A2B3C7"
CYAN = "#58DDF7"       # incident wave
GOLD = "#FFC478"       # transmitted wave
MINT = "#61E8B0"       # incidence angle
PURPLE = "#8795E5"


class Figura03Refraccion(Scene):
    """Figure 3: incident and transmitted rays obey Snell's law."""

    def construct(self):
        self.camera.background_color = BG

        n1, n2 = 1.00, 1.50
        theta_i = ValueTracker(45 * DEGREES)
        incoming_progress = ValueTracker(0.0)
        outgoing_progress = ValueTracker(0.0)
        clock = ValueTracker(0.0)
        P = np.array([-0.25, -0.09, 0.0])   # point at the interface
        ray_length = 2.07

        def theta_t():
            """Transmitted angle, always measured from the downward normal."""
            s = (n1 / n2) * np.sin(theta_i.get_value())
            return float(np.arcsin(np.clip(s, -1.0, 1.0)))

        def incident_dir():
            a = theta_i.get_value()
            return np.array([-np.sin(a), np.cos(a), 0.0])

        def refracted_dir():
            a = theta_t()
            return np.array([np.sin(a), -np.cos(a), 0.0])

        def source():
            return P + ray_length * incident_dir()

        def target():
            return P + ray_length * refracted_dir()

        # Layout and headings, matching the preceding Figure 2 animation.
        header = Text(
            "FIGURE 03   /   CLASSICAL WAVE OPTICS",
            font="Lato", font_size=19, color=GOLD,
        ).to_corner(UL, buff=0.5)
        title = Text(
            "REFRACTION & SNELL'S LAW",
            font="Lato", font_size=34, weight=BOLD, color=WHITE_SOFT,
        ).next_to(header, DOWN, aligned_edge=LEFT, buff=0.13)
        subtitle = Text(
            "Light changes direction when its phase velocity changes across an interface.",
            font="Lato", font_size=18, color=DIM,
        ).next_to(title, DOWN, aligned_edge=LEFT, buff=0.10)
        divider = Line(
            [-6.56, 2.14, 0], [6.56, 2.14, 0],
            color=BORDER, stroke_width=1.4,
        )
        stage = RoundedRectangle(
            width=13.15, height=4.08, corner_radius=0.16,
            stroke_color=BORDER, stroke_width=1.3,
            fill_color=PANEL, fill_opacity=1,
        ).move_to([0, -0.09, 0])
        footer = RoundedRectangle(
            width=13.15, height=1.28, corner_radius=0.16,
            stroke_color=BORDER, stroke_width=1.3,
            fill_color=PANEL, fill_opacity=1,
        ).move_to([0, -3.03, 0])

        # Two macroscopic media on either side of a planar interface.
        # Their visual transparency has no physical significance.
        upper = Rectangle(
            width=12.84, height=2.00,
            stroke_width=0, fill_color="#19324D", fill_opacity=0.52,
        ).move_to([0, 0.91, 0])
        lower = Rectangle(
            width=12.84, height=2.02,
            stroke_width=0, fill_color="#263C61", fill_opacity=0.66,
        ).move_to([0, -1.10, 0])
        interface = Line(
            [-6.36, P[1], 0], [6.36, P[1], 0],
            stroke_width=3.2, color=PURPLE,
        )
        normal = DashedLine(
            P + 1.86 * UP, P + 1.87 * DOWN,
            dash_length=0.15, dashed_ratio=0.58,
            stroke_width=2.0, color=WHITE_SOFT,
        )
        normal_label = Text(
            "NORMAL", font="Lato", font_size=16, color=DIM,
        ).move_to(P + [0.67, 1.72, 0])
        hit = Dot(P, radius=0.075, color=WHITE_SOFT)

        medium_1 = VGroup(
            Text("MEDIUM 1  /  AIR", font="Lato", font_size=19, color=WHITE_SOFT),
            MathTex(r"n_1=1.00", font_size=29, color=CYAN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10).move_to([4.36, 1.12, 0])
        medium_2 = VGroup(
            Text("MEDIUM 2  /  GLASS", font="Lato", font_size=19, color=WHITE_SOFT),
            MathTex(r"n_2=1.50", font_size=29, color=GOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10).move_to([4.36, -1.37, 0])

        ray_in_label = Text(
            "INCIDENT RAY", font="Lato", font_size=17, color=CYAN,
        ).move_to([-3.72, 1.19, 0])
        ray_out_label = Text(
            "REFRACTED RAY", font="Lato", font_size=17, color=GOLD,
        ).move_to([2.66, -1.90, 0])

        def ray_arrow(start, end, progress, color):
            t = float(np.clip(progress.get_value(), 0.035, 1.0))
            return Arrow(
                start, start + t * (end - start),
                buff=0, stroke_width=5.0, color=color,
                max_tip_length_to_length_ratio=0.16,
                max_stroke_width_to_length_ratio=8,
            )

        incident_ray = always_redraw(
            lambda: ray_arrow(source(), P, incoming_progress, CYAN)
        )
        transmitted_ray = always_redraw(
            lambda: ray_arrow(P, target(), outgoing_progress, GOLD)
        )

        def angle_sector(start_angle, extent, color):
            """A shaded wedge plus an arc, avoiding Angle quadrant ambiguity."""
            radius = 0.77
            angles = np.linspace(start_angle, start_angle + extent, 26)
            points = [P] + [
                P + radius * np.array([np.cos(a), np.sin(a), 0.0])
                for a in angles
            ]
            wedge = Polygon(
                *points, stroke_width=0,
                fill_color=color, fill_opacity=0.19,
            )
            arc = Arc(
                radius=radius, start_angle=start_angle,
                angle=extent, arc_center=P, color=color, stroke_width=2.9,
            )
            return VGroup(wedge, arc)

        incident_sector = always_redraw(
            lambda: angle_sector(PI / 2, theta_i.get_value(), MINT)
        )
        refracted_sector = always_redraw(
            lambda: angle_sector(-PI / 2, theta_t(), GOLD)
        )

        # Create mathematical labels only once and move them with updaters.
        label_theta_i = MathTex(r"\theta_i", font_size=34, color=MINT)
        label_theta_t = MathTex(r"\theta_t", font_size=34, color=GOLD)

        def move_incident_label(mob):
            a = PI / 2 + theta_i.get_value() / 2
            mob.move_to(P + 1.17 * np.array([np.cos(a), np.sin(a), 0]))

        def move_transmitted_label(mob):
            a = -PI / 2 + theta_t() / 2
            mob.move_to(P + 1.16 * np.array([np.cos(a), np.sin(a), 0]))

        label_theta_i.add_updater(move_incident_label)
        label_theta_t.add_updater(move_transmitted_label)

        def wavefront_marks(is_incident):
            """Wavefront markers: lambda_2/lambda_1 = n1/n2 at fixed frequency.

            Marks are normal to the ray and move at relative phase speed 1/n.
            They are schematic and do not represent a wave-amplitude solver.
            """
            n = n1 if is_incident else n2
            direction = incident_dir() if is_incident else refracted_dir()
            spacing = 0.62 / n
            v = 1.0 / n
            travel_sign = -1 if is_incident else +1
            marks = VGroup()
            perpendicular = np.array([-direction[1], direction[0], 0.0])
            for j in range(-10, 20):
                distance = j * spacing + travel_sign * v * clock.get_value()
                if 0.20 <= distance <= ray_length - 0.14:
                    center = P + distance * direction
                    marks.add(Line(
                        center - 0.145 * perpendicular,
                        center + 0.145 * perpendicular,
                        stroke_width=2.0,
                        color=CYAN if is_incident else GOLD,
                        stroke_opacity=0.78,
                    ))
            return marks

        wave_in = always_redraw(lambda: wavefront_marks(True))
        wave_out = always_redraw(lambda: wavefront_marks(False))

        # Footer: Snell equation and live numerical angles, in degrees.
        eq = MathTex(
            r"n_1\sin\theta_i=n_2\sin\theta_t",
            font_size=43, color=WHITE_SOFT,
        ).move_to([-3.23, -2.91, 0])
        live_i_label = MathTex(
            r"\theta_i=", font_size=31, color=MINT,
        ).move_to([0.85, -2.83, 0])
        live_t_label = MathTex(
            r"\theta_t=", font_size=31, color=GOLD,
        ).move_to([3.73, -2.83, 0])
        live_i_value = always_redraw(
            lambda: DecimalNumber(
                theta_i.get_value() / DEGREES,
                num_decimal_places=1, font_size=31, color=WHITE_SOFT,
            ).move_to([2.01, -2.83, 0])
        )
        live_t_value = always_redraw(
            lambda: DecimalNumber(
                theta_t() / DEGREES,
                num_decimal_places=1, font_size=31, color=WHITE_SOFT,
            ).move_to([4.95, -2.83, 0])
        )
        degree_i = MathTex(r"{}^\circ", font_size=23, color=DIM).move_to([2.47, -2.72, 0])
        degree_t = MathTex(r"{}^\circ", font_size=23, color=DIM).move_to([5.41, -2.72, 0])
        note = Text(
            "n2 > n1  :  the refracted ray bends toward the normal",
            font="Lato", font_size=16, color=DIM,
        ).move_to([2.98, -3.38, 0])

        # --------------------------------------------------------------
        # The animation (approximately 15 seconds)
        # --------------------------------------------------------------
        self.play(
            FadeIn(stage), FadeIn(footer),
            FadeIn(header, shift=UP * .12), Write(title),
            FadeIn(subtitle), Create(divider), run_time=1.5,
        )
        self.play(
            FadeIn(upper), FadeIn(lower), Create(interface),
            Create(normal), FadeIn(normal_label),
            FadeIn(medium_1), FadeIn(medium_2),
            FadeIn(hit), run_time=1.4,
        )

        # Draw incoming ray first, followed by the transmitted ray.
        self.add(incident_ray)
        self.play(
            incoming_progress.animate.set_value(1.0),
            FadeIn(ray_in_label), run_time=1.4, rate_func=linear,
        )
        self.add(transmitted_ray)
        self.play(
            outgoing_progress.animate.set_value(1.0),
            FadeIn(ray_out_label), run_time=1.3, rate_func=linear,
        )
        self.play(
            FadeIn(incident_sector), FadeIn(refracted_sector),
            FadeIn(label_theta_i), FadeIn(label_theta_t),
            Write(eq), FadeIn(live_i_label), FadeIn(live_t_label),
            FadeIn(live_i_value), FadeIn(live_t_value),
            FadeIn(degree_i), FadeIn(degree_t), FadeIn(note),
            run_time=1.4,
        )

        self.add(wave_in, wave_out)
        self.play(
            theta_i.animate.set_value(65 * DEGREES),
            clock.animate.set_value(2.8),
            run_time=2.4, rate_func=smooth,
        )
        self.play(
            theta_i.animate.set_value(20 * DEGREES),
            clock.animate.set_value(6.4),
            run_time=2.9, rate_func=smooth,
        )
        self.play(
            theta_i.animate.set_value(45 * DEGREES),
            clock.animate.set_value(9.4),
            run_time=2.4, rate_func=smooth,
        )
        self.wait(1.0)
