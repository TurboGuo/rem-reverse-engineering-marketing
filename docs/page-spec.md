# Page specification

The REM output is one HTML page titled **REM: [Name] Social Playbook**. The section order is fixed. Body text is large (19px) for easy reading, and every color is a token with light and dark values.

## 1. Header

Eyebrow "Reverse engineered marketing · Teardown no. N", the title, a 3 to 4 sentence thesis with one highlighted phrase, a slate (window, accounts, posts read, time zone) and a source line naming every Monid endpoint used.

## 2. One day at [Name]

The whole month folded into one day. Rows are hours (PT), columns are platforms. Each block shows how many posts went out in that hour and the most common type, colored by type, solid when the count is high. For busy accounts show only slots with 2 or more posts and drop empty hours; for sparse accounts show single posts and say so.

## 3. An average week at [Name]

The month folded into one week. Seven columns, Mon to Sun. Each column lists that weekday's regular slots: the hour (PT), the platform (colored, with a legend), how often it happened ("3 of 5 Weds") and the usual post type. A slot counts as regular when the same platform posted in the same hour on at least two different dates of that weekday. Each day header shows posts per day:

```text
posts on that weekday ÷ number of that weekday in the window
```

Posts that are not the target's own (for example creator videos) are left out.

## 4. The overall playbook

Number tiles only: posts per day per platform, a green peak time line and a one line note; inactive platforms in amber.

## 5. What they post about

Six to eight theme cards. Each one has a real example and a real number.

## 6. When they post (optional)

A heatmap of posts per PT hour per platform.

## 7. Platform by platform

One tab per platform:

* **Facts row**: format, cadence, peak time, call to action.
* **What reached the most people**: a bar per content type with its average metric. Bars are buttons with a "Click any bar to open its recipe" hint, a › arrow and a selected state.
* **Recipe**: a strip of numbered colored part pills, then a post card of the best real post of that type. Each part is a colored block with a label, a one line hint and the real text. The media block links to the real post. Real metrics and a Copy text button sit at the bottom.
* **Prompt to make this kind of video**: a copyable shot list for an AI video tool that changes with the clicked type. It gives the aspect ratio (16:9 for X, LinkedIn and YouTube long; 9:16 for Reels, Shorts and TikTok), length, each shot with timing, style, sound, and the caption or title pattern for that platform. Words in [CAPS] are the slots to replace.
* **Platform notes** and a **Top posts** table.

The page says plainly that video structure is read from captions, not from watching the videos.

## 8. Content calendar

The last section. A five week Sunday to Saturday grid. Each post is a chip with platform, time and a two line title, colored by type and linked to the post. Filter buttons for platforms and types show counts. On phones the grid becomes an agenda list.

## Not on the page

No "One post, every surface" table, no topics table, no per post content breakdown, no "Copy it" weekly plan and no calculations section. Sources sit under each block, and calculation steps go in the chat reply.
