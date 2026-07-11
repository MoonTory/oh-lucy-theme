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

The theme is **generated**, not hand-written. The original theme is cloned into `reference/oh-lucy-vscode-theme` (git-ignored) and its built `dist/*.json` files are the source of truth:

```sh
git clone https://github.com/hermitter/oh-lucy-vscode-theme reference/oh-lucy-vscode-theme
python3 scripts/build_themes.py   # regenerates themes/oh-lucy.json
```

`notes/` contains the research used for the port: the Zed theme format reference (`zed-theme-format.md`) and the extracted color data of the original (`extracted/`).

## Porting notes

Zed's theme model differs from VSCode's (tree-sitter captures instead of TextMate scopes, different UI keys), so a few deliberate mapping decisions were made — all documented in `scripts/build_themes.py`:

- Bracket-match highlight uses the theme's translucent white; the original relied on a border, which Zed doesn't have.
- Active tabs keep the original backgrounds but rely on Zed's text/muted-text distinction (Zed has no per-tab border/text colors).
- Inlay hints use the original's dim `editorInlayHint` gray rather than the purple `editorHint` diagnostic color.
- Scrollbars, collaboration players, and UI accents are not themed in the original; they are built from the theme's own palette.
