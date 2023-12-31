import sys
import logging
import * from tkinter
from pysitemap import crawler
from pysitemap.parsers.lxml_parser import Parser
# This python program is for creating sitemap of a website

if __name__ == '__main__':
    if '--iocp' in sys.argv:
        from asyncio import events, windows_events
        sys.argv.remove('--iocp')
        logging.info('using iocp')
        el = windows_events.ProactorEventLoop()
        events.set_event_loop(el)

    # root_url = sys.argv[1]
    root_url = 'https://www.codeavenues.com'
    crawler(
        root_url, out_file='debug/sitemap.xml', exclude_urls=[".pdf", ".jpg", ".zip"],
        http_request_options={"ssl": False}, parser=Parser
    )
