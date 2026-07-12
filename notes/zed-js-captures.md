# Current Zed JavaScript, TypeScript, and Rust highlight captures

Research date: 2026-07-12. Queries fetched from Zed `main` (the paths in the question have moved):

* [JavaScript `highlights.scm`](https://raw.githubusercontent.com/zed-industries/zed/main/crates/grammars/src/javascript/highlights.scm)
* [TypeScript `highlights.scm`](https://raw.githubusercontent.com/zed-industries/zed/main/crates/grammars/src/typescript/highlights.scm)
* [Rust `highlights.scm`](https://raw.githubusercontent.com/zed-industries/zed/main/crates/grammars/src/rust/highlights.scm)

The relevant JavaScript and TypeScript query portions are the same (apart from unrelated TypeScript additions). The text below quotes the query lines verbatim.

## 1. JS/TS keyword captures

`const`, `let`, and `var` are **not** plain `@keyword`; all three are `@keyword.declaration` in both queries:

```scm
[
  "const"
  "let"
  "var"
  "function"
  "class"
  "enum"
  "interface"
  "type"
] @keyword.declaration
```

The complete set of dotted `keyword` captures present in **each** current JS and TS query is:

```text
@keyword.control
@keyword.declaration
@keyword.import
@keyword.operator.regex
```

Plain `@keyword` is also present. There is no `@keyword.storage` capture.

For the requested individual words, the exact assignments are:

| Word | Capture | Evidence |
| --- | --- | --- |
| `const`, `let`, `var` | `@keyword.declaration` | declaration block above |
| `function`, `class` | `@keyword.declaration` | declaration block above |
| `typeof`, `async`, `new` | `@keyword` | plain-keyword block below |
| `await` | `@keyword.control` | control-keyword block below |

Plain-keyword query (verbatim; this contains `async`, `new`, and `typeof`):

```scm
[
  "abstract"
  "as"
  "async"
  "debugger"
  "declare"
  "default"
  "delete"
  "extends"
  "get"
  "implements"
  "in"
  "instanceof"
  "keyof"
  "module"
  "namespace"
  "new"
  "of"
  "override"
  "private"
  "protected"
  "public"
  "readonly"
  "set"
  "static"
  "target"
  "typeof"
  "using"
  "void"
  "with"
] @keyword
```

Control-keyword query (verbatim; this contains `await`):

```scm
[
  "await"
  "break"
  "case"
  "catch"
  "continue"
  "do"
  "else"
  "finally"
  "for"
  "if"
  "return"
  "switch"
  "throw"
  "try"
  "while"
  "yield"
] @keyword.control
```

The other two dotted groups (also verbatim) are:

```scm
[
  "export"
  "from"
  "import"
] @keyword.import

(regex_flags) @keyword.operator.regex
```

## 2. JS/TS declared names and identifier uses

Both queries begin with this global match:

```scm
; Variables
(identifier) @variable
```

Therefore a normal declaration name in a `variable_declarator`, such as `x` in `const x = 1`, is captured as `@variable`; there is **no separate ordinary** `(variable_declarator name: (identifier) @variable.declaration)` query.

Crucially, that same global `(identifier) @variable` also captures bare identifier usages elsewhere. They are **not uncaptured**. More-specific structural queries add captures for some contexts; for example, a variable declared with a function/arrow-function initializer has this additional/specialized capture:

```scm
(variable_declarator
  name: (identifier) @function
  value: [
    (function_expression)
    (arrow_function)
  ])
```

Calls, parameters, and special identifiers are likewise captured specifically (verbatim):

```scm
(call_expression
  function: (identifier) @function)

(required_parameter
  (identifier) @variable.parameter)

(optional_parameter
  (identifier) @variable.parameter)

(catch_clause
  parameter: (identifier) @variable.parameter)

(arrow_function
  parameter: (identifier) @variable.parameter)

(this) @variable.special

(super) @variable.special
```

So, for theme design, set `variable` for the default/bare-name baseline, and set more-specific captures such as `function` and `variable.parameter` if desired. Query captures can overlap; the specialized query is why a theme should not assume every identifier will render only as `variable`.

## 3. Rust comparison

Yes: Rust likewise has a global identifier capture at the very start of its current query:

```scm
(identifier) @variable

(metavariable) @variable
```

Thus Rust bare identifiers and ordinary binding names receive the `@variable` baseline; Rust does not need a `let_declaration` query to establish that baseline. As in JS/TS, specialized contexts are additionally matched. Relevant lines include:

```scm
(call_expression
  function: [
    (identifier) @function
    (scoped_identifier
      name: (identifier) @function)
    (field_expression
      field: (field_identifier) @function.method)
  ])

(function_item
  name: (identifier) @function.definition)

((identifier) @type
  (#match? @type "^[A-Z]"))

((identifier) @constant
  (#match? @constant "^_*[A-Z][A-Z\\d_]*$"))

(parameter
  (identifier) @variable.parameter)
```

Accordingly, “Rust assigns `@variable` globally” is correct as a statement about the global query line, but it is not an exclusive rendering guarantee: call targets, definition names, parameter names, uppercase type-like identifiers, and all-caps constants have more-specific matches too.

## Direct answers

1. JS and TS: `const`/`let`/`var` are `@keyword.declaration`; dotted keyword names are `keyword.control`, `keyword.declaration`, `keyword.import`, and `keyword.operator.regex`. No `keyword.storage` exists. `typeof`, `async`, and `new` are `@keyword`; `await` is `@keyword.control`; `class` and `function` are `@keyword.declaration`.
2. Normal variable-declarator names get the global `@variable`, and bare identifier usages also get global `@variable`. A function-valued declarator is specially matched as `@function`.
3. Rust has the same global `(identifier) @variable` rule, with specialized overlapping matches.
4. The exact relevant query blocks are quoted above.
