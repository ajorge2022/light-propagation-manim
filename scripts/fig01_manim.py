"""Manim Community scene for Figure 1 of 'Light Propagation for Undergraduates'.

Figure 1: Single-slit diffraction (scalar Fraunhofer approximation).

Run:
    manim -pqh figura_01_manim.py Figura01Difraccion

Notes:
- The wavefront circles are a schematic Huygens-style representation.
- The far-field intensity is quantitatively I/I(0) = sinc^2(pi*a*sin(theta)/lambda).
- a/lambda is dimensionless and varied from 8.0 to 3.8.
- This file has been syntax checked, but not rendered with Manim in this environment.
"""
from manim import *
import numpy as np

BG = "#0C1524"
PANEL = "#122236"
LINE = "#2A4058"
WHITE = "#F0F7FF"
DIM = "#A2B3C7"
CYAN = "#58DDF7"
GOLD = "#FFC478"
MINT = "#61E8B0"


def single_slit_intensity(theta, a_over_lambda):
    """Normalized Fraunhofer intensity for a single rectangular slit."""
    return float(np.sinc(a_over_lambda * np.sin(theta)) ** 2)


class Figura01Difraccion(Scene):
    """Single-slit diffraction: incident plane waves, aperture and far-field fringes."""

    def construct(self):
        self.camera.background_color = BG
        aperture = ValueTracker(8.0)  # a/lambda
        clock = ValueTracker(0.0)

        header = Text(
            "FIGURE 01   /   CLASSICAL WAVE OPTICS",
            font="Lato", font_size=19, color=GOLD,
        ).to_corner(UL, buff=0.50)
        title = Text(
            "SINGLE-SLIT DIFFRACTION",
            font="Lato", font_size=34, weight=BOLD, color=WHITE,
        ).align_to(header, LEFT).next_to(header, DOWN, aligned_edge=LEFT, buff=0.15)
        subtitle = Text(
            "A narrower aperture produces a wider diffraction pattern.",
            font="Lato", font_size=20, color=DIM,
        ).align_to(title, LEFT).next_to(title, DOWN, aligned_edge=LEFT, buff=0.12)
        divider = Line([-6.55, 2.18, 0], [6.55, 2.18, 0], color=LINE)

        left_card = RoundedRectangle(
            corner_radius=0.16, width=9.30, height=4.20,
            stroke_color=LINE, stroke_width=1.4, fill_color=PANEL, fill_opacity=1,
        ).move_to([-2.36, -0.12, 0])
        right_card = RoundedRectangle(
            corner_radius=0.16, width=3.75, height=4.20,
            stroke_color=LINE, stroke_width=1.4, fill_color=PANEL, fill_opacity=1,
        ).move_to([4.61, -0.12, 0])
        footer = RoundedRectangle(
            corner_radius=0.16, width=13.15, height=1.28,
            stroke_color=LINE, stroke_width=1.4, fill_color=PANEL, fill_opacity=1,
        ).move_to([0.0, -3.06, 0])

        labels = VGroup(
            Text("INCIDENT PLANE WAVE", font="Lato", font_size=15, color=DIM).move_to([-5.24, 1.60, 0]),
            Text("SLIT", font="Lato", font_size=15, color=DIM).move_to([-2.28, 1.60, 0]),
            Text("SCREEN", font="Lato", font_size=15, color=DIM).move_to([1.64, 1.60, 0]),
            Text("FAR-FIELD INTENSITY", font="Lato", font_size=17, color=WHITE).move_to([4.59, 1.60, 0]),
            Text("Schematic wavefronts", font="Lato", font_size=14, color=DIM).move_to([-3.81, -1.96, 0]),
        )

        yc = -0.12
        bx = -2.42

        def make_barrier():
            gap = 0.11 * aperture.get_value()
            ytop = yc + gap / 2
            ybot = yc - gap / 2
            return VGroup(
                Line([bx, 1.32, 0], [bx, ytop, 0], color=GOLD, stroke_width=9),
                Line([bx, ybot, 0], [bx, -1.80, 0], color=GOLD, stroke_width=9),
                Line([bx-.16, ytop, 0], [bx+.16, ytop, 0], color=WHITE, stroke_width=2),
                Line([bx-.16, ybot, 0], [bx+.16, ybot, 0], color=WHITE, stroke_width=2),
            )

        barrier = always_redraw(make_barrier)

        def incident_waves():
            result = VGroup()
            for j in range(7):
                x = -6.35 + ((j * .62 + clock.get_value() * .62) % 3.7)
                if x < bx - 0.16:
                    result.add(Line([x, 1.17, 0], [x, -1.72, 0],
                                    color=CYAN, stroke_opacity=.55, stroke_width=2))
            return result

        incoming = always_redraw(incident_waves)

        def outgoing_wavefronts():
            wavefronts = VGroup()
            for j in range(7):
                r = ((j * .47 + clock.get_value() * .64) % 3.0) + .08
                if r > 2.8:
                    continue
                arc = Arc(radius=r, start_angle=-PI / 2, angle=PI,
                          arc_center=[bx+.08, yc, 0], color=CYAN,
                          stroke_width=2.0, stroke_opacity=.57)
                wavefronts.add(arc)
            return wavefronts

        outgoing = always_redraw(outgoing_wavefronts)

        theta_max = .32
        graph_x0 = 3.32
        graph_w = 2.62
        graph_yc = -.09
        graph_h = 3.05

        guides = VGroup(
            Line([graph_x0, graph_yc-graph_h/2, 0],
                 [graph_x0, graph_yc+graph_h/2, 0], color=DIM, stroke_width=1),
            Line([graph_x0, graph_yc-graph_h/2, 0],
                 [graph_x0+graph_w, graph_yc-graph_h/2, 0], color=DIM, stroke_width=1),
        )
        for fraction in [0.25, 0.5, 0.75, 1.0]:
            guides.add(Line([graph_x0 + fraction*graph_w, graph_yc-graph_h/2, 0],
                            [graph_x0 + fraction*graph_w, graph_yc+graph_h/2, 0],
                            color=LINE, stroke_opacity=.60))

        axis_labels = VGroup(
            MathTex("I/I(0)", color=DIM, font_size=23).move_to([4.63,-1.84,0]),
            MathTex(r"\theta", color=DIM, font_size=25).move_to([3.05,1.43,0]),
        )

        def make_profile():
            theta = np.linspace(theta_max, -theta_max, 320)
            pts = [
                [graph_x0 + graph_w*single_slit_intensity(th,aperture.get_value()),
                 graph_yc + graph_h*th/(2*theta_max), 0]
                for th in theta
            ]
            path = VMobject(color=CYAN, stroke_width=4)
            path.set_points_as_corners(pts)
            return path

        graph = always_redraw(make_profile)

        # The vertical screen brightness also follows the calculated sinc^2 envelope.
        def make_screen():
            strips = VGroup()
            for i in range(92):
                th = theta_max*(2*i/91-1)
                bright = single_slit_intensity(th,aperture.get_value())
                yy = graph_yc + graph_h*th/(2*theta_max)
                strips.add(Line([1.47,yy,0],[1.75,yy,0],
                                color=interpolate_color(BLUE, YELLOW, bright),
                                stroke_width=4, stroke_opacity=.15+.85*bright))
            return strips

        screen = always_redraw(make_screen)
        screen_border = Rectangle(width=.32,height=graph_h+0.02,
                                  stroke_color=DIM,stroke_width=1,fill_opacity=0)
        screen_border.move_to([1.61,graph_yc,0])

        def make_zeros():
            th0 = np.arcsin(1/aperture.get_value())
            return VGroup(*[
                Dot([graph_x0, graph_yc + graph_h*s*th0/(2*theta_max), 0],
                    radius=.055, color=GOLD)
                for s in (-1,1)
            ])

        zeros = always_redraw(make_zeros)
        formula = MathTex(
            r"I(\theta)=I(0)\left[\frac{\sin\beta}{\beta}\right]^2",
            color=WHITE, font_size=38,
        ).move_to([-4.00,-3.04,0])
        beta = MathTex(r"\beta=\frac{\pi a\sin\theta}{\lambda}",
                       color=WHITE,font_size=37).move_to([0.15,-3.04,0])
        a_label = MathTex(r"a/\lambda=", color=GOLD, font_size=35).move_to([3.99,-3.00,0])
        value = always_redraw(lambda: DecimalNumber(aperture.get_value(),
            num_decimal_places=1, color=WHITE, font_size=38).move_to([5.34,-3.00,0]))
        note = Text("First minimum: sin(theta) = lambda / a",
                    color=DIM,font="Lato",font_size=15).move_to([4.70,-3.51,0])

        self.add(header,title,subtitle,divider,left_card,right_card,footer,
                 labels,guides,axis_labels,screen_border,barrier,incoming,outgoing,
                 screen,graph,zeros,formula,beta,a_label,value,note)
        self.play(clock.animate.set_value(4),run_time=4,rate_func=linear)
        self.play(clock.animate.set_value(9),aperture.animate.set_value(3.8),
                  run_time=5,rate_func=linear)
        self.play(clock.animate.set_value(12),run_time=3,rate_func=linear)
