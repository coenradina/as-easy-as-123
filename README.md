# as-easy-as-123

A little password-gated site: a cute CSS-drawn jar that blinks, greets you,
asks how you're feeling, and hands you a random letter for that mood.

## Running it

It's a static site. The live version is built and deployed by GitHub
Actions to GitHub Pages (see "Deploying" below). To poke at it locally,
serve the folder (e.g. `python3 -m http.server`) — see "Password &
local testing" for how to log in without a real deploy.

## Structure

- `index.html` — markup for the password screen and the app screen
- `styles.css` — all styling, including the CSS-drawn jar and its blink/bob animations
- `script.js` — password check (hash comparison), greeting/nickname randomization, mood → letter logic
- `data/letters.js` — the 123 letters (20 each for happy/sad/tired/bored/idk, 23 for missingMe)
- `data/auth.js` — **generated at deploy time, gitignored, never committed.** Holds only `window.SITE_PASSWORD_HASH`, the SHA-256 hash of the real password.
- `.github/workflows/deploy.yml` — builds `data/auth.js` from the `SITE_PASSWORD` secret and deploys to GitHub Pages
- `assets/bg-desktop.png`, `assets/bg-mobile.png` — the cozy pixel-art backgrounds (swapped via a CSS media query); regenerate with `scripts/gen_backgrounds.py`

## Password & local testing

The real password lives **only** as a GitHub Actions secret — it's never
in the repo, in git history, or in anything shipped to the browser. At
deploy time the workflow hashes it (SHA-256) and writes just the hash into
`data/auth.js`; the page hashes whatever the visitor types and compares
hashes.

**One-time setup on GitHub:**

1. Go to the repo's **Settings → Secrets and variables → Actions**.
2. **New repository secret** → name it `SITE_PASSWORD` → value is the
   actual password → **Add secret**.
3. Go to **Settings → Pages** → under "Build and deployment", set
   **Source** to **GitHub Actions**.
4. Push to `main` (or run the "Deploy site" workflow manually from the
   Actions tab) — the site deploys and the secret is picked up automatically.

To change the password later, just update the `SITE_PASSWORD` secret value
and re-run the workflow (push a commit, or trigger it manually) — no code
change needed.

**Local testing** (no real password touches your machine):

```
cp data/auth.example.js data/auth.js
```

This gives you a working login with the password `changeme` (see the
comments in `data/auth.example.js` to use a different one). `data/auth.js`
is gitignored so it's never accidentally committed.

## Editing the letters

Open `data/letters.js`. Each mood is an array of strings wrapped in
backticks (so you can write multi-line text freely). Replace the
placeholder text — don't add or remove entries, since the counts are fixed
at 20/20/20/20/20/23 (123 total). Letters are drawn from a shuffled bag per
mood so the same one won't repeat until all 20 (or 23) have been shown.

## Regenerating the backgrounds

The two pixel-art scenes are generated, not hand-drawn:

```
pip install Pillow
python3 scripts/gen_backgrounds.py
```

Edit the palette/layout constants at the top of `scripts/gen_backgrounds.py`
to tweak colors or composition, then re-run.

## Deploying

Deployment is via `.github/workflows/deploy.yml` to GitHub Pages (see the
one-time setup above). If you'd rather use a different static host
(Netlify, Vercel, etc.), you'll need an equivalent build step there that
sets the `SITE_PASSWORD` env var / secret and writes `data/auth.js` the
same way the GitHub Actions workflow does.