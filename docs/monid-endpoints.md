# Monid endpoints

REM pulls all social data through [Monid](https://monid.ai). Always call `monid_inspect` before `monid_run` (schemas change), then poll `monid_get_run` until the run is `COMPLETED`. Large results are saved to a file; parse them with jq or Python.

Window: the 31 days ending today. Filter by date yourself; several endpoints ignore or misread date fields.

| Platform | Provider + endpoint | Input that worked | Notes |
| --- | --- | --- | --- |
| X timeline | anyapi `/twitter.user_posts` | `{"handle":"rowancheung","route":"lynx"}` | About 20 posts per page. Follow `nextCursor` until `createdUtc` is older than the window. Includes self replies (`isReply: true`), which is where brands put their links. Save the full post text as you go. |
| X search | apify `/apidojo/tweet-scraper` | `{"searchTerms":["from:handle since:2026-09-23 until:2026-10-24"],"sort":"Latest"}` | Fallback only. Returned 9 of a person's posts where the timeline returned all of them. `startUrls` with single tweet URLs returned nothing. |
| Instagram | apify `/apify/instagram-post-scraper` | `{"username":["higgsfield.ai"],"resultsLimit":120,"onlyPostsNewerThan":"2026-09-23","dataDetailLevel":"basicData"}` | Basic data has no view counts; likes and comments are the reach measures. `likesCount: -1` means likes are hidden. |
| TikTok profile | apify `/apidojo/tiktok-profile-scraper` | `{"startUrls":["https://www.tiktok.com/@rowancheung"],"maxItems":60}` | The `until`/`since` fields returned nothing in one run; pull recent items and filter by `uploadedAtFormatted`. Hashtags may contain `null`. |
| TikTok creators | anyapi `/tiktok.search_keyword` | `{"query":"higgsfield","sortBy":"most-liked","datePosted":30}` | Use when the official account is idle. Shows the top of creator activity, not all of it. |
| YouTube | apify `/streamers/youtube-scraper` | `{"startUrls":[{"url":"https://www.youtube.com/@HiggsfieldAI"}],"maxResults":40,"maxResultsShorts":40,"maxResultStreams":5,"oldestPostDate":"2026-09-23","sortVideosBy":"NEWEST"}` | First item is channel info (subscribers, total videos). If Shorts hit the cap, say the real count is higher. Descriptions include chapters and tracked links. |
| LinkedIn | apify `/harvestapi/linkedin-profile-posts` | `{"targetUrls":["https://www.linkedin.com/company/higgsfield/"],"maxPosts":60,"postedLimit":"month"}` | Works for `/company/` and `/in/` URLs. Reposts carry a `repost` object or a header; count them separately. |
| Threads | anyapi `/threads.user_posts` | `{"username":"rowancheung","route":"giraffe"}` | Mostly cross posts; compare timestamps with X and LinkedIn. |
| Facebook | anyapi `/facebook.profile_posts` | `{"url":"https://www.facebook.com/page","route":"giraffe"}` | Often dormant for creators; report the last post date. |

## Cost

The two test runs (Higgsfield, Rowan Cheung) each cost well under $1 in Monid credits. Check `monid_balance` before you start and record each run's `cost`.
