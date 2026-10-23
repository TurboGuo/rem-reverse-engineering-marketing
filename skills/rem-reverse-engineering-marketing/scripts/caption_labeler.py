"""Caption labeler for REM (Reverse Engineering Marketing).

Splits a social post caption (or a YouTube title and description) into labeled
parts such as Hook, Feature bullets, Keyword CTA, Offer, Availability and
Creator credit. Each part comes back as [kind, label, hint, text]; `kind` maps
to a color slot on the REM page.

Usage:
    from caption_labeler import segment
    parts = segment(caption)                                        # X, Instagram, LinkedIn, TikTok
    parts = segment(description, title=title, yt=True, own_domain="example.com")  # YouTube
"""
import re

HINT = {
    'Hook': 'The first line. A claim or a name.',
    'Product name': '"Introducing [Name]." on its own line.',
    'Value line': 'What it does for the viewer.',
    'Feature bullets': 'Short lines starting with ">" or an arrow.',
    'Keyword CTA': 'Comment a word, get the link by DM.',
    'Availability': 'Where and when to get it.',
    'Offer': 'A number, a deadline or free use.',
    'Creator credit': 'Tags the creator who made it.',
    'Tech': 'What powers it.',
    'Question': 'Invites replies.',
    'Story': 'Context or a short story.',
    'Tags': 'Hashtags or partner tags.',
    'Link': 'A link out.',
    'Title': 'The video title.',
    'Thanks': 'A thank you to the community.',
    'Promise': 'One line on what you will learn or get.',
    'Free prompts': 'Gives away prompts and assets for a click.',
    'Chapters': 'Timestamped steps, so it reads like a course.',
}

# label -> color slot on the page
KIND = {
    'Hook': 'hook', 'Product name': 'proof', 'Value line': 'story', 'Feature bullets': 'list',
    'Keyword CTA': 'cta', 'Availability': 'cta', 'Offer': 'twist', 'Creator credit': 'tag',
    'Tech': 'tag', 'Question': 'close', 'Story': 'story', 'Tags': 'tag', 'Link': 'cta',
    'Title': 'hook', 'Thanks': 'close', 'Promise': 'proof', 'Free prompts': 'prompt', 'Chapters': 'list',
}

MERGE = ('Feature bullets', 'Story', 'Tags', 'Value line', 'Chapters', 'Link')


def label(line, i, own_domain=None):
    l = line.strip()
    L = l.lower()
    if i == 0:
        return 'Hook'
    if re.match(r'^(>|→|›|•|\d+[.)]|routine \d)', L) or l.startswith('- '):
        return 'Feature bullets'
    if re.search(r'comment\s*[“"«]', L):
        return 'Keyword CTA'
    if L.startswith(('credits', 'starring', 'made with', 'original video')):
        return 'Creator credit'
    if L.startswith('powered by'):
        return 'Tech'
    if re.match(r'^(#\S+\s*)+$', l) or L.startswith('#'):
        return 'Tags'
    if L.startswith(('introducing', 'meet ')):
        return 'Product name'
    if re.search(r'(cashback|% off|free|expires|until |closes|first come|\$\d|unlimited|bonus)', L):
        return 'Offer'
    if (L.startswith(('available', 'try ', 'start ', 'apply', 'learn', 'connect', 'click', 'sign up',
                      'read more', 'explore', 'watch'))
            or 'available now' in L or 'link in' in L):
        return 'Availability'
    if 'http' in L or 'lnkd.in' in L or (own_domain and own_domain in L):
        return 'Link'
    if 'thank' in L:
        return 'Thanks'
    if l.endswith('?'):
        return 'Question'
    return 'Value line' if i <= 2 else 'Story'


def segment(text, title=None, maxseg=9, yt=False, own_domain=None):
    lines = [x.strip() for x in re.split(r'\n+', text or '') if x.strip()]
    out = []
    if title:
        out.append(['Title', title])
    for i, l in enumerate(lines):
        lab = label(l, i if not title else i + 1, own_domain)
        if yt:
            L = l.lower()
            # stop at the social links footer of a YouTube description
            if L.strip(': ') in ('links', 'useful links') or 'discord' in L or L.startswith(('twitter', 'instagram')):
                break
            if i == 0:
                lab = 'Promise'
            elif re.match(r'^\d{1,2}:\d{2}', l) or L.startswith('chapters'):
                lab = 'Chapters'
            elif 'prompt' in L and ('http' in L or (own_domain and own_domain in L)):
                lab = 'Free prompts'
            elif 'http' in L or (own_domain and own_domain in L):
                lab = 'Link'
            elif lab != 'Keyword CTA':
                lab = 'Story'
        if out and out[-1][0] == lab and lab in MERGE:
            out[-1][1] += '\n' + l
        else:
            out.append([lab, l])
    out = out[:maxseg]
    for o in out:
        if o[0] == 'Chapters':
            ls = o[1].split('\n')
            o[1] = '\n'.join(ls[:5]) + ('\n…' if len(ls) > 5 else '')
        if o[0] == 'Story' and len(o[1]) > 260:
            o[1] = o[1][:260].rsplit(' ', 1)[0] + '…'
    # REM output rule: no hyphen characters in visible text
    return [[KIND[a], a, HINT[a], b.replace('-', ' ')] for a, b in out]


if __name__ == '__main__':
    demo = ("Kling is back.\n\nKling 4.0 is now live on Higgsfield.\n\n"
            "> Omni Reference\n> 30 second scenes\n\nAvailable now on Higgsfield.")
    for part in segment(demo):
        print(part[1], '|', part[3])
