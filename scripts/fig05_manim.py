"""FIGURE 05 — LINEAR POLARIZATION AND MALUS'S LAW

Manim Community Edition (v0.19+). Based on Figure 5 and Section 3.4 in
"Light Propagation for Undergraduates" (A. W. Romero Jorge et al.).

The original Figure 5 shows UNPOLARIZED light becoming LINEARLY POLARIZED
when it crosses a single ideal polarizer. This animation includes that
step first, then *extends* the figure with a rotating second polarizer
(analyzer) to illustrate Malus's law correctly.

Render, Full HD / 60 fps:
    manim -pqh figura_05_manim.py Figura05PolarizacionMalus
Render, fast preview:
    manim -pql figura_05_manim.py Figura05PolarizacionMalus

PHYSICS
  • Unpolarized -> ideal linear polarizer: I_1 = I_0 / 2 (time average).
  • A second ideal polarizer at angle theta relative to the first:
            E_2 = E_1 cos(theta)    (field amplitude projection)
            I_2 = I_1 cos^2(theta) (time-averaged intensity)
    Angles are 0..90 degrees; theta=90 degrees gives crossed polarizers.
  • The vector fan represents ensemble polarization orientations, not
    simultaneous classical vectors of a single monochromatic beam.
  • Drawings are schematic. No finite extinction ratio, absorption,
    interface reflection or partial-polarization/Stokes effects included.

All headings in English to match the manuscript. The broad 16:9 layout and
colors follow the earlier Figure 02/04 animations.
"""

from manim import *
import numpy as np

BG = "#0C1524"
PANEL = "#122236"
BORDER = "#2A4058"
WHITE_SOFT = "#F0F7FF"
DIM = "#A2B3C7"
CYAN = "#58DDF7"
GOLD = "#FFC478"
MINT = "#61E8B0"
PURPLE = "#8795E5"
PINK = "#FF818F"


