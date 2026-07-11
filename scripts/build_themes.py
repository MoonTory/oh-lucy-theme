#!/usr/bin/env python3
"""Generate the Zed theme family from the original Oh Lucy VSCode theme.

Reads the built VSCode themes in reference/oh-lucy-vscode-theme/dist/ and
emits themes/oh-lucy.json (Zed theme schema v0.2.0). All colors come from the
original theme files; the only hand-picked values are documented fallbacks for
concepts VSCode expresses differently (see MAPPING NOTES below).

MAPPING NOTES
- VSCode marks the matching bracket with a border; Zed only has a background,
  and the original background equals the editor background (invisible). We use
  the theme's own translucent white (#ffffff12) instead.
- VSCode distinguishes the active tab with a yellow top border + yellow text;
  Zed has no per-tab text/border colors, so tabs rely on Zed's built-in
  text vs text.muted distinction (backgrounds stay faithful).
- Zed panels (project/git/outline docks) map to VSCode's sideBar, not
  VSCode's bottom panel: they are the file-tree surfaces of the original.
- Zed's `created`/`modified`/`deleted` statuses follow the original's gutter
  colors (added=green, modified=orange, deleted=pink). Note the original's
  file-tree colors disagree with its own gutter (modified files are green);
  the gutter semantics are the conventional ones so we use those.
- players/accents (Zed-only concepts) are built from the theme's own palette.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "reference" / "oh-lucy-vscode-theme" / "dist"
OUT = ROOT / "themes" / "oh-lucy.json"

VARIANTS = [
    ("oh-lucy.json", "Oh Lucy"),
    ("lucy.json", "Lucy"),
    ("lucy-evening.json", "Lucy Evening"),
]

TRANSPARENT = "#00000000"


def build_variant(vscode: dict, name: str) -> dict:
    c = vscode["colors"]

    def scope(target: str) -> dict:
        """Find the settings of the tokenColors rule matching a scope exactly."""
        for rule in vscode["tokenColors"]:
            scopes = rule.get("scope", [])
            if isinstance(scopes, str):
                scopes = [s.strip() for s in scopes.split(",")]
            if target in scopes:
                return rule.get("settings", {})
        raise KeyError(f"scope not found in {name}: {target}")

    def syn(target: str, **overrides) -> dict:
        s = scope(target)
        entry = {}
        if "foreground" in s:
            entry["color"] = s["foreground"]
        style = s.get("fontStyle", "")
        if "italic" in style:
            entry["font_style"] = "italic"
        if "bold" in style:
            entry["font_weight"] = 700
        entry.update(overrides)
        return entry

    # The base palette's translucent whites differ slightly per variant
    # (#ffffff0c vs #ffffff0d); read them from the theme itself.
    hover_wash = c["editor.hoverHighlightBackground"]
    strong_wash = c["editor.wordHighlightBackground"]  # #ffffff26
    faint_wash = "#ffffff12"  # `translucent9` in both source palettes

    accent = c["list.activeSelectionForeground"]  # signature yellow
    cursor = c["editorCursor.foreground"]

    def player(color: str) -> dict:
        return {"background": color, "cursor": color, "selection": color + "3d"}

    style = {
        # General surfaces
        "background.appearance": "opaque",
        "background": c["titleBar.activeBackground"],
        "surface.background": c["sideBar.background"],
        "elevated_surface.background": c["dropdown.listBackground"],
        "panel.background": c["sideBar.background"],
        "drop_target.background": c["list.dropBackground"],
        # Borders
        "border": c["sideBar.border"],
        "border.variant": c["editorGroup.border"],
        "border.focused": c["focusBorder"],
        "border.selected": c["focusBorder"],
        "border.disabled": c["sideBar.border"],
        "border.transparent": TRANSPARENT,
        # Elements (buttons, list rows, inputs)
        "element.background": c["button.background"],
        "element.hover": c["list.hoverBackground"],
        "element.active": c["statusBarItem.activeBackground"],
        "element.selected": c["list.activeSelectionBackground"],
        "ghost_element.background": TRANSPARENT,
        "ghost_element.hover": hover_wash,
        "ghost_element.active": faint_wash,
        "ghost_element.selected": c["list.activeSelectionBackground"],
        # Text
        "text": c["editor.foreground"],
        "text.muted": c["sideBar.foreground"],
        "text.placeholder": c["input.placeholderForeground"],
        "text.disabled": c["input.placeholderForeground"],
        "text.accent": accent,
        # Icons
        "icon": c["activityBar.foreground"],
        "icon.muted": c["sideBarSectionHeader.foreground"],
        "icon.disabled": c["sideBarTitle.foreground"],
        "icon.placeholder": c["input.placeholderForeground"],
        "icon.accent": accent,
        "link_text.hover": c.get(
            "textLink.activeForeground", c["editorLink.activeForeground"]
        ),
        # Panels / panes
        "pane_group.border": c["editorGroup.border"],
        "pane.focused_border": c["focusBorder"],
        "panel.focused_border": c["focusBorder"],
        "panel.indent_guide": c["editorIndentGuide.background"],
        "panel.indent_guide_active": c["editorRuler.foreground"],
        "panel.indent_guide_hover": c["editorRuler.foreground"],
        "scrollbar.thumb.background": c.get("scrollbarSlider.background", faint_wash),
        "scrollbar.thumb.hover_background": c.get(
            "scrollbarSlider.hoverBackground", strong_wash
        ),
        "scrollbar.thumb.border": TRANSPARENT,
        "scrollbar.track.background": TRANSPARENT,
        "scrollbar.track.border": TRANSPARENT,
        # Bars
        "status_bar.background": c["statusBar.background"],
        "title_bar.background": c["titleBar.activeBackground"],
        "title_bar.inactive_background": c["titleBar.inactiveBackground"],
        "toolbar.background": c["editor.background"],
        "tab_bar.background": c["editorGroupHeader.tabsBackground"],
        "tab.active_background": c["tab.activeBackground"],
        "tab.inactive_background": c["tab.inactiveBackground"],
        # Editor
        "editor.background": c["editor.background"],
        "editor.foreground": c["editor.foreground"],
        "editor.gutter.background": c["editorGutter.background"],
        "editor.line_number": c["editorLineNumber.foreground"],
        "editor.active_line_number": c["editorLineNumber.activeForeground"],
        "editor.active_line.background": c["editor.lineHighlightBackground"],
        "editor.highlighted_line.background": c["editor.rangeHighlightBackground"],
        "editor.indent_guide": c["editorIndentGuide.background"],
        "editor.indent_guide_active": c["editorRuler.foreground"],
        "editor.invisible": c["editorWhitespace.foreground"],
        "editor.wrap_guide": c["editorRuler.foreground"],
        "editor.active_wrap_guide": c["editorRuler.foreground"],
        "editor.document_highlight.read_background": c["editor.wordHighlightBackground"],
        "editor.document_highlight.write_background": c["editor.wordHighlightStrongBackground"],
        "editor.document_highlight.bracket_background": faint_wash,
        "editor.subheader.background": c["editorGroupHeader.tabsBackground"],
        "search.match_background": c["editor.findMatchBackground"],
        # Status colors
        "error": c["editorError.foreground"],
        "error.background": c["inputValidation.errorBackground"],
        "error.border": c["inputValidation.errorBorder"],
        "warning": c["editorWarning.foreground"],
        "warning.background": c["inputValidation.errorBackground"],
        "warning.border": c["inputValidation.warningBorder"],
        "info": c["editorInfo.foreground"],
        "info.background": c["inputValidation.infoBackground"],
        "info.border": c["inputValidation.infoBorder"],
        # Zed renders inlay hints with the `hint` status color; the original
        # styles inlays dim gray (editorInlayHint), not the purple editorHint
        # diagnostic color, and inlays are far more visible than hint dots.
        "hint": c.get("editorInlayHint.foreground", c["editorCodeLens.foreground"]),
        "success": c["terminal.ansiGreen"],
        "created": c["editorGutter.addedBackground"],
        "created.background": c["diffEditor.insertedTextBackground"],
        "modified": c["editorGutter.modifiedBackground"],
        "deleted": c["editorGutter.deletedBackground"],
        "deleted.background": c["diffEditor.removedTextBackground"],
        "conflict": c["gitDecoration.conflictingResourceForeground"],
        "renamed": c["editorInfo.foreground"],
        "hidden": c["gitDecoration.ignoredResourceForeground"],
        "ignored": c["gitDecoration.ignoredResourceForeground"],
        "predictive": c["editorCodeLens.foreground"],
        "hint.background": c.get("editorInlayHint.background"),
        "unreachable": c["sideBar.foreground"],
        # Terminal (the original renders it on the VSCode panel background)
        "terminal.background": c["panel.background"],
        "terminal.foreground": c["editor.foreground"],
        "terminal.bright_foreground": c["terminal.ansiBrightWhite"],
        "terminal.dim_foreground": c["terminal.ansiBrightBlack"],
        "terminal.ansi.black": c["terminal.ansiBlack"],
        "terminal.ansi.red": c["terminal.ansiRed"],
        "terminal.ansi.green": c["terminal.ansiGreen"],
        "terminal.ansi.yellow": c["terminal.ansiYellow"],
        "terminal.ansi.blue": c["terminal.ansiBlue"],
        "terminal.ansi.magenta": c["terminal.ansiMagenta"],
        "terminal.ansi.cyan": c["terminal.ansiCyan"],
        "terminal.ansi.white": c["terminal.ansiWhite"],
        "terminal.ansi.bright_black": c["terminal.ansiBrightBlack"],
        "terminal.ansi.bright_red": c["terminal.ansiBrightRed"],
        "terminal.ansi.bright_green": c["terminal.ansiBrightGreen"],
        "terminal.ansi.bright_yellow": c["terminal.ansiBrightYellow"],
        "terminal.ansi.bright_blue": c["terminal.ansiBrightBlue"],
        "terminal.ansi.bright_magenta": c["terminal.ansiBrightMagenta"],
        "terminal.ansi.bright_cyan": c["terminal.ansiBrightCyan"],
        "terminal.ansi.bright_white": c["terminal.ansiBrightWhite"],
        # Zed-only concepts, built from the theme's own palette
        "accents": [
            accent,
            c["terminal.ansiRed"],
            c["terminal.ansiCyan"],
            c["terminal.ansiGreen"],
            c["terminal.ansiBlue"],
            c["terminal.ansiMagenta"],
        ],
        "players": [
            player(cursor),
            player(c["terminal.ansiRed"]),
            player(c["terminal.ansiGreen"]),
            player(c["terminal.ansiYellow"]),
            player(c["terminal.ansiCyan"]),
            player(c["terminal.ansiMagenta"]),
            player(c["editorLineNumber.activeForeground"]),
            player(c["terminal.ansiBrightWhite"]),
        ],
        "syntax": {
            "attribute": syn("entity.other.attribute-name"),
            "boolean": syn("constant.language"),
            "comment": syn("comment"),
            "comment.doc": syn("comment"),
            "constant": syn("constant"),
            "constructor": syn("meta.instance.constructor"),
            "embedded": syn("string source"),
            "emphasis": {"font_style": "italic"},
            "emphasis.strong": {"font_weight": 700},
            "enum": syn("constant"),
            "function": syn("entity.name.function"),
            "function.method": syn("entity.name.function"),
            "function.definition": syn("entity.name.function"),
            "hint": {
                "color": c.get(
                    "editorInlayHint.foreground", c["editorCodeLens.foreground"]
                )
            },
            "keyword": syn("keyword"),
            "label": syn("string.unquoted.label"),
            "link_text": syn("markup.underline.link"),
            "link_uri": syn("markup.underline.link"),
            "number": syn("constant.numeric"),
            "operator": syn("keyword.operator"),
            "predictive": {
                "color": c["editorLineNumber.foreground"],
                "font_style": "italic",
            },
            "preproc": syn("meta.preprocessor"),
            "primary": syn("variable"),
            "property": syn("support.type.property-name"),
            "punctuation": syn("punctuation"),
            "punctuation.bracket": syn("meta.brace.round"),
            "punctuation.delimiter": syn("punctuation"),
            "punctuation.list_marker": syn("punctuation"),
            "punctuation.special": syn("punctuation.section.embedded"),
            "string": syn("string"),
            "string.escape": syn("constant.character.escape"),
            "string.regex": syn("string"),
            "string.special": syn("constant.other.symbol"),
            "string.special.symbol": syn("constant.other.symbol"),
            "tag": syn("entity.name.tag"),
            "text.literal": syn("markup.raw"),
            "title": syn("markup.heading"),
            "type": syn("entity.name.class"),
            "variable": syn("variable"),
            "variable.parameter": syn("variable.parameter"),
            "variable.special": syn("variable.language"),
            "variant": syn("constant"),
            "diff.plus": syn("markup.inserted"),
            "diff.minus": syn("markup.deleted"),
        },
    }

    style = {k: v for k, v in style.items() if v is not None}
    return {"name": name, "appearance": "dark", "style": style}


def main() -> None:
    family = {
        "$schema": "https://zed.dev/schema/themes/v0.2.0.json",
        "name": "Oh Lucy",
        "author": "hermitter (ported by Gustavo Quinta)",
        "themes": [
            build_variant(json.loads((DIST / fname).read_text()), name)
            for fname, name in VARIANTS
        ],
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(family, indent=2) + "\n")
    print(f"wrote {OUT} ({len(family['themes'])} themes)")


if __name__ == "__main__":
    main()
