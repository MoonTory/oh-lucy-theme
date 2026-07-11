# Zed theme-extension format

Research date: 2026-07-12. This describes the published **v0.2.0** theme schema, not an inferred VS Code mapping.

## Sources

* Zed, [Theme Extensions](https://zed.dev/docs/extensions/themes)
* Zed, [Developing Extensions](https://zed.dev/docs/extensions/developing-extensions)
* Zed, [theme JSON Schema v0.2.0](https://zed.dev/schema/themes/v0.2.0.json) (the normative list below)
* Published example: [catppuccin/zed](https://github.com/catppuccin/zed), specifically its [`extension.toml`](https://github.com/catppuccin/zed/blob/main/extension.toml) and [`themes/catppuccin-mauve.json`](https://github.com/catppuccin/zed/blob/main/themes/catppuccin-mauve.json).
* For the supported built-in syntax vocabulary (which the JSON schema intentionally does not enumerate): Zed source, [`fallback_themes.rs`](https://github.com/zed-industries/zed/blob/main/crates/theme/src/fallback_themes.rs).

## Minimal extension layout

A theme extension is a Git repository with a manifest and a `themes/` directory. A theme-only extension needs no Rust, `Cargo.toml`, or `src/` directory.

```text
my-zed-theme/
├── extension.toml
└── themes/
    └── my-theme.json
```

`themes/` contains one or more JSON **theme-family** files, each conforming to the schema URL above. The extension docs explicitly say themes should be published as a distinct extension rather than bundled with a language/debugger/MCP extension.

The required manifest fields shown by Zed's extension-development docs are:

```toml
id = "my-theme"
name = "My Theme"
version = "0.0.1"
schema_version = 1
authors = ["Your Name <you@example.com>"]
description = "A Zed theme"
repository = "https://github.com/your-name/my-zed-theme"
```

The real Catppuccin extension uses exactly these fields (with its own values). `id` must identify the extension; `schema_version` is the extension-manifest schema version, not the theme JSON schema version.

## Theme-family JSON

At the top level the schema requires `name`, `author`, and `themes`. Put the schema URI in `$schema` for editor validation (useful, but not one of the schema's required fields). `themes` is an array; every item requires `name`, `appearance`, and `style`. `appearance` is exactly `"light"` or `"dark"`.

```json
{
  "$schema": "https://zed.dev/schema/themes/v0.2.0.json",
  "name": "My Theme Family",
  "author": "Jane Doe <jane@example.com>",
  "themes": [
    {
      "name": "My Theme Dark",
      "appearance": "dark",
      "style": {
        "background": "#101015",
        "editor.background": "#101015",
        "text": "#e6e1f0",
        "syntax": {
          "keyword": { "color": "#cba6f7", "font_weight": 700 },
          "comment": { "color": "#7f849c", "font_style": "italic" }
        }
      }
    }
  ]
}
```

### Color and value rules

* Every listed ordinary color key is `string | null`; `null` leaves it unspecified. Color strings can be `#rrggbb` or alpha-bearing `#rrggbbaa`. Thus alpha is accepted for **all color-valued string fields**, including `accents` entries, `players.*`, every ordinary style color, and syntax `color`/`background_color`. Example: `"element.active": "#ffffff4d"`. Zed parses color strings as RGBA; the schema itself does not impose a hex pattern.
* `background.appearance` is not a color: `"opaque"`, `"transparent"`, or `"blurred"` (or `null`).
* `accents` is an array of color strings or `null` entries. `players` is an array of objects whose `background`, `cursor`, and `selection` are color strings or null.
* `style` fields are optional in this schema. A practical theme should supply the fundamental UI/editor/terminal values it needs rather than rely on fallback values.

## All `style` keys defined by schema v0.2.0

This is the exhaustive set of actual property names in `ThemeStyleContent` (142). Apart from the structured entries called out above, each is a color string or null and therefore may use `#rrggbbaa`.

**General, surfaces, borders, element states**

```text
accents
background
background.appearance
border
border.disabled
border.focused
border.selected
border.transparent
border.variant
drop_target.background
elevated_surface.background
element.active
element.background
element.disabled
element.hover
element.selected
ghost_element.active
ghost_element.background
ghost_element.disabled
ghost_element.hover
ghost_element.selected
surface.background
```

**Text, icons, navigation/panels, and scrolling**

```text
text
text.accent
text.disabled
text.muted
text.placeholder
icon
icon.accent
icon.disabled
icon.muted
icon.placeholder
link_text.hover
pane.focused_border
pane_group.border
panel.background
panel.focused_border
panel.indent_guide
panel.indent_guide_active
panel.indent_guide_hover
scrollbar.thumb.background
scrollbar.thumb.border
scrollbar.thumb.hover_background
scrollbar.track.background
scrollbar.track.border
status_bar.background
tab.active_background
tab.inactive_background
tab_bar.background
title_bar.background
title_bar.inactive_background
toolbar.background
```

**Status colors** — each status has foreground/status key, `.background`, and `.border`:

```text
conflict
conflict.background
conflict.border
created
created.background
created.border
deleted
deleted.background
deleted.border
error
error.background
error.border
hidden
hidden.background
hidden.border
hint
hint.background
hint.border
ignored
ignored.background
ignored.border
info
info.background
info.border
modified
modified.background
modified.border
predictive
predictive.background
predictive.border
renamed
renamed.background
renamed.border
success
success.background
success.border
unreachable
unreachable.background
unreachable.border
warning
warning.background
warning.border
```

**Editor and search**

```text
editor.active_line.background
editor.active_line_number
editor.active_wrap_guide
editor.background
editor.document_highlight.bracket_background
editor.document_highlight.read_background
editor.document_highlight.write_background
editor.foreground
editor.gutter.background
editor.highlighted_line.background
editor.indent_guide
editor.indent_guide_active
editor.invisible
editor.line_number
editor.subheader.background
editor.wrap_guide
search.match_background
```

**Collaboration**

```text
players
```

`players` is the structured array noted above: each entry has `background`, `cursor`, and `selection` color fields (all alpha-capable).

**Terminal**

```text
terminal.background
terminal.foreground
terminal.bright_foreground
terminal.dim_foreground
terminal.ansi.background
terminal.ansi.black
terminal.ansi.red
terminal.ansi.green
terminal.ansi.yellow
terminal.ansi.blue
terminal.ansi.magenta
terminal.ansi.cyan
terminal.ansi.white
terminal.ansi.bright_black
terminal.ansi.bright_red
terminal.ansi.bright_green
terminal.ansi.bright_yellow
terminal.ansi.bright_blue
terminal.ansi.bright_magenta
terminal.ansi.bright_cyan
terminal.ansi.bright_white
terminal.ansi.dim_black
terminal.ansi.dim_red
terminal.ansi.dim_green
terminal.ansi.dim_yellow
terminal.ansi.dim_blue
terminal.ansi.dim_magenta
terminal.ansi.dim_cyan
terminal.ansi.dim_white
```

**Syntax**

```text
syntax
```

This is an object, described next. It is deliberately `additionalProperties`, so its token names are not a closed enum in the schema.

## `style.syntax`: token names and properties

Each entry is a capture/token name mapped to a highlight-style object:

```json
"syntax": {
  "function.method": {
    "color": "#89b4fa",
    "background_color": "#1e1e2e80",
    "font_style": "italic",
    "font_weight": 600
  }
}
```

The complete allowed properties of each highlight-style object are:

* `color`: color string or null; alpha-capable (`#rrggbbaa`).
* `background_color`: color string or null; alpha-capable.
* `font_style`: `"normal"`, `"italic"`, `"oblique"`, or null.
* `font_weight`: `100`, `200`, `300`, `400`, `500`, `600`, `700`, `800`, `900`, or null.

### Token-name list: important schema nuance

There is **no finite token-name list in v0.2.0.json**: `syntax` has `additionalProperties` whose value is the highlight-style object. A key is useful when it matches a language grammar's Tree-sitter highlight capture (or its parent fallback); languages can define capture names beyond a universal list. Therefore a claim that the schema itself accepts only a fixed list would be incorrect.

For a complete, concrete baseline, these are all names in Zed's built-in fallback syntax theme (the official Zed source linked above):

```text
attribute
boolean
comment
comment.doc
constant
constructor
embedded
emphasis
emphasis.strong
enum
function
function.method
function.definition
hint
keyword
label
link_text
link_uri
number
operator
predictive
preproc
primary
property
punctuation
punctuation.bracket
punctuation.delimiter
punctuation.list_marker
punctuation.special
string
string.escape
string.regex
string.special
string.special.symbol
tag
text.literal
title
type
variable
variable.special
variant
diff.plus
diff.minus
```

Use these as the portable Zed vocabulary, then add language-specific capture names after inspecting that language's `highlights.scm`. Dot names are hierarchical: a more-specific capture such as `string.escape` can have its own style while `string` remains the fallback. The Catppuccin example also demonstrates that extensions may carry compatibility/extra keys (for example `vim.*`); do not mistake such keys for properties enumerated by the v0.2.0 schema.

## Install and test locally

1. Ensure the directory is a Git repository and contains `extension.toml` plus `themes/*.json`.
2. Zed's development docs say to install Rust via **rustup** before installing a dev extension (Rust installed only through Homebrew/another source does not work for this workflow, even though a theme-only extension has no Rust code).
3. In Zed, open Extensions and choose **Install Dev Extension**, or run the command-palette action **`zed: install dev extension`**. Select the extension root directory, not its `themes/` subdirectory.
4. Select the theme by its per-theme `themes[].name` in Zed's theme picker. Change JSON and re-test; if Zed reports a loading/validation problem, inspect **`zed: open log`**. For more logging, quit and run `zed --foreground` from a terminal.
5. If a marketplace version with the same ID is installed, Zed uninstalls it and marks the extension as **“Overridden by dev extension”**. Test that override before publishing.

## VS Code porting gotchas

* **Different selector model.** VS Code themes principally target TextMate scope selectors (often comma-separated and specificity-sensitive), e.g. `entity.name.function`, plus VS Code workbench color IDs. Zed `style.syntax` is a dictionary of Tree-sitter highlight capture names such as `function`, `function.method`, and `string.escape`; it is not a TextMate selector engine. Translate intent/scope categories rather than copy VS Code `tokenColors` scopes verbatim.
* **No one-to-one token map.** A grammar may emit only a parent capture, a more-specific dotted capture, or a language-specific capture. Start with Zed's fallback names, inspect the target language's `highlights.scm`, and use parent styles as fallbacks. Semantic/LSP information may also affect what is displayed, so verify representative files in Zed.
* **UI names differ.** VS Code `colors` keys (for example `editorWidget.background`) do not transfer. Map them deliberately to the exact Zed style keys above; Zed separates `background`, `surface.background`, `elevated_surface.background`, `element.*`, `ghost_element.*`, panel/tab/title-bar keys, and its own terminal palette.
* **Alpha is useful but must be intentional.** VS Code may use hex alpha or transparency in workbench colors. Zed accepts `#rrggbbaa` on every color-valued schema field, but transparency can expose underlying surface colors differently because Zed has separate surface/element layers.
* **Schema openness is not guaranteed rendering.** The schema permits extra `style` and `syntax` properties; that does not make a random VS Code key recognized by Zed. Prefer the enumerated v0.2.0 keys and captures actually emitted by Zed grammars.
