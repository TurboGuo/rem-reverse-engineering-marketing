---
name: "rem-reverse-engineering-marketing"
description: "Run REM (Reverse Engineering Marketing): tear down a person's or company's last month of social posts via Monid into an interactive HTML playbook. Use for 'REM [name]' or 'reverse engineer @handle'."
---

# REM: Reverse Engineering Marketing

Input: one person or company (name or handle). Output: one published HTML Artifact titled "REM: [Name] Social Playbook" that shows how much they post on each platform, when, what about, and how each kind of post is built, using their real posts as examples.

House rules for every REM run

* Use Exa for web search and Monid for all social data (X included).
* No hyphen character anywhere in visible output (page text, recipe text, chat reply). Replace hyphens in quoted post text with spaces; keep them only inside URLs and code.
* Cite the source for every number (Monid provider + endpoint, pull date). Show calculation steps in the chat reply when you compute a rate or ratio (example: 22 videos ÷ 31 days = 0.71 per day).
* Text on the page is large (body 19px).
* Window = the 31 days ending today. Times shown in Pacific Time (PT).
* Never show placeholder templates like [Product] or angle bracket slots. Every recipe is a real post broken into labeled parts.

## Step 1: Find the official handles

Search with Exa for the target's official accounts (company sites often list them in JSON LD `sameAs`; people list them on a personal site or LinkedIn). Collect: X, Instagram, TikTok, YouTube, LinkedIn (company or /in/ profile), Threads, Facebook. Check Monid balance (`monid_balance`).

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
3. **Content calendar**: 5 week Sun to Sat grid covering the window; each post is a chip (platform, time, 2 line title) colored by type and linking to the post; filter buttons for platforms and types with counts; on phones switch to an agenda list.
4. **The overall playbook**: number tiles first (rate per platform, a green peak time line, one line note, inactive platforms in amber), then a table Platform / Main topics / Call to action.
5. **What they post about**: 6 to 8 theme cards, each with a real number.
6. **One post, every surface**: table of 3 to 4 posts traced across platforms with PT timestamps.
7. **When they post**: optional heatmap of posts per PT hour per platform.
8. **Platform by platform** tabs. Each tab: a facts row (format, cadence, peak time, call to action). Left column "What reached the most people" with a green "👉 Click any bar to open its recipe" hint and clickable bar buttons per type (bordered, › arrow, selected state). Right column is the recipe: a strip of numbered colored part pills, then a post card of the best real post of that type (avatar, name, handle, PT time, platform tag, each part as a colored block with label, one line hint and the real text, a dark media block that links to the real post as "Watch on X ↗", real metrics, Copy text button), then "Open the real post". Below: a Top posts table and a **Content breakdown**: every post newest first as expandable cards with type pill, topic and metric; inside: When, Format and length, Hook (first line or title), Structure (numbered pills), Source of information, What to learn (top and bottom performers, notable ratios), Open the post. Add an Expand all button. Say plainly that video structure is read from captions because the videos were not watched, and say when a caption names no source.
9. **Copy it**: a scaled week for a small team or solo creator (labeled as your adaptation), a checklist, and what not to copy.

No "How the numbers were calculated" section on the page (the user removed it); keep source lines under each block and put calculation steps in the chat reply.

Before publishing: syntax check the script, render once with Playwright (Chromium at /opt/pw-browsers) and look at the one day view, the calendar and one tab; scan visible text for hyphens. Publish with the Artifact tool, icon "megaphone".

## Step 6: Reply in chat

A short summary: the main finding per platform with numbers and their calculation steps, data gaps (no Instagram views, Shorts cap, inferred paid reach), a Sources list, and one question about what to adjust. Handle artifact comment threads by editing the page, replying in the thread, and resolving it.