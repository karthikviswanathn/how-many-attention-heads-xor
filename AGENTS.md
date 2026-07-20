# AGENTS.md

Conventions for writing theorem / writeup markdown in this repo so that it renders cleanly in GitHub, VS Code preview, and Obsidian.

## Math

Use LaTeX math delimiters, not backticks.

- **Inline math:** wrap in single dollar signs, e.g. `$f : \lbrace 0,1\rbrace^n \to \lbrace 0,1\rbrace$`.
- **Display math:** wrap in double dollar signs, with a blank line before and after the block. Keep the whole `$$...$$` on one source line; multi-line `$$` blocks are fragile (GitHub can mis-parse an equation line as a heading or list item).

  ```markdown
  Some lead-in text.

  $$ z(a,b) = \frac{N(a,b)}{D(a,b)} $$

  Continuation text.
  ```

- Use `\lbrace`, `\rbrace` for set braces (space before a following letter, e.g. `\lbrace f\rbrace`), `\to` for arrows, `\neq`, `\geq`, `\leq`, `\in`, `\cdot`, `\top` (for transpose), `\blacksquare` for Q.E.D.
- Use `\lt`, `\gt` for bare `<` and `>` inside math (space before a following letter/digit, e.g. `2 \lt 3`); `\leq`, `\geq`, `\neq`, `\langle`, `\rangle` are macros and already safe.
- Use `\ast` instead of a literal `*` inside math; `*` is Markdown emphasis and corrupts the block.
- Never use `\,`, `\;`, `\!` spacing commands inside math; delete them (a plain space or nothing is fine).
- No math inside headings, list-item display blocks, or `*italic*`/`_italic_` (bold `**...**` is fine).
- When an opener-shaped `_` (e.g. `}_n`) precedes a closer-shaped `_` (e.g. `T_{`) in the same paragraph, insert a space before the closer-shaped `_` (`$T _{n,1}$`) so it can't emphasis-pair.
- Never use the `&#95;` HTML entity for underscores; it renders on GitHub but breaks KaTeX previews (VS Code, GitLab).
- Multi-line derivations use `\begin{aligned} ... \end{aligned}` inside a `$$` block, with `&=` alignment (collapsed onto one line; `&` survives).
- Row separators in a single-line `$$...$$` block (`aligned`, `cases`, `array`, `substack`) are `\cr`, never `\\`; GitHub eats one backslash of `\\` on a single source line and the row break silently vanishes.
- Group short related equations with `\qquad` spacing on one display line rather than stacking many tiny blocks.
- Never use plain ASCII like `!=`, `>=`, `^T`, `sum`, `alpha` in math; always use the LaTeX command.
- Never wrap math in backticks. Backticks are reserved for code identifiers and file paths.

## Structure

- `#` for the theorem title, `##` for top-level sections (`Statement`, `Proof`, `Consequence`, etc.).
- Sub-theorems inside a proof use `###` with a period-separated title like `### Theorem 2. Antipode identities`. Never put an em dash in a heading.
- Inline mini-proofs use **bold run-in headers**: `**Proof.**`, `**Reason.**`, `**Claim.**`.
- Use blockquotes (`>`) for informal restatements or remarks that sit alongside the formal statement.
- Use ordered lists (`1.`, `2.`, ...) for enumerated cases and unordered lists (`-`) for bullet points.

## Prose

- No em dashes anywhere (user global rule). Use `,`, `;`, `:`, or `.` instead. No exceptions for headings, captions, or run-in labels.
- Italicize short emphases with `*...*`; bold with `**...**` for labels and run-in headers.
- Keep paragraphs short. Blank line between paragraphs, between display math and prose, and between list items that contain display math.

## Code and identifiers

- Use backticks only for: file names, directory paths, Lean identifiers, shell commands, and literal code snippets.
- Do **not** use backticks for mathematical variables or expressions. Those go in `$...$`.

## Example skeleton

```markdown
# Theorem Title

## Statement

Let $f : \lbrace 0,1\rbrace^n \to \lbrace 0,1\rbrace$. Suppose ...

$$ \text{main equation} $$

> **Equivalently.** Informal restatement.

## Proof

Prose lead-in.

### Theorem 1. Short name

**Claim.** Something.

**Proof.** Expand:

$$ \begin{aligned} X &= Y + Z \cr &= W. \end{aligned} $$

### Conclusion

Wrap up. $\blacksquare$

## Consequence

$$ H^{\ast}(f) \geq 2. $$
```

Apply this style to every file under `theorems/` and to
`artifacts/intro-materials/writeup.md`.
