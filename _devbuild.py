# -*- coding: utf-8 -*-
"""Build xem thu cuc bo cho muc /writings.
Khong phai Jekyll that (sandbox chan rubygems), chi dung de kiem tra bo cuc.
Ho tro dung phan Liquid ma writings.html + _layouts/frame2.html dang dung.
"""
import os, re, glob, shutil, datetime
import yaml, markdown
from liquid import Environment, FileSystemLoader
from liquid import Markup

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, '_devsite')

env = Environment(loader=FileSystemLoader(os.path.join(ROOT,'_includes')))

def relative_url(v):
    return v if not v else ('/' + str(v).lstrip('/'))

def absolute_url(v):
    return 'https://upzi-employers.vercel.app' + ('/' + str(v).lstrip('/') if v else '')

def slugify(v):
    return re.sub(r'[^a-z0-9]+', '-', str(v).lower()).strip('-')

def strip_newlines(v):
    return str(v).replace('\n', ' ').replace('\r', '')

env.filters.update(dict(relative_url=relative_url, absolute_url=absolute_url,
                        slugify=slugify, strip_newlines=strip_newlines))

def load_posts():
    posts = []
    for p in sorted(glob.glob(os.path.join(ROOT, '_posts', '*'))):
        raw = open(p, encoding='utf-8').read()
        m = re.match(r'^---\n(.*?)\n---\n(.*)$', raw, re.S)
        if not m:
            continue
        fm = yaml.safe_load(m.group(1)) or {}
        if fm.get('published') is False:
            print('  (bo qua, published:false)', os.path.basename(p))
            continue
        body = m.group(2)
        if p.endswith('.md'):
            body = markdown.markdown(body, extensions=['extra'])
        base = os.path.basename(p)
        date = fm.get('date') or datetime.date.fromisoformat(base[:10])
        slug = re.sub(r'\.(md|html)$', '', base[11:])
        fm.update(dict(content=body, url=f'/insights/{slug}/', slug=slug,
                       date=str(date), path=p))
        posts.append(fm)
    posts.sort(key=lambda x: x['date'], reverse=True)
    return posts

def inline_includes(raw, depth=0):
    """Jekyll cho phep {% include ten.html %} khong dat trong dau nhay;
    python-liquid thi khong, nen ghep san noi dung include vao truoc khi render."""
    if depth > 5:
        return raw
    def sub(m):
        f = os.path.join(ROOT, '_includes', m.group(1))
        return inline_includes(open(f, encoding='utf-8').read(), depth + 1)
    return re.sub(r'\{%-?\s*include\s+([A-Za-z0-9._-]+)\s*-?%\}', sub, raw)

def render_page(src, ctx):
    raw = open(os.path.join(ROOT, src), encoding='utf-8').read()
    raw = re.sub(r'^---\n.*?\n---\n', '', raw, flags=re.S)
    return env.from_string(inline_includes(raw)).render(**ctx)

def main():
    posts = load_posts()
    print(f'{len(posts)} bai duoc build')
    site = dict(posts=posts, description='Chia se bai viet & kien thuc')
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT, exist_ok=True)

    # index
    html = render_page('writings.html', dict(site=site, page={}))
    os.makedirs(os.path.join(OUT, 'writings'), exist_ok=True)
    open(os.path.join(OUT, 'writings', 'index.html'), 'w', encoding='utf-8').write(html)

    # tung bai
    layout = open(os.path.join(ROOT, '_layouts', 'frame2.html'), encoding='utf-8').read()
    tpl = env.from_string(inline_includes(layout))
    for p in posts:
        html = tpl.render(site=site, page=p, content=Markup(p['content']))
        d = os.path.join(OUT, 'insights', p['slug'])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(html)
        print('  ->', p['url'])

    for d in ('assets', 'images'):
        shutil.copytree(os.path.join(ROOT, d), os.path.join(OUT, d), dirs_exist_ok=True)
    print('xong ->', OUT)

if __name__ == '__main__':
    main()
