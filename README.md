# as-easy-as-123

A little password-gated site: a cute CSS-drawn jar that blinks, greets you,
asks how you're feeling, and hands you a random letter for that mood.

## Running it

It's a static site — no build step. Either open `index.html` directly in a
browser, or serve the folder (e.g. `python3 -m http.server`) and visit it.

Password: `gutierritos`

## Structure

- `index.html` — markup for the password screen and the app screen
- `styles.css` — all styling, including the CSS-drawn jar and its blink/bob animations
- `script.js` — password check, greeting/nickname randomization, mood → letter logic
- `data/letters.js` — the 123 letters (20 each for happy/sad/tired/bored/idk, 23 for missingMe)

## Editing the letters

Open `data/letters.js`. Each mood is an array of strings wrapped in
backticks (so you can write multi-line text freely). Replace the
placeholder text — don't add or remove entries, since the counts are fixed
at 20/20/20/20/20/23 (123 total). Letters are drawn from a shuffled bag per
mood so the same one won't repeat until all 20 (or 23) have been shown.

## Deploying

Any static host works — GitHub Pages, Netlify, Vercel, etc. Just point it
at this folder.