# Oh Lucy for Zed

A faithful port of the [Oh Lucy VSCode theme](https://github.com/hermitter/oh-lucy-vscode-theme) by [hermitter](https://github.com/hermitter) to the [Zed](https://zed.dev) editor.

Includes all three variants of the original extension:

- **Oh Lucy**
- **Lucy**
- **Lucy Evening**

## Installing (dev extension)

1. Clone this repo.
2. In Zed, open the command palette and run `zed: install dev extension`, then select this repo's root directory.
3. Pick a variant via `theme selector: toggle` (search "Lucy").

## Development

`themes/oh-lucy.json` is maintained by hand. The initial version was generated from the original theme's built JSONs by `notes/build_themes.py` (retired — do not rerun; the theme has hand adjustments on top). To compare against the source of truth, clone the original into `reference/`:

```sh
git clone https://github.com/hermitter/oh-lucy-vscode-theme reference/oh-lucy-vscode-theme
```

`notes/` contains the research used for the port: the Zed theme format reference (`zed-theme-format.md`), Zed's JS/TS highlight captures (`zed-js-captures.md`), and the extracted color data of the original (`extracted/`).

## Porting notes

Zed's theme model differs from VSCode's (tree-sitter captures instead of TextMate scopes, different UI keys), so a few deliberate mapping decisions were made — all documented in `scripts/build_themes.py`:

- Bracket-match highlight uses the theme's translucent white; the original relied on a border, which Zed doesn't have.
- Active tabs keep the original backgrounds but rely on Zed's text/muted-text distinction (Zed has no per-tab border/text colors).
- Inlay hints use the original's dim `editorInlayHint` gray rather than the purple `editorHint` diagnostic color.
- Scrollbars, collaboration players, and UI accents are not themed in the original; they are built from the theme's own palette.
- `const`/`let`/`function`/`class` keywords use Zed's `keyword.declaration` capture, matching the original's italic-cyan `storage.type`.
- Zed captures every identifier as `variable` (declarations and usages alike), while the original colors only const-declared names purple (TextMate's `variable.other.constant`) and keeps usages white. As a middle ground, variables use the theme's soft lavender everywhere.
