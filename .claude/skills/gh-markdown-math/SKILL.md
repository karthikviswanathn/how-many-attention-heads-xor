---
name: gh-markdown-math
description: Write and verify LaTeX math in Markdown that renders correctly on GitHub. Use whenever authoring or editing .md files containing $...$ or $$...$$ math that will be viewed on github.com (READMEs, docs, notes, proofs). GitHub's pipeline mangles backslash-punctuation, emphasis-pairs * and _, mis-parses multi-line $$ as headings/lists, and drops math in headings/lists/italics. This skill lists every failure mode, the fix, and a faithful audit method.
---

# GitHub-safe Markdown math

GitHub renders `$...$` (inline) and `$$...$$` (display) math, but its Markdown
parser runs **before/around** the math step, so Markdown tokens inside math get
mangled and some placements silently fail. Every rule below was verified against
GitHub's real renderer (see **Auditing**). KaTeX/MathJax validity is **not enough** —
it must survive GitHub's Markdown layer too.

## The rules (left = breaks on GitHub → right = fix)

### Inside any `$…$` / `$$…$$`
- `\{` `\}` → `\lbrace` `\rbrace` — GitHub unescapes backslash-punctuation; `\left\{` becomes `\left{` (a hard error that kills the whole block); `\{0,1\}` loses its braces.
- `\,` `\;` `\!` → **delete them** (use a normal space or nothing). They get unescaped to literal `, ; !`. Their named forms `\thinspace`/`\thickspace`/`\negthinspace` are **not supported** by GitHub's renderer, so don't substitute those.
- `*` → `\ast` — a literal `*` is Markdown emphasis. Two `*` on a line/block (e.g. `H^{*}` twice) pair into `<em>` and corrupt the math ("missing open brace"). `\ast` renders identically and isn't a Markdown char.
- `\operatorname{X}` → `\mathrm{X}` — `\operatorname` is unreliable on GitHub.
- `\#` (literal hash, e.g. `\#\{set\}`) → cardinality bars `\lvert\lbrace…\rbrace\rvert`. `\#` unescapes to `#`, a TeX error.
- After substituting a **letter-command** (`\lbrace`, `\rbrace`, …) that is immediately followed by a letter, insert a space: `\{f` → `\lbrace f`, never `\lbracef` (one undefined token).

### Underscores (subscripts)
- A single `_` is fine; intraword `_` (`a_i`, alnum both sides) is always inert. The problem is **two _flankable_ underscores** on the same line or in the same span (e.g. `$\mathrm{OR}_n$ … $T_{n,1}$`, or `$\deg_{\pm}(\mathrm{XOR}_n)$`). A `_` is *flankable* when a neighbor is non-alphanumeric (`}_`, `_{`, `)_`). Two of them pair into `<em>` and break the math.
- Fix: replace those `_` with the HTML entity `&#95;` (e.g. `\mathrm{OR}&#95;n`, `\deg&#95;{\pm}`). GitHub decodes `&#95;`→`_` **after** Markdown, so MathJax sees a real subscript but the emphasis parser never sees a `_`. Apply only on at-risk lines to keep the source readable; display `$$` blocks rarely need it.

### Delimiter placement
- **Opening `$` must be preceded by whitespace/start.** `degree-$d$` fails (hyphen abuts `$`). Fix: `degree $d$` (drop the hyphen) or reword. `$d$-degree` (hyphen *after* the closing `$`) is fine.
- **Closing `$` must not be followed by a letter.** `$b$th` fails. Fix: `$b$-th`.
- **Closing `$` with punctuation on both sides fails**, e.g. `…(a)$)` in `(respectively $\alpha(a)$)` (pattern `)$)`). Fix: reword so the span is followed by a space/word, or pull the formula out of the parenthetical.
- **Inline math must stay on one line.** A `$…$` span that wraps across a source line break does not render. Join it onto one line. (Detect: a line whose single-`$` count, after masking `$$…$$`, is odd.)

