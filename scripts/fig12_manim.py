"""FIGURE 12 — VACUUM POLARIZATION IN A MAGNETIC FIELD.

Manim Community scene for "Light Propagation for Undergraduates".

The one-loop photon self-energy diagram is a photon line with a CLOSED
VIRTUAL FERMION LOOP connecting two QED vertices. When an external magnetic
field modifies the vacuum polarization tensor, the two physical photon
polarization eigenmodes generally acquire different phase velocities.

In the weak-field, low-frequency limit used in the article,

    n_parallel - 1 = (7 alpha / 90 pi) (B / B_Q)^2 sin^2(theta),
    n_perp     - 1 = (2 alpha / 45 pi) (B / B_Q)^2 sin^2(theta),
    Delta n = n_parallel - n_perp = (alpha / 30 pi)
                                    (B / B_Q)^2 sin^2(theta).

'parallel' means E in the plane formed by k and B; 'perpendicular'
means E normal to that plane. Here k and B are perpendicular.

The illustrative relative phase shown at the end is EXAGGERATED so that
its effect is visible. It is not a quantitative prediction for a given
laboratory magnet. Internal fermion lines are virtual propagators, NOT
physical e+ / e- particle trajectories; the building order of the diagram
is not a physical time ordering.

Render in Full HD:
    python -m manim -pqh figura_12_manim.py Figura12VacuumPolarization

Quick preview:
    python -m manim -pql figura_12_manim.py Figura12VacuumPolarization

Requires Manim Community, NumPy, and a LaTeX distribution for MathTex.
"""

from manim import *
import numpy as np

# Visual continuity with Figures 8–11.
BG = "#0C1524"
PANEL = "#122236"
BORDER = "#2A4058"
WHITE_SOFT = "#F0F7FF"
DIM = "#A2B3C7"
CYAN = "#58DDF7"     # photons / perpendicular eigenmode
GOLD = "#FFC478"     # parallel eigenmode
MINT = "#61E8B0"     # virtual fermion propagators
PURPLE = "#A79EFF"   # external magnetic field


def fit_width(mob, width):
    """Shrink (never enlarge) a label to the target width."""
    if mob.width > width:
        mob.scale(width / mob.width)
    return mob


def photon_line(start, finish, color=CYAN, oscillations=8, amplitude=0.075):
    """A schematic wavy Feynman-photon propagator between two points."""
    p0 = np.array(start, dtype=float)
    p1 = np.array(finish, dtype=float)
    direction = p1 - p0
    unit = direction / np.linalg.norm(direction)
    transverse = np.array([-unit[1], unit[0], 0.0])
    path = VMobject()
    points = [
        p0 + t * direction
        + amplitude * np.sin(TAU * oscillations * t) * transverse
        for t in np.linspace(0, 1, 181)
    ]
    path.set_points_smoothly(points)
    path.set_stroke(color=color, width=3.2)
    return path


def virtual_loop_vertices(left, right):
    """Top and bottom fermion propagators forming a closed bubble graph.

    Arrows follow one consistent fermion-flow orientation; they do not
    represent a literal particle moving around a spatial orbit.
    """
    lx, ly, _ = left
    rx, ry, _ = right
    width = rx - lx
    top = CubicBezier(
        left,
        [lx + 0.17 * width, ly + 1.37, 0],
        [rx - 0.17 * width, ry + 1.37, 0],
        right,
        color=MINT,
        stroke_width=3.6,
    )
    bottom = CubicBezier(
        right,
        [rx - 0.17 * width, ry - 1.37, 0],
        [lx + 0.17 * width, ly - 1.37, 0],
        left,
        color=MINT,
        stroke_width=3.6,
    )
    return top, bottom


def arrow_on_path(path, color=MINT):
    """Short tangent arrow communicating Feynman fermion-number flow."""
    a = path.point_from_proportion(0.43)
    b = path.point_from_proportion(0.55)
    return Arrow(
        a, b, buff=0, color=color, stroke_width=3,
        tip_length=0.13, max_tip_length_to_length_ratio=0.45,
    )


def relative_phase_wave(y, color, common_phase, extra_phase=0.0):
    """Draw a schematic sinusoidal field with a controllable phase."""
    start, stop = -4.76, 1.46
    xs = np.linspace(start, stop, 250)
    values = 0.095 * np.sin(
        2.70 * (xs - start) - common_phase - extra_phase
    )
    curve = VMobject()
    curve.set_points_smoothly([
        np.array([x, y + offset, 0])
        for x, offset in zip(xs, values)
    ])
    curve.set_stroke(color=color, width=2.8)
    return curve


