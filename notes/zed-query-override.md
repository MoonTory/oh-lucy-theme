# Can Zed distinguish JS/TS `const` declaration names from uses?

Research verified 2026-07-12 against current Zed `main`, current Zed docs, Zed issues/PR discussion, and the TypeScript semantic-token implementation. The short answer is: **do not try to solve this with a theme override; use LSP semantic tokens plus a semantic-token rule.** That is a supported settings-based solution, with the cost of enabling semantic highlighting and relying on the language server.

## Sources

* Zed docs: [Language Extensions](https://zed.dev/docs/extensions/languages), especially [semantic tokens](https://zed.dev/docs/extensions/languages#syntax-highlighting-with-semantic-tokens)
* Zed docs: [Semantic Tokens](https://zed.dev/docs/semantic-tokens)
* Zed docs: [Theme Overrides](https://zed.dev/docs/themes#theme-overrides)
* Zed source: [`LanguageRegistry::register_language`](https://github.com/zed-industries/zed/blob/main/crates/language/src/language_registry.rs) and extension query loading in [`extension_host.rs`](https://github.com/zed-industries/zed/blob/main/crates/extension_host/src/extension_host.rs)
* Zed maintainer answer: [PR #46547](https://github.com/zed-industries/zed/pull/46547#issuecomment-3743600183) (closed; not merged)
* Relevant current issues: [#42722](https://github.com/zed-industries/zed/issues/42722#issuecomment-3556554997), [#40539](https://github.com/zed-industries/zed/issues/40539), and [#40532](https://github.com/zed-industries/zed/issues/40532#issuecomment-3409144818)
* TypeScript semantic-token source: [`classifier2020.ts`](https://github.com/microsoft/TypeScript/blob/main/src/services/classifier2020.ts) and [`typescript-language-server` LSP server](https://github.com/typescript-language-server/typescript-language-server/blob/master/src/lsp-server.ts)

## 1. User query overrides under `~/.config/zed`: no

There is **no supported user configuration directory/file mechanism** to append, replace, or override the `highlights.scm` query of a built-in language. In particular, putting `languages/typescript/highlights.scm` in a local/user extension directory is not a supported built-in-language override.

This is not an inference from the absence of a documented setting:

* In the maintainer response on [#42722](https://github.com/zed-industries/zed/issues/42722#issuecomment-3556554997), to a report specifically attempting a local user extension override, Zed says: **“There currently is no way to provide such overrides”** and suggests changing/contributing core files.
* The proposed feature [PR #46547](https://github.com/zed-industries/zed/pull/46547) was closed unmerged. Its maintainer response says: **“The only supported way of providing new Tree-sitter queries is via extensions.”** It declined user-extensible queries as a support risk.

Therefore there is no Neovim-like user runtime-query path to add only this pattern to stock JavaScript/TypeScript.

## 2. Extension replacement of a built-in language: technically possible, costly, not a documented per-query override API

An extension can define languages under `languages/<language>/` with a `config.toml` and query files; that is the documented extension language mechanism. Zed's [Language Extensions docs](https://zed.dev/docs/extensions/languages) document `highlights.scm` as the syntax-highlighting query file. A maintainer also identifies extensions as the supported route for *new* Tree-sitter queries (PR #46547 above).

### What current source does

Current `LanguageRegistry::register_language` checks language names and, if the name already exists, replaces the existing registration's grammar, matcher, loader, and manifest name:

```rust
for existing_language in &mut state.available_languages {
    if existing_language.name == name {
        existing_language.grammar = grammar_name;
        existing_language.matcher = matcher;
        existing_language.load = load;
        existing_language.manifest_name = manifest_name;
        return;
    }
}
```

The extension host calls that method with the extension language's `language_name`, and its loader reads query files from the extension's language directory:

```rust
let config = LanguageConfig::load(language_path.join(LanguageConfig::FILE_NAME))?;
let queries = load_plugin_queries(&language_path);
```

So an extension defining a language with the *same Zed language name* (for example `name = "TypeScript"`) can replace the built-in registration when it is registered. In that concrete source-level sense, Zed will prefer the extension registration for the duplicate name.

### Important limitation / cost

This is a **language replacement**, not an additive user-query overlay. `load_plugin_queries` constructs `LanguageQueries` from the extension directory; it does not append the built-in TypeScript `highlights.scm` to the extension's file. Therefore a replacement extension needs to carry a complete compatible copy/fork of the built-in JS/TS language metadata and highlight query, then add the `const` capture. It must be maintained as Zed grammars/configuration change, and it may affect matching, language-server association, injections, indentation, outlines, etc.

The docs do not advertise “override the built-in TypeScript language” as a stable customization interface. Treat duplicate-name replacement as an implementation-backed extension technique, not a small supported settings customization. This also reconciles the apparently conflicting issue reports: extensions are the supported mechanism for defining/providing queries, while [#42722](https://github.com/zed-industries/zed/issues/42722#issuecomment-3556554997) says a local user override of an existing built-in query is not available.

## 3. `theme_overrides`: yes for styles, no for new distinctions

`settings.json` supports the documented `theme_overrides` object, keyed by theme name, and it can override syntax capture styles. Zed's docs show this exact shape:

```json
{
  "theme_overrides": {
    "One Dark": {
      "syntax": {
        "comment": { "font_style": "italic" }
      }
    }
  }
}
```

`experimental_theme_overrides` also exists in current source/settings internals, but **use the documented `theme_overrides` setting**, not an experimental key.

It cannot solve the requested distinction on its own. Theme overrides only say how `variable`, `constant`, etc. render. Stock JS/TS Tree-sitter queries assign ordinary declaration names and ordinary bare uses the same `@variable` baseline. Setting `syntax.variable` purple changes both; it cannot make a capture that the query did not emit.

## 4. The proposed Tree-sitter query is valid

This query is valid for the current JavaScript and TypeScript grammars:

```scm
(lexical_declaration
  "const"
  (variable_declarator
    name: (identifier) @constant))
```

Direct evidence is [Zed issue #40539](https://github.com/zed-industries/zed/issues/40539): it proposes this exact query for JS/TS lowercase `const` bindings and explicitly reports it was tested and works. It can express **const declaration names only**. It deliberately does not match references/usages, so a use remains covered by the stock global `(identifier) @variable` query.

If applied by a full replacement language query, use a new capture such as `@constant` (or a project-specific dotted capture) and set that style purple. But, per section 2, safely applying it means carrying the rest of the built-in query too.

## 5. Zed does use LSP semantic tokens, and this is the supported practical solution

Zed supports LSP semantic-token highlighting, but it is **off by default**. Per the [Semantic Tokens docs](https://zed.dev/docs/semantic-tokens):

* `"off"` — Tree-sitter only (default)
* `"combined"` — Tree-sitter base highlighting plus LSP semantic-token overlays
* `"full"` — LSP semantic tokens replace Tree-sitter for buffers whose server supports them

The docs also support user `global_lsp_settings.semantic_token_rules`; rules match `token_type` plus required `token_modifiers`, are ordered (first match wins), and can use a theme style or explicit foreground color.

### Why this can express exactly the requested JS/TS rule

This is verified at the TypeScript classifier level, not guessed from the word `const`:

1. TypeScript's semantic classifier declares modifiers `declaration` and `readonly`.
2. It adds `declaration` when the identifier is the name of its declaration.
3. For a symbol whose declaration has `NodeFlags.Const`, it adds `readonly`:

```ts
if ((modifiers & ModifierFlags.Readonly) || (nodeFlags & NodeFlags.Const) || (symbol.getFlags() & SymbolFlags.EnumMember)) {
    modifierSet |= 1 << TokenModifier.readonly;
}
```

4. `typescript-language-server` exposes those exact semantic-token modifiers (`declaration`, `static`, `async`, `readonly`, `defaultLibrary`, `local`) in its LSP semantic-token legend and forwards TypeScript's encoded semantic classifications.

Thus a rule requiring **both** `declaration` and `readonly` selects a `const` binding at its declaration but not an ordinary reference. References may carry `readonly` because they resolve to a `const`, but they do not carry `declaration`, which is precisely why both modifiers are required.

Use `combined` initially so normal Tree-sitter highlighting remains in place, then add a rule before less-specific variable rules. For a fixed purple:

```json
{
  "semantic_tokens": "combined",
  "global_lsp_settings": {
    "semantic_token_rules": [
      {
        "token_type": "variable",
        "token_modifiers": ["declaration", "readonly"],
        "foreground_color": "#cba6f7"
      }
    ]
  }
}
```

Or, to keep the palette in the theme, make the theme's `syntax.constant.color` purple and use:

```json
{
  "semantic_tokens": "combined",
  "global_lsp_settings": {
    "semantic_token_rules": [
      {
        "token_type": "variable",
        "token_modifiers": ["declaration", "readonly"],
        "style": ["constant"]
      }
    ]
  }
}
```

The TypeScript language server must be running and advertising semantic tokens. After changing `semantic_tokens`, Zed's docs note that a language-server restart may be required (`editor::RestartLanguageServer`). If the project changes the configured TS server or that server does not provide these modifiers, inspect the token in Zed and this exact rule will not fire; that is the LSP dependency/cost.

## Verdict

**Yes, there is a supported way today:** enable LSP semantic tokens in `"combined"` mode and add a `variable` rule requiring `["declaration", "readonly"]`, styled purple (or mapped to `constant`). For current TypeScript semantic classification, that separates `const` declaration names from usages while leaving the latter on the normal `variable`/white styling.

**Not supported:** a user `~/.config/zed` query override, or doing this with a theme/theme override alone.

**Alternative at much higher cost:** a duplicate-name language extension that replaces JS/TS and ships/maintains a full copied `highlights.scm` with the valid `lexical_declaration` query. It is unnecessary for this goal unless semantic tokens cannot be used.
