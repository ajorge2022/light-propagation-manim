"""FIGURA 11 — LIGHT-BY-LIGHT SCATTERING (ONE-LOOP QED BOX).

Manim Community | Light Propagation for Undergraduates

The manuscript's Figure 11 represents the reaction

    gamma(k1) + gamma(k2) -> gamma(k3) + gamma(k4)

through a virtual charged-fermion loop. This animation builds ONE
representative one-loop box topology and then emphasizes the four QED
vertices. The complete QED scattering amplitude requires the appropriate
permutations of external photon attachments (and spin-dependent terms).

In the low-energy limit (hbar = c = 1, omega << m_e), for equal photon
energies omega in the center-of-mass frame:

    sigma(gamma gamma -> gamma gamma) ~ alpha^4 * omega^6 / m_e^8.

IMPORTANT PHYSICS NOTE:
- Internal e-/e+ propagators are VIRTUAL and NOT physical particle tracks.
- The order in which lines are drawn is for instruction only; it is NOT a
  time ordering of a process or a real charged particle circulating in space.
- External photon paths are schematic Feynman lines, not ray trajectories.

Full HD: python -m manim -pqh figura_11_manim.py Figura11LightByLight
Quick:   python -m manim -pql figura_11_manim.py Figura11LightByLight

Requires Manim Community, NumPy and LaTeX for MathTex.
"""

from manim import *
import numpy as np

# Same palette and widescreen layout as the preceding figures.
BG = "#0C1524"
PANEL = "#122236"
BORDER = "#2A4058"
WHITE_SOFT = "#F0F7FF"
DIM = "#A2B3C7"
CYAN = "#58DDF7"       # incident photons
GOLD = "#FFC478"       # outgoing photons
MINT = "#61E8B0"       # virtual electron loop
PURPLE = "#A79EFF"     # highlight of virtual propagators


def fit_width(mob, max_width):
    """Make a label fit inside its panel without enlarging it."""
    if mob.width > max_width:
        mob.scale(max_width / mob.width)
    return mob


def photon_wave(start, end, color, cycles=7, amplitude=0.075):
    """Smooth wavy photon line with zero displacement at its vertices."""
    a = np.array(start, dtype=float)
    b = np.array(end, dtype=float)
    v = b - a
    u = v / np.linalg.norm(v)
    normal = np.array([-u[1], u[0], 0.0])
    ts = np.linspace(0.0, 1.0, 161)
    pts = [
        a + t * v + normal * (amplitude * np.sin(TAU * cycles * t))
        for t in ts
    ]
    obj = VMobject()
    obj.set_points_smoothly(pts)
    obj.set_stroke(color=color, width=3.2)
    return obj


def flow_arrow(a, b, fraction1=0.35, fraction2=0.65):
    """Small arrow on a fermion propagator: Feynman fermion-number flow."""
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    v = b - a
    return Arrow(
        a + fraction1 * v, a + fraction2 * v,
        buff=0, color=MINT, stroke_width=3.0, tip_length=0.12,
        max_tip_length_to_length_ratio=0.35,
    )


