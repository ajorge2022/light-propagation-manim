"""Figure 13 — Photon splitting in an external magnetic field.

Manim Community scene for the article "Light Propagation for Undergraduates".

Physics represented:
    gamma -> gamma + gamma, ASSISTED by an external magnetic field.

The original Figure 13 is a triangular charged-fermion-loop diagram with
three external photon legs (one incoming and two outgoing). The animation
first constructs this representative one-loop topology, then switches to
an explicitly SCHEMATIC real-space view of photon splitting in B.

The two pictures are not the same: the internal Feynman fermion lines are
VIRTUAL PROPAGATORS, not spatial electron/positron trajectories. The order
in which they are drawn is not a physical time ordering. The background
field is necessary: an isolated real photon cannot split into two real
photons in otherwise empty Lorentz-invariant vacuum.

The paper gives, for sufficiently slowly varying subcritical B and
low-energy probe photons, a PARAMETRIC (not numerically normalized) rate:

    kappa_split ~ (alpha^3 / lambda_C_bar) * (B / B_Q)^6
                   * (hbar*omega / (m_e*c^2))^5 * F(theta, polarization)

This does NOT claim every polarization channel is allowed. The geometry,
field strength and photon angles in the picture are schematic and NOT
scaled to real experimental numbers. Doubling B increases the leading
weak-field rate by 2^6 = 64 for fixed energy, angle and an allowed mode.

Full HD: python -m manim -pqh figura_13_manim.py Figura13PhotonSplitting
Quick:   python -m manim -pql figura_13_manim.py Figura13PhotonSplitting

Requirements: Manim Community, NumPy and LaTeX (for MathTex).
"""

from manim import *
import numpy as np


# Same visual design as Figures 8–12.
BG = "#0C1524"
PANEL = "#122236"
BORDER = "#2A4058"
WHITE_SOFT = "#F0F7FF"
DIM = "#A2B3C7"
CYAN = "#58DDF7"       # incoming photon
GOLD = "#FFC478"       # outgoing photons
MINT = "#61E8B0"       # virtual charged-fermion propagators
PURPLE = "#A79EFF"     # external magnetic field


def fit_width(mobject, max_width):
    """Shrink an object to fit; never magnify a small equation."""
    if mobject.width > max_width:
        mobject.scale(max_width / mobject.width)
    return mobject


def photon_wave(start, end, color, oscillations=8, amplitude=0.075):
    """Smooth sinusoidal photon-line symbol between two vertices."""
    start = np.array(start, dtype=float)
    end = np.array(end, dtype=float)
    delta = end - start
    length = np.linalg.norm(delta)
    if length < 1.0e-10:
        raise ValueError("Photon line must have nonzero length")
    direction = delta / length
    normal = np.array([-direction[1], direction[0], 0.0])
    ts = np.linspace(0.0, 1.0, 181)
    points = [
        start + t * delta + amplitude * np.sin(TAU * oscillations * t) * normal
        for t in ts
    ]
    wave = VMobject()
    wave.set_points_smoothly(points)
    wave.set_stroke(color=color, width=3.3)
    return wave


def fermion_arrow(start, end):
    """A small arrow marking oriented fermion-number flow in the loop."""
    p, q = np.array(start, dtype=float), np.array(end, dtype=float)
    return Arrow(
        p + 0.41 * (q - p),
        p + 0.61 * (q - p),
        color=MINT, buff=0, stroke_width=3.3, tip_length=0.13,
        max_tip_length_to_length_ratio=0.5,
    )


def magnetic_field_arrows():
    """Vertical B-field indicators behind the diagram, not photon legs."""
    field = VGroup()
    for x in [-5.38, -4.60, -3.80, -2.97, -2.14, -1.31, -0.48, 0.35, 1.10]:
        a = Arrow(
            [x, -1.96, 0], [x, 0.98, 0],
            buff=0, color=PURPLE, stroke_width=2.1,
            tip_length=0.14,
            max_tip_length_to_length_ratio=0.08,
        )
        a.set_opacity(0.15)
        field.add(a)
    return field


