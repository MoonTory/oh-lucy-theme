# Oh Lucy for Zed

Lucy is a soft but clear dark theme that has passed through a few caring hands. [Juliette Prétot](https://github.com/jul-sh) knitted the [original Lucy](https://github.com/jul-sh/lucy-vscode-theme) for VSCode, [hermitter](https://github.com/hermitter) gave it a second home under the name [Oh Lucy](https://github.com/hermitter/oh-lucy-vscode-theme), and this project carries it, color by color, to [Zed](https://zed.dev). The palette's charm is all theirs. The porting mistakes are ours.

Four variants are included:

- **Lucy**: the original theme
- **Lucy Evening**: the original's warmer evening companion
- **Lucy Dawn**: new in this port, the same palette under a cool pre-dawn light
- **Lucy Midnight**: new in this port, deeper and darker for late nights

## Screenshots

<!-- SCREENSHOT: open examples/example.ts in Zed with the "Lucy" theme, capture the editor. Save as assets/lucy-zed.png -->
![Lucy](assets/lucy-zed.png)

<!-- SCREENSHOT: same file with the "Lucy Evening" theme. Save as assets/lucy-evening-zed.png -->
![Lucy Evening](assets/lucy-evening.png)

<!-- SCREENSHOT: same file with the "Lucy Dawn" theme. Save as assets/lucy-dawn-zed.png -->
![Lucy Dawn](assets/lucy-dawn.png)

<!-- SCREENSHOT: same file with the "Lucy Midnight" theme. Save as assets/lucy-midnight-zed.png -->
![Lucy Midnight](assets/lucy-midnight.png)

The screenshots show [`examples/example.ts`](examples/example.ts), a small file that touches the theme's signature tokens: italic cyan declaration keywords, purple constants, green types and function calls, pink keywords, and yellow strings.

## Installation

Until the extension lands on the Zed registry, install it as a dev extension:

1. Clone this repo.
2. In Zed, run `zed: install dev extension` from the command palette and pick the repo's root directory.
3. Choose a variant via `theme selector: toggle` (search "Lucy").

## Recommended settings

One of Lucy's nicest touches is that a `const` name is purple where it's declared and plain where it's used. Zed's tree-sitter highlighting can't tell those two apart, but its LSP semantic tokens can. Add this to your Zed `settings.json` and restart the language server (`editor: restart language server`):

```json
{
  "semantic_tokens": "combined",
  "global_lsp_settings": {
    "semantic_token_rules": [
      {
        "token_type": "class"
      },
      {
        "token_type": "variable",
        "token_modifiers": ["declaration", "readonly"],
        "style": ["constant"]
      }
    ]
  }
}
```

<!-- SCREENSHOT: examples/example.ts with the semantic token settings applied (const names purple at declaration). Save as assets/semantic-on.png -->
![With semantic tokens](assets/semantic-on.png)

<!-- SCREENSHOT: the same file without the settings (const names plain white). Save as assets/semantic-off.png -->
![Without semantic tokens](assets/semantic-off.png)

Two things worth knowing:

- The empty `class` rule needs to stay first. Zed only treats a rule without a style as "don't apply semantic styling" when it's the highest-priority rule, and that's what lets tree-sitter keep class names green when used as types and plain when used in expressions. Zed's default rules would otherwise paint both the same.
- Without these settings, or when no language server is running, const names simply render white like other variables. Nothing breaks.

## Credits

- [Juliette Prétot](https://github.com/jul-sh) created the original [Lucy theme](https://github.com/jul-sh/lucy-vscode-theme).
- [hermitter](https://github.com/hermitter) maintains the [Oh Lucy re-upload](https://github.com/hermitter/oh-lucy-vscode-theme) this port was built from.

Licensed MIT, preserving the original copyright.