class Figura11LightByLight(Scene):
    def construct(self):
        self.camera.background_color = BG

        # --------------------------------------------------------------
        # 1) Header and explanatory panels.
        # --------------------------------------------------------------
        eyebrow = Text(
            "FIGURE 11   /   QUANTUM ELECTRODYNAMICS",
            font_size=18, color=GOLD,
        ).to_corner(UL, buff=0.42)
        title = Text(
            "LIGHT-BY-LIGHT SCATTERING",
            font_size=33, weight=BOLD, color=WHITE_SOFT,
        ).next_to(eyebrow, DOWN, aligned_edge=LEFT, buff=0.14)
        subtitle = Text(
            "One-loop box diagram: photons interact through a virtual charged-fermion loop.",
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
            width=13.05, height=1.03, corner_radius=0.15,
            stroke_color=BORDER, stroke_width=1.4,
            fill_color=PANEL, fill_opacity=1,
        ).move_to([0.0, -3.07, 0])

        left_header = Text(
            "REPRESENTATIVE ONE-LOOP BOX GRAPH",
            font_size=16, color=WHITE_SOFT,
        ).move_to([-2.18, 1.43, 0])
        right_header = Text(
            "PROCESS AND LOW-ENERGY LIMIT",
            font_size=15, color=WHITE_SOFT,
        ).move_to([4.37, 1.43, 0])

        self.play(
            FadeIn(eyebrow, shift=UP * 0.08),
            Write(title),
            FadeIn(subtitle),
            Create(title_rule),
            run_time=1.6,
        )
        self.play(
            FadeIn(left_panel), FadeIn(right_panel), FadeIn(footer),
            FadeIn(left_header), FadeIn(right_header),
            run_time=0.8,
        )

        # --------------------------------------------------------------
        # 2) Four vertices of a fermion loop (clockwise convention).
        #    Every corner has precisely one external photon line.
        # --------------------------------------------------------------
        tl = np.array([-3.56, 0.70, 0.0])
        tr = np.array([-0.91, 0.70, 0.0])
        br = np.array([-0.91, -0.75, 0.0])
        bl = np.array([-3.56, -0.75, 0.0])

        # Two incoming photons on the left, two outgoing on the right.
        k1_start = np.array([-5.94, 1.03, 0.0])
        k2_start = np.array([-5.94, -1.29, 0.0])
        k3_end = np.array([1.56, 1.05, 0.0])
        k4_end = np.array([1.56, -1.29, 0.0])

        incoming = VGroup(
            photon_wave(k1_start, tl, CYAN, cycles=8),
            photon_wave(k2_start, bl, CYAN, cycles=8),
        )
        outgoing = VGroup(
            photon_wave(tr, k3_end, GOLD, cycles=8),
            photon_wave(br, k4_end, GOLD, cycles=8),
        )
        internals = VGroup(
            Line(tl, tr, color=MINT, stroke_width=3.5),
            Line(tr, br, color=MINT, stroke_width=3.5),
            Line(br, bl, color=MINT, stroke_width=3.5),
            Line(bl, tl, color=MINT, stroke_width=3.5),
        )
        arrows = VGroup(
            flow_arrow(tl, tr),
            flow_arrow(tr, br),
            flow_arrow(br, bl),
            flow_arrow(bl, tl),
        )
        vertices = VGroup(*[
            Dot(v, radius=0.075, color=WHITE_SOFT)
            for v in (tl, tr, br, bl)
        ])

        k_labels = VGroup(
            MathTex(r"\gamma(k_1)", color=CYAN, font_size=27)
                .move_to([-5.13, 1.33, 0]),
            MathTex(r"\gamma(k_2)", color=CYAN, font_size=27)
                .move_to([-5.13, -1.62, 0]),
            MathTex(r"\gamma(k_3)", color=GOLD, font_size=27)
                .move_to([0.81, 1.34, 0]),
            MathTex(r"\gamma(k_4)", color=GOLD, font_size=27)
                .move_to([0.81, -1.63, 0]),
        )
        loop_label = Text(
            "virtual charged-fermion loop", font_size=18, color=MINT,
        ).move_to([-2.23, -0.02, 0])
        little_label = MathTex(
            r"e^\pm\;\mathrm{(virtual)}", font_size=24, color=PURPLE,
        ).move_to([-2.23, -0.40, 0])

        # Build up a Feynman graph, not a physical time sequence.
        self.play(Create(incoming), FadeIn(k_labels[0:2]), run_time=1.8)
        self.play(
            LaggedStart(*[Create(edge) for edge in internals], lag_ratio=0.23),
            run_time=2.4,
        )
        self.play(FadeIn(vertices), FadeIn(arrows), run_time=0.8)
        self.play(Create(outgoing), FadeIn(k_labels[2:4]), run_time=1.8)
        self.play(FadeIn(loop_label), FadeIn(little_label), run_time=0.8)
        self.wait(0.4)

        # --------------------------------------------------------------
        # 3) Physics panel: reaction, loop origin and cross section.
        # --------------------------------------------------------------
        process = fit_width(MathTex(
            r"\gamma\gamma\longrightarrow\gamma\gamma",
            font_size=36, color=WHITE_SOFT,
        ), 3.88).move_to([4.37, 0.91, 0])

        loop_heading = Text(
            "FIRST APPEARS AT ONE LOOP",
            font_size=15, color=DIM,
        ).move_to([4.37, 0.28, 0])
        loop_text = fit_width(MathTex(
            r"4\;\gamma e e\;\mathrm{vertices}",
            font_size=30, color=MINT,
        ), 3.86).move_to([4.37, -0.12, 0])

        regime_heading = Text(
            "LOW-ENERGY REGIME",
            font_size=15, color=DIM,
        ).move_to([4.37, -0.68, 0])
        regime = MathTex(
            r"\omega\ll m_e", font_size=32, color=WHITE_SOFT,
        ).move_to([4.37, -1.04, 0])
        scaling = fit_width(MathTex(
            r"\sigma_{\gamma\gamma\to\gamma\gamma}"
            r"\propto\alpha^4\frac{\omega^6}{m_e^8}",
            font_size=30, color=GOLD,
        ), 3.95).move_to([4.37, -1.79, 0])

        self.play(Write(process), run_time=1.0)
        self.play(
            FadeIn(loop_heading), Write(loop_text),
            run_time=1.0,
        )
        self.play(FadeIn(regime_heading), Write(regime), run_time=0.9)
        self.play(Write(scaling), run_time=1.4)

        # --------------------------------------------------------------
        # 4) Explicit caveat: a fermion loop is NOT real pair creation.
        # --------------------------------------------------------------
        foot1 = fit_width(Text(
            "Internal fermion lines are VIRTUAL propagators — not an on-shell electron–positron pair.",
            font_size=18, color=WHITE_SOFT,
        ), 12.4).move_to([0.0, -2.87, 0])
        foot2 = fit_width(Text(
            "One box ordering is shown; the full amplitude includes the required photon permutations.",
            font_size=16, color=DIM,
        ), 12.4).move_to([0.0, -3.26, 0])
        self.play(FadeIn(foot1), FadeIn(foot2), run_time=1.0)

        # Emphasize all FOUR interaction vertices and the loop.
        self.play(
            *[Indicate(dot, color=GOLD, scale_factor=1.65) for dot in vertices],
            run_time=1.5,
        )
        self.play(
            *[edge.animate.set_color(PURPLE) for edge in internals],
            loop_label.animate.set_color(PURPLE),
            run_time=1.1,
        )
        self.play(
            *[edge.animate.set_color(MINT) for edge in internals],
            loop_label.animate.set_color(MINT),
            run_time=0.9,
        )
        self.wait(2.0)