class Figura13PhotonSplitting(Scene):
    """Feynman triangle -> field-assisted splitting -> B^6 scaling."""

    def construct(self):
        self.camera.background_color = BG

        # ----------------------------------------------------------
        # 1) Header and layout, consistent with earlier figures.
        # ----------------------------------------------------------
        eyebrow = Text(
            "FIGURE 13   /   QUANTUM ELECTRODYNAMICS",
            font_size=18, color=GOLD,
        ).to_corner(UL, buff=0.42)
        title = Text(
            "PHOTON SPLITTING IN A MAGNETIC FIELD",
            font_size=32, weight=BOLD, color=WHITE_SOFT,
        ).next_to(eyebrow, DOWN, aligned_edge=LEFT, buff=0.13)
        title = fit_width(title, 12.8)
        subtitle = Text(
            "A magnetic background can enable a polarization-dependent photon splitting process.",
            font_size=18, color=DIM,
        ).next_to(title, DOWN, aligned_edge=LEFT, buff=0.13)
        subtitle = fit_width(subtitle, 12.7)
        top_rule = Line(
            [-6.55, 2.13, 0], [6.55, 2.13, 0],
            stroke_color=BORDER, stroke_width=1.5,
        )

        left_center = np.array([-2.18, -0.24, 0.0])
        right_center = np.array([4.37, -0.24, 0.0])
        left_panel = RoundedRectangle(
            width=8.48, height=4.03, corner_radius=0.15,
            stroke_color=BORDER, stroke_width=1.5,
            fill_color=PANEL, fill_opacity=1,
        ).move_to(left_center)
        right_panel = RoundedRectangle(
            width=4.33, height=4.03, corner_radius=0.15,
            stroke_color=BORDER, stroke_width=1.5,
            fill_color=PANEL, fill_opacity=1,
        ).move_to(right_center)
        footer = RoundedRectangle(
            width=13.05, height=1.06, corner_radius=0.15,
            stroke_color=BORDER, stroke_width=1.4,
            fill_color=PANEL, fill_opacity=1,
        ).move_to([0, -3.06, 0])

        diag_header = Text(
            "ONE-LOOP SCHEMATIC DIAGRAM",
            font_size=16, color=WHITE_SOFT,
        ).move_to([-2.18, 1.44, 0])
        right_header = Text(
            "FIELD-ASSISTED PROCESS",
            font_size=16, color=WHITE_SOFT,
        ).move_to([4.37, 1.44, 0])

        self.play(
            FadeIn(eyebrow, shift=UP * 0.08),
            Write(title), FadeIn(subtitle), Create(top_rule),
            run_time=1.5,
        )
        self.play(
            FadeIn(left_panel), FadeIn(right_panel), FadeIn(footer),
            FadeIn(diag_header), FadeIn(right_header),
            run_time=0.9,
        )

        # ----------------------------------------------------------
        # 2) Triangle diagram with three external photon legs.
        #    The virtual charged lines form a CLOSED loop, not a
        #    literal e+e- pair moving through ordinary space.
        # ----------------------------------------------------------
        external_field = magnetic_field_arrows()
        b_caption = MathTex(
            r"\mathbf B_{\rm ext}", color=PURPLE, font_size=29,
        ).move_to([1.06, 0.95, 0])
        self.play(FadeIn(external_field), FadeIn(b_caption), run_time=0.8)

        vertex_in = np.array([-3.97, -0.30, 0])
        vertex_top = np.array([-1.66, 0.59, 0])
        vertex_bottom = np.array([-1.66, -1.18, 0])

        p_in = photon_wave([-6.05, -0.30, 0], vertex_in, CYAN)
        p_top = photon_wave(vertex_top, [0.77, 0.93, 0], GOLD)
        p_bottom = photon_wave(vertex_bottom, [0.77, -1.74, 0], GOLD)

        fermion_1 = Line(vertex_in, vertex_top, stroke_color=MINT, stroke_width=3.6)
        fermion_2 = Line(vertex_top, vertex_bottom, stroke_color=MINT, stroke_width=3.6)
        fermion_3 = Line(vertex_bottom, vertex_in, stroke_color=MINT, stroke_width=3.6)
        fermions = VGroup(fermion_1, fermion_2, fermion_3)
        flow = VGroup(
            fermion_arrow(vertex_in, vertex_top),
            fermion_arrow(vertex_top, vertex_bottom),
            fermion_arrow(vertex_bottom, vertex_in),
        )
        vertices = VGroup(*[
            Dot(v, radius=0.060, color=WHITE_SOFT)
            for v in (vertex_in, vertex_top, vertex_bottom)
        ])

        in_label = MathTex(r"\gamma(k)", font_size=26, color=CYAN)
        in_label.move_to([-5.00, 0.09, 0])
        out1_label = MathTex(r"\gamma(k_1)", font_size=25, color=GOLD)
        out1_label.move_to([0.02, 1.18, 0])
        out2_label = MathTex(r"\gamma(k_2)", font_size=25, color=GOLD)
        out2_label.move_to([0.00, -1.98, 0])
        internal_label = Text(
            "virtual charged\nfermion loop",
            font_size=15, color=MINT, line_spacing=0.9,
        ).move_to([-2.75, -0.30, 0])

        self.play(Create(p_in), FadeIn(in_label), run_time=1.0)
        self.play(
            LaggedStart(*[Create(edge) for edge in fermions], lag_ratio=0.27),
            run_time=1.9,
        )
        self.play(FadeIn(vertices), FadeIn(flow), FadeIn(internal_label), run_time=0.8)
        self.play(
            Create(p_top), Create(p_bottom),
            FadeIn(out1_label), FadeIn(out2_label),
            run_time=1.5,
        )

        # Right panel: the external field is essential, and selection
        # rules decide which polarization channels are nonzero.
        reaction = MathTex(
            r"\gamma\;\longrightarrow\;\gamma+\gamma",
            color=WHITE_SOFT, font_size=37,
        ).move_to([4.37, 0.75, 0])
        assisted = Text(
            "Requires an external background",
            color=PURPLE, font_size=17,
        ).move_to([4.37, 0.08, 0])
        selection = Text(
            "Polarization selection rules apply",
            color=GOLD, font_size=16,
        ).move_to([4.37, -0.39, 0])
        caveat1 = Text(
            "Not a spontaneous decay",
            color=DIM, font_size=17,
        ).move_to([4.37, -1.04, 0])
        caveat2 = Text(
            "in an otherwise empty vacuum",
            color=DIM, font_size=16,
        ).move_to([4.37, -1.36, 0])
        self.play(Write(reaction), run_time=1.15)
        self.play(
            FadeIn(assisted), FadeIn(selection),
            FadeIn(caveat1), FadeIn(caveat2),
            run_time=1.15,
        )

        # The paper's leading weak-field/low-energy parametric scaling.
        # Split the formula across the footer to avoid microscopic type.
        scaling = MathTex(
            r"\kappa_{\rm split}\sim\frac{\alpha^3}{\bar\lambda_C}"
            r"\left(\frac{B}{B_{\rm Q}}\right)^6"
            r"\left(\frac{\hbar\omega}{m_e c^2}\right)^5"
            r"\mathcal F(\vartheta,\mathrm{polarization})",
            font_size=28, color=WHITE_SOFT,
        )
        fit_width(scaling, 12.35)
        scaling.move_to([0, -2.95, 0])
        regime = Text(
            "Parametric scaling only  |  slowly varying subcritical field  |  low-energy photons  |  allowed modes",
            font_size=14, color=DIM,
        ).move_to([0, -3.35, 0])
        fit_width(regime, 12.3)
        self.play(Write(scaling), FadeIn(regime), run_time=2.4)
        self.wait(1.0)

        # ----------------------------------------------------------
        # 3) Replace the Feynman diagram with a separate schematic
        #    picture of the splitting EVENT in the background field.
        #    Neither drawing gives physical emission angles or rates.
        # ----------------------------------------------------------
        diagram = VGroup(
            p_in, p_top, p_bottom, fermions, flow, vertices,
            in_label, out1_label, out2_label, internal_label,
        )
        splitting_header = Text(
            "SCHEMATIC PHOTON-SPLITTING EVENT",
            font_size=16, color=WHITE_SOFT,
        ).move_to([-2.18, 1.44, 0])
        self.play(
            FadeOut(diagram), ReplacementTransform(diag_header, splitting_header),
            run_time=0.95,
        )

        split_vertex = np.array([-2.85, -0.32, 0])
        incident_path = Line([-5.86, -0.32, 0], split_vertex)
        upper_path = Line(split_vertex, [0.67, 0.73, 0])
        lower_path = Line(split_vertex, [0.67, -1.41, 0])
        incident_track = DashedLine(
            incident_path.get_start(), incident_path.get_end(),
            dash_length=0.14, color=CYAN, stroke_width=1.5,
        ).set_opacity(0.25)
        upper_track = DashedLine(
            upper_path.get_start(), upper_path.get_end(),
            dash_length=0.14, color=GOLD, stroke_width=1.5,
        ).set_opacity(0.25)
        lower_track = DashedLine(
            lower_path.get_start(), lower_path.get_end(),
            dash_length=0.14, color=GOLD, stroke_width=1.5,
        ).set_opacity(0.25)
        interaction = Dot(split_vertex, radius=0.10, color=WHITE_SOFT)
        interaction_halo = Circle(
            radius=0.32, color=PURPLE, stroke_width=2,
        ).move_to(split_vertex).set_opacity(0.55)
        schematic_note = Text(
            "Schematic only: angles and positions not to scale",
            font_size=14, color=DIM,
        ).move_to([-2.18, -2.00, 0])

        self.play(
            FadeIn(incident_track), FadeIn(upper_track),
            FadeIn(lower_track), FadeIn(interaction_halo),
            FadeIn(schematic_note),
            run_time=0.7,
        )
        incoming_packet = Dot(incident_path.get_start(), radius=0.11, color=CYAN)
        self.add(incoming_packet)
        self.play(MoveAlongPath(incoming_packet, incident_path), run_time=2.1,
                  rate_func=linear)
        self.play(
            FadeOut(incoming_packet), FadeIn(interaction),
            Flash(split_vertex, color=PURPLE, line_length=0.20,
                  flash_radius=0.30, num_lines=12),
            run_time=0.65,
        )
        first_out = Dot(split_vertex, radius=0.11, color=GOLD)
        second_out = Dot(split_vertex, radius=0.11, color=GOLD)
        self.add(first_out, second_out)
        self.play(
            MoveAlongPath(first_out, upper_path),
            MoveAlongPath(second_out, lower_path),
            run_time=2.2, rate_func=linear,
        )
        out_label_a = MathTex(r"\gamma_1", color=GOLD, font_size=27)
        out_label_a.next_to(first_out, UP, buff=0.14)
        out_label_b = MathTex(r"\gamma_2", color=GOLD, font_size=27)
        out_label_b.next_to(second_out, DOWN, buff=0.14)
        self.play(FadeIn(out_label_a), FadeIn(out_label_b), run_time=0.7)
        self.wait(0.8)

        # ----------------------------------------------------------
        # 4) Visualize the B^6 dependence WITHOUT implying a physical
        #    numerical probability (the coefficient F is unspecified).
        # ----------------------------------------------------------
        scaling_title = Text(
            "WEAK-FIELD DEPENDENCE",
            font_size=16, color=WHITE_SOFT,
        ).move_to([4.37, 1.44, 0])
        self.play(
            FadeOut(VGroup(reaction, assisted, selection, caveat1, caveat2)),
            ReplacementTransform(right_header, scaling_title),
            run_time=0.9,
        )

        b6 = MathTex(
            r"\kappa_{\rm split}\propto B^6",
            font_size=36, color=WHITE_SOFT,
        ).move_to([4.37, 0.77, 0])
        b_1 = MathTex(r"B", color=PURPLE, font_size=29)
        b_2 = MathTex(r"2B", color=PURPLE, font_size=29)
        b_1.move_to([3.37, -0.01, 0])
        b_2.move_to([5.35, -0.01, 0])
        divider = Line(
            [4.37, 0.24, 0], [4.37, -0.45, 0],
            stroke_color=BORDER, stroke_width=1.2,
        )
        ratio = MathTex(
            r"\frac{\kappa(2B)}{\kappa(B)}=2^6=64",
            font_size=33, color=GOLD,
        ).move_to([4.37, -0.93, 0])
        disclaimer = Text(
            "Fixed energy, geometry and allowed mode",
            font_size=15, color=DIM,
        ).move_to([4.37, -1.72, 0])
        fit_width(disclaimer, 3.95)
        self.play(Write(b6), run_time=1.0)
        self.play(FadeIn(b_1), FadeIn(b_2), Create(divider), run_time=0.7)
        self.play(Write(ratio), FadeIn(disclaimer), run_time=1.4)
        self.play(Indicate(ratio, color=GOLD, scale_factor=1.08), run_time=1.2)
        self.wait(1.7)


# Optional short alias: python -m manim -pqh figura_13_manim.py fig13
class fig13(Figura13PhotonSplitting):
    pass
