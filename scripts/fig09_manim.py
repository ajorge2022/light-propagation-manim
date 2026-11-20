"""FIGURE 09 — BREIT–WHEELER PAIR PRODUCTION (Manim Community).

Based on Fig. 9 and Sec. "Kinematics of pair creation and annihilation"
from *Light Propagation for undergraduates* (user-supplied LaTeX version).

     gamma(k1) + gamma(k2) -> e-(p_-) + e+(p_+)

Figure 9 contains TWO tree-level QED diagrams with virtual fermion exchange.
The diagrams shown here are the t-channel and the u-channel, in which
photon k1 attaches to the electron-side or positron-side vertex,
respectively.  Both amplitudes contribute to the same physical process.

Mandelstam invariants (hbar = c = 1):
  t = (k1 - p_-)^2,   u = (k1 - p_+)^2,
  s = (k1 + k2)^2 = 2*omega1*omega2*(1-cos(vartheta)) >= 4*m_e^2.
For equal-energy head-on photons: omega >= m_e.

IMPORTANT: Feynman lines depict terms in a scattering amplitude; they are
not literal particle tracks, and the internal electron is virtual/off shell.
The crossing of photon lines in the u-channel is NOT an interaction vertex.

Full HD: manim -pqh figura_09_manim.py Figura09BreitWheeler
Quick:   manim -pql figura_09_manim.py Figura09BreitWheeler

Requires Manim Community, NumPy and LaTeX (for MathTex).
"""

from manim import *
import numpy as np

# Visual style matches the previous Compton-scattering animations.
BG = "#0C1524"
PANEL = "#122236"
BORDER = "#2A4058"
WHITE_SOFT = "#F0F7FF"
MUTED = "#A2B3C7"
GAMMA1 = "#58DDF7"
GAMMA2 = "#FFC478"
FERMION = "#61E8B0"
INTERNAL = "#A79EFF"


def photon_leg(start, end, color, cycles=7, amplitude=0.085):
    """Wavy line representing an external photon leg in a Feynman diagram."""
    start = np.array(start, dtype=float)
    end = np.array(end, dtype=float)
    direction = end - start
    tangent = direction / np.linalg.norm(direction)
    normal = np.array([-tangent[1], tangent[0], 0.0])
    ts = np.linspace(0.0, 1.0, 165)
    points = [
        start + t * direction
        + (amplitude * np.sin(2 * PI * cycles * t) * np.sin(PI * t)) * normal
        for t in ts
    ]
    line = VMobject()
    line.set_points_smoothly(points)
    line.set_stroke(color=color, width=3.25)
    return line


def momentum_arrow(start, end, color):
    """Arrow parallel to the photon line, pointing toward the vertex."""
    a = np.array(start, dtype=float)
    b = np.array(end, dtype=float)
    return Arrow(
        a + 0.48 * (b - a),
        a + 0.72 * (b - a),
        buff=0,
        color=color,
        stroke_width=2.4,
        tip_length=0.12,
        max_tip_length_to_length_ratio=0.45,
    )


