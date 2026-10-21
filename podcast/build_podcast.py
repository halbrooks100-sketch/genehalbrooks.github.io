"""Rebuild podcast/feed.xml and podcast/index.html from the Muse feed.

Muse's feed lacks tags Apple Podcasts requires (itunes:author, itunes:category,
channel link), so we republish it here with those added. Audio stays on Muse.
Run from the repo root: python podcast/build_podcast.py
"""
import html
import pathlib
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

SOURCE = "https://muse.ai/podcasts/feed/1134902803030549/5731bf1e-7078-4a4e-87ac-9474c7e4533b"
SITE = "https://genehalbrooks.com"
FEED_URL = f"{SITE}/podcast/feed.xml"
COVER_URL = f"{SITE}/podcast/cover.png"
AUTHOR = "Gene Halbrooks"
ITUNES = "http://www.itunes.com/dtds/podcast-1.0.dtd"
OUT = pathlib.Path(__file__).parent


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "genehalbrooks-podcast-sync"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def esc(s):
    return html.escape(s or "", quote=True)


def main():
    channel = ET.fromstring(fetch(SOURCE)).find("channel")
    title = channel.findtext("title")
    desc = channel.findtext("description").strip()
    if "AI Generated" not in desc:
        desc += "\n\nAI Generated"

    cover = OUT / "cover.png"
    if not cover.exists():
        cover.write_bytes(fetch(channel.find(f"{{{ITUNES}}}image").get("href")))

    items = []
    for it in channel.findall("item"):
        enc = it.find("enclosure")
        items.append({
            "title": it.findtext("title"),
            "desc": (it.findtext("description") or "").strip(),
            "url": enc.get("url"),
            "length": enc.get("length") or "0",
            "guid": it.findtext("guid"),
            "pub": it.findtext("pubDate"),
            "dur": it.findtext(f"{{{ITUNES}}}duration") or "",
        })
    items.sort(key=lambda i: parsedate_to_datetime(i["pub"]), reverse=True)

    xml_items = "".join(f"""
    <item>
      <title>{esc(i['title'])}</title>
      <description>{esc(i['desc'])}</description>
      <enclosure url="{esc(i['url'])}" length="{esc(i['length'])}" type="audio/mpeg"/>
      <guid isPermaLink="false">{esc(i['guid'])}</guid>
      <pubDate>{esc(i['pub'])}</pubDate>
      <itunes:duration>{esc(i['dur'])}</itunes:duration>
      <itunes:explicit>false</itunes:explicit>
      <itunes:episodeType>full</itunes:episodeType>
    </item>""" for i in items)

    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
     xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{esc(title)}</title>
    <link>{SITE}/podcast/</link>
    <language>en-us</language>
    <description>{esc(desc)}</description>
    <copyright>© 2026 {AUTHOR}</copyright>
    <atom:link href="{FEED_URL}" rel="self" type="application/rss+xml"/>
    <itunes:author>{AUTHOR}</itunes:author>
    <itunes:category text="Business"><itunes:category text="Investing"/></itunes:category>
    <itunes:category text="Technology"/>
    <itunes:image href="{COVER_URL}"/>
    <itunes:explicit>false</itunes:explicit>
    <itunes:type>episodic</itunes:type>
    <itunes:owner>
      <itunes:name>{AUTHOR}</itunes:name>
    </itunes:owner>
    <image>
      <url>{COVER_URL}</url>
      <title>{esc(title)}</title>
      <link>{SITE}/podcast/</link>
    </image>{xml_items}
  </channel>
</rss>
"""
    (OUT / "feed.xml").write_text(feed, encoding="utf-8")

    cards = "".join(f"""
    <article class="ep">
      <p class="ep-date">{parsedate_to_datetime(i['pub']).strftime('%B %d, %Y').replace(' 0', ' ')}</p>
      <h2>{esc(i['title'])}</h2>
      <p>{esc(i['desc'].replace('AI Generated', '').strip())}</p>
      <audio controls preload="none" src="{esc(i['url'])}"></audio>
    </article>""" for i in items)

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | Gene Halbrooks</title>
<meta name="description" content="{esc(desc.splitlines()[0])}">
<link rel="alternate" type="application/rss+xml" title="{esc(title)}" href="{FEED_URL}">
<style>
:root{{--navy:#0f1f3d;--accent:#c9a227;--text:#1d2433;--muted:#5b6475;--bg:#f6f7f9;--card:#fff;}}
*{{box-sizing:border-box;}}
body{{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:var(--text);background:var(--bg);line-height:1.55;}}
header{{background:var(--navy);color:#fff;padding:40px 16px;}}
.wrap{{max-width:760px;margin:0 auto;}}
header .wrap{{display:flex;gap:24px;align-items:center;flex-wrap:wrap;}}
header img{{width:140px;height:140px;border-radius:10px;}}
header h1{{margin:0 0 8px;font-size:1.8rem;}}
header p{{margin:0 0 12px;color:rgba(255,255,255,.8);}}
header a{{color:var(--accent);}}
.back{{display:inline-block;margin-bottom:16px;color:rgba(255,255,255,.7);text-decoration:none;font-size:.9rem;}}
main{{padding:24px 16px 48px;}}
.ep{{background:var(--card);border-radius:10px;padding:20px;margin-bottom:16px;box-shadow:0 1px 3px rgba(0,0,0,.06);}}
.ep h2{{font-size:1.1rem;margin:0 0 8px;}}
.ep p{{margin:0 0 12px;color:var(--muted);}}
.ep-date{{font-size:.8rem;text-transform:uppercase;letter-spacing:.05em;color:var(--accent)!important;font-weight:600;}}
audio{{width:100%;}}
footer{{text-align:center;color:var(--muted);font-size:.85rem;padding:24px 16px;}}
</style>
</head>
<body>
<header><div class="wrap">
  <div style="flex-basis:100%"><a class="back" href="/">← genehalbrooks.com</a></div>
  <img src="cover.png" alt="{esc(title)} cover art">
  <div style="flex:1;min-width:240px">
    <h1>{esc(title)}</h1>
    <p>{esc(desc.splitlines()[0])}</p>
    <p><a href="feed.xml">RSS feed</a> · AI generated</p>
  </div>
</div></header>
<main class="wrap">{cards}
</main>
<footer>&copy; 2026 {AUTHOR}</footer>
</body>
</html>
"""
    (OUT / "index.html").write_text(page, encoding="utf-8")
    print(f"{len(items)} episodes written")


if __name__ == "__main__":
    main()
