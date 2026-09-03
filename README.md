# Systematic Trading Arena

An interactive companion for a 9-week systematic-trading course. Ten pages —
a course map plus one page per week — each built around live, clickable
widgets rather than static slides: order books you can cross, event loops you
can block, backtests you can bias, complexity curves you can double, parameter
sweeps you can fan out, walk-forward folds you can peek at, and a season
leaderboard you can lock.

The weeks build one system, and nothing is thrown away:

| Week | Topic |
|------|-------|
| 1 | UML & Object-Oriented Programming |
| 2 | Concurrency & Async in Python |
| 3 | Socket Streaming & Protocols |
| 4 | Backtester Architecture |
| 5 | Algorithmic Complexity & Data Structures |
| 6 | Big Data & Distributed Computing |
| 7 | Machine Learning Signals & Model Ops |
| 8 | CI/CD, Testing & UI |
| 9 | Integration & Demo — Season Finale |

The code the weeks refer to is **AlgoArena**, a Python trading-competition
platform. The public starter repo is
[algoarena-team-template](https://github.com/sdonadio/algoarena-team-template).

## Self-contained static HTML

Every page is a single `.html` file with exactly one inline `<style>` block and
one inline `<script>` block. There are no images, no build step, no package
manifest, no CDN and no external requests of any kind — the only outbound links
are to this repository, to the AlgoArena starter template, and (from the course
map) to the prequel site. All diagrams are inline SVG or `<canvas>` drawn by the
page's own script. Each page shares one byte-identical CSS custom-property
palette, so re-theming the site means editing the `:root` block.

## Run it locally

```sh
git clone https://github.com/sdonadio/systematic-trading-arena
cd systematic-trading-arena
python3 -m http.server
```

Then open <http://localhost:8000/>.

Opening `index.html` directly from the filesystem also works, since nothing is
fetched over the network.

## Deploying

The site is plain static files, so GitHub Pages serves it as-is from the
repository root. `.nojekyll` is present so Pages skips Jekyll processing.

## Browser support

Any current browser. The pages use CSS custom properties, CSS grid, inline SVG
and ES5-compatible scripts, and honour `prefers-reduced-motion`. Layout
collapses to a single column below 720px.

## Licence

Content © the author, all rights reserved.
