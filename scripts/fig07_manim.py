"""FIGURE 07 — COMPTON SCATTERING (Manim Community Edition)

Based on Figure 7 and the subsection "Compton scattering: connecting
kinematics to QED" in *Light Propagation for undergraduates*.

The electron is initially at rest. For a photon scattered through angle theta:

    E_gamma' = E_gamma / [1 + (E_gamma / (m_e c^2)) (1 - cos(theta))]
    lambda' - lambda = (h / (m_e c)) (1 - cos(theta))

Momentum conservation determines the electron-recoil direction:
    p_e,x c = E_gamma - E_gamma' cos(theta)
    p_e,y c = -E_gamma' sin(theta)

Photon energies are displayed in units of m_e c^2. The incoming photon has
E_gamma = 0.80 m_e c^2 (a chosen illustrative value). The visual sinusoidal
wave packets represent an electromagnetic-field carrier, NOT an oscillating
photon trajectory. All angles/energy ratios are evaluated from the formulas.

Render high quality:
    manim -pqh figura_07_manim.py Figura07Compton

Render quickly:
    manim -pql figura_07_manim.py Figura07Compton

Requirements: Manim Community, NumPy, and a LaTeX installation for MathTex.
"""

from manim import *
import numpy as np

# Visual identity shared with the earlier figure animations.
BG = "#0C1524"
PANEL = "#122236"
BORDER = "#2A4058"
WHITE_SOFT = "#F0F7FF"
DIM = "#A2B3C7"
CYAN = "#58DDF7"        # Incident photon
GOLD = "#FFC478"        # Scattered photon
MINT = "#61E8B0"        # Recoiling electron
PURPLE = "#8795E5"


