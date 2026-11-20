# Light Propagation for Undergraduates — Manim Animations

Companion repository with **13 Manim animations**, one for each figure of the paper *Light Propagation for Undergraduates*.

**Naming conventions:** The source scripts and MP4 filenames listed below match the author's exported files exactly, including uppercase/lowercase. Do not rename them before uploading.

## Import your already-rendered files (recommended)

You already have the 13 MP4 files and the corresponding Manim `.py` scripts together in one directory on your computer.

1. Extract this repository ZIP.
2. Open a terminal in the `light-propagation-manim` directory.
3. Run (replace the path with your local folder):

   ```bash
   python import_local_assets.py "C:\Users\YourName\Videos\LightAnimations"
   ```

4. Check that `scripts/` now contains `fig01_manim.py` to `fig13_manim.py`, and `docs/videos/` contains the actual `Fig01_*.mp4` to `Fig13_*.mp4` videos.
5. Commit and push to GitHub. The HTML pages refer directly to those exact filenames.

The ZIP does **not** include the final MP4 exports from your computer. The included Python scripts are the prior working copies; the import command replaces them with your locally finalized scripts.

If you prefer, manually copy each file into `scripts/` and `docs/videos/` using the table below.

## Exact file mapping

| Figure | Topic | MP4 filename (`docs/videos/`) | Source (`scripts/`) | Manim scene |
|:--|:--|:--|:--|:--|
| 01 | Single-slit diffraction | `Fig01_Single_slit_diffraction.mp4` | `fig01_manim.py` | `Figura01Difraccion` |
| 02 | Law of reflection | `Fig02_Law_of_Reflection.mp4` | `fig02_manim.py` | `Figura02Reflexion` |
| 03 | Refraction and Snell's law | `Fig03_Refraction.mp4` | `fig03_manim.py` | `Figura03Refraccion` |
| 04 | Dispersion of light through a prism | `Fig04_Dispersion_Prism.mp4` | `fig04_manim.py` | `Figura04DispersionPrisma` |
| 05 | Linear polarization and Malus's law | `Fig05_Linear_Polarization.mp4` | `fig05_manim.py` | `Figura05PolarizacionMalus` |
| 06 | Material birefringence | `Fig06_Birefringence.mp4` | `fig06_manim.py` | `Figura06Birrefringencia` |
| 07 | Compton scattering | `Fig07_Compton_Scattering.mp4` | `fig07_manim.py` | `Figura07Compton` |
| 08 | QED Compton scattering: s- and u-channels | `Fig08_Compton_QED.mp4` | `fig08_manim.py` | `Figura08ComptonQED` |
| 09 | Breit–Wheeler pair production | `Fig09_Breit_Wheeler.mp4` | `fig09_manim.py` | `Figura09BreitWheeler` |
| 10 | Bethe–Heitler pair production | `Fig10_Bethe_Heitler.mp4` | `fig10_manim.py` | `Figura10BetheHeitler` |
| 11 | Light-by-light scattering | `Fig11_Light_Light_Scattering.mp4` | `fig11_manim.py` | `Figura11LightByLight` |
| 12 | Vacuum polarization | `Fig12_Vacuum_Polarization.mp4` | `fig12_manim.py` | `Figura12VacuumPolarization` |
| 13 | Photon splitting in an external magnetic field | `Fig13_Photon_Splitting.mp4` | `fig13_manim.py` | `Figura13PhotonSplitting` |

## Web gallery and links in the paper

The home page displays silent inline video previews for all 13 figures. Individual pages provide full playback, video downloads, and source-code links to the public GitHub scripts.

The LaTeX manuscript in `manuscript/Light_Propagation_with_animation_links.tex` links to the individual **HTML pages**, so **the figure links do not need to change** just because the MP4 filenames have changed. The website uses the GitHub account `ajorge2022`.

- Repository: `https://github.com/ajorge2022/light-propagation-manim`
- Gallery: `https://ajorge2022.github.io/light-propagation-manim/`
- Figure 01: `https://ajorge2022.github.io/light-propagation-manim/fig01.html`
- Figure 13: `https://ajorge2022.github.io/light-propagation-manim/fig13.html`

**Enable GitHub Pages:** Settings → Pages → Deploy from a branch → `main` → `/docs`.

## If you need to render again

Install Manim Community and LaTeX/ffmpeg dependencies. For one figure:

```bash
python -m manim -pqh scripts/fig01_manim.py Figura01Difraccion
```

To create all MP4s with the exact filenames in the table, run:

```bash
python render_all.py --quality high
```

Or a single figure:

```bash
python render_all.py --quality high --figure 6
```

`render_all.py` writes the MP4s to `docs/videos/`. It is optional if you already imported your final MP4s.

## Publishing checks

- Verify 13 MP4 videos and 13 `.py` source files in the correct folders.
- Play the videos in GitHub Pages and test the 13 download/code links.
- Inspect the scientific content and labels. The original supplied scripts have not all been rendered and validated in Manim in this environment.
- If any MP4 is too large for GitHub, consider an optimized encode or a suitable external archive; GitHub's ordinary Git size limit is 100 MiB per file.
- Keep the repository public before claiming open availability in the paper.
- Consider archiving a stable GitHub release on Zenodo to obtain a DOI.

## Licensing

The source code in `scripts/` is under the MIT license (`LICENSE`). The media license proposal is CC BY 4.0 (`MEDIA_LICENSE.md`). Confirm authors' consent and rights before publishing.
