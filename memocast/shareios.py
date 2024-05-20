from . import PODCAST_PREFIX


def get_share_url_from_ios():
    import appex

    url = appex.get_url()
    okay = str(url).startswith(PODCAST_PREFIX)
    if not okay:
        print(f'The URL you are sharing is {url} but we require {PODCAST_PREFIX}')
    result = url if okay else None
    return result
