---
name: gh-markdown-math
description: Write and verify LaTeX math in Markdown that renders correctly on GitHub AND in local KaTeX previews (VS Code's built-in Markdown preview). Use whenever authoring or editing .md files containing $...$ or $$...$$ math that will be viewed on github.com (READMEs, docs, notes, proofs). GitHub's pipeline mangles backslash-punctuation, emphasis-pairs * and _, mis-parses multi-line $$ as headings/lists, and drops math in headings/lists/italics. This skill lists every failure mode, a fix that works on both platforms, and a faithful audit method for each.
---

# GitHub-safe Markdown math

GitHub renders `$...$` (inline) and `$$...$$` (display) math, but its Markdown
parser runs **before/around** the math step, so Markdown tokens inside math get
mangled and some placements silently fail. Every rule below was verified against
GitHub's real renderer (see **Auditing**). KaTeX/MathJax validity is **not enough** —
it must survive GitHub's Markdown layer too.

**Dual target.** The same file is usually also read in VS Code's built-in Markdown
preview, which feeds the raw text between `$` delimiters straight to KaTeX (entities
NOT decoded, Markdown emphasis not applied inside math). Every fix in this skill is
KaTeX-safe and works on both platforms, with one flagged exception: the `&#95;`
entity trick (see *Underscores*), which is GitHub-only and shows as a KaTeX parse
error in VS Code. Prefer the dual-safe fixes.

## The rules (left = breaks on GitHub → right = fix)

### Inside any `$…$` / `$$…$$`
- `\{` `\}` → `\lbrace` `\rbrace` — GitHub unescapes backslash-punctuation; `\left\{` becomes `\left{` (a hard error that kills the whole block); `\{0,1\}` loses its braces.
- `\,` `\;` `\!` → **delete them** (use a normal space or nothing). They get unescaped to literal `, ; !`. Their named forms `\thinspace`/`\thickspace`/`\negthinspace` are **not supported** by GitHub's renderer, so don't substitute those.
- `*` → `\ast` — a literal `*` is Markdown emphasis. Two `*` on a line/block (e.g. `H^{*}` twice) pair into `<em>` and corrupt the math ("missing open brace"). `\ast` renders identically and isn't a Markdown char.
- `\operatorname{X}` → `\mathrm{X}` — `\operatorname` is unreliable on GitHub.
- `\#` (literal hash, e.g. `\#\{set\}`) → cardinality bars `\lvert\lbrace…\rbrace\rvert`. `\#` unescapes to `#`, a TeX error.
- After substituting a **letter-command** (`\lbrace`, `\rbrace`, …) that is immediately followed by a letter, insert a space: `\{f` → `\lbrace f`, never `\lbracef` (one undefined token).

### Underscores (subscripts)
- Intraword `_` (`a_i`, `x_i` — alnum on both sides) is always inert; any number of them is fine. The hazard comes from two shapes (classified by the characters adjacent to the `_`):
  - **opener-shaped**: punctuation before, letter/digit after — `}_n`, `)_n` (e.g. `$\mathrm{OR}_n$`);
  - **closer-shaped**: letter/digit before, punctuation after — `T_{`, `g_{` (e.g. `$T_{n,1}$`, `$\deg_{\pm}$`).
- Math breaks **iff an opener-shaped `_` is followed later by a closer-shaped `_` in the same paragraph** — they emphasis-pair into `<em>` across everything in between. This crosses source lines (a wrapped list item is one paragraph), crosses `$…$` span boundaries, and even happens inside `**bold**`. Verified: `$\mathrm{OR}_n$ … $T_{n,1}$` breaks (opener→closer, even on different lines); `$T_{n,1}$ … $\mathrm{OR}_n$` is fine (closer first); `$\deg_{\pm}(\mathrm{XOR}_n)$` alone is fine (closer before opener); any number of opener-shaped `_` alone is fine.
- **Fix (dual-safe, use this): put a space before each closer-shaped `_`** — `$T _{n,1}$`, `$\deg _{\pm}$`. A `_` preceded by whitespace cannot close emphasis, and TeX ignores the space, so GitHub, KaTeX, and MathJax all render a normal subscript. (The spaced `_` can at worst act as an opener, which is harmless.) Alternatively move the subscript inside the argument (`\mathrm{XOR_n}` — intraword, inert) if the upright subscript style is acceptable.
- GitHub-only fallback: the HTML entity `&#95;` (e.g. `\mathrm{OR}&#95;n`) also works because GitHub decodes it after Markdown — but it **breaks VS Code / any KaTeX preview**, which passes the entity raw into KaTeX (parse error on `&`). Avoid unless the file is GitHub-only.

### Delimiter placement
- **Opening `$` must be preceded by whitespace/start.** `degree-$d$` fails (hyphen abuts `$`). Fix: `degree $d$` (drop the hyphen) or reword. `$d$-degree` (hyphen *after* the closing `$`) is fine.
- **Closing `$` must not be followed by a letter.** `$b$th` fails. Fix: `$b$-th`.
- **Closing `$` with punctuation on both sides fails**, e.g. `…(a)$)` in `(respectively $\alpha(a)$)` (pattern `)$)`). Fix: reword so the span is followed by a space/word, or pull the formula out of the parenthetical.
- **Inline math must stay on one line.** A `$…$` span that wraps across a source line break does not render. Join it onto one line. (Detect: a line whose single-`$` count, after masking `$$…$$`, is odd.)

### Block / placement structure
- **Multi-line `$$` blocks are fragile** — GitHub leaks block-level Markdown into them. A line that is bare `=`/`-` becomes a Setext heading (the equation renders as a big `<h1>`); a line starting with `+`/`-`/`*` becomes a bullet. **Collapse every `$$…$$` onto a single line** (newlines in math are just whitespace; `\\` and `&` for `aligned`/`cases` are preserved).
- **Display `$$` does not render inside list items.** Use inline `$…$` instead (inline renders on a list-continuation line). ` ```math ` fenced blocks also fail inside lists.
- **No math in headings.** `# … $n$` is unreliable; use plain text / Unicode (`ₙ`, `…`, `≤`).
- **Math inside `*italic*` / `_italic_` does NOT render** — the `$…$` is left raw (`*foo $H$ bar*` renders a literal `$H$`). Move the math outside the italic: `*foo* $H$ *bar*`. **Math inside `**bold**` DOES render** (`**foo $H$ bar**` is fine) — with one exception: an opener→closer underscore pair (e.g. `**…$\mathrm{OR}_n$…$T_{n,1}$…**`) still emphasis-pairs inside bold and breaks it; apply the space-before-closer fix from *Underscores* (`$T _{n,1}$`), which is verified to work inside bold. (Verified on GitHub: `**$H$**`→math, `*$H$*`→raw.)
- **`\begin{cases}` does not render inline.** Use a display `$$` block (not inside a list) or rewrite as prose: `$f(x)=1$ if …, and $2$ otherwise.`

### Generally safe (do not "fix" these)
`\lbrace \rbrace \lvert \rvert \lVert \rVert`, `\mathrm \mathbf \mathbb \mathcal \mathfrak`,
`\bigl \bigr \left \right`, `\frac \sum \prod \binom \sqrt`, `\langle \rangle`,
`\widehat \widetilde \overline`, `\ldots \cdots`, `\leq \geq \neq \pm \in \to \subseteq`,
`\begin{aligned}` / `\begin{cases}` / `\begin{array}` (as single-line `$$`, with `\\` and `&`),
`\substack{a\\b}`, `\blacksquare \varnothing \subsetneq`, `\qquad \quad`. `\\` row breaks survive.

## Auditing (do this, don't guess)

GitHub renders math client-side, so a passing KaTeX check alone proves nothing. Get the
**faithful** render via the Markdown render API — no commit, push, or branch needed
(needs auth: `gh auth status`):

```bash
jq -n --rawfile t FILE.md '{text:$t, mode:"gfm", context:"OWNER/REPO"}' \
  | gh api markdown --input -
```

This is the same pipeline GitHub uses for README rendering. (Alternative, for auditing
exactly what a pushed branch shows: `gh api "repos/OWNER/REPO/contents/PATH?ref=BRANCH"
-H "Accept: application/vnd.github.html+json"`.)

The returned HTML wraps recognized math in `<math-renderer>…</math-renderer>` holding
the exact LaTeX fed to the engine. Two checks:

1. **Residual `$`** — strip `<math-renderer>…</math-renderer>`, `<code>`, `<pre>`, then
   look for a literal `$`. Any leftover `$` = a delimiter GitHub did **not** recognize =
   broken math. This single check catches almost every failure above.
2. **Leak into structure** — a `<h1-6>` or `<li>` whose text contains raw `\sum`/`\frac`/
   `\begin`/`<em>` where math should be = the block was mis-parsed.

The render API also makes candidate fixes cheap to test: put the variants in a small
throwaway .md, render it, and compare which shapes survive — no scratch branch required.

**VS Code / KaTeX side.** After the GitHub audit passes, verify the KaTeX side by
extracting every math span (mask code fences and inline code first; `$$…$$` before
`$…$`) and running each through `katex.renderToString(tex, {throwOnError: true})`
(`npm install katex`, then a short node script). 0 failures = the file renders in
VS Code's preview. If katex isn't installable, a static scan for the one known
divergence — `&#…;` entities inside math — is usually sufficient, since every other
fix in this skill is KaTeX-safe.

## Quick fix recipe (mechanical, in order)

1. Collapse every `$$…$$` to one line.
2. In all math: `\{`→`\lbrace`, `\}`→`\rbrace`, `*`→`\ast`, `\operatorname`→`\mathrm`; delete `\,` `\;` `\!`; add a space where a letter-command abuts a letter.
3. In each paragraph where an opener-shaped `_` (`}_n`) precedes a closer-shaped `_` (`T_{`), insert a space before each closer-shaped `_`: `$T _{n,1}$`, `$\deg _{\pm}$`. (Do NOT use `&#95;` — it breaks KaTeX previews.)
4. Fix delimiter placement: `word-$x$`→`word $x$`; `$x$y`→`$x$-y`; reword `)$)`; join wrapped inline spans.
5. Move math out of headings, list-item display blocks, and `*italic*`/`_italic_` (bold `**…**` is fine).
6. Re-run the residual-`$` audit until it reports 0, then run the KaTeX check.

Pitfall: never "fix" delimiter spacing with a regex like `\$[^$]+?\$([A-Za-z])` — its
non-greedy `[^$]+?` mis-pairs the **gap between** two spans and corrupts text. Operate
per-span with explicit positions, or do exact string replaces for known cases.
