import reminders
from protocols import Url
from logging_ import logger


def add_reminder_from_url(url: Url):
    r = reminders.Reminder()
    short_podname = url.parser.get_podcast_short_name()
    episode_number = url.parser.get_current_episode_number()
    r.title = url.description
    r.url = url.url
    r.notes = f'{short_podname} #{episode_number}'
    r.save()
    logger(f'Reminder added for {r.title}')