class Figura05PolarizacionMalus(Scene):
    """First polarizer: I1=I0/2; rotating analyzer: I2/I1=cos²(theta)."""

    def construct(self):
        self.camera.background_color = BG
        theta = ValueTracker(0.0)  # RADIANS, angle measured from vertical

        # ── Reusable layout: figure header, large stage and formula footer.
        header = Text(
            "FIGURE 05   /   CLASSICAL WAVE OPTICS",
            font="Lato", font_size=19, color=GOLD,
        ).to_corner(UL, buff=0.50)
        title = Text(
            "LINEAR POLARIZATION AND MALUS'S LAW",
            font="Lato", font_size=32, weight=BOLD, color=WHITE_SOFT,
        ).next_to(header, DOWN, aligned_edge=LEFT, buff=0.13)
        subtitle = Text(
            "An ideal polarizer selects one electric-field component.",
            font="Lato", font_size=19, color=DIM,
        ).next_to(title, DOWN, aligned_edge=LEFT, buff=0.11)
        divider = Line(
            [-6.56, 2.14, 0], [6.56, 2.14, 0],
            color=BORDER, stroke_width=1.4,
        )
        stage = RoundedRectangle(
            width=13.15, height=4.08, corner_radius=0.16,
            stroke_color=BORDER, stroke_width=1.3,
            fill_color=PANEL, fill_opacity=1.0,
        ).move_to([0, -0.06, 0])
        footer = RoundedRectangle(
            width=13.15, height=1.26, corner_radius=0.16,
            stroke_color=BORDER, stroke_width=1.3,
            fill_color=PANEL, fill_opacity=1.0,
        ).move_to([0, -3.03, 0])

        # Positions in Manim units; the diagram is schematic, not a 3-D ray trace.
        center_y = -0.13
        source_xy = np.array([-5.20, center_y, 0.0])
        analyzer_xy = np.array([0.05, center_y, 0.0])

        # ── Source: a fan of many orientations as a visual shorthand for
        #    polarization-averaged, unpolarized illumination.
        polarization_fan = VGroup()
        for j in range(12):
            a = j * TAU / 12
            u = np.array([np.cos(a), np.sin(a), 0.0])
            polarization_fan.add(
                Arrow(
                    source_xy + 0.09 * u,
                    source_xy + 0.59 * u,
                    buff=0, tip_length=0.11, stroke_width=2.8,
                    color=[CYAN, MINT, PURPLE, PINK][j % 4],
                )
            )
        source_center = Dot(source_xy, radius=0.07, color=WHITE_SOFT)
        source_label = Text(
            "UNPOLARIZED", font="Lato", font_size=17,
            color=WHITE_SOFT,
        ).move_to([-5.20, 1.53, 0])
        source_hint = Text(
            "mixed orientations", font="Lato", font_size=14,
            color=DIM,
        ).move_to([-5.20, -1.52, 0])

        # Source beam/propagation reference line (indicates light traveling
        # left -> right, not a time-varying electric field component).
        incoming_path = Line(
            [-4.50, center_y, 0], [-3.48, center_y, 0],
            color=CYAN, stroke_width=4,
        )
        first_plate = RoundedRectangle(
            width=0.28, height=2.38, corner_radius=0.08,
            stroke_color=PURPLE, stroke_width=2,
            fill_color="#5268A1", fill_opacity=0.65,
        ).move_to([-3.33, center_y, 0])
        first_plate_axis = Line(
            [-3.33, center_y - .88, 0], [-3.33, center_y + .88, 0],
            color=GOLD, stroke_width=4,
        )
        first_plate_label = Text(
            "POLARIZER 1", font="Lato", font_size=16,
            color=WHITE_SOFT,
        ).move_to([-3.63, 1.53, 0])

        intermediate_beam = Line(
            [-3.14, center_y, 0], [-0.92, center_y, 0],
            color=CYAN, stroke_width=4.2,
        )
        polarized_vectors = VGroup()
        for x in [-2.61, -2.04, -1.47]:
            polarized_vectors.add(
                DoubleArrow(
                    [x, center_y - .55, 0],
                    [x, center_y + .55, 0],
                    buff=0, tip_length=.12, stroke_width=3.4,
                    color=CYAN,
                )
            )
        middle_label = Text(
            "LINEARLY POLARIZED", font="Lato", font_size=15,
            color=CYAN,
        ).move_to([-1.95, 1.53, 0])

        # ── Rotating analyzer shown end-on. Its gold axis is transverse to
        #    the direction of light propagation, as required physically.
        analyzer_disk = Circle(
            radius=0.90, color=PURPLE, stroke_width=2.4,
            fill_color="#5666A6", fill_opacity=0.17,
        ).move_to(analyzer_xy)
        analyzer_label = Text(
            "ROTATING ANALYZER", font="Lato", font_size=15,
            color=WHITE_SOFT,
        ).move_to([0.05, 1.53, 0])
        analyzer_crosshair = DashedLine(
            analyzer_xy + DOWN * 0.87,
            analyzer_xy + UP * 0.87,
            dash_length=.09, dashed_ratio=.52,
            color=DIM, stroke_width=1.6,
        )

        def axis_direction():
            a = theta.get_value()
            return np.array([np.sin(a), np.cos(a), 0.0])

        analyzer_axis = always_redraw(lambda: Line(
            analyzer_xy - 0.77 * axis_direction(),
            analyzer_xy + 0.77 * axis_direction(),
            color=GOLD, stroke_width=4.2,
        ))

        def projected_vector():
            """E2 / E1 = cos(theta): linearly projected field amplitude."""
            strength = max(0.0, np.cos(theta.get_value()))
            if strength < 0.025:
                return VGroup(Dot(analyzer_xy, radius=0.05, color=CYAN))
            u = axis_direction()
            return VGroup(
                Arrow(
                    analyzer_xy, analyzer_xy + .67 * strength * u,
                    buff=0, tip_length=.12, stroke_width=6,
                    color=CYAN,
                )
            )

        analyzer_projection = always_redraw(projected_vector)
        angle_arc = always_redraw(lambda: Arc(
            radius=.46,
            start_angle=PI / 2 - max(.001, theta.get_value()),
            angle=max(.001, theta.get_value()),
            arc_center=analyzer_xy,
            stroke_color=MINT, stroke_width=3,
        ))
        angle_label = always_redraw(lambda: VGroup(
            Text("theta =", font="Lato", font_size=17, color=DIM),
            DecimalNumber(
                np.rad2deg(theta.get_value()),
                num_decimal_places=0, font_size=20, color=MINT,
            ),
            Text("deg", font="Lato", font_size=17, color=MINT),
        ).arrange(RIGHT, buff=.11).move_to([0.05, -1.50, 0]))

        # ── An amplitude indicator and brightness-modulated output beam.
        #    Its HEIGHT is proportional to |E2/E1| (not to intensity).
        amplitude_label = Text(
            "FIELD AMPLITUDE", font="Lato", font_size=14,
            color=WHITE_SOFT,
        ).move_to([1.95, 1.53, 0])
        amp_baseline = Line(
            [1.35, -.97, 0], [2.57, -.97, 0],
            color=BORDER, stroke_width=2,
        )
        amp_track = RoundedRectangle(
            width=.36, height=1.49, corner_radius=.07,
            stroke_color=BORDER, stroke_width=1.5,
            fill_color="#152A40", fill_opacity=.8,
        ).move_to([1.95, -.21, 0])

        def amplitude_bar():
            fraction = max(0.0001, np.cos(theta.get_value()))
            h = 1.40 * fraction
            return Rectangle(
                width=.27, height=h,
                stroke_width=0,
                fill_color=CYAN, fill_opacity=.95,
            ).move_to([1.95, -.94 + h / 2, 0])

        amp_fill = always_redraw(amplitude_bar)
        amp_value = always_redraw(lambda: VGroup(
            Text("E2/E1", font="Lato", font_size=15, color=DIM),
            DecimalNumber(
                max(0.0, np.cos(theta.get_value())),
                num_decimal_places=2, font_size=21, color=CYAN,
            ),
        ).arrange(DOWN, buff=.07).move_to([1.96, -1.53, 0]))

        # ── Right panel: function and moving dot represent intensity,
        #    not electric field amplitude.
        graph_title = Text(
            "TRANSMITTED INTENSITY", font="Lato", font_size=15,
            color=WHITE_SOFT,
        ).move_to([4.63, 1.53, 0])
        axes = Axes(
            x_range=[0, 90, 30],
            y_range=[0, 1, .25],
            x_length=2.71,
            y_length=1.77,
            tips=False,
            axis_config={"color": DIM, "stroke_width": 1.7},
        )
        axes.shift(np.array([3.25, -1.23, 0]) - axes.c2p(0, 0))
        intensity_curve = axes.plot(
            lambda deg: np.cos(deg * DEGREES) ** 2,
            x_range=[0, 90, 1],
            color=MINT, stroke_width=3.5,
        )
        for val in [0, 45, 90]:
            axes.add(Text(
                str(val), font="Lato", font_size=13,
                color=DIM,
            ).next_to(axes.c2p(val, 0), DOWN, buff=.09))
        for val, label in [(0.5, "0.5"), (1.0, "1")]:
            axes.add(Text(
                label, font="Lato", font_size=12, color=DIM,
            ).next_to(axes.c2p(0, val), LEFT, buff=.11))
        plot_ylabel = Text(
            "I2/I1", font="Lato", font_size=14,
            color=CYAN,
        ).move_to([3.28, 1.06, 0])
        plot_xlabel = Text(
            "angle (deg)", font="Lato", font_size=14,
            color=DIM,
        ).move_to([5.17, -1.72, 0])
        moving_dot = always_redraw(lambda: Dot(
            axes.c2p(
                np.rad2deg(theta.get_value()),
                max(0.0, np.cos(theta.get_value()) ** 2),
            ),
            radius=.091, color=GOLD,
        ))
        moving_guide = always_redraw(lambda: DashedLine(
            axes.c2p(np.rad2deg(theta.get_value()), 0),
            axes.c2p(
                np.rad2deg(theta.get_value()),
                max(.001, np.cos(theta.get_value()) ** 2),
            ),
            color=GOLD, stroke_width=1.8, dash_length=.08,
        ))

        # ── Bottom panel: NEVER apply Malus law directly to unpolarized
        #    illumination without first defining a polarized I1.
        first_eq_label = Text(
            "FIRST POLARIZER", font="Lato", font_size=14,
            color=GOLD,
        ).move_to([-4.65, -2.68, 0])
        first_equation = MathTex(
            r"I_1 = \frac{I_0}{2}", font_size=35,
            color=WHITE_SOFT,
        ).move_to([-4.57, -3.18, 0])
        second_eq_label = Text(
            "MALUS'S LAW", font="Lato", font_size=14,
            color=GOLD,
        ).move_to([0.15, -2.68, 0])
        malus_equation = MathTex(
            r"I_2=I_1\cos^2\theta", font_size=35,
            color=WHITE_SOFT,
        ).move_to([0.02, -3.18, 0])
        second_transmission_label = Text(
            "RELATIVE TRANSMISSION", font="Lato", font_size=14,
            color=GOLD,
        ).move_to([4.53, -2.68, 0])
        transmission_value = always_redraw(lambda: VGroup(
            DecimalNumber(
                100.0 * max(0.0, np.cos(theta.get_value()) ** 2),
                num_decimal_places=1,
                font_size=34, color=MINT,
            ),
            Text("%", font="Lato", font_size=27, color=MINT),
        ).arrange(RIGHT, buff=.06).move_to([4.53, -3.20, 0]))

        # ── Animation timeline ───────────────────────────────────────────────
        self.play(
            FadeIn(header, shift=DOWN * .12),
            FadeIn(title, shift=DOWN * .12),
            FadeIn(subtitle), Create(divider),
            FadeIn(stage), FadeIn(footer), run_time=1.2,
        )
        self.play(
            FadeIn(source_label),
            Create(polarization_fan), FadeIn(source_center),
            FadeIn(source_hint), Create(incoming_path),
            run_time=1.0,
        )
        self.play(
            FadeIn(first_plate, scale=.95),
            Create(first_plate_axis), FadeIn(first_plate_label),
            run_time=.8,
        )
        self.play(
            Create(intermediate_beam),
            LaggedStart(*[Create(a) for a in polarized_vectors],
                        lag_ratio=.22),
            FadeIn(middle_label),
            FadeIn(first_eq_label), Write(first_equation),
            run_time=1.35,
        )
        self.wait(.5)
        self.play(
            Create(analyzer_disk), FadeIn(analyzer_label),
            Create(analyzer_crosshair),
            Create(amp_track), Create(amp_baseline),
            FadeIn(amplitude_label),
            Create(axes), Create(intensity_curve),
            FadeIn(graph_title), FadeIn(plot_xlabel), FadeIn(plot_ylabel),
            FadeIn(second_eq_label), Write(malus_equation),
            FadeIn(second_transmission_label),
            run_time=1.3,
        )
        self.add(
            analyzer_axis, analyzer_projection, angle_arc, angle_label,
            amp_fill, amp_value, moving_guide, moving_dot,
            transmission_value,
        )
        self.wait(.3)

        for angle_deg, time_sec in [
            (30, 1.9), (60, 1.9), (90, 2.0),
            (90, .6), (45, 2.0), (0, 2.0),
        ]:
            if abs(theta.get_value() - angle_deg * DEGREES) < 1e-9:
                self.wait(time_sec)
            else:
                self.play(
                    theta.animate.set_value(angle_deg * DEGREES),
                    run_time=time_sec, rate_func=smooth,
                )
        self.wait(.7)


# Optional short alias for notebook subprocess workflows:
# manim -pqh figura_05_manim.py fig5
class fig5(Figura05PolarizacionMalus):
    pass
