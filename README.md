# Mnemonic Library

A clean, searchable gallery for your own study images — your private version of a
Pixorize-style image wall, hosted at a real URL.

You drop images into folders by system, push, and they appear online. Search by
name, filter by system, click any image to view it full size.

---

## One-time setup (≈5 minutes)

1. **Make a new GitHub repo** (public is simplest for free Pages; a free private
   repo also works). Name it whatever you like, e.g. `mnemonics`.

2. **Add these files** to the repo (drag-and-drop in GitHub's web UI is fine, or
   `git push` if you prefer the command line):
   - `index.html`
   - `build_manifest.py`
   - `.github/workflows/deploy.yml`
   - the `images/` folder

3. **Turn on Pages:** repo **Settings → Pages → Build and deployment → Source:
   GitHub Actions.**

4. **Push once.** The Action builds the image list and publishes the site. Your
   URL will be:
   ```
   https://<your-username>.github.io/<repo-name>/
   ```
   (Find the exact link under the repo's **Actions** tab → latest run → the
   `Deploy` step, or under **Settings → Pages**.)

That's it. Open the URL on any device.

---

## Adding images later

1. Put image files inside `images/<system>/`. The **folder name becomes the
   system label** shown in the gallery:
   ```
   images/
     endo/
       thyroid_storm.png
       cushing_moon_face.jpg
     cardio/
       afib.png
   ```
2. Commit / push. The site rebuilds automatically in ~1 minute.

**Titles** come from the filename: `thyroid_storm.png` → "Thyroid Storm".
Common acronyms (DKA, TSH, AFib…) stay capitalized.

---

## Adding anchors + explanation under an image

To get the Pixorize-style write-up below the sketch, drop a text file **next to the
image with the same name**, ending in `.md` (or `.txt`):

```
images/endo/palopegteriparatide.png
images/endo/palopegteriparatide.md     <- anchors + explanation
```

Whatever you put in that file shows up under the image when you open it. It's the
same anchor text you already write — just save it as a `.md`. Markdown formatting
works: `**bold**`, `*italic*`, `` `code` ``, `[links](url)`, `- bullets`, and
`# headings`. Example file contents:

```markdown
ANCHORS:
- Pal + Peg + Ptero + Para + -tide = **Palopegteriparatide** (name anchor)
- Full-day clock unwinding = **24-hour sustained release** of active PTH 1-34
- Overflowing Calci-Yum mountain = **hypercalcemia** (key AE; monitor Ca²⁺)

Pegylated prodrug of PTH 1-34, indicated for **hypoparathyroidism**.
```

Cards with a write-up show a small **NOTES** badge in the gallery. There's a
ready-to-copy `notes-template.md` in this folder.

---

## Nicer titles & tags (optional)

Create a `titles.json` in the project root to override any title or add search
tags. You can also put the notes here instead of a sidecar file:

```json
{
  "images/endo/thyroid_storm.png": {
    "title": "Thyroid Storm — Burning House",
    "tags": ["thyroid", "hyperthyroid", "burch-wartofsky"],
    "notes": "ANCHORS:\n- Burning house = **thyroid storm**\n..."
  }
}
```
Tags are searchable but not shown on the card. (A sidecar `.md` wins over `notes`
here if both exist.)

---

## Preview locally before pushing

From the project folder:
```bash
python build_manifest.py        # builds manifest.json
python -m http.server 8000      # then open http://localhost:8000
```
(Opening `index.html` by double-click works too — it shows demo placeholders
until a `manifest.json` exists.)

---

## Not into GitHub?

The same files work on **Netlify** or **Cloudflare Pages**: run
`python build_manifest.py` locally, then drag the whole folder into Netlify Drop
(netlify.com/drop) for an instant URL. You just re-run the script + re-drag when
you add images, instead of it happening automatically.
