"""Figure 8 — Leading-order QED diagrams for Compton scattering.

Based on Fig. 8 of "Light Propagation for undergraduates" (updated LaTeX).
The two tree-level amplitudes for
    gamma(k) + e-(p) -> gamma(k') + e-(p')
contain different orderings of the external photon vertices along the
fermion line:

    s-channel: internal momentum q_s = p + k
    u-channel: internal momentum q_u = p - k'

Diagrams are perturbative amplitudes, NOT classical particle trajectories
or a literal time-ordered movie. An internal electron is virtual/off-shell.
Both amplitudes contribute coherently to the same external state.

Render Full HD:
    manim -pqh figura_08_manim.py Figura08ComptonQED

Quick test:
    manim -pql figura_08_manim.py Figura08ComptonQED

Dependencies: Manim Community, numpy, and a working LaTeX installation.
"""

from manim import *
import numpy as np

# Visual style shared with Figures 6 and 7.
BG = "#0C1524"
PANEL = "#122236"
BORDER = "#2A4058"
SOFT_WHITE = "#F0F7FF"
MUTED = "#A2B3C7"
ELECTRON = "#61E8B0"
IN_PHOTON = "#FFC478"
OUT_PHOTON = "#58DDF7"
PROPAGATOR = "#A79EFF"


def wavy_photon(start, end, color, cycles=7, amplitude=0.085):
    """Draw a Feynman photon line; wiggles indicate a propagating photon leg."""
    start = np.array(start, dtype=float)
    end = np.array(end, dtype=float)
    direction = end - start
    norm = np.linalg.norm(direction[:2])
    normal = np.array([-direction[1], direction[0], 0.0]) / norm

    ts = np.linspace(0.0, 1.0, 140)
    points = [
        start + t * direction
        + amplitude * np.sin(2 * PI * cycles * t) * np.sin(PI * t) * normal
        for t in ts
    ]
    wave = VMobject()
    wave.set_points_smoothly(points)
    wave.set_stroke(color=color, width=3.2)
    return wave


def photon_momentum_arrow(start, end, color):
    """Small arrow marking the direction of the *external photon momentum*."""
    start = np.array(start, dtype=float)
    end = np.array(end, dtype=float)
    a = start + 0.52 * (end - start)
    b = start + 0.73 * (end - start)
    return Arrow(
        a, b, buff=0,
        color=color, stroke_width=2.4,
        tip_length=0.11,
        max_tip_length_to_length_ratio=0.45,
    )


