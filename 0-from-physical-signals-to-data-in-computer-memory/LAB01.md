# Lab 1 — Signals & Systems

Three levels, plus one for fun. 

- **A** familiarizes you (low stakes).
- **B** contains core tasks of the lecture and requires reasoning,
- **C** is the challenge that demands rigor
- **D** repeats the whole lecture on a photograph you took with your own phone.

## Course Policy for Lab Completion

- Aim to complete **A and B level labs on the same day** as the lab session.
- **C level labs are advanced challenges**. It is meant to encourage your own exploration. For example, it may contain a term not included in the lecture text. This would be a perfect place for the use of AI assistant to find information about this. You may submit C-level lab  them later (within the course period) after you have mastered the required concepts.
- In industry at your job, you may not know know all things needed for the job. You should be able to learn what needs to be learned for the job at hand by finding the relevant knowledge sources. C level labs will foster this habit.
- Completing every C level lab is **not mandatory** for assessment.
- However, successfully completing all C level challenges demonstrates advanced understanding and strong performance, and you are highly encouraged to make an attempt.

---

**Setup** (once):

```bash
pip install -r requirements.txt
```

```bash
python make_assets.py
```

```bash
python check_setup.py
```

**Code Deliverables via Gitlab** go in a `lab01/` folder containing:

```
lab01/
├── README.md            # what you did, how to run it
├── lab01a_starter.py    # your modified/completed copies
├── lab01b_starter.py    # your modified/completed copies
├── lab01c_starter.py    # your modified/completed copies
├── any other files you generated
└── figures/             # any plots you produced
```
**Rememeber: Report per lab and AI-log go to TIM.**

---

## Lab 1A — "Watch the world become numbers"

*Level: Familiarize yourself (do it individually or in a group. Getting help from peer or instructor is okay)*

Run `python lab01a_starter.py` and work through its three TODOs.

1. **Sample a sine wave** at 4, 8 and 50 Hz and look at the numbers you
   actually stored. Which rates satisfy Nyquist for a 1 Hz tone?
2. **Open a real 16-bit WAV file.** Read its sample rate, bit depth, channel
   count and duration. Predict its size in bytes *before* you look, then
   compare. (You will be 44 bytes short. Note what that header is for.)
3. **Make a sound louder and quieter with arithmetic alone** — multiply the
   samples by 2 and by 0.5, write the WAVs, and listen. Then multiply by 4 and
   listen to what happens when you leave the range.

**Report** (`lab01a_report.md`, roughly one page): answer Q1, Q2 and Q3 printed by the script, in your own words.

**Learning outcomes.** In your report, describe sampling as measurement at instants; relate a media file's size to its rate and bit depth; experience "processing is arithmetic" first-hand.

---

## Lab 1B — "Make aliasing and quantization happen"

*Core tasks. Do it in a group of 2.*

Now you produce the phenomena yourself. Work in `lab01b_starter.py`; the
self-checks at the bottom of the file tell you whether your numbers are right.They do not grade your explanations.

1. **Alias on purpose.** Choose a sampling rate and two distinct tone
   frequencies: 1) one below the Nyquist frequency, 2) one above whose samples come out numerically **identical**. Print both vectors and show they match. State the folding-rule prediction by hand first, then confirm it.
2. **Quantize and measure.** Write your own *N*-bit quantizer (do not call `sslab.quantize` for this part — build it). For *N* = 4, 8, 12, 16 report the measured SNR next to 6.02*N* + 1.76 dB in a table, and explain the ~6 dB-per-bit  trend in one paragraph.
3. **Reconcile a data rate.** Pick one row of the lecture's Part-5 table,
   recompute its raw data rate from first principles, and reconcile it against a  real file you create or download. Account for any difference.

**Report** (`lab01b_report.md`): the three tables, the three answers, and one paragraph naming the exact moment at which aliased information is lost. Include names of group members in the report at the very begining.

**Learning outcomes.**
   - Demonstrate and predict aliasing from the folding rule.
   - implement a quantizer and empirically confirm the SNR law; compute a media data rate and reconcile it with reality.

**Before you submit:** every self-check line prints `PASS`.

---

## Lab 1C — "Build the whole loop"

*Challenge level. Do it in a  group of 2-4. Seeking AI assistant's help in getting explaination is fine*

Work in `lab01c_starter.py`.

1. **Pipeline.** Implement sample → quantize → **process** → reconstruct for a
   wanted low tone plus an unwanted high tone. Remove the unwanted tone with a
   moving average (or better), reconstruct, and report SNR at the input and at
   the output. Plot original, contaminated and recovered signals.
   *Choose your own frequencies* — make the filter's null at `fs / taps` land on
   your interference deliberately, and say why it lands there.