### Block / placement structure
- **Multi-line `$$` blocks are fragile** — GitHub leaks block-level Markdown into them. A line that is bare `=`/`-` becomes a Setext heading (the equation renders as a big `<h1>`); a line starting with `+`/`-`/`*` becomes a bullet. **Collapse every `$$…$$` onto a single line** (newlines in math are just whitespace; `\\` and `&` for `aligned`/`cases` are preserved).
- **Display `$$` does not render inside list items.** Use inline `$…$` instead (inline renders on a list-continuation line). ` ```math ` fenced blocks also fail inside lists.
- **No math in headings.** `# … $n$` is unreliable; use plain text / Unicode (`ₙ`, `…`, `≤`).
- **Math inside `*italic*` / `_italic_` does NOT render** — the `$…$` is left raw (`*foo $H$ bar*` renders a literal `$H$`). Move the math outside the italic: `*foo* $H$ *bar*`. **Math inside `**bold**` DOES render** (`**foo $H$ bar**` is fine) — with one exception: if the bolded math span contains a flankable `_` (e.g. `**…$\mathrm{OR}_n$…$T_{n,1}$…**`), the `_` still emphasis-pairs even inside bold and breaks it; apply the `&#95;` fix from *Underscores* there. (Verified on GitHub: `**$H$**`→math, `*$H$*`→raw.)
- **`\begin{cases}` does not render inline.** Use a display `$$` block (not inside a list) or rewrite as prose: `$f(x)=1$ if …, and $2$ otherwise.`

### Generally safe (do not "fix" these)
`\lbrace \rbrace \lvert \rvert \lVert \rVert`, `\mathrm \mathbf \mathbb \mathcal \mathfrak`,
`\bigl \bigr \left \right`, `\frac \sum \prod \binom \sqrt`, `\langle \rangle`,
`\widehat \widetilde \overline`, `\ldots \cdots`, `\leq \geq \neq \pm \in \to \subseteq`,
`\begin{aligned}` / `\begin{cases}` / `\begin{array}` (as single-line `$$`, with `\\` and `&`),
`\substack{a\\b}`, `\blacksquare \varnothing \subsetneq`, `\qquad \quad`. `\\` row breaks survive.

## Auditing (do this, don't guess)

GitHub renders math client-side, so a passing KaTeX check proves nothing. Get the
**faithful** render via the contents API (needs auth: `gh auth status`):

```bash
gh api "repos/OWNER/REPO/contents/PATH?ref=BRANCH" \
  -H "Accept: application/vnd.github.html+json"
```

The returned HTML wraps recognized math in `<math-renderer>…</math-renderer>` holding
the exact LaTeX fed to the engine. Two checks:

1. **Residual `$`** — strip `<math-renderer>…</math-renderer>`, `<code>`, `<pre>`, then
   look for a literal `$`. Any leftover `$` = a delimiter GitHub did **not** recognize =
   broken math. This single check catches almost every failure above.
2. **Leak into structure** — a `<h1-6>` or `<li>` whose text contains raw `\sum`/`\frac`/
   `\begin`/`<em>` where math should be = the block was mis-parsed.

To test a candidate fix without touching the working branch: push a tiny scratch file
to a throwaway branch, fetch it with the API, inspect, then delete the branch.

## Quick fix recipe (mechanical, in order)

1. Collapse every `$$…$$` to one line.
2. In all math: `\{`→`\lbrace`, `\}`→`\rbrace`, `*`→`\ast`, `\operatorname`→`\mathrm`; delete `\,` `\;` `\!`; add a space where a letter-command abuts a letter.
3. On lines with ≥2 flankable `_` in inline math, change those `_`→`&#95;`.
4. Fix delimiter placement: `word-$x$`→`word $x$`; `$x$y`→`$x$-y`; reword `)$)`; join wrapped inline spans.
5. Move math out of headings, list-item display blocks, and `*italic*`/`_italic_` (bold `**…**` is fine).
6. Re-run the residual-`$` audit until it reports 0.

Pitfall: never "fix" delimiter spacing with a regex like `\$[^$]+?\$([A-Za-z])` — its
non-greedy `[^$]+?` mis-pairs the **gap between** two spans and corrupts text. Operate
per-span with explicit positions, or do exact string replaces for known cases.