def diagram(cx, channel):
    """Build the two Feynman diagrams for gamma gamma -> e- e+.

    The external states are identical in both panels.  Only which photon
    attaches to which charged-fermion vertex is exchanged.

    Top charged leg: electron e- with outward fermion-flow arrow.
    Bottom charged leg: positron e+ with inward fermion-flow arrow.
    The internal fermion-flow arrow points bottom -> top.
    """
    assert channel in ("t", "u")

    top = np.array([cx - 0.22, 0.49, 0.0])
    bottom = np.array([cx - 0.22, -0.78, 0.0])
    k1_start = np.array([cx - 2.70, 1.07, 0.0])
    k2_start = np.array([cx - 2.70, -1.42, 0.0])
    electron_end = np.array([cx + 2.41, 0.49, 0.0])
    positron_end = np.array([cx + 2.41, -0.78, 0.0])

    # t-channel: gamma1 at the electron-side vertex (top), gamma2 bottom.
    # u-channel: gamma1 bottom, gamma2 top (crossed photon legs).
    gamma1_vertex = top if channel == "t" else bottom
    gamma2_vertex = bottom if channel == "t" else top

    photons = VGroup(
        photon_leg(k1_start, gamma1_vertex, GAMMA1),
        photon_leg(k2_start, gamma2_vertex, GAMMA2),
    )
    momentum = VGroup(
        momentum_arrow(k1_start, gamma1_vertex, GAMMA1),
        momentum_arrow(k2_start, gamma2_vertex, GAMMA2),
    )

    # Straight fermion lines are the external charged legs.
    charged = VGroup(
        Line(top, electron_end, color=FERMION, stroke_width=3.6),
        Line(bottom, positron_end, color=FERMION, stroke_width=3.6),
    )
    internal = Line(bottom, top, color=INTERNAL, stroke_width=4.7)
    flow = VGroup(
        Arrow(
            top + RIGHT * 0.88, top + RIGHT * 1.36,
            buff=0, color=FERMION, stroke_width=2.4, tip_length=0.14,
        ),
        Arrow(
            bottom + RIGHT * 1.36, bottom + RIGHT * 0.88,
            buff=0, color=FERMION, stroke_width=2.4, tip_length=0.14,
        ),
        Arrow(
            bottom + UP * 0.48, top + DOWN * 0.48,
            buff=0, color=INTERNAL, stroke_width=2.8, tip_length=0.13,
        ),
    )
    vertices = VGroup(
        Dot(top, radius=0.075, color=WHITE_SOFT),
        Dot(bottom, radius=0.075, color=WHITE_SOFT),
    )

    # External-state labels are the same in both diagrams.
    k1_label = MathTex(r"\gamma(k_1)", font_size=27, color=GAMMA1)
    k1_label.move_to(k1_start + np.array([0.55, 0.37, 0]))
    k2_label = MathTex(r"\gamma(k_2)", font_size=27, color=GAMMA2)
    k2_label.move_to(k2_start + np.array([0.55, -0.32, 0]))
    e_minus_label = MathTex(r"e^-(p_-)", font_size=27, color=FERMION)
    e_minus_label.move_to([cx + 1.40, 0.90, 0])
    e_plus_label = MathTex(r"e^+(p_+)", font_size=27, color=FERMION)
    e_plus_label.move_to([cx + 1.40, -1.16, 0])

    propagator_label = MathTex(
        r"q_t" if channel == "t" else r"q_u",
        font_size=25, color=INTERNAL,
    ).move_to([cx + 0.21, -0.16, 0])

    invariants = MathTex(
        r"t=(k_1-p_-)^2" if channel == "t" else r"u=(k_1-p_+)^2",
        font_size=31, color=WHITE_SOFT,
    ).move_to([cx, -2.17, 0])

    return {
        "photons": photons,
        "momentum": momentum,
        "charged": charged,
        "internal": internal,
        "flow": flow,
        "vertices": vertices,
        "labels": VGroup(
            k1_label, k2_label, e_minus_label, e_plus_label,
            propagator_label,
        ),
        "invariant": invariants,
    }


