#!/usr/bin/env python3
"""Convert a Disqus export (.xml.gz) into data/comments.json, displayed statically by the site.

Usage: scripts/disqus-to-data.py <disqus-export.xml.gz>
"""
import gzip
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

NS = {'d': 'http://disqus.com'}
DSQ_ID = '{http://disqus.com/disqus-internals}id'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECTIONS = ('posts', 'projects')


def page_key(link):
    """Map an old page URL to a content bundle key, e.g. "posts/control-robot-two-engines"."""
    segments = [s for s in urlparse(link).path.split('/') if s]
    if not segments:
        return None
    slug = re.sub(r'_\d+$', '', re.sub(r'^\d{4}-\d\d-\d\d-', '', segments[-1]))
    for section in SECTIONS:
        if os.path.isdir(os.path.join(ROOT, 'content', section, slug)):
            return '%s/%s' % (section, slug)
    return None


def main(export_path):
    with gzip.open(export_path) as f:
        root = ET.parse(f).getroot()

    thread_keys = {}
    for thread in root.findall('d:thread', NS):
        link = thread.findtext('d:link', namespaces=NS)
        key = page_key(link)
        if key is None:
            print('Unmatched thread: %s' % link, file=sys.stderr)
        thread_keys[thread.get(DSQ_ID)] = key

    comments = {}
    for post in root.findall('d:post', NS):
        if post.findtext('d:isSpam', namespaces=NS) == 'true':
            continue
        parent = post.find('d:parent', NS)
        comments[post.get(DSQ_ID)] = {
            'key': thread_keys.get(post.find('d:thread', NS).get(DSQ_ID)),
            'parent': parent.get(DSQ_ID) if parent is not None else None,
            'deleted': post.findtext('d:isDeleted', namespaces=NS) == 'true',
            'author': post.findtext('d:author/d:name', namespaces=NS),
            'date': post.findtext('d:createdAt', namespaces=NS),
            'message': post.findtext('d:message', namespaces=NS),
            'replies': [],
        }

    roots = []
    for comment in sorted(comments.values(), key=lambda c: c['date']):
        if comment['parent'] in comments:
            comments[comment['parent']]['replies'].append(comment)
        else:
            roots.append(comment)

    def clean(comment):
        """Drop deleted comments, keep a placeholder when they have visible replies."""
        replies = [r for r in map(clean, comment['replies']) if r]
        if comment['deleted'] and not replies:
            return None
        out = {'date': comment['date'], 'replies': replies}
        if comment['deleted']:
            out['deleted'] = True
        else:
            out['author'] = comment['author']
            out['message'] = comment['message']
        return out

    pages = {}
    for comment in roots:
        cleaned = clean(comment)
        if cleaned and comment['key']:
            pages.setdefault(comment['key'], []).append(cleaned)

    os.makedirs(os.path.join(ROOT, 'data'), exist_ok=True)
    with open(os.path.join(ROOT, 'data', 'comments.json'), 'w') as f:
        json.dump(pages, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write('\n')

    for key, threads in sorted(pages.items()):
        count = sum(1 for _ in walk(threads))
        print('%s: %d comments' % (key, count))


def walk(comments):
    for comment in comments:
        if not comment.get('deleted'):
            yield comment
        yield from walk(comment['replies'])


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
