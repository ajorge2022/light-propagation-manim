"""FIGURE 06 — MATERIAL BIREFRINGENCE (Manim Community Edition)

Based on Figure 6 and the subsection "Polarization and material
birefringence" of *Light Propagation for Undergraduates*.

Physics and conventions
-----------------------
- A lossless uniaxial plate with optical axis perpendicular to the
  propagation direction k has two orthogonal eigenpolarizations.
- In this geometry n_eff(90 deg) = n_e; the two phase indices are
  n_o = 1.50 and n_e = 1.60 (ILLUSTRATIVE, not a named material).
- The input is linearly polarized at 45 degrees to the eigenaxes:
      E_o = E0 cos(u),        E_e = E0 cos(u + Delta_phi)
- The relative phase is Delta_phi = 2*pi*(L/lambda_0)*(n_e - n_o).
  The two colored traces indicate different electric-field components,
  NOT spatially separated rays. The outgoing Jones vector is proportional
  to (1, exp(i*Delta_phi)), so its tip traces a polarization ellipse.
- For L/lambda_0 = 2.5, Delta_phi = pi/2 and the equal-amplitude output
  is circular; for 5.0 it is linear again (rotated by 90 degrees).
- Increasing plate thickness is a parameter sweep, rather than the
  time-dependent motion of a physical crystal surface.

Render (Full HD):
    manim -pqh figura_06_manim.py Figura06Birrefringencia

Render (fast test):
    manim -pql figura_06_manim.py Figura06Birrefringencia

Requires: Manim Community, NumPy, and LaTeX (for MathTex).
"""

from manim import *
import numpy as np

# Visual identity from the other figure animations
BG = "#0C1524"
PANEL = "#122236"
BORDER = "#2A4058"
WHITE_SOFT = "#F0F7FF"
DIM = "#A2B3C7"
BLUE = "#58DDF7"     # ordinary eigenmode
GOLD = "#FFC478"     # extraordinary eigenmode
MINT = "#61E8B0"
PURPLE = "#8795E5"