class Figura12VacuumPolarization(Scene):
    def construct(self):
        self.camera.background_color = BG

        # -----------------------------------------------------------
        # 1. Header and panels (same visual language as Figure 11).
        # -----------------------------------------------------------
        eyebrow = Text(
            "FIGURE 12   /   QUANTUM ELECTRODYNAMICS",
            font_size=18, color=GOLD,
        ).to_corner(UL, buff=0.42)
        title = Text(
            "VACUUM POLARIZATION",
            font_size=33, weight=BOLD, color=WHITE_SOFT,
        ).next_to(eyebrow, DOWN, aligned_edge=LEFT, buff=0.14)
        subtitle = Text(
            "A virtual fermion loop modifies photon propagation in a magnetic background.",
            font_size=18, color=DIM,
        ).next_to(title, DOWN, aligned_edge=LEFT, buff=0.13)
        title_rule = Line(
            [-6.55, 2.13, 0], [6.55, 2.13, 0],
            stroke_color=BORDER, stroke_width=1.5,
        )

        left_panel = RoundedRectangle(
            width=8.48, height=4.02, corner_radius=0.15,
            stroke_color=BORDER, stroke_width=1.5,
            fill_color=PANEL, fill_opacity=1,
        ).move_to([-2.18, -0.24, 0])
        right_panel = RoundedRectangle(
            width=4.33, height=4.02, corner_radius=0.15,
            stroke_color=BORDER, stroke_width=1.5,
            fill_color=PANEL, fill_opacity=1,
        ).move_to([4.37, -0.24, 0])
        footer = RoundedRectangle(
            width=13.05, height=1.05, corner_radius=0.15,
            stroke_color=BORDER, stroke_width=1.4,
            fill_color=PANEL, fill_opacity=1,
        ).move_to([0, -3.07, 0])
        left_header = Text(
            "ONE-LOOP PHOTON SELF-ENERGY",
            font_size=16, color=WHITE_SOFT,
        ).move_to([-2.18, 1.43, 0])
        right_header = Text(
            "MAGNETIC VACUUM",
            font_size=16, color=WHITE_SOFT,
        ).move_to([4.37, 1.43, 0])

        self.play(
            FadeIn(eyebrow, shift=UP * 0.08),
            Write(title), FadeIn(subtitle), Create(title_rule),
            run_time=1.6,
        )
        self.play(
            FadeIn(left_panel), FadeIn(right_panel), FadeIn(footer),
            FadeIn(left_header), FadeIn(right_header),
            run_time=0.8,
        )

        # -----------------------------------------------------------
        # 2. Photon self-energy bubble (two photon vertices).
        #    Drawing it sequentially is not a time ordering.
        # -----------------------------------------------------------
        v_left = np.array([-3.44, -0.20, 0])
        v_right = np.array([-0.92, -0.20, 0])
        incoming = photon_line([-5.96, -0.20, 0], v_left, CYAN)
        outgoing = photon_line(v_right, [1.58, -0.20, 0], CYAN)
        upper, lower = virtual_loop_vertices(v_left, v_right)
        arrows = VGroup(arrow_on_path(upper), arrow_on_path(lower))
        vertices = VGroup(
            Dot(v_left, color=WHITE_SOFT, radius=0.073),
            Dot(v_right, color=WHITE_SOFT, radius=0.073),
        )
        gamma_labels = VGroup(
            MathTex(r"\gamma(k)", color=CYAN, font_size=28)
                .move_to([-4.70, 0.19, 0]),
            MathTex(r"\gamma(k)", color=CYAN, font_size=28)
                .move_to([0.31, 0.19, 0]),
        )
        loop_label = Text(
            "virtual fermion loop", font_size=18, color=MINT,
        ).move_to([-2.18, -0.18, 0])
        q_label = MathTex(
            r"e^{\pm}\;\mathrm{(virtual)}", font_size=24, color=MINT,
        ).move_to([-2.18, -0.62, 0])

        self.play(Create(incoming), FadeIn(gamma_labels[0]), run_time=1.2)
        self.play(Create(upper), Create(lower), FadeIn(vertices), run_time=1.9)
        self.play(FadeIn(arrows), run_time=0.65)
        self.play(Create(outgoing), FadeIn(gamma_labels[1]), run_time=1.2)
        self.play(FadeIn(loop_label), FadeIn(q_label), run_time=0.65)
        self.wait(0.5)

        # -----------------------------------------------------------
        # 3. External magnetic field: schematic BACKGROUND arrows.
        #    For the diagram k is horizontal, B vertical: theta=90°.
        #    In a full external-field treatment the internal electron
        #    propagators are modified by B; this is not an additional
        #    real incoming photon.
        # -----------------------------------------------------------
        b_arrows = VGroup(*[
            Arrow(
                [x, -1.66, 0], [x, 0.86, 0],
                color=PURPLE, stroke_width=2.7, buff=0,
                tip_length=0.17,
            ).set_opacity(0.26)
            for x in (-5.33, -4.58, 0.45, 1.21)
        ])
        b_text = MathTex(
            r"\mathbf B\perp\mathbf k", color=PURPLE, font_size=25,
        ).move_to([-2.18, -1.71, 0])
        self.play(FadeIn(b_arrows), FadeIn(b_text), run_time=1.2)
        self.play(Indicate(loop_label, color=PURPLE, scale_factor=1.08),
                  run_time=1.0)

        # -----------------------------------------------------------
        # 4. Polarization dependence of the refractive index.
        #    These equations are the article's weak-field results.
        # -----------------------------------------------------------
        eq1 = fit_width(MathTex(
            r"n_{\parallel}-1="
            r"\frac{7\alpha}{90\pi}"
            r"\left(\frac{B}{B_{\rm Q}}\right)^2"
            r"\sin^2\vartheta",
            color=GOLD, font_size=31,
        ), 3.94).move_to([4.37, 0.79, 0])
        eq2 = fit_width(MathTex(
            r"n_{\perp}-1="
            r"\frac{2\alpha}{45\pi}"
            r"\left(\frac{B}{B_{\rm Q}}\right)^2"
            r"\sin^2\vartheta",
            color=CYAN, font_size=31,
        ), 3.94).move_to([4.37, 0.06, 0])
        separator = Line(
            [2.54, -0.39, 0], [6.18, -0.39, 0],
            stroke_color=BORDER, stroke_width=1.4,
        )
        d_label = Text(
            "BIREFRINGENCE",
            color=DIM, font_size=15,
        ).move_to([4.37, -0.72, 0])
        delta_n = fit_width(MathTex(
            r"\Delta n="
            r"\frac{\alpha}{30\pi}"
            r"\left(\frac{B}{B_{\rm Q}}\right)^2"
            r"\sin^2\vartheta",
            color=WHITE_SOFT, font_size=31,
        ), 3.89).move_to([4.37, -1.15, 0])
        regime = Text(
            "Weak field / low photon energy",
            font_size=15, color=DIM,
        ).move_to([4.37, -1.80, 0])

        self.play(Write(eq1), run_time=1.4)
        self.play(Write(eq2), run_time=1.4)
        self.play(Create(separator), FadeIn(d_label), Write(delta_n),
                  FadeIn(regime), run_time=1.6)
        self.wait(0.4)

        # -----------------------------------------------------------
        # 5. Relative phase accumulation in the TWO eigenmodes.
        #    The phase difference is GREATLY EXAGGERATED for teaching.
        #    x is a schematic propagation coordinate, not a pixel-to-
        #    meter calibration or measured quantum-vacuum phase shift.
        # -----------------------------------------------------------
        parallel_tag = MathTex(
            r"E_{\parallel}", color=GOLD, font_size=24,
        ).move_to([-5.59, -2.91, 0])
        perp_tag = MathTex(
            r"E_{\perp}", color=CYAN, font_size=24,
        ).move_to([-5.59, -3.29, 0])
        phase_label = fit_width(MathTex(
            r"\Delta\phi="
            r"\frac{2\pi L}{\lambda_0}\,\Delta n",
            color=WHITE_SOFT, font_size=27,
        ), 3.45).move_to([4.40, -3.02, 0])
        not_scale = Text(
            "phase exaggerated", color=DIM, font_size=14,
        ).move_to([4.40, -3.35, 0])

        progress = ValueTracker(0.0)
        lag = ValueTracker(0.0)
        wave_parallel = always_redraw(lambda: relative_phase_wave(
            -2.91, GOLD, progress.get_value(), lag.get_value()
        ))
        wave_perp = always_redraw(lambda: relative_phase_wave(
            -3.29, CYAN, progress.get_value(), 0.0
        ))
        self.play(
            FadeIn(parallel_tag), FadeIn(perp_tag),
            FadeIn(phase_label), FadeIn(not_scale),
            Create(wave_parallel), Create(wave_perp),
            run_time=1.7,
        )
        self.play(
            progress.animate.set_value(2 * TAU),
            lag.animate.set_value(PI / 2),
            rate_func=linear, run_time=5.0,
        )
        self.play(
            progress.animate.set_value(3 * TAU),
            lag.animate.set_value(PI),
            rate_func=linear, run_time=2.5,
        )
        self.wait(1.3)


# Optional short name for the user's earlier run command style:
class fig12(Figura12VacuumPolarization):
    pass