def compton_diagram(center_x, channel):
    """Return the diagram, vertices and useful annotations for s or u channel.

    Horizontal direction represents electron-fermion flow, not a fixed time axis.
    The two upper photon legs are assigned physical incoming/outgoing momenta.
    """
    assert channel in ("s", "u")
    y0 = -0.49
    left = np.array([center_x - 0.88, y0, 0.0])
    right = np.array([center_x + 0.88, y0, 0.0])
    e_in = np.array([center_x - 2.64, y0, 0.0])
    e_out = np.array([center_x + 2.64, y0, 0.0])
    upper_left = left + np.array([-0.65, 1.30, 0.0])
    upper_right = right + np.array([0.65, 1.30, 0.0])

    e_legs = VGroup(
        Line(e_in, left, color=ELECTRON, stroke_width=3.8),
        Line(left, right, color=PROPAGATOR, stroke_width=4.5),
        Line(right, e_out, color=ELECTRON, stroke_width=3.8),
    )
    # Electron arrow on internal propagator: fermion flow left -> right.
    fermion_arrow = Triangle(
        color=PROPAGATOR, fill_color=PROPAGATOR,
        fill_opacity=1, stroke_width=0,
    ).scale(0.085).rotate(-PI / 2).move_to(
        0.5 * (left + right)
    )
    vertices = VGroup(
        Dot(left, radius=0.075, color=SOFT_WHITE),
        Dot(right, radius=0.075, color=SOFT_WHITE),
    )

    if channel == "s":
        # Photon k enters at first vertex, k' leaves at second vertex.
        first_wave = wavy_photon(upper_left, left, IN_PHOTON)
        second_wave = wavy_photon(right, upper_right, OUT_PHOTON)
        first_arrow = photon_momentum_arrow(upper_left, left, IN_PHOTON)
        second_arrow = photon_momentum_arrow(right, upper_right, OUT_PHOTON)
        first_label = MathTex(r"\gamma(k)", font_size=27, color=IN_PHOTON)
        second_label = MathTex(r"\gamma(k')", font_size=27, color=OUT_PHOTON)
        order = "Absorption  →  emission"
        q = MathTex(r"q_s=p+k", font_size=29, color=PROPAGATOR)
    else:
        # Photon k' leaves at first vertex, k enters at second vertex.
        first_wave = wavy_photon(left, upper_left, OUT_PHOTON)
        second_wave = wavy_photon(upper_right, right, IN_PHOTON)
        first_arrow = photon_momentum_arrow(left, upper_left, OUT_PHOTON)
        second_arrow = photon_momentum_arrow(upper_right, right, IN_PHOTON)
        first_label = MathTex(r"\gamma(k')", font_size=27, color=OUT_PHOTON)
        second_label = MathTex(r"\gamma(k)", font_size=27, color=IN_PHOTON)
        order = "Emission  →  absorption"
        q = MathTex(r"q_u=p-k'", font_size=29, color=PROPAGATOR)

    # Photon labels do not overlap the upper border of the panel.
    first_label.move_to(upper_left + np.array([-0.12, 0.22, 0.0]))
    second_label.move_to(upper_right + np.array([0.12, 0.22, 0.0]))
    p = MathTex(r"e^-(p)", font_size=28, color=ELECTRON).move_to(
        e_in + np.array([0.30, -0.35, 0.0])
    )
    pp = MathTex(r"e^-(p')", font_size=28, color=ELECTRON).move_to(
        e_out + np.array([-0.30, -0.35, 0.0])
    )
    q.move_to([center_x, 0.03, 0])

    order_text = Text(order, color=SOFT_WHITE, font_size=20)
    order_text.move_to([center_x, -1.64, 0])
    footnote = Text(
        "Vertex order along the fermion line",
        color=MUTED, font_size=15,
    ).move_to([center_x, -2.00, 0])

    return {
        "left_vertex": left,
        "right_vertex": right,
        "electron_lines": e_legs,
        "fermion_arrow": fermion_arrow,
        "vertices": vertices,
        "photons": VGroup(first_wave, second_wave),
        "momentum_arrows": VGroup(first_arrow, second_arrow),
        "labels": VGroup(first_label, second_label, p, pp, q),
        "order": order_text,
        "footnote": footnote,
    }


