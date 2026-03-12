import re


def get_video_embed(url):
    if not url or not url.strip():
        return None, False
    url = url.strip()
    if 'youtube.com' in url or 'youtu.be' in url:
        video_id = None
        if 'youtu.be/' in url:
            m = re.search(r'youtu\.be/([a-zA-Z0-9_-]+)', url)
            if m:
                video_id = m.group(1)
        else:
            m = re.search(r'[?&]v=([a-zA-Z0-9_-]+)', url)
            if m:
                video_id = m.group(1)
            if not video_id:
                m = re.search(r'youtube\.com/embed/([a-zA-Z0-9_-]+)', url)
                if m:
                    video_id = m.group(1)
        if video_id:
            return f'https://www.youtube-nocookie.com/embed/{video_id}', True
    if 'vimeo.com' in url:
        m = re.search(r'vimeo\.com/(?:video/)?(\d+)', url)
        if m:
            return f'https://player.vimeo.com/video/{m.group(1)}', True
    return url, False
