---
name: "rem-reverse-engineering-marketing"
description: "Run REM (Reverse Engineering Marketing): tear down a person's or company's last month of social posts via Monid into an interactive HTML playbook. Use for 'REM [name]' or 'reverse engineer @handle'."
---

# REM: Reverse Engineering Marketing

Input: one person or company (name or handle). Output: one published HTML Artifact titled "REM: [Name] Social Playbook" that shows how much they post on each platform, when, what about, and how each kind of post is built, using their real posts as examples.

House rules for every REM run

* Use Monid for everything: web search and all social data (X included). Do not use other search tools.
* No hyphen character anywhere in visible output (page text, recipe text, chat reply). Replace hyphens in quoted post text with spaces; keep them only inside URLs and code.
* Cite the source for every number (Monid provider + endpoint, pull date). Show calculation steps in the chat reply when you compute a rate or ratio (example: 22 videos ÷ 31 days = 0.71 per day).
* Text on the page is large (body 19px).
* Window = the 31 days ending today. Times shown in Pacific Time (PT).
* Never show placeholder templates like [Product] or angle bracket slots in recipes. Every recipe is a real post broken into labeled parts. The only place [CAPS] slots are allowed is the "Prompt to make this kind of video" box, which says to replace them.

## Step 1: Find the official handles

Search the web through Monid for the target's official accounts: `monid_inspect` then `monid_run` on search1api `/search` (query like "[Name] official X Instagram TikTok YouTube LinkedIn"), and scrape the official site with context.dev `/web/scrape/markdown` when you need its `sameAs` list (company sites often list them in JSON LD `sameAs`; people list them on a personal site or LinkedIn). Collect: X, Instagram, TikTok, YouTube, LinkedIn (company or /in/ profile), Threads, Facebook. Check Monid balance (`monid_balance`).

## Step 2: Pull the month with Monid

Always `monid_inspect` before `monid_run`. Runs are async: poll `monid_get_run`. Large outputs get saved to a file automatically; copy that file into a working folder and parse it with jq or Python. Endpoints that worked:

| Platform | Provider + endpoint | Input notes |
|---|---|---|
| X timeline | anyapi `/twitter.user_posts` | `{handle, route:"lynx"}`, about 20 posts per page, follow `nextCursor` until `createdUtc` is older than the window. Includes self replies (`isReply`). Save full post texts to a file as you go. |
| X search fallback | apify `/apidojo/tweet-scraper` | `searchTerms:["from:handle since:YYYY MM DD until:YYYY MM DD"]` (dates with dashes). Often incomplete; prefer the timeline. startUrls of single tweets returned nothing. |
| Instagram | apify `/apify/instagram-post-scraper` | `{username:[...], resultsLimit:120, onlyPostsNewerThan, dataDetailLevel:"basicData"}` (basic has no view counts). |
| TikTok profile | apify `/apidojo/tiktok-profile-scraper` | `startUrls:["https://www.tiktok.com/@handle"]`, maxItems 60, filter dates yourself (the since/until fields misbehave). |
| TikTok creators | anyapi `/tiktok.search_keyword` | `{query:brand, sortBy:"most-liked", datePosted:30}`. Use when the official account is idle; creators may be the real channel. |
| YouTube | apify `/streamers/youtube-scraper` | `startUrls:[{url:channel}]`, maxResults 30 to 40, maxResultsShorts 40 to 60, `oldestPostDate`, `sortVideosBy:"NEWEST"`. First item is channel info. Note if the Shorts cap is hit. |
| LinkedIn | apify `/harvestapi/linkedin-profile-posts` | `targetUrls:[company or /in/ URL], maxPosts 60 to 80, postedLimit:"month"`. Detect reposts via the `header` or `repost` field. |
| Threads | anyapi `/threads.user_posts` | `{username, route:"giraffe"}`. |
| Facebook | anyapi `/facebook.profile_posts` | `{url, route:"giraffe"}`. |

A full run has cost well under $1. Record each run ID and cost.

## Step 3: Normalize

Build one list of posts, each with: platform, PT date and time, type, short title, URL, metrics (views or likes, comments, bookmarks, shares, duration). Keep self reply link posts as their own type ("Link reply") and replies to other accounts as "Reply to builders". Mark inactive platforms (0 posts, last post date) instead of dropping them.

