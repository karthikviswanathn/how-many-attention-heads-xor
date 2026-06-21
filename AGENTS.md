# AGENTS.md

Conventions for writing lemma / writeup markdown in this repo so that it renders cleanly in GitHub, VS Code preview, and Obsidian.

GitHub's markdown layer mangles math before MathJax sees it, so a KaTeX-valid expression is not always enough. The full ruleset and a faithful audit method live in the [`gh-markdown-math`](.claude/skills/gh-markdown-math/SKILL.md) skill; the essentials are below.

## Math

Use LaTeX math delimiters, not backticks.

- **Inline math:** wrap in single dollar signs, e.g. `$f : \lbrace0,1\rbrace^n \to \lbrace0,1\rbrace$`. Keep each inline span on one source line.
- **Display math:** wrap in double dollar signs. Keep the whole expression on a single line, e.g. `$$ z(a,b) = \frac{N(a,b)}{D(a,b)} $$`, with a blank line before and after.

  ```markdown
  Some lead-in text.

  $$ z(a,b) = \frac{N(a,b)}{D(a,b)} $$

  Continuation text.
  ```

- Use `\lbrace`, `\rbrace` for set braces (not `\{`, `\}`, which GitHub unescapes and breaks). Use `\to` for arrows, `\neq`, `\geq`, `\leq`, `\in`, `\cdot`, `\top` (for transpose), `\blacksquare` for Q.E.D.
- Use `\ast` for an asterisk/superscript-star (e.g. `H^{\ast}`), never a literal `*` inside math (a literal `*` is markdown emphasis and corrupts the span).
- Use `\mathrm{...}` for operator names, not `\operatorname{...}`.
- Do not use the spacing macros `\,` `\;` `\!` (GitHub unescapes them to literal punctuation); use a normal space or `\quad` / `\qquad`.
- Multi-line derivations use `\begin{aligned} ... \end{aligned}` inside a single-line `$$` block, with `&=` alignment and `\\` row breaks.
- Group short related equations with `\qquad` spacing on one display line rather than stacking many tiny blocks.
- Never use plain ASCII like `!=`, `>=`, `^T`, `sum`, `alpha` in math; always use the LaTeX command.
- Never wrap math in backticks. Backticks are reserved for code identifiers and file paths.

### Placement gotchas (GitHub)

- No math in headings (`# ... $n$` is unreliable); use plain text or Unicode.
- Math inside `*italic*` / `_italic_` does not render; keep the `$...$` outside the italics. Math inside `**bold**` is fine.
- Display `$$` does not render inside a list item; use inline `$...$` on the continuation line instead.
- An opening `$` must follow whitespace (`degree $d$`, not `degree-$d$`); a closing `$` must not be immediately followed by a letter (`$b$-th`, not `$b$th`).

## Structure

- `#` for the lemma title, `##` for top-level sections (`Statement`, `Proof`, `Consequence`, etc.).
- Sub-lemmas inside a proof use `###` with a period-separated title like `### Lemma 2. Antipode identities`. Never put an em dash in a heading.
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
# Lemma Title

## Statement

Let $f : \lbrace0,1\rbrace^n \to \lbrace0,1\rbrace$. Suppose ...

$$ \text{main equation} $$

> **Equivalently.** Informal restatement.

## Proof

Prose lead-in.

### Lemma 1. Short name

**Claim.** Something.

**Proof.** Expand:

$$ \begin{aligned} X &= Y + Z \\ &= W. \end{aligned} $$

### Conclusion

Wrap up. $\blacksquare$

## Consequence

$$ H^{\ast}(f) \geq 2. $$
```

Apply this style to every file under `lemmas/` and to `writeup.md`.
