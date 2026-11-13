# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A layout + terminal theme + mod for the **Herdr** desktop app (`herdr-app`), not a standalone app. There is
no package manager, build step or test suite. The mod is plain ES-module JavaScript run by Herdr's embedded
runtime against the `gpui-kit`, `gpui-base` and `herdr` modules (types in `~/.config/herdr-app/*.d.ts`).
`RECIPE.md` is the authoritative spec of what the UI shows and how it behaves; read it before changing behaviour.

This repo is a fork: `origin` = tildtr/world-of-codecraft, `upstream` = kevinpardo/world-of-codecraft.

## Commands

```sh
tools/install.sh                       # copy mod, layout, theme into ~/.config/herdr-app (HERDR_APP_HOME overrides)
tools/install.sh --integrations        # also symlink the Claude Code hook / OpenCode plugin
herdr-app check mods/world-of-codecraft   # load the mod once, report errors (renders every role when no props.role)
herdr-app status                       # current layout + runtime "errors" array — must be empty
herdr-app shot out.png                 # screenshot of the live window, for visual checks
herdr-app do layout.switch '{"name":"World-of-Codecraft"}'
herdr-app commands                     # every command the mod/layout can call
```

"Done" = `check` passes and `status` shows no errors (see RECIPE.md "Done when").

Edit the repo, never the installed copy, then re-run `tools/install.sh`. It must install **real files, not
symlinks**: Herdr loads images and hot-reloads mods only from real paths inside its home. Dozens of hot
reloads can exhaust the mod's JS heap ("out of memory"/"Null"); restart the Herdr window.

## Architecture

- `layouts/World-of-Codecraft.json`: the block tree. Root column = `fronton` (top bar) / `bourg` row
  (`gauche` column: `tableau` + `commande`; `droite` column: `place-immersion` + `arene`, which holds four
  `rail` blocks around the `main` tab block) / `place` (bottom village). Every custom block points at the same
  mod with a different `props.role`. Immersive mode is not a second layout: it is `layout.show`/`hide`/`resize`
  calls on this one (triggered from `fronton.js`, key `world-of-codecraft.mode`).
- `mods/world-of-codecraft/main.js` dispatches on `props.role` → `fronton.js`, `tableau.js`, `place.js`,
  `pane.js` (pane header), `commande.js`, or the `rail` frame from `ui.js`.
- Shared modules: `kit.js` (palette `C`, fonts, hero identity: class from the agent's program, race/name from
  a hash of the terminal address; hours; optional cduo quota reader), `ui.js` (frames built from corners +
  edge strips, since Herdr has no 9-slice), `lieux.js` (unit spots, road, hit boxes), `activite.js` (activity
  scenes from `~/.local/state/world-of-codecraft/<terminal>.json`), `ambiance.js` (village life),
  `i18n.js` (**every** visible string, French and English, plus language detection), `demo.js` (fake data for
  screenshots via `demo: true` props).
- Cross-block communication goes through the Herdr store: `wocc.view`/`wocc.goto` (village ↔ minimap),
  `wocc.chronicle`, `wocc.anim`, `wocc.lang`.
- `*-data.js` (`heros-data.js`, `monde-data.js`, `creatures-data.js`, `terre-data.js`) are **generated** by
  the Python tools in `tools/` (`sync_heroes.py`, `sync_creatures.py`, `bake_world.py`, `bake_lands.py`, `ui.py`)
  from art sources; don't hand-edit them. Art pipeline lives in `tools/village-art/` (needs its own `.venv`
  with numpy/Pillow; `build_assets.sh`), and some scripts default to source paths on the original author's
  machine.
- Identifiers, file names and art names are in French (`place` = village square, `fronton` = pediment,
  `tableau` = board, `heros`, `lieux`, `nuit` = night-graded variant, `-assis` = seated sprite).

## Gotchas (from RECIPE.md)

- Declare `transition` on every render (16 ms while standing); GPUI only animates changes made after the
  transition exists.
- Animation frames are all stacked at opacity 0/1 so swaps never load an image; units are depth-sorted by y and
  building "front cut-outs" are redrawn above units behind them.
- Only the visible village block runs timers/writes the chronicle; hidden blocks must keep none.
- The theme's terminal font size is intentionally unset (left to Herdr settings).

## This fork's customizations (branch `my-customization`)

- **Right panel:** `bourg` has a third child, `panneau` (hidden column) holding the stack `panneau-corps` with
  Herdr's stock `files` and `changes` mods. `fronton.js` (`panelView`/`togglePanel`) opens it from the top-bar
  buttons and the commands `world-of-codecraft.files` / `.changes` (`KEYS.json`: ctrl-shift-e / ctrl-shift-g).
  A stack `"header": "tabs"` is rejected by this Herdr version despite AGENTS.md; don't add it back.
- **Middle-earth theme:** display text only, in `i18n.js` (EN + FR), the `NAMES` lists in `kit.js`, the title in
  `fronton.js` and `demo.js`. Art keys stay French/original: race `humain` is shown as Hobbit, `mort-vivant`
  as Barrow-wight; buildings `tour`/`atelier`/`caserne`/`temple`/`taverne`/`hotel`/`grange` are Wizard's Tower,
  Smithy, Shirriff-house, Mathom-house, The Green Dragon, Mayor's Hall, Farmstead. Keep new strings about as
  short as the originals: the hour plaque fits ~63 px of Alegreya Sans Bold 16 before it hits the clock.
- **Realm pennants are baked PNGs** (`art/ui/banniere-<cloth index>-<charge>.png`), not the `blason-*.svg`
  files. `ui.js` maps a colour to its PNG by index in `CLOTH`, so `CLOTH` in `tools/ui.py`, `CLOTH` in `ui.js`
  and `COLORS` in `kit.js` must stay identical; an unknown colour falls back to index 0, a missing charge draws
  nothing. Re-bake with `python3 tools/ui.py banners` (numpy, scipy, Pillow). It writes to `<repo>/art/ui/`,
  so move the PNGs into `mods/world-of-codecraft/art/ui/` afterwards. An unchanged re-bake is pixel-identical.
  PNG bytes can differ even when pixels don't, so compare pixels before copying a re-bake over the shipped art.
- **Heraldry:** the top-left `blason` is the Ring, and the realm charges are Middle-earth ones (`etoile` = Star of
  Elendil, `arbre` = White Tree, `cheval` = Rohan, `enclume` = Durin, `couronne`, `feuille` = Lórien, `epee`,
  `tour`). `CHARGES` in `tools/ui.py` and in `kit.js` must list the same names. The `blason-*.svg` files belong
  to the unused `pennant()` and were left as they are.
- **Checking all states and French without waiting for them:** temporarily add `"demo": true` and
  `"lang": "fr"` to the props of the `fronton`, `tableau`, `commande` and `place` blocks, install, run
  `herdr-app shot`, then restore the layout and reinstall. Never commit the demo props.