class Figura06Birrefringencia(Scene):
    """Two polarization eigenmodes accumulate a relative phase in a crystal."""

    def construct(self):
        self.camera.background_color = BG

        # Constant indices; sweep the *thickness in vacuum wavelengths*.
        no = 1.50
        ne = 1.60
        delta_n = ne - no
        lambda0_scene = 0.90  # 1 vacuum wavelength = 0.9 Manim units
        k0 = TAU / lambda0_scene
        x_left = -2.35
        x_min, x_max = -5.78, 2.55

        thickness_lambda = ValueTracker(0.45)  # L / lambda_0
        optical_phase = ValueTracker(0.0)     # omega*t, illustrative units

        def width_of_crystal():
            return lambda0_scene * thickness_lambda.get_value()

        def x_right():
            return x_left + width_of_crystal()

        def retardation():
            return TAU * delta_n * thickness_lambda.get_value()

        # ─────────── Header / layout ───────────
        header = Text(
            "FIGURE 06   /   CLASSICAL WAVE OPTICS",
            font_size=18, color=GOLD,
        ).to_corner(UL, buff=0.47)
        title = Text(
            "MATERIAL BIREFRINGENCE",
            font_size=34, weight=BOLD, color=WHITE_SOFT,
        ).next_to(header, DOWN, aligned_edge=LEFT, buff=0.12)
        subtitle = Text(
            "Different phase velocities change the polarization state.",
            font_size=19, color=DIM,
        ).next_to(title, DOWN, aligned_edge=LEFT, buff=0.12)
        rule = Line([-6.55, 2.17, 0], [6.55, 2.17, 0],
                    color=BORDER, stroke_width=1.5)

        stage = RoundedRectangle(
            width=13.12, height=4.25, corner_radius=0.16,
            stroke_color=BORDER, stroke_width=1.25,
            fill_color=PANEL, fill_opacity=1,
        ).move_to([0, -0.06, 0])
        footer = RoundedRectangle(
            width=13.12, height=1.06, corner_radius=0.16,
            stroke_color=BORDER, stroke_width=1.25,
            fill_color=PANEL, fill_opacity=1,
        ).move_to([0, -3.05, 0])
        separator = Line([2.83, 1.86, 0], [2.83, -1.95, 0],
                         stroke_color=BORDER, stroke_width=1.5)

        left_heading = Text("TWO PROPAGATING EIGENMODES",
                            font_size=17, color=WHITE_SOFT).move_to([-2.4, 1.74, 0])
        right_heading = Text("OUTPUT POLARIZATION",
                             font_size=17, color=WHITE_SOFT).move_to([4.63, 1.74, 0])

        # ─────────── Crystal plate (normal to the propagation axis) ───────────
        crystal = always_redraw(lambda: Rectangle(
            width=max(0.01, width_of_crystal()), height=2.85,
            stroke_color=PURPLE, stroke_width=1.8,
            fill_color=PURPLE, fill_opacity=0.16,
        ).move_to([(x_left + x_right()) / 2, -0.04, 0]))
        entrance = Line([x_left, -1.47, 0], [x_left, 1.39, 0],
                        color=PURPLE, stroke_width=2.2)
        exit_face = always_redraw(lambda: Line(
            [x_right(), -1.47, 0], [x_right(), 1.39, 0],
            color=MINT, stroke_width=2.5,
        ))

        # Propagation direction: horizontal. The transverse component
        # traces are vertically displaced only to make them readable.
        y_o, y_e = 0.78, -0.76
        baselines = VGroup(
            DashedLine([x_min, y_o, 0], [x_max, y_o, 0],
                       dash_length=0.13, color=BORDER),
            DashedLine([x_min, y_e, 0], [x_max, y_e, 0],
                       dash_length=0.13, color=BORDER),
        )

        # Top row is ordinary E_o (transverse to both k and optical axis).
        # Bottom row is extraordinary E_e (along the optical axis for k ⟂ OA).
        ordinary_label = MathTex(r"E_o", color=BLUE, font_size=30)
        ordinary_label.move_to([-6.04, y_o + 0.43, 0])
        extraordinary_label = MathTex(r"E_e", color=GOLD, font_size=30)
        extraordinary_label.move_to([-6.04, y_e + 0.43, 0])

        x_grid = np.linspace(x_min, x_max, 310)

        def wave_curve(n, center_y, color):
            """Continuous phase across both crystal boundaries.

            Vacuum to the left: path = x-x_left.
            In the plate:       path = n*(x-x_left).
            Vacuum to the right:path = n*width + (x-x_right).
            """
            width = width_of_crystal()
            right = x_right()
            path = np.where(
                x_grid < x_left,
                x_grid - x_left,
                np.where(
                    x_grid <= right,
                    n * (x_grid - x_left),
                    n * width + (x_grid - right),
                ),
            )
            values = center_y + 0.28 * np.cos(k0 * path - optical_phase.get_value())
            vertices = np.column_stack((x_grid, values, np.zeros_like(x_grid)))
            curve = VMobject(color=color, stroke_width=3.1)
            curve.set_points_smoothly(vertices)
            return curve

        mode_o = always_redraw(lambda: wave_curve(no, y_o, BLUE))
        mode_e = always_redraw(lambda: wave_curve(ne, y_e, GOLD))

        plate_caption = Text("UNIAXIAL CRYSTAL", font_size=17,
                             color=PURPLE).move_to([-0.16, -1.72, 0])
        axis_caption = MathTex(
            r"\mathbf{k}\perp\mathrm{optical\ axis}",
            font_size=25, color=DIM,
        ).move_to([-4.24, -1.73, 0])

        # ─────────── Polarization at the plate output ───────────
        # The transverse plane is spanned by orthogonal eigenmodes E_o/E_e.
        chart_center = np.array([4.60, -0.17, 0.0])
        chart_radius = 1.08
        axis_x = Line(chart_center + LEFT * 1.33,
                      chart_center + RIGHT * 1.33,
                      color=BORDER, stroke_width=1.9)
        axis_y = Line(chart_center + DOWN * 1.33,
                      chart_center + UP * 1.33,
                      color=BORDER, stroke_width=1.9)
        unit_circle = Circle(
            radius=chart_radius, color=BORDER,
            stroke_width=1.5, stroke_opacity=0.65,
        ).move_to(chart_center)
        output_x_label = MathTex("E_o", font_size=25, color=BLUE)
        output_x_label.next_to(axis_x, RIGHT, buff=0.08)
        output_y_label = MathTex("E_e", font_size=25, color=GOLD)
        output_y_label.next_to(axis_y, UP, buff=0.06)

        parameter = np.linspace(0, TAU, 181)

        def polarization_curve():
            """Tip trajectory of (E_o, E_e), relative phase delta."""
            delta = retardation()
            xs = chart_center[0] + chart_radius * np.cos(parameter)
            ys = chart_center[1] + chart_radius * np.cos(parameter + delta)
            path = VMobject(color=MINT, stroke_width=3.3)
            path.set_points_smoothly(
                np.column_stack((xs, ys, np.zeros_like(xs)))
            )
            return path

        def field_tip():
            """An instantaneous sample, consistent with the wave curves."""
            phase_at_exit_o = k0 * no * width_of_crystal() - optical_phase.get_value()
            phase_at_exit_e = k0 * ne * width_of_crystal() - optical_phase.get_value()
            return Dot(
                chart_center + chart_radius * np.array([
                    np.cos(phase_at_exit_o), np.cos(phase_at_exit_e), 0,
                ]),
                radius=0.066, color=WHITE_SOFT,
            )

        ellipse = always_redraw(polarization_curve)
        tip = always_redraw(field_tip)
        footer_formula = MathTex(
            r"\Delta\phi=\frac{2\pi L}{\lambda_0}(n_e-n_o)",
            font_size=25, color=WHITE_SOFT,
        )
        footer_formula.move_to([4.65, -1.78, 0])
        footer_formula.scale_to_fit_width(min(3.35, footer_formula.width))

        # ─────────── Live parameters / physics footer ───────────
        index_o = MathTex(r"n_o=1.50", color=BLUE, font_size=28)
        index_e = MathTex(r"n_e=1.60", color=GOLD, font_size=28)
        index_o.move_to([-4.9, -2.97, 0])
        index_e.move_to([-2.72, -2.97, 0])

        l_symbol = MathTex(r"L/\lambda_0=", font_size=28,
                           color=WHITE_SOFT).move_to([-0.82, -2.97, 0])
        l_value = DecimalNumber(
            thickness_lambda.get_value(), num_decimal_places=2,
            font_size=28, color=WHITE_SOFT,
        ).next_to(l_symbol, RIGHT, buff=0.09)
        l_value.add_updater(lambda m: m.set_value(thickness_lambda.get_value()))

        phi_symbol = MathTex(r"\Delta\phi=", font_size=30,
                             color=MINT).move_to([2.48, -2.97, 0])
        phi_value = DecimalNumber(
            retardation() / PI, num_decimal_places=2,
            font_size=30, color=MINT,
        ).next_to(phi_symbol, RIGHT, buff=0.08)
        phi_value.add_updater(lambda m: m.set_value(retardation() / PI))
        pi_unit = MathTex(r"\pi", font_size=29,
                          color=MINT).next_to(phi_value, RIGHT, buff=0.10)
        pi_unit.add_updater(lambda m: m.next_to(phi_value, RIGHT, buff=0.10))

        no_absorption = Text("LOSSLESS", font_size=17, color=DIM)
        no_absorption.move_to([5.28, -2.97, 0])

        # ─────────── Animation sequence ───────────
        self.play(
            FadeIn(header, shift=DOWN * 0.1),
            Write(title), FadeIn(subtitle),
            Create(rule),
            run_time=1.5,
        )
        self.play(FadeIn(stage), FadeIn(footer), Create(separator),
                  FadeIn(left_heading), FadeIn(right_heading), run_time=0.8)
        self.play(
            FadeIn(crystal), Create(entrance), FadeIn(exit_face),
            Create(baselines),
            FadeIn(ordinary_label), FadeIn(extraordinary_label),
            FadeIn(plate_caption), FadeIn(axis_caption),
            Create(axis_x), Create(axis_y), Create(unit_circle),
            FadeIn(output_x_label), FadeIn(output_y_label),
            run_time=1.4,
        )
        self.play(
            FadeIn(mode_o), FadeIn(mode_e),
            FadeIn(ellipse), FadeIn(tip), FadeIn(footer_formula),
            FadeIn(index_o), FadeIn(index_e), FadeIn(l_symbol),
            FadeIn(l_value), FadeIn(phi_symbol), FadeIn(phi_value),
            FadeIn(pi_unit), FadeIn(no_absorption),
            run_time=1.3,
        )

        # Crystal thickness is swept, while the monochromatic field moves.
        # At L/lambda_0=2.5, Delta phi=pi/2 (circular for equal amplitudes).
        self.play(
            thickness_lambda.animate.set_value(2.50),
            optical_phase.animate.increment_value(3 * TAU),
            rate_func=linear, run_time=5.0,
        )
        self.wait(0.4)

        # At L/lambda_0=5.0, Delta phi=pi (linear, rotated orientation).
        self.play(
            thickness_lambda.animate.set_value(5.00),
            optical_phase.animate.increment_value(3 * TAU),
            rate_func=linear, run_time=5.0,
        )
        self.wait(0.4)

        # Return to a generic elliptically polarized output.
        self.play(
            thickness_lambda.animate.set_value(1.70),
            optical_phase.animate.increment_value(2 * TAU),
            rate_func=linear, run_time=4.2,
        )
        self.play(
            optical_phase.animate.increment_value(2 * TAU),
            rate_func=linear, run_time=2.2,
        )
        self.wait(1.0)
