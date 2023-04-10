from . import PODCAST_PREFIX


def get_share_url_from_ios():
    import appex
    url = appex.get_url()
    return url if str(url).startswith(PODCAST_PREFIX) else None