2. **Nyquist experiment.** Sweep the sampling rate from well below 2*B* to well
   above it. For each rate, detect the dominant recovered frequency with an FFT
   and plot apparent vs true frequency. Show the characteristic fold and mark
   exactly where reconstruction stops being faithful.
   *Check you can trust:* a 6 kHz tone sampled at 8 kHz must peak at 2 kHz.
3. **Quantization analysis.** Measure SNR for *N* = 2…16, overlay
   6.02*N* + 1.76, and discuss the deviations **honestly** — is the signal truly
   full scale? Is the error correlated with the signal at low *N*? Then add
   dither at low *N* and report what changes and what it costs.
4. **Transfer to systems.** A service spikes for 30 seconds every 5 minutes.
   Determine the maximum safe metrics-sampling interval, justify it with
   Nyquist, simulate a dashboard that misses the outage entirely, and state one
   practical mitigation an engineer would actually deploy.


**Report** (`lab01c_report.md`): method, figures, measured numbers, and a section titled *Where my results deviate from theory and why*. An honest account of a deviation scores higher than a suspiciously perfect result. Include names of group memebers in the report at the very begining.

**Learning outcomes.** Construct and validate an end-to-end ADC→DSP→DAC
pipeline and quantify its improvement; design an experiment that exposes the
Nyquist boundary and interpret it with an FFT; conduct an honest quantitative
error analysis; **transfer** the sampling theorem from hardware to a systems
decision and defend it.

---

## Lab 1D — "Your own photo through the whole loop"

*Optional. Doing it alone or in group is okay.*

Everything above happened to sounds. This does the same thing to a photograph
**you took yourself**, because an image is just a signal sampled in space
instead of time — the same theorem, with cycles per second replaced by cycles
per pixel.

First watch it run on the built-in test pictures:

```bash
python demo_07_image_pipeline.py
```

Then work in `lab01d_starter.py` with your own photo.

### Getting a photo off your phone

Any of these works — pick whichever you already know how to do:

- email or message the photo to yourself, then download it;
- plug the phone into your computer with a cable and copy one file across;
- open your cloud photo library in a browser and download one photo.

Save it in the `code_samples` folder and put its filename in `PHOTO` at the top
of `lab01d_starter.py`.

**Choose a photo with fine repeating detail**: a brick wall, a striped shirt, a
radiator, a keyboard, a distant fence, a tiled floor, a window screen. That
detail is the part that will misbehave, and misbehaving is the point.

**Your photo stays on your computer.** Nothing in this course uploads it
anywhere, and `.gitignore` is already set so photos are never committed — a
phone photo often carries GPS coordinates inside the file, and the lab will
tell you when it finds them. That is a privacy lesson arriving early; you will
meet it properly in the security lecture.

### The tasks

1. **What your camera already decided.** Compute your photo's raw size by hand
   (width × height × channels × bits ÷ 8) and compare it with the file on disk.
   Where did the missing bytes go, and what was traded away?
2. **Sample it two ways.** Throw away 15 of every 16 pixels — once by simply
   taking every 4th pixel, once by averaging the neighbourhood first. Both keep
   exactly the same number of pixels; only the *order* of filter and sampler
   differs. Then open both files and look at the fine detail.
3. **Quantize it.** Step the picture down from 8 bits per pixel to 2 and find
   the depth at which *you* first see banding. Then compare plain rounding with
   dither at that depth: one wins on the number, the other wins on the eye.
4. **Repair something with arithmetic.** Clean up a grainy version using nothing
   but averaging, and find where a wider filter stops helping and starts eating
   the picture.
5. **Reconstruct it.** Bring the small grid back to full size twice — repeating
   each pixel (the DAC's staircase) and interpolating between them (the
   reconstruction filter). Compare the numbers, then compare the pictures.

**Report** (`lab01d_report.md`, template provided): your pictures, your tables,
and — the part that matters — what you *saw*, with the mechanism named.

**Learning outcomes.** Recognise sampling and quantization in a second medium
and carry the vocabulary across; predict spatial aliasing with the folding rule;
say what a single quality metric does and does not capture; explain the costs
your own camera committed you to before you ever saw the photo.

---

## Using AI on this lab

Allowed, and expected, but make sure to log every interactions in `AI-log.md` (template in `templates/`): By interaction, we mean: what you asked, what you got, and what you did with it.

Two habits worth forming this week:

- Ask the AI to *explain* a result you already produced, rather than to produce
  the result. You cannot log an understanding you never had.
- When an AI hands you a number, check it against the theory in the lecture.
  The folding rule and the *q*/2 bound are arithmetic — you can verify them by
  hand in thirty seconds, and models do get these wrong.
