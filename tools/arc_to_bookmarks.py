"""Read Arc's sidebar file (read-only) and write a Netscape bookmarks HTML file Vivaldi can import.

Usage: python3 arc_to_bookmarks.py ~/Desktop/arc-spaces-for-vivaldi.html
"""
import html, json, os, sys

SRC = os.path.expanduser('~/Library/Application Support/Arc/StorableSidebar.json')
OUT = sys.argv[1]

d = json.load(open(SRC))
c = d['sidebar']['containers'][1]
it = c['items']
items = {}
for x in it:
    if isinstance(x, dict) and 'id' in x:
        items[x['id']] = x

counts = {'tabs': 0, 'folders': 0}


def esc(s):
    return html.escape(s or '', quote=True)


def render(item_id, ind):
    x = items.get(item_id)
    if not x:
        return []
    pad = '    ' * ind
    tab = (x.get('data') or {}).get('tab')
    if tab:
        url = tab.get('savedURL')
        if not url:
            return []
        title = x.get('title') or tab.get('savedTitle') or url
        counts['tabs'] += 1
        return [f'{pad}<DT><A HREF="{esc(url)}">{esc(title)}</A>']
    kids = []
    for k in x.get('childrenIds', []):
        kids += render(k, ind + 1)
    if not kids:
        return []
    counts['folders'] += 1
    title = x.get('title') or 'Folder'
    return [f'{pad}<DT><H3>{esc(title)}</H3>', f'{pad}<DL><p>'] + kids + [f'{pad}</DL><p>']


def folder(title, child_ids, ind):
    pad = '    ' * ind
    kids = []
    for k in child_ids:
        kids += render(k, ind + 1)
    if not kids:
        return []
    return [f'{pad}<DT><H3>{esc(title)}</H3>', f'{pad}<DL><p>'] + kids + [f'{pad}</DL><p>']


def container_children(cid):
    x = items.get(cid)
    return x.get('childrenIds', []) if x else []


body = []
summary = []
for s in c['spaces']:
    if not isinstance(s, dict):
        continue
    ids = s.get('containerIDs', [])
    pinned = ids[ids.index('pinned') + 1] if 'pinned' in ids else None
    unpinned = ids[ids.index('unpinned') + 1] if 'unpinned' in ids else None
    before = counts['tabs']
    inner = []
    for k in container_children(pinned):
        inner += render(k, 2)
    inner += folder('Today tabs (unpinned)', container_children(unpinned), 2)
    title = s.get('title') or 'Untitled Space'
    if inner:
        body += [f'    <DT><H3>{esc(title)}</H3>', '    <DL><p>'] + inner + ['    </DL><p>']
    summary.append((title, counts['tabs'] - before))

# Favorites (the icons at the top of Arc's sidebar), one list per profile
fav_ids = c.get('topAppsContainerIDs', [])
fav_kids = []
for i in range(1, len(fav_ids), 2):
    fav_kids += container_children(fav_ids[i])
before = counts['tabs']
body += folder('Arc Favorites', fav_kids, 1)
summary.append(('Arc Favorites', counts['tabs'] - before))

out = ['<!DOCTYPE NETSCAPE-Bookmark-file-1>',
       '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">',
       '<TITLE>Bookmarks</TITLE>', '<H1>Bookmarks</H1>', '<DL><p>',
       '<DT><H3>Arc Spaces</H3>', '<DL><p>'] + body + ['</DL><p>', '</DL><p>']
open(OUT, 'w').write('\n'.join(out) + '\n')

for t, n in summary:
    print(f'{n:4}  {t}')
print(f'total links: {counts["tabs"]}')