class Figura07Compton(Scene):
    """Photon-electron collision with energy-momentum conserving recoil."""

    def construct(self):
        self.camera.background_color = BG

        # We use dimensionless energies: epsilon = E_gamma / (m_e c^2).
        epsilon = 0.80
        theta = ValueTracker(48.0)  # Compton scattering angle, degrees.
        incoming_position = ValueTracker(0.35)
        outgoing_position = ValueTracker(-0.65)
        electron_position = ValueTracker(0.0)

        vertex = np.array([-1.45, -0.29, 0.0])
        source = np.array([-5.86, -0.29, 0.0])
        outgoing_length = 2.20
        electron_length = 1.78

        def theta_rad():
            return np.deg2rad(theta.get_value())

        def scattered_energy():
            ang = theta_rad()
            return epsilon / (1.0 + epsilon * (1.0 - np.cos(ang)))

        def lambda_ratio():
            return epsilon / scattered_energy()

        def kinetic_electron():
            return epsilon - scattered_energy()

        def photon_direction():
            ang = theta_rad()
            return np.array([np.cos(ang), np.sin(ang), 0.0])

        def recoil_direction():
            ang = theta_rad()
            e_out = scattered_energy()
            p = np.array([
                epsilon - e_out * np.cos(ang),
                -e_out * np.sin(ang),
                0.0,
            ])
            length = np.linalg.norm(p)
            return p / length if length > 1e-12 else np.array([1.0, 0.0, 0.0])

        # -----------------------------------------------------------------
        # Layout: an event display on the left and live observables on right.
        # -----------------------------------------------------------------
        eyebrow = Text(
            "FIGURE 07   /   QUANTUM OPTICS",
            font_size=18, color=GOLD,
        ).to_corner(UL, buff=0.45)
        title = Text(
            "COMPTON SCATTERING",
            font_size=34, weight=BOLD, color=WHITE_SOFT,
        ).next_to(eyebrow, DOWN, aligned_edge=LEFT, buff=0.14)
        subtitle = Text(
            "A photon transfers energy and momentum to an electron.",
            font_size=18, color=DIM,
        ).next_to(title, DOWN, aligned_edge=LEFT, buff=0.12)

        line_top = Line(
            [-6.55, 2.15, 0], [6.55, 2.15, 0],
            color=BORDER, stroke_width=1.5,
        )
        left_panel = RoundedRectangle(
            width=8.83, height=4.24, corner_radius=0.15,
            stroke_color=BORDER, stroke_width=1.4,
            fill_color=PANEL, fill_opacity=1,
        ).move_to([-2.15, -0.19, 0])
        right_panel = RoundedRectangle(
            width=4.12, height=4.24, corner_radius=0.15,
            stroke_color=BORDER, stroke_width=1.4,
            fill_color=PANEL, fill_opacity=1,
        ).move_to([4.46, -0.19, 0])
        footer = RoundedRectangle(
            width=13.12, height=1.05, corner_radius=0.15,
            stroke_color=BORDER, stroke_width=1.4,
            fill_color=PANEL, fill_opacity=1,
        ).move_to([0, -3.04, 0])
        left_caption = Text(
            "SCATTERING GEOMETRY",
            font_size=17, color=WHITE_SOFT,
        ).move_to([-3.78, 1.66, 0])
        right_caption = Text(
            "KINEMATICS",
            font_size=17, color=WHITE_SOFT,
        ).move_to([4.46, 1.66, 0])

        # Incoming photon approaches from left along positive x.
        incident_ray = Arrow(
            source, vertex,
            buff=0, stroke_width=3.6, tip_length=0.17, color=CYAN,
        )
        reference_axis = DashedLine(
            vertex, vertex + RIGHT * 2.57,
            dash_length=0.12, color=DIM, stroke_width=1.35,
        ).set_opacity(0.50)
        vertex_dot = Dot(vertex, color=WHITE_SOFT, radius=0.073)
        electron_at_rest = Dot(vertex, radius=0.145, color=MINT)

        source_label = MathTex(
            r"\gamma,\ E_\gamma", font_size=28, color=CYAN,
        ).move_to([-4.73, 0.23, 0])
        electron_label = MathTex(
            r"e^-\ \mathrm{(at\ rest)}", font_size=24, color=MINT,
        ).move_to([-1.18, -0.85, 0])

        # Drawn angles are measured from the incident propagation direction.
        outgoing_ray = always_redraw(lambda: Arrow(
            vertex,
            vertex + outgoing_length * photon_direction(),
            buff=0, stroke_width=4.2, tip_length=0.17,
            color=GOLD,
        ))
        recoil_ray = always_redraw(lambda: Arrow(
            vertex,
            vertex + electron_length * recoil_direction(),
            buff=0, stroke_width=3.7, tip_length=0.17,
            color=MINT,
        ))
        angle_arc = always_redraw(lambda: Arc(
            radius=0.70,
            start_angle=0.0,
            angle=theta_rad(),
            arc_center=vertex,
            color=PURPLE,
            stroke_width=3.0,
        ))
        theta_label = always_redraw(lambda: MathTex(
            r"\theta", font_size=29, color=PURPLE,
        ).move_to(vertex + 1.04 * np.array([
            np.cos(theta_rad() / 2), np.sin(theta_rad() / 2), 0.0,
        ])))

        scattered_label = always_redraw(lambda: MathTex(
            r"\gamma',\ E_\gamma'", font_size=26, color=GOLD,
        ).move_to(vertex + 1.66 * photon_direction()
                  + np.array([0.0, 0.25, 0.0])))
        recoil_label = always_redraw(lambda: MathTex(
            r"e^-", font_size=28, color=MINT,
        ).move_to(vertex + 1.40 * recoil_direction()
                  + np.array([0.32, 0.00, 0.0])))

        def photon_wave(origin, direction, center_s, wavelength, max_s, color):
            """Gaussian-windowed transverse carrier (not photon orbit)."""
            lo = max(0.0, center_s - 0.76)
            hi = min(max_s, center_s + 0.76)
            if hi <= lo + 0.015:
                return VGroup()
            s = np.linspace(lo, hi, 95)
            direct = np.asarray(direction, dtype=float)
            normal = np.array([-direct[1], direct[0], 0.0])
            envelope = np.exp(-0.5 * ((s - center_s) / 0.30) ** 2)
            oscillation = np.sin(TAU * (s - center_s) / wavelength)
            transverse = 0.19 * envelope * oscillation
            points = np.array([
                origin + si * direct + ai * normal
                for si, ai in zip(s, transverse)
            ])
            curve = VMobject(stroke_color=color, stroke_width=4.4)
            curve.set_points_smoothly(points)
            return curve

        incoming_packet = always_redraw(lambda: photon_wave(
            source, RIGHT, incoming_position.get_value(),
            0.26, np.linalg.norm(vertex - source), CYAN,
        ))
        outgoing_packet = always_redraw(lambda: photon_wave(
            vertex, photon_direction(), outgoing_position.get_value(),
            0.26 * lambda_ratio(), outgoing_length, GOLD,
        ))
        moving_electron = always_redraw(lambda: Dot(
            vertex + electron_length * electron_position.get_value()
            * recoil_direction(), radius=0.125, color=MINT,
        ))

        # -----------------------------------------------------------------
        # Live physics dashboard (all values are dimensionless ratios).
        # -----------------------------------------------------------------
        def info_row(y, label, getter, color, decimals=2, suffix=""):
            caption = MathTex(label, font_size=25, color=DIM)
            caption.move_to([3.66, y, 0])
            result = always_redraw(lambda: DecimalNumber(
                getter(), num_decimal_places=decimals,
                font_size=30, color=color,
            ).move_to([5.48, y, 0]))
            group = VGroup(caption, result)
            if suffix:
                unit = MathTex(suffix, font_size=21, color=DIM)
                unit.move_to([6.05, y, 0])
                group.add(unit)
            return group

        rows = VGroup(
            info_row(0.89, r"\theta", theta.get_value, PURPLE, 1, r"{}^\circ"),
            info_row(0.20, r"E_\gamma/(m_ec^2)", lambda: epsilon, CYAN),
            info_row(-0.49, r"E_\gamma'/(m_ec^2)", scattered_energy, GOLD),
            info_row(-1.18, r"\lambda'/\lambda", lambda_ratio, GOLD),
            info_row(-1.87, r"K_e/(m_ec^2)", kinetic_electron, MINT),
        )
        # Align dashboard captions without relying on MathTex's varying widths.
        for i, group in enumerate(rows):
            group[0].move_to([3.77, 0.89 - 0.69 * i, 0])

        formula_left = MathTex(
            r"\lambda'-\lambda=\frac{h}{m_ec}(1-\cos\theta)",
            font_size=30, color=WHITE_SOFT,
        ).move_to([-3.20, -3.03, 0])
        formula_right = MathTex(
            r"E_\gamma'=\frac{E_\gamma}"
            r"{1+\frac{E_\gamma}{m_ec^2}(1-\cos\theta)}",
            font_size=29, color=WHITE_SOFT,
        ).move_to([3.42, -3.03, 0])
        formula_right.scale_to_fit_width(5.70)

        # -----------------------------------------------------------------
        # Animation narrative.
        # -----------------------------------------------------------------
        self.play(
            FadeIn(left_panel), FadeIn(right_panel), FadeIn(footer),
            FadeIn(line_top),
            FadeIn(eyebrow), Write(title), FadeIn(subtitle),
            FadeIn(left_caption), FadeIn(right_caption),
            run_time=1.35,
        )
        self.play(FadeIn(source_label), FadeIn(electron_label),
                  FadeIn(electron_at_rest), Create(incident_ray),
                  FadeIn(incoming_packet), run_time=1.30)
        self.play(incoming_position.animate.set_value(4.40),
                  run_time=2.30, rate_func=linear)
        self.play(Flash(vertex, color=WHITE_SOFT, flash_radius=0.38),
                  run_time=0.55)

        # After the interaction the electron recoils and the photon scatters.
        self.play(
            FadeOut(incoming_packet), FadeOut(electron_at_rest),
            FadeOut(electron_label),
            FadeIn(vertex_dot), FadeIn(reference_axis),
            FadeIn(outgoing_ray), FadeIn(recoil_ray),
            FadeIn(angle_arc), FadeIn(theta_label),
            FadeIn(outgoing_packet), FadeIn(moving_electron),
            FadeIn(scattered_label), FadeIn(recoil_label),
            FadeIn(rows), Write(formula_left), Write(formula_right),
            run_time=1.7,
        )
        self.play(
            outgoing_position.animate.set_value(2.30),
            electron_position.animate.set_value(1.0),
            run_time=2.25, rate_func=linear,
        )
        # Parameter scan: each new theta represents another scattering event,
        # rather than a single photon bending in flight.
        self.play(FadeOut(outgoing_packet), FadeOut(moving_electron),
                  run_time=0.5)
        self.play(theta.animate.set_value(72.0), run_time=2.0,
                  rate_func=smooth)
        self.wait(0.5)
        self.play(theta.animate.set_value(22.0), run_time=2.0,
                  rate_func=smooth)
        self.wait(0.5)
        self.play(theta.animate.set_value(48.0), run_time=1.5,
                  rate_func=smooth)
        self.wait(1.2)


# Optional alias for consistency with simpler earlier scene names.
fig7 = Figura07Compton