Classify each post into 6 to 12 content types from its text. Types that worked: Own product launch, Partner model launch, AI agent tie in, Money offer, Company milestone, Community program, Tutorial / breakdown, Story / series, Paid launch explainer (#ad or #partner), AI science and robotics, One line take, Founder life; YouTube splits Long vs Short types. Use ordered keyword rules, then sanity read every assignment.

For each post, segment the caption into labeled parts with line rules (implemented in `scripts/caption_labeler.py`): first line = Hook; lines starting with > → • or numbers = Feature bullets; "Comment WORD" = Keyword CTA; Available / Try / Apply / link in bio = Availability; Credits / Made with = Creator credit; Powered by = Tech; $, %, free, expires, cashback = Offer; ending in ? = Question; hashtags = Tags; Introducing = Product name; else Value line or Story. YouTube: Title, Promise (first description line), Free prompts, Chapters, Link; cut the description at the social links footer. Add the self reply as a final "Self reply" part when one exists. For a person with few posts, write the parts and breakdowns by hand.

## Step 4: Analyze

Per platform: posts, rate (posts ÷ days), peak PT hours, weekdays, average and median metric, top and bottom posts, average metric per type. Cross platform: find the same post published on several platforms and the time gap (often under a minute). Look for: where the link lives (self reply vs bio vs keyword DM), bookmarks vs likes, paid partner tags, likely paid reach (huge views with tiny likes, label it inferred), one liners tested first as replies, creator programs carrying a platform.

## Step 5: Build the page (section order is fixed)

Run the Artifact quickstart once (intent other) and follow its page contract (color tokens for light and dark, side gutter, no external images or iframes, works at phone width).

1. **Header**: eyebrow "Reverse engineered marketing · Teardown no. N", H1 "REM: [Name] Social Playbook", a 3 to 4 sentence thesis with one highlighted phrase, a slate (window, accounts, posts read, PT), and a source line listing every Monid endpoint used.
2. **One day at [Name]**: the month folded into one day. Grid of hour rows by platform columns; a block per hour slot showing count and main type, colored by type, solid when the count is high. For busy accounts show only slots with 2+ posts and drop empty hours (single faded blocks looked empty to the user); for sparse accounts show single posts too and say so.
3. **An average week at [Name]**: seven columns, Mon to Sun. Each column lists the regular slots for that weekday, sorted by hour: hour (PT), platform (colored by platform, with a legend), "N of M [weekday]s" and the usual post type. A slot is regular when the same platform posted in the same hour on at least 2 different dates of that weekday. The day header shows posts per day = posts on that weekday ÷ how many of that weekday fell in the window (state which weekdays occur 5 times). Leave out posts that are not the target's own (for example TikTok creator videos) and say so in the source line.
4. **The overall playbook**: number tiles only: rate per platform, a green peak time line, a one line note, inactive platforms in amber. No topics or call to action table (the user removed it).
5. **What they post about**: 6 to 8 theme cards, each with a real example and a real number.
6. **When they post**: optional heatmap of posts per PT hour per platform.
7. **Platform by platform** tabs. Each tab:
   * Facts row (format, cadence, peak time, call to action).
   * Left column "What reached the most people": a green "👉 Click any bar to open its recipe" hint and clickable bar buttons per type (bordered, › arrow, selected state).
   * Right column, the recipe: a strip of numbered colored part pills, then a post card of the best real post of that type (avatar, name, PT time, platform tag, each part as a colored block with label, one line hint and the real text, a dark media block that links to the real post as "Watch on X ↗", real metrics, Copy text button), then "Open the real post".
   * Under the recipe, **Prompt to make this kind of video**: a copyable prompt that changes with the clicked type, one per type on every platform. Write it as a shot list for an AI video tool: aspect ratio and format for that platform (16:9 for X, LinkedIn and YouTube long; 9:16 for Reels, Shorts and TikTok), length, each shot with its timing and what is on screen, style, sound, and the caption or title pattern that goes with it (keyword call to action on Instagram, title, thumbnail and description lines on YouTube, business framing on LinkedIn). Base it on the real posts of that type and note that videos were read from captions, not watched.
   * A short notes block on what is special about the platform (for example the Comment KEYWORD engine), then a Top posts table.
   * No static caption or title template boxes and no per post Content breakdown (the user removed both).
8. **Content calendar** (last section): a 5 week Sun to Sat grid covering the window; each post is a chip (platform, time, 2 line title) colored by type and linking to the post; filter buttons for platforms and types with counts; on phones switch to an agenda list.

Not on the page (the user removed them): "One post, every surface", "Copy it" weekly plan, "How the numbers were calculated", the topics table, Content breakdown. Keep source lines under each block and put calculation steps in the chat reply. Cross platform timing findings can go in the thesis or theme cards.

Before publishing: syntax check the script, render once with Playwright and check the one day view, the average week, one tab (click every bar and confirm a prompt shows) and the calendar; check for page errors; scan visible text for hyphens. Publish with the Artifact tool, icon "megaphone". When updating a page published in an earlier conversation (or before a context reset), publish to its url after reading it, or the tool creates a separate artifact.

## Step 6: Reply in chat

A short summary: the main finding per platform with numbers and their calculation steps, data gaps (no Instagram views, Shorts cap, inferred paid reach), a Sources list, and one question about what to adjust. Handle artifact comment threads by editing the page, replying in the thread, and resolving it.