class Figura08ComptonQED(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ------------------------------------------------------------
        # Header and diagram panels.
        # ------------------------------------------------------------
        eyebrow = Text(
            "FIGURE 08   /   QUANTUM ELECTRODYNAMICS",
            font_size=17, color=IN_PHOTON,
        ).to_corner(UL, buff=0.40)
        title = Text(
            "COMPTON SCATTERING: TREE-LEVEL DIAGRAMS",
            font_size=31, weight=BOLD, color=SOFT_WHITE,
        ).next_to(eyebrow, DOWN, aligned_edge=LEFT, buff=0.13)
        subtitle = MathTex(
            r"\gamma(k)+e^-(p)\ \longrightarrow\ \gamma(k')+e^-(p')",
            font_size=31, color=MUTED,
        ).next_to(title, DOWN, aligned_edge=LEFT, buff=0.17)
        separator = Line(
            [-6.57, 2.09, 0], [6.57, 2.09, 0],
            stroke_width=1.4, color=BORDER,
        )

        left_center, right_center = -3.25, 3.25
        panels = VGroup(*[
            RoundedRectangle(
                width=6.27, height=4.41, corner_radius=0.13,
                stroke_color=BORDER, stroke_width=1.5,
                fill_color=PANEL, fill_opacity=1,
            ).move_to([x, -0.25, 0])
            for x in (left_center, right_center)
        ])
        s_heading = Text(
            "s-CHANNEL", font_size=20,
            color=IN_PHOTON, weight=BOLD,
        ).move_to([left_center, 1.62, 0])
        u_heading = Text(
            "u-CHANNEL", font_size=20,
            color=OUT_PHOTON, weight=BOLD,
        ).move_to([right_center, 1.62, 0])

        banner = RoundedRectangle(
            width=12.92, height=1.02, corner_radius=0.12,
            stroke_color=BORDER, stroke_width=1.4,
            fill_color=PANEL, fill_opacity=1,
        ).move_to([0, -3.11, 0])
        amplitude = MathTex(
            r"\mathcal{M}=\mathcal{M}_{s}+\mathcal{M}_{u}",
            font_size=37, color=SOFT_WHITE,
        ).move_to(banner.get_center())
        interference = MathTex(
            r"|\mathcal{M}|^2=|\mathcal{M}_s|^2+|\mathcal{M}_u|^2"
            r"+2\,\mathrm{Re}(\mathcal{M}_s\mathcal{M}_u^{*})",
            font_size=29, color=SOFT_WHITE,
        ).move_to(banner.get_center())
        amplitude.set_color_by_tex(r"\mathcal{M}_{s}", IN_PHOTON)
        amplitude.set_color_by_tex(r"\mathcal{M}_{u}", OUT_PHOTON)

        s = compton_diagram(left_center, "s")
        u = compton_diagram(right_center, "u")

        self.play(
            FadeIn(eyebrow, shift=DOWN * 0.12),
            Write(title),
            FadeIn(subtitle, shift=DOWN * 0.15),
            Create(separator),
            run_time=1.8,
        )
        self.play(
            FadeIn(panels), FadeIn(s_heading), FadeIn(u_heading),
            run_time=0.9,
        )

        # Step 1: draw the external electron states and virtual propagators.
        self.play(
            Create(s["electron_lines"]), Create(u["electron_lines"]),
            run_time=1.7,
        )
        self.play(
            FadeIn(s["fermion_arrow"], u["fermion_arrow"]),
            FadeIn(s["vertices"], u["vertices"]),
            run_time=0.5,
        )

        # Step 2: add incoming/outgoing photon legs, all kinematics labels.
        self.play(
            Create(s["photons"]), Create(u["photons"]),
            run_time=1.8,
        )
        self.play(
            FadeIn(s["momentum_arrows"], u["momentum_arrows"]),
            FadeIn(s["labels"], u["labels"]),
            FadeIn(s["order"], u["order"]),
            FadeIn(s["footnote"], u["footnote"]),
            run_time=1.2,
        )
        self.wait(0.65)

        # Step 3: the vertex order differs between s and u contributions.
        for side in ("left_vertex", "right_vertex"):
            s_color = IN_PHOTON if side == "left_vertex" else OUT_PHOTON
            u_color = OUT_PHOTON if side == "left_vertex" else IN_PHOTON
            rings = VGroup(
                Circle(radius=0.25, color=s_color, stroke_width=3.3)
                .move_to(s[side]),
                Circle(radius=0.25, color=u_color, stroke_width=3.3)
                .move_to(u[side]),
            )
            self.play(Create(rings), run_time=0.48)
            self.play(FadeOut(rings), run_time=0.35)

        # Step 4: amplitudes interfere: never square diagrams separately.
        self.play(FadeIn(banner), Write(amplitude), run_time=1.3)
        self.wait(1.15)
        self.play(
            FadeOut(amplitude, shift=UP * 0.06),
            FadeIn(interference, shift=UP * 0.06),
            run_time=1.1,
        )
        self.wait(2.0)


# Optional aliases for the short scene naming convention.
class fig8(Figura08ComptonQED):
    pass
