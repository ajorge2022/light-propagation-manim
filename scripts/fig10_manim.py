"""FIGURE 10 — BETHE–HEITLER PAIR PRODUCTION

Manim Community Edition | Light Propagation for Undergraduates

Based on the manuscript's Figure 10 and its Bethe–Heitler subsection:

    gamma(k) + Z(P) -> e-(p_minus) + e+(p_plus) + Z(P_prime)

A nucleus can absorb recoil momentum, which makes pair conversion from a
single real incident photon kinematically possible. The electromagnetic
interaction with the nucleus is represented by a virtual Coulomb photon.

This scene animates TWO representative tree-level photon orderings. They
contain two separate QED vertices joined by a virtual electron propagator.
Neither the virtual photon nor the virtual electron is an on-shell particle,
and the Feynman diagram is not a literal spacetime trajectory.

    q = P - P_prime
    k + P = p_minus + p_plus + P_prime
    E_gamma,th = 2*m_e*c^2 * (1 + m_e/M)

The nuclear mass M is assumed to refer to a target initially at rest and to
an elastic final-state nucleus. This threshold is almost 2*m_e*c^2 for a
heavy nucleus. The geometry, colors and line lengths are schematic, not a
numerical event simulation or a cross-section calculation.

Render:
    manim -pqh figura_10_manim.py Figura10BetheHeitler

Requires Manim Community, NumPy and working LaTeX for MathTex.
"""

from manim import *
import numpy as np

# Same visual language as the preceding figures.
BG = "#0C1524"
PANEL = "#122236"
BORDER = "#2A4058"
WHITE_SOFT = "#F0F7FF"
DIM = "#A2B3C7"
CYAN = "#58DDF7"      # real photon
GOLD = "#FFC478"      # nuclear line / recoil
MINT = "#61E8B0"      # electron / positron lines
PURPLE = "#8795E5"    # virtual Coulomb photon


def fit_width(mobject, maximum):
    """Shrink labels only if they are wider than the available panel."""
    if mobject.width > maximum:
        mobject.scale(maximum / mobject.width)
    return mobject


def photon_wave(start, end, color, cycles=8, amplitude=0.085, width=3.5):
    """Schematic wavy Feynman photon line with exact endpoints."""
    start = np.array(start, dtype=float)
    end = np.array(end, dtype=float)
    direction = end - start
    unit = direction / np.linalg.norm(direction)
    normal = np.array([-unit[1], unit[0], 0.0])

    return ParametricFunction(
        lambda t: start + t * direction
        + amplitude * np.sin(TAU * cycles * t) * normal,
        t_range=[0, 1],
        stroke_color=color,
        stroke_width=width,
    )