class Figura09BreitWheeler(Scene):
    """Animated t/u-channel Breit–Wheeler diagrams matching Figure 9."""

    def construct(self):
        self.camera.background_color = BG

        eyebrow = Text(
            "FIGURE 09   /   QUANTUM ELECTRODYNAMICS",
            font_size=17, color=GAMMA2,
        ).to_corner(UL, buff=0.41)
        title = Text(
            "BREIT-WHEELER PAIR PRODUCTION",
            font_size=32, color=WHITE_SOFT, weight=BOLD,
        ).next_to(eyebrow, DOWN, aligned_edge=LEFT, buff=0.15)
        reaction = MathTex(
            r"\gamma(k_1)+\gamma(k_2)\longrightarrow e^-(p_-)+e^+(p_+)",
            font_size=28, color=MUTED,
        ).next_to(title, DOWN, aligned_edge=LEFT, buff=0.15)
        separator = Line(
            [-6.56, 2.04, 0], [6.56, 2.04, 0],
            color=BORDER, stroke_width=1.4,
        )

        centers = (-3.29, 3.29)
        panels = VGroup(*[
            RoundedRectangle(
                width=6.29, height=4.53, corner_radius=0.14,
                fill_color=PANEL, fill_opacity=1,
                stroke_color=BORDER, stroke_width=1.55,
            ).move_to([cx, -0.32, 0])
            for cx in centers
        ])
        headers = VGroup(
            Text("t-CHANNEL", font_size=22, color=GAMMA1, weight=BOLD)
            .move_to([centers[0], 1.58, 0]),
            Text("u-CHANNEL", font_size=22, color=GAMMA2, weight=BOLD)
            .move_to([centers[1], 1.58, 0]),
        )

        # Banner at bottom, separate from both diagram panels.
        bottom_banner = RoundedRectangle(
            width=13.09, height=0.86, corner_radius=0.13,
            fill_color=PANEL, fill_opacity=1,
            stroke_color=BORDER, stroke_width=1.5,
        ).move_to([0, -3.16, 0])
        summed_amplitude = MathTex(
            r"\mathcal{M}_{\gamma\gamma\to e^-e^+}="
            r"\mathcal{M}_{t}+\mathcal{M}_{u}",
            font_size=38, color=WHITE_SOFT,
        ).move_to(bottom_banner.get_center())
        threshold = MathTex(
            r"s=2\omega_1\omega_2(1-\cos\vartheta)\geq 4m_e^2",
            font_size=35, color=WHITE_SOFT,
        ).move_to(bottom_banner.get_center())
        t = diagram(centers[0], "t")
        u = diagram(centers[1], "u")

        # Header and stage.
        self.play(FadeIn(eyebrow, shift=DOWN * 0.12), run_time=0.55)
        self.play(Write(title), FadeIn(reaction, shift=DOWN * 0.1), run_time=1.15)
        self.play(
            Create(separator), FadeIn(panels), Write(headers),
            FadeIn(bottom_banner),
            run_time=1.15,
        )

        # Reveal first diagram. The visuals build an amplitude, not a time
        # sequence of scattering particles.
        self.play(
            Create(t["photons"][0]), Create(t["photons"][1]),
            *[Create(line) for line in t["charged"]],
            run_time=1.50,
        )
        self.play(
            Create(t["internal"]), FadeIn(t["vertices"]),
            run_time=0.80,
        )
        self.play(
            *[GrowArrow(a) for a in t["momentum"]],
            *[GrowArrow(a) for a in t["flow"]],
            FadeIn(t["labels"]), Write(t["invariant"]),
            run_time=1.30,
        )
        self.play(Indicate(t["internal"], color=INTERNAL), run_time=0.65)

        # Cross the incoming photon attachments to obtain the u-channel.
        # The crossing of wavy lines is NOT a photon-photon vertex.
        self.play(
            Create(u["photons"][0]), Create(u["photons"][1]),
            *[Create(line) for line in u["charged"]],
            run_time=1.50,
        )
        self.play(
            Create(u["internal"]), FadeIn(u["vertices"]),
            run_time=0.80,
        )
        self.play(
            *[GrowArrow(a) for a in u["momentum"]],
            *[GrowArrow(a) for a in u["flow"]],
            FadeIn(u["labels"]), Write(u["invariant"]),
            run_time=1.35,
        )
        self.play(Indicate(u["internal"], color=INTERNAL), run_time=0.65)

        # The physical transition probability depends on the coherent sum.
        self.play(Write(summed_amplitude), run_time=1.20)
        self.wait(1.0)
        self.play(Transform(summed_amplitude, threshold), run_time=1.15)
        self.wait(0.95)
        self.wait(1.8)
