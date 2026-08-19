# Setup Guide — 5 minutes

## 1. Where these files go
This is your **profile repo** — the special one named exactly like your username
(`PrakharPurwar12/PrakharPurwar12`). If it doesn't exist yet, create it on GitHub
first (public, with a README).

Copy these into that repo, keeping the folder structure:

```
README.md
.github/workflows/snake.yml
.github/workflows/update-readme.yml
scripts/update_pinned_repos.py
```

## 2. Turn on Actions
Repo → **Settings → Actions → General → Workflow permissions** →
select **"Read and write permissions"** → Save.
(This lets the workflows push the auto-updated README and the snake SVGs
back to your repo using the default `GITHUB_TOKEN` — no extra secrets needed.)

## 3. Run the workflows once
Repo → **Actions** tab → you'll see two workflows:
- **Generate Contribution Snake** → click "Run workflow" once. It creates an
  `output` branch with `github-contribution-grid-snake.svg` (light) and
  `github-contribution-grid-snake-dark.svg` (dark). After that it re-runs
  automatically every day at 2 AM UTC.
- **Update README** → click "Run workflow" once. It fills in the
  "Recent GitHub Activity" and "Pinned Repositories" sections and commits
  the change. After that it re-runs automatically every 6 hours.

## 4. Dark/light mode
All the `<picture>` blocks in `README.md` already point to the right image
depending on whether a visitor's GitHub theme is light or dark — nothing
else to configure. GitHub reads the `prefers-color-scheme` media query
natively.

## 5. Customize
- Swap `PrakharPurwar12` anywhere in `README.md` if your GitHub handle
  changes.
- `MAX_REPOS` in `scripts/update_pinned_repos.py` controls how many
  repositories show in the pinned-repos table (default 6).
- Want WakaTime coding-time stats or a Spotify "now playing" widget too?
  Say the word and I'll wire those in as well.