class Figura10BetheHeitler(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ----------------------------------------------------------
        # (1) Layout
        # ----------------------------------------------------------
        eyebrow = Text(
            "FIGURE 10   /   QUANTUM ELECTRODYNAMICS",
            font_size=18, color=GOLD,
        ).to_corner(UL, buff=0.45)
        title = Text(
            "BETHE–HEITLER PAIR PRODUCTION",
            font_size=32, weight=BOLD, color=WHITE_SOFT,
        ).next_to(eyebrow, DOWN, aligned_edge=LEFT, buff=0.13)
        subtitle = Text(
            "A real photon creates an electron–positron pair in a nuclear field.",
            font_size=18, color=DIM,
        ).next_to(title, DOWN, aligned_edge=LEFT, buff=0.12)
        rule = Line(
            [-6.55, 2.13, 0], [6.55, 2.13, 0],
            color=BORDER, stroke_width=1.5,
        )

        left_panel = RoundedRectangle(
            width=8.47, height=4.03, corner_radius=0.15,
            stroke_color=BORDER, stroke_width=1.4,
            fill_color=PANEL, fill_opacity=1,
        ).move_to([-2.20, -0.25, 0])
        right_panel = RoundedRectangle(
            width=4.35, height=4.03, corner_radius=0.15,
            stroke_color=BORDER, stroke_width=1.4,
            fill_color=PANEL, fill_opacity=1,
        ).move_to([4.37, -0.25, 0])
        footer = RoundedRectangle(
            width=13.06, height=1.02, corner_radius=0.15,
            stroke_color=BORDER, stroke_width=1.4,
            fill_color=PANEL, fill_opacity=1,
        ).move_to([0.0, -3.07, 0])

        diagram_label = Text(
            "TREE-LEVEL QED DIAGRAM   •   PHOTON ORDERING 1",
            font_size=16, color=WHITE_SOFT,
        ).move_to([-2.2, 1.43, 0])
        panel_label = Text(
            "REACTION AND CONSERVATION LAWS",
            font_size=15, color=WHITE_SOFT,
        ).move_to([4.38, 1.43, 0])

        # ----------------------------------------------------------
        # (2) External and internal lines of a representative
        # Bethe–Heitler diagram.
        # Fermion arrows indicate fermion-number flow, not velocity.
        # ----------------------------------------------------------
        photon_source = np.array([-5.85, 0.91, 0.0])
        nuclear_source = np.array([-5.80, -1.50, 0.0])
        nuclear_vertex = np.array([-3.45, -1.50, 0.0])
        nuclear_exit = np.array([-2.05, -1.70, 0.0])

        vertex_top = np.array([-1.89, 0.32, 0.0])
        vertex_bottom = np.array([-0.73, -0.65, 0.0])
        e_minus_exit = np.array([1.32, 0.98, 0.0])
        e_plus_exit = np.array([1.32, -1.48, 0.0])

        incoming_nucleus = Arrow(
            nuclear_source, nuclear_vertex, buff=0,
            color=GOLD, stroke_width=3.5, tip_length=0.16,
        )
        outgoing_nucleus = Arrow(
            nuclear_vertex, nuclear_exit, buff=0,
            color=GOLD, stroke_width=3.5, tip_length=0.16,
        )
        nucleus_vertex_dot = Dot(
            nuclear_vertex, radius=0.075, color=WHITE_SOFT,
        )

        # Photon order 1: real gamma -> upper QED vertex;
        # virtual Coulomb gamma -> lower QED vertex.
        real_gamma = photon_wave(
            photon_source, vertex_top, CYAN,
            cycles=10, amplitude=0.073,
        )
        virtual_gamma = photon_wave(
            nuclear_vertex, vertex_bottom, PURPLE,
            cycles=7, amplitude=0.058,
        )

        # Standard fermion-arrow convention: flow points towards e- and
        # from the e+ external leg into the diagram.
        positron_leg = Arrow(
            e_plus_exit, vertex_bottom,
            buff=0, color=MINT, stroke_width=3.5, tip_length=0.14,
        )
        electron_propagator = Arrow(
            vertex_bottom, vertex_top,
            buff=0, color=MINT, stroke_width=3.6, tip_length=0.13,
        )
        electron_leg = Arrow(
            vertex_top, e_minus_exit,
            buff=0, color=MINT, stroke_width=3.5, tip_length=0.16,
        )
        qed_vertices = VGroup(
            Dot(vertex_top, radius=0.076, color=WHITE_SOFT),
            Dot(vertex_bottom, radius=0.076, color=WHITE_SOFT),
        )

        nuclear_in_label = MathTex(
            r"Z(P)", font_size=26, color=GOLD,
        ).move_to([-5.17, -1.92, 0])
        nuclear_out_label = MathTex(
            r"Z(P')", font_size=26, color=GOLD,
        ).move_to([-2.04, -1.94, 0])
        photon_label = MathTex(
            r"\gamma(k)", font_size=27, color=CYAN,
        ).move_to([-4.43, 1.05, 0])
        virtual_label = MathTex(
            r"\gamma^*(q)", font_size=26, color=PURPLE,
        ).move_to([-2.35, -0.95, 0])
        electron_label = MathTex(
            r"e^-(p_-)", font_size=25, color=MINT,
        ).move_to([1.18, 1.34, 0])
        positron_label = MathTex(
            r"e^+(p_+)", font_size=25, color=MINT,
        ).move_to([1.20, -1.83, 0])
        propagator_label = Text(
            "virtual electron", font_size=15, color=MINT,
        ).move_to([-0.24, 0.21, 0])

        # ----------------------------------------------------------
        # (3) Physics panel, typeset with the same variables as paper.
        # ----------------------------------------------------------
        process = fit_width(MathTex(
            r"\gamma+Z\rightarrow e^-+e^++Z",
            font_size=31, color=WHITE_SOFT,
        ), 3.94).move_to([4.37, 0.92, 0])

        momentum_heading = Text(
            "FOUR-MOMENTUM CONSERVATION",
            font_size=14, color=DIM,
        ).move_to([4.37, 0.38, 0])
        momentum = fit_width(MathTex(
            r"k^\mu+P^\mu=p_-^\mu+p_+^\mu+P'^\mu",
            font_size=27, color=WHITE_SOFT,
        ), 3.98).move_to([4.37, -0.03, 0])

        transfer_heading = Text(
            "NUCLEAR MOMENTUM TRANSFER",
            font_size=14, color=DIM,
        ).move_to([4.37, -0.57, 0])
        transfer = MathTex(
            r"q^\mu=P^\mu-P'^\mu",
            font_size=30, color=PURPLE,
        ).move_to([4.37, -0.95, 0])

        threshold_heading = Text(
            "THRESHOLD: NUCLEUS INITIALLY AT REST",
            font_size=13, color=DIM,
        ).move_to([4.37, -1.37, 0])
        threshold = fit_width(MathTex(
            r"E_{\gamma,\mathrm{th}}=2m_ec^2"
            r"\left(1+\frac{m_e}{M}\right)",
            font_size=27, color=GOLD,
        ), 3.92).move_to([4.37, -1.76, 0])

        # Footer clarifies the role of the internal lines.
        foot_a = Text(
            "The nucleus absorbs recoil momentum; one free photon cannot create a massive pair in empty space.",
            font_size=17, color=WHITE_SOFT,
        )
        fit_width(foot_a, 12.35)
        foot_a.move_to([0, -2.92, 0])
        foot_b = Text(
            "Virtual lines encode a QED amplitude, not real intermediate particles or classical paths.",
            font_size=15, color=DIM,
        )
        fit_width(foot_b, 12.35)
        foot_b.move_to([0, -3.24, 0])

        # ----------------------------------------------------------
        # (4) Animation sequence
        # ----------------------------------------------------------
        self.play(
            FadeIn(eyebrow, shift=0.1 * DOWN),
            Write(title),
            FadeIn(subtitle),
            Create(rule),
            run_time=1.6,
        )
        self.play(
            FadeIn(left_panel), FadeIn(right_panel), FadeIn(footer),
            FadeIn(diagram_label), FadeIn(panel_label),
            run_time=1.1,
        )

        # Real photon and incoming nucleus.
        self.play(
            Create(real_gamma),
            GrowArrow(incoming_nucleus),
            FadeIn(photon_label), FadeIn(nuclear_in_label),
            run_time=1.6,
        )
        self.play(
            FadeIn(nucleus_vertex_dot),
            GrowArrow(outgoing_nucleus),
            FadeIn(nuclear_out_label),
            run_time=1.0,
        )

        # Virtual Coulomb exchange: it carries the nucleus recoil.
        self.play(
            Create(virtual_gamma), FadeIn(virtual_label),
            run_time=1.2,
        )
        self.play(
            GrowArrow(positron_leg), GrowArrow(electron_propagator),
            GrowArrow(electron_leg), FadeIn(qed_vertices),
            run_time=1.45,
        )
        self.play(
            FadeIn(electron_label), FadeIn(positron_label),
            FadeIn(propagator_label),
            run_time=0.7,
        )

        self.play(Write(process), run_time=0.95)
        self.play(
            FadeIn(momentum_heading), Write(momentum),
            run_time=1.1,
        )
        self.play(
            FadeIn(transfer_heading), Write(transfer),
            run_time=1.0,
        )
        self.play(
            FadeIn(threshold_heading), Write(threshold),
            run_time=1.0,
        )
        self.play(FadeIn(foot_a), FadeIn(foot_b), run_time=0.95)
        self.wait(1.0)

        # (5) The other tree-level Bethe-Heitler amplitude is obtained
        # by interchanging which of the two QED vertices couples to
        # the real photon and which couples to the Coulomb photon.
        other_real_gamma = photon_wave(
            photon_source, vertex_bottom, CYAN,
            cycles=10, amplitude=0.073,
        )
        other_virtual_gamma = photon_wave(
            nuclear_vertex, vertex_top, PURPLE,
            cycles=7, amplitude=0.058,
        )
        ordering_two = Text(
            "TREE-LEVEL QED DIAGRAM   •   PHOTON ORDERING 2",
            font_size=16, color=WHITE_SOFT,
        ).move_to(diagram_label)
        photon_label_two = MathTex(
            r"\gamma(k)", font_size=27, color=CYAN,
        ).move_to([-4.45, 0.92, 0])
        virtual_label_two = MathTex(
            r"\gamma^*(q)", font_size=26, color=PURPLE,
        ).move_to([-3.02, -0.37, 0])

        self.play(
            Transform(diagram_label, ordering_two),
            Transform(real_gamma, other_real_gamma),
            Transform(virtual_gamma, other_virtual_gamma),
            Transform(photon_label, photon_label_two),
            Transform(virtual_label, virtual_label_two),
            run_time=2.2,
        )
        self.wait(0.9)

        # Interference is at the amplitude level: no isolated probability
        # is assigned to either graph before summing the amplitudes.
        sum_amplitudes = MathTex(
            r"\mathcal M_{\rm BH}=\mathcal M_1+\mathcal M_2",
            font_size=29, color=WHITE_SOFT,
        ).move_to([4.37, 0.92, 0])
        fit_width(sum_amplitudes, 3.94)
        self.play(Transform(process, sum_amplitudes), run_time=1.15)
        self.play(Circumscribe(process, color=CYAN, time_width=0.8),
                  run_time=1.5)
        self.wait(1.6)
