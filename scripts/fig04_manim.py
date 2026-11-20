"""FIGURE 04 — DISPERSION OF LIGHT THROUGH A PRISM

Manim Community Edition 0.19+.

Animated interpretation of Figure 4 (page 4) of
"Light Propagation for Undergraduates" by A. W. Romero Jorge et al.

Render (1080p):
    manim -pqh figura_04_manim.py Figura04DispersionPrisma
Render (quick test):
    manim -pql figura_04_manim.py Figura04DispersionPrisma

Physics:
    - A ray is refracted at BOTH interfaces using Snell's law.
    - The incident frequency stays constant; n(lambda) gives different
      propagation speeds and hence distinct outgoing directions.
    - Seven representative monochromatic components approximate white light.
    - Reflected power and Fresnel losses are omitted, as in the source sketch.
    - The Cauchy-style index below is ILLUSTRATIVE (not calibrated to glass).
      Its visible-range spread is chosen to make angular dispersion legible.
    - The diagram uses a geometrical-optics (not a full-wave) model.

Coordinates are in Manim scene units. The prism points upwards, so the
emerging rays are deflected down towards the prism's base. Violet deviates
more than red for the assumed normal dispersion.
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
PURPLE = "#8795E5"

# Wavelengths in nm; visible colors are illustrative, not spectral colorimetry.
SPECTRUM = [
    (700.0, "#FF6666", "RED"),
    (630.0, "#FF9C57", "ORANGE"),
    (590.0, "#FFDC70", "YELLOW"),
    (550.0, "#5EE899", "GREEN"),
    (490.0, "#5CE1E6", "CYAN"),
    (440.0, "#668FFF", "BLUE"),
    (400.0, "#BD8BFF", "VIOLET"),
]

# Prism vertices (counterclockwise in the A-C-B path in physical geometry).
LEFT = np.array([-1.40, -1.20, 0.0])
APEX = np.array([0.00, 1.35, 0.0])
RIGHT = np.array([1.40, -1.20, 0.0])

# Intersection of the incoming light with the left prism face.
ENTRY_Y = 0.25
ENTRY = LEFT + ((ENTRY_Y - LEFT[1]) / (APEX[1] - LEFT[1])) * (APEX - LEFT)
THETA_IN = 22 * DEGREES  # angle of incoming ray above the horizontal
D_IN = np.array([np.cos(THETA_IN), np.sin(THETA_IN), 0.0])
SOURCE = ENTRY - 3.02 * D_IN
SCREEN_X = 5.30
AIR_N = 1.0
N_RED = 1.510
FULL_DISPERSION = 0.030


def cross2(a, b):
    return float(a[0] * b[1] - a[1] * b[0])


def unit(v):
    return v / np.linalg.norm(v)


def index_of_refraction(wavelength_nm, dispersion_strength):
    """A pedagogical Cauchy-type dispersion law, n(700 nm) = 1.510."""
    return N_RED + dispersion_strength * ((700.0 / wavelength_nm) ** 2 - 1.0)


def refract(direction, n_from, n_to, normal_to_next_medium):
    """Vector Snell's law (unit normal points into the *next* medium).

    Returns a normalized transmitted vector or None for total internal
    reflection. The geometry below remains below the critical angle.
    """
    d = unit(direction)
    normal = unit(normal_to_next_medium)
    eta = n_from / n_to
    longitudinal = np.dot(d, normal)
    discriminant = 1.0 - eta**2 * (1.0 - longitudinal**2)
    if discriminant < -1e-10:
        return None
    tangential = eta * (d - longitudinal * normal)
    return unit(tangential + np.sqrt(max(0.0, discriminant)) * normal)


def intersect_ray_with_segment(point, direction, first, second):
    """Intersection with the second surface; requires a forward ray hit."""
    edge = second - first
    denominator = cross2(direction, edge)
    if abs(denominator) < 1e-10:
        raise ValueError("Ray is parallel to prism face")
    delta = first - point
    t = cross2(delta, edge) / denominator
    u = cross2(delta, direction) / denominator
    if t <= 0 or not -1e-6 <= u <= 1 + 1e-6:
        raise ValueError("No valid exit-face intersection")
    return point + t * direction


def trace_prism(wavelength_nm, dispersion_strength):
    """Return entrance, exit and screen hit for one monochromatic ray."""
    n_prism = index_of_refraction(wavelength_nm, dispersion_strength)
    left_edge = APEX - LEFT
    normal_in = unit(np.array([left_edge[1], -left_edge[0], 0.0]))
    # The normal on the exit face points from prism to air (right and up).
    right_edge = RIGHT - APEX
    normal_out = unit(np.array([-right_edge[1], right_edge[0], 0.0]))

    direction_inside = refract(D_IN, AIR_N, n_prism, normal_in)
    if direction_inside is None:
        raise ValueError("Unexpected TIR on entry")
    exit_point = intersect_ray_with_segment(
        ENTRY, direction_inside, APEX, RIGHT
    )
    direction_out = refract(direction_inside, n_prism, AIR_N, normal_out)
    if direction_out is None:
        raise ValueError("TIR at prism exit; alter geometry/index model")
    if direction_out[0] <= 0:
        raise ValueError("Emerging light does not move toward the screen")
    screen_t = (SCREEN_X - exit_point[0]) / direction_out[0]
    screen_hit = exit_point + screen_t * direction_out
    return ENTRY.copy(), exit_point, screen_hit, direction_out


class Figura04DispersionPrisma(Scene):
    """Figure 4: wavelength-dependent refraction at two prism surfaces."""

    def construct(self):
        self.camera.background_color = BG
        dispersion = ValueTracker(0.0)
        beam_progress = ValueTracker(0.001)

        # Fixed header positions: keep the three lines separated even when
        # the title is longer than in Figure 03.
        header = Text(
            "FIGURE 04   /   CLASSICAL WAVE OPTICS",
            font="Lato", font_size=19, color=GOLD,
        ).to_edge(LEFT, buff=0.55).set_y(3.55)

        title = Text(
            "DISPERSION OF LIGHT THROUGH A PRISM",
            font="Lato", font_size=32, weight=BOLD, color=WHITE_SOFT,
        )
        # The available horizontal width is 13.33 - 2*0.55 = 12.23.
        # Never enlarge short titles: only shrink titles that would overflow.
        if title.width > 12.20:
            title.scale_to_fit_width(12.20)
        title.to_edge(LEFT, buff=0.55).set_y(2.95)

        subtitle = Text(
            "Different wavelengths refract by different amounts.",
            font="Lato", font_size=19, color=DIM,
        ).to_edge(LEFT, buff=0.55).set_y(2.48)
        if subtitle.width > 12.20:
            subtitle.scale_to_fit_width(12.20)

        divider = Line(
            [-6.56, 2.14, 0], [6.56, 2.14, 0],
            color=BORDER, stroke_width=1.4,
        )
        stage = RoundedRectangle(
            width=13.15, height=4.08, corner_radius=0.16,
            stroke_color=BORDER, stroke_width=1.3,
            fill_color=PANEL, fill_opacity=1,
        ).move_to([0, -0.09, 0])
        footer = RoundedRectangle(
            width=13.15, height=1.28, corner_radius=0.16,
            stroke_color=BORDER, stroke_width=1.3,
            fill_color=PANEL, fill_opacity=1,
        ).move_to([0, -3.03, 0])

        prism_fill = Polygon(
            LEFT, APEX, RIGHT,
            color=PURPLE, stroke_width=3,
            fill_color="#5666A6", fill_opacity=0.23,
        )
        prism_glint = Line(
            LEFT * .20 + APEX * .80, RIGHT * .18 + APEX * .82,
            color=WHITE_SOFT, stroke_width=1.5,
            stroke_opacity=0.45,
        )
        prism_label = Text(
            "DISPERSIVE PRISM", font="Lato", font_size=16,
            color=WHITE_SOFT,
        ).move_to([-0.1, -0.94, 0])
        incident_label = Text(
            "WHITE LIGHT", font="Lato", font_size=18, color=WHITE_SOFT,
        ).move_to([-4.05, -0.39, 0])
        screen = Line(
            [SCREEN_X, 0.60, 0], [SCREEN_X, -1.79, 0],
            color=WHITE_SOFT, stroke_width=5.0,
        )
        screen_label = Text(
            "SCREEN", font="Lato", font_size=16, color=DIM,
        ).move_to([SCREEN_X, 0.92, 0])
        incidence_dot = Dot(ENTRY, radius=0.052, color=WHITE_SOFT)

        # The white incident beam is common to all monochromatic components.
        incident = Arrow(
            SOURCE, ENTRY, buff=0, stroke_width=5.5,
            color=WHITE_SOFT, tip_length=0.14,
        )

        p0, exit0, screen0, _ = trace_prism(700.0, 0.0)
        initial_inside = Line(
            p0, exit0, color=WHITE_SOFT, stroke_width=5.2,
        )
        initial_out = Line(
            exit0, screen0, color=WHITE_SOFT, stroke_width=5.2,
        )

        def fan_rays():
            group = VGroup()
            for wavelength, color, _ in SPECTRUM:
                p, q, end, _ = trace_prism(
                    wavelength, dispersion.get_value()
                )
                group.add(Line(
                    p, q, color=color, stroke_width=3.2,
                    stroke_opacity=0.72,
                ))
                end_animated = q + beam_progress.get_value() * (end - q)
                group.add(Line(
                    q, end_animated, color=color, stroke_width=4.0,
                    stroke_opacity=0.95,
                ))
                if beam_progress.get_value() > 0.995:
                    group.add(Dot(end, radius=0.045, color=color))
            return group

        # One always_redraw object for all ray components is faster than 21
        # individual redraw callbacks.
        chromatic_fan = always_redraw(fan_rays)

        # Legend for the visible spectrum, well away from emerging rays.
        spectrum_label = Text(
            "VISIBLE SPECTRUM", font="Lato", font_size=16, color=DIM,
        ).move_to([3.25, 1.55, 0])
        spectrum_bar = VGroup(*[
            Rectangle(
                width=0.37, height=0.11, stroke_width=0,
                fill_opacity=1, fill_color=colour,
            )
            for _, colour, _ in SPECTRUM
        ]).arrange(RIGHT, buff=0).move_to([3.25, 1.27, 0])
        spectrum_red = Text(
            "700 nm", font="Lato", font_size=14,
            color=SPECTRUM[0][1],
        ).move_to([2.15, 1.04, 0])
        spectrum_violet = Text(
            "400 nm", font="Lato", font_size=14,
            color=SPECTRUM[-1][1],
        ).move_to([4.35, 1.04, 0])

        # Footer: make the normal dispersion clear without identifying a
        # specific substance. D=0 corresponds to no chromatic dispersion.
        equation = MathTex(
            r"n(\lambda)=1.510+D\left[\left(\frac{700\,\mathrm{nm}}{\lambda}\right)^2-1\right]",
            color=WHITE_SOFT, font_size=29,
        ).move_to([-2.72, -2.88, 0])
        d_label = MathTex(
            r"D=", font_size=28, color=GOLD,
        ).move_to([1.93, -2.80, 0])
        d_value = always_redraw(lambda: DecimalNumber(
            dispersion.get_value(),
            num_decimal_places=3, font_size=28,
            color=WHITE_SOFT,
        ).move_to([2.76, -2.80, 0]))
        red_label = MathTex(
            r"n_{700}=1.510", font_size=26,
            color=SPECTRUM[0][1],
        ).move_to([4.51, -2.77, 0])
        violet_label = MathTex(
            r"n_{400}=", font_size=26,
            color=SPECTRUM[-1][1],
        ).move_to([4.05, -3.26, 0])
        violet_value = always_redraw(lambda: DecimalNumber(
            index_of_refraction(400.0, dispersion.get_value()),
            num_decimal_places=3, font_size=27,
            color=WHITE_SOFT,
        ).move_to([5.42, -3.26, 0]))
        note = Text(
            "Illustrative normal-dispersion model; not calibrated to glass",
            font="Lato", font_size=16, color=DIM,
        ).move_to([-2.58, -3.45, 0])

        # ------------------------ ANIMATION -----------------------------
        self.play(
            FadeIn(stage), FadeIn(footer),
            FadeIn(header, shift=.10 * UP), Write(title),
            FadeIn(subtitle), Create(divider), run_time=1.35,
        )
        self.play(
            FadeIn(prism_fill), Create(prism_glint),
            FadeIn(prism_label), Create(screen),
            FadeIn(screen_label), FadeIn(incidence_dot),
            run_time=1.15,
        )
        self.play(Create(incident), FadeIn(incident_label), run_time=1.1)
        self.play(Create(initial_inside), Create(initial_out), run_time=1.2)

        self.play(
            Write(equation), FadeIn(d_label), FadeIn(d_value),
            FadeIn(red_label), FadeIn(violet_label),
            FadeIn(violet_value), FadeIn(note),
            FadeIn(spectrum_label), FadeIn(spectrum_bar),
            FadeIn(spectrum_red), FadeIn(spectrum_violet),
            run_time=1.15,
        )

        # First emerge together, then split continuously as D increases.
        self.add(chromatic_fan)
        self.play(
            FadeOut(initial_inside), FadeOut(initial_out),
            beam_progress.animate.set_value(1.0),
            dispersion.animate.set_value(FULL_DISPERSION),
            run_time=3.3, rate_func=smooth,
        )
        self.wait(1.0)
        # Visual comparison: remove and restore the dispersion.
        self.play(
            dispersion.animate.set_value(0.0),
            run_time=2.0, rate_func=smooth,
        )
        self.play(
            dispersion.animate.set_value(FULL_DISPERSION),
            run_time=2.3, rate_func=smooth,
        )
        self.wait(1.0)
