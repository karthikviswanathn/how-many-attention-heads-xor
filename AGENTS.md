# AGENTS.md

Conventions for writing lemma / writeup markdown in this repo so that it renders cleanly in GitHub, VS Code preview, and Obsidian.

## Math

Use LaTeX math delimiters, not backticks.

- **Inline math:** wrap in single dollar signs, e.g. `$f : \lbrace0,1\rbrace^n \to \lbrace0,1\rbrace$`.
- **Display math:** wrap in double dollar signs on their own lines, with a blank line before and after.

  ```markdown
  Some lead-in text.

  $z(a,b) = \frac{N(a,b)}{D(a,b)}$

  Continuation text.
  ```

- Use `\{`, `\}` for set braces, `\to` for arrows, `\neq`, `\geq`, `\leq`, `\in`, `\cdot`, `\top` (for transpose), `\blacksquare` for Q.E.D.
- Multi-line derivations use `\begin{aligned} ... \end{aligned}` inside a `$$ ` block, with `&=` alignment. - Group short related equations with `\qquad` spacing on one display line rather than stacking many tiny blocks. - Never use plain ASCII like `!=`, `>=`, `^T`, `sum`, `alpha` in math; always use the LaTeX command. - Never wrap math in backticks. Backticks are reserved for code identifiers and file paths. ## Structure - `#` for the lemma title, `##` for top-level sections (`Statement`, `Proof`, `Consequence`, etc.). - Sub-lemmas inside a proof use `###` with a period-separated title like `### Lemma 2. Antipode identities`. Never put an em dash in a heading. - Inline mini-proofs use \ast\astbold run-in headers\ast\ast: `\ast\astProof.\ast\ast`, `\ast\astReason.\ast\ast`, `\ast\astClaim.\ast\ast`. - Use blockquotes (`>`) for informal restatements or remarks that sit alongside the formal statement. - Use ordered lists (`1.`, `2.`, ...) for enumerated cases and unordered lists (`-`) for bullet points. ## Prose - No em dashes anywhere (user global rule). Use `,`, `;`, `:`, or `.` instead. No exceptions for headings, captions, or run-in labels. - Italicize short emphases with `\ast...\ast`; bold with `\ast\ast...\ast\ast` for labels and run-in headers. - Keep paragraphs short. Blank line between paragraphs, between display math and prose, and between list items that contain display math. ## Code and identifiers - Use backticks only for: file names, directory paths, Lean identifiers, shell commands, and literal code snippets. - Do \ast\astnot\ast\ast use backticks for mathematical variables or expressions. Those go in `$...$`. ## Example skeleton ```markdown # Lemma Title ## Statement Let $f : \lbrace0,1\rbrace^n \to \lbrace0,1\rbrace$. Suppose ... $$
\text{main equation}
$$ > \ast\astEquivalently.\ast\ast Informal restatement. ## Proof Prose lead-in. ### Lemma 1. Short name \ast\astClaim.\ast\ast Something. \ast\astProof.\ast\ast Expand: $$
\begin{aligned}
X &= Y + Z \\
  &= W.
\end{aligned}
$$ ### Conclusion Wrap up. $\blacksquare$ ## Consequence $$
H^{*}(f) \geq 2.
$$
```

Apply this style to every file under `lemmas/` and to `writeup.md`.
