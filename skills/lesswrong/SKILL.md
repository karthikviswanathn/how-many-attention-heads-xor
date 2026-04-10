---
name: lesswrong
version: 2.0.0
description: APIs for reading content on LessWrong, and helping users edit posts they share with an agent.
homepage: https://www.lesswrong.com
---

LessWrong: A site dedicated to improving the art of rationality
===============================================================

Most pages on LessWrong have an HTML version and a Markdown version. Routes starting with `/api/` are either Markdown or JSON.

For routes not starting with `/api`, you can control which version you get with the `Accept` header or with a query parameter `?format=markdown`, for example:

```sh
curl -H "Accept: text/markdown" https://www.lesswrong.com
curl https://www.lesswrong.com/?format=markdown
```

The Markdown versions of pages are designed to be more AI-agent-friendly than the HTML versions.

If your `Accept` header is `text/markdown`, you will only get Markdown pages. Pages that do not have a markdown version will return `406`.

Finding content to read:
- `/api/home`
- `/api/latest`
- `/api/recent`
- `/api/curated`
- `/api/search` docs when no query, results with `?search=...`
- `/api/community` with `?lat=..&lng=..` for nearby in-person events
- Add `?limit=n` to list routes, max `100`

Reading posts:
- `/api/post/[id]`
- `/api/events/[id]`
- `/api/events/[id]/[slug]`
- `/api/rationality/[slug]`
- `/api/codex/[slug]`
- `/api/hpmor/[slug]`
- `/api/about`
- `/api/faq`
- `/api/contact`
- Add `?compact=1` on post route to omit some heavy media, math, and table content

Post comments:
- `/api/post/[id]/comments`
- `/api/post/[id]/comments/[commentId]`
- Comments route supports `?sort=top|new|old`, `?limit=n`, `?includeReactionUsers=1`

Reading tags:
- `/api/tag/[slug]`

Reading users:
- `/api/user/[slug]`

Reading sequences:
- `/api/sequence/[id]`
- `/api/sequence/[id]/post/[postId]`

Reading collections:
- `/api/rationality`
- `/api/codex`
- `/api/hpmor`

Testing network access:
- `/api/agent/ping` with `GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `OPTIONS`, `HEAD`

Reporting Feedback About This API
=================================

AI agents should use this endpoint to report:
- Bugs in the markdown or agent API
- Gaps in functionality that make the API harder to use
- Anything the user asks the agent to report to the LessWrong developers

Submit feedback with:

```text
POST /api/agent/feedback
```

JSON body:

```json
{
  "message": "string",
  "type": "bug_report|functionality_gap|user_requested_report|other",
  "agentName": "string",
  "userRequest": "string",
  "endpoint": "string",
  "details": {}
}
```

This endpoint forwards the message to the developers' Slack channel.

Helping Users With Drafts
=========================

This feature is in development. The API should not be assumed stable, and users should be reminded of LessWrong's LLM writing policy at `https://www.lesswrong.com/post/KXujJjnmP85u8eM6B`.

Before using the API to leave feedback, check whether network access to the domain is available. You can do this by checking the allowed domains list in the harness or by making an empty test request to `https://www.lesswrong.com/api/agent/ping`.

## Default Review Structure

If the user asks for feedback on their post, consider the following by default unless they explicitly request otherwise. Skip items that are obviously irrelevant.

- Well-established premises
  Consider the likely target audience of the post within the broader LessWrong community. Do any arguments depend on premises likely to be controversial or unfamiliar to that audience?
- Local validity
  Do any claims fail to follow from the stated premises?
- Missed considerations
  Take a broad-picture view of the post and its claims. What important considerations might be missing?
- Accurate representation of sources
  Wherever the post cites a source or links to another resource as part of an argument, fetch that resource and verify that it is accurately understood and represented.
- Existing arguments
  Are there existing arguments, research, or writing on the subject that are relevant enough that omitting them would be a major oversight?
- Clarity
  Is the writing clear and easy to understand? Look for explicit mistakes, ambiguous references, and sentences that are too long.
- Everything else
  This is not comprehensive. Call out any other mistakes, issues, or areas for improvement.

## Setup And Usage Instructions

If the harness permits standard HTTP requests with tools like `curl`, the endpoints below should work without special setup.

When making POST requests, prefer piping JSON from a heredoc to avoid shell escaping issues:

```sh
cat <<'EOF' | curl -X POST https://www.lesswrong.com/api/agent/commentOnDraft \
  -H 'Content-Type: application/json' \
  -d @-
{
  "postId": "...",
  "key": "...",
  "comment": "..."
}
EOF
```

## API Documentation

The API can be used to edit and comment on post drafts, which will appear in the post editor. This is only available for posts written using the lexical editor.

To give an AI agent access, the user needs to set the permissions for "Anyone with the link can" to "Edit", then copy the edit-post URL:

```text
https://www.lesswrong.com/editPost?postId=XYZXYZ&key=XYZXYZ
```

The `key` in the URL is the link-sharing key and should not be shared unless the user explicitly asks for that.

Read the draft with:

```text
GET /editPost?postId=[id]&key=[linkSharingKey]
```

The `editPost` response includes a "Comment Threads" section after the post body if there are open comment or suggestion threads.

Add comments to the draft:

```text
POST /api/agent/commentOnDraft
{ postId, key, agentName?, quote?, comment }
```

If a `quote` is provided, the comment is attached to matching quoted text. Both the quote and the comment should be markdown.

Reply to an existing thread:

```text
POST /api/agent/replyToComment
{ postId, key, agentName?, threadId, comment }
```

Replace text inside the draft:

```text
POST /api/agent/replaceText
{ postId, key, agentName?, quote, replacement, mode?: "edit"|"suggest" }
```

If the user does not specify a mode, use `suggest`.

Insert new blocks of text:

```text
POST /api/agent/insertBlock
{ postId, key, agentName?, location: "start"|"end"|{ before: string }|{ after: string }, markdown, mode?: "edit"|"suggest" }
```

`location` should match the start of an existing paragraph.

Delete an existing block:

```text
POST /api/agent/deleteBlock
{ postId, key, prefix, mode?: "edit"|"suggest" }
```

Insert an LLM content block:

```text
POST /api/agent/insertLLMBlock
{ postId, key, modelName?: string, markdown: string, location: "start"|"end"|{ before: string }|{ after: string } }
```

If `modelName` is omitted, it defaults to `AI Agent`. LLM content blocks are inserted directly and do not use suggest mode.

LLM content blocks are represented in markdown as:

```text
%%% llm-output model="Claude Opus 4.6"
The markdown content of the block...
%%% /llm-output
```

Insert a custom widget:

```text
POST /api/agent/insertWidget
{ postId, key, agentName?, content, location }
```

The content is raw HTML or JS, not markdown.

Replace a widget:

```text
POST /api/agent/replaceWidget
{ postId, key, agentName?, widgetId, replacement?: string, unifiedDiff?: string, mode?: "edit"|"suggest" }
```

Provide exactly one of `replacement` or `unifiedDiff`.
