# Lecture 1 artefacts: From Physical Signals to Data in Memory

Runnable code for **[Lecture 1: From Physical Signals to Data in Memory](https://tim.jyu.fi/view/kurssit/it/iseai/26-27/introduction-to-it/01-digitization/lesson.md)**.

Everything here is plain Python and `numpy`. 

---

## Get started (5 minutes)

```bash
pip install -r requirements.txt
```

```bash
python make_assets.py
```

```bash
python check_setup.py
```

If `check_setup.py` prints **All good**, you are ready. `matplotlib` is
optional — every script prints its results as numbers and only *adds* a picture
if matplotlib is installed.

---

## What is here

| File | What it does | Lecture section |
|---|---|---|
| `sslab.py` | The whole toolkit for sound: make a signal, sample it, quantize it, filter it, measure it. ~15 small functions. | all |
| `imlab.py` | The same toolkit for pictures. Every function has a twin in `sslab.py`, because an image is a signal sampled in space. | all |
| `wavtools.py` | Read and write `.wav` files with the standard library. A WAV really is a 44-byte header plus samples. | 5 |
| `check_setup.py` | Run first. Confirms Python, numpy, and that the maths works on your machine. | — |
| `make_assets.py` | Builds the sound files the labs use, and prints how big each one *should* be. | 5 |
| `demo_01_sampling.py` | One sine, three sampling rates. Making **time** discrete. | 2.1–2.2 |
| `demo_02_aliasing.py` | Three different tones, one identical set of numbers. The folding rule and the wagon wheel. | 2.3 |
| `demo_03_quantization.py` | A 3-bit quantizer sample by sample; the ~6 dB-per-bit law; clipping and dither. | 2.4 |
| `demo_04_full_chain.py` | The whole loop: a 3 kHz whine deleted by five lines of arithmetic, +40 dB. | 3.3 |
| `demo_05_reconstruction.py` | When reconstruction is faithful, and when it confidently lies. | 4.2 |
| `demo_06_data_rates.py` | Why raw 1080p is 1.49 Gbit/s, and where that number was decided. | 5 |
| `demo_07_image_pipeline.py` | The whole loop again, in pictures: moire, banding, and the folding rule predicting both. Runs on your own photo. | 2–5 |
| `lab01a_starter.py` | **Lab 1A** — familiarize. Three small TODOs. | — |
| `lab01b_starter.py` | **Lab 1B** — the graded core. Self-checks included. | — |
| `lab01c_starter.py` | **Lab 1C** — the optional challenge. | — |
| `lab01d_starter.py` | **Lab 1D** — your own phone photo through the whole loop. | — |
| `live_demo/` | **The projector demo.** One web page running the whole chain live, with knobs. See [live_demo/README.md](live_demo/README.md). | all |
| `network_demo/` | **The two-computer demo.** Voice from one laptop to another over WiFi, with the packets on screen. See [network_demo/README.md](network_demo/README.md). | 3.1, Part 5 |
| `templates/` | Report and AI-log templates you must fill in. | — |

The demo scripts reproduce the numbers printed in the lecture exactly — the
`+40.1 dB` clean-up of §3.3 and the `3.0 / 3.0 / 2.0 Hz` reconstruction table
of §4.2 come out of `demo_04` and `demo_05` as they stand. If you change a
parameter and the numbers move, that is the experiment working.

## The live demo

Before or after the scripts, run the whole pipeline in real time and turn the
knobs yourself:

```bash
python -m http.server 8000 --directory live_demo
```

Open <http://localhost:8000/voice_pipeline.html>, press Start, and drag the test
tone past half the sampling rate. The lecture choreography is in
[live_demo/README.md](live_demo/README.md).

## Two computers, one voice

Run the chain across an actual network — microphone on one laptop, loudspeaker
on another, packets visible in between:

```bash
python network_demo/relay.py
```

It prints the addresses to open on each machine. Full runbook:
[network_demo/README.md](network_demo/README.md).

## Suggested order

1. `python demo_01_sampling.py` — what sampling *is*
2. `python demo_02_aliasing.py` — what goes wrong, irreversibly
3. `python demo_03_quantization.py` — the error you can never remove
4. `python demo_04_full_chain.py` — why we put up with all of it
5. `python demo_05_reconstruction.py` — getting back out to the world
6. `python demo_06_data_rates.py` — the bill
7. `python demo_07_image_pipeline.py` — the same loop, in pictures

Then start `lab01a_starter.py`.

Demo 7 also runs on a photo of your own, which is the version worth seeing:

```bash
python demo_07_image_pipeline.py my_photo.jpg
```


## Reading the code

Start with `sslab.py`. Every function is under fifteen lines and does exactly
one thing from the lecture:

```python
import sslab

t, x = sslab.sine(440.0, duration_s=1.0, fs_hz=44100)   # a signal
xq, q = sslab.quantize(x, n_bits=8)                     # amplitude -> levels
print(sslab.snr_db(x, xq))                              # how much did we lose?
print(sslab.alias_frequency(6000, 8000))                # -> 2000.0
```

The image toolkit reads the same way, one dimension further:

```python
import imlab

photo = imlab.load_image("my_photo.jpg", max_side=512, grey=True)  # a grid of numbers
small = imlab.downsample(photo, 4, prefilter=True)                 # sample it, filter first
back  = imlab.upsample_bilinear(small, 4)                          # reconstruct it
print(imlab.psnr(photo, back))                                     # how much survived?
```


## Common Troubleshooting Issues

- **`ModuleNotFoundError: No module named 'sslab'`**  run the scripts from
  inside this folder, not from the repository root.
- **`FileNotFoundError: assets/tone_a440.wav`**  run `python make_assets.py`.
- **No pictures appear** — install matplotlib (`pip install matplotlib`). The
  scripts save PNGs into `assets/`; they never open a window.
- **The WAV files sound wrong** — check the peak amplitude. Anything beyond
  ±1.0 is clipped on the way to the file, exactly as a real converter clips.
- **`ImportError: this needs Pillow`**  the image demo and Lab 1D read real
  image files: `pip install pillow`.
- **The image demo is slow on my photo** it shrinks anything huge to 512
  pixels first. If you removed that, a 12-megapixel photo will take a while;
  put `max_side=512` back.
