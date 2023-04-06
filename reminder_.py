from io_ import get_device_and_import_modules
from protocols import Url, DeviceType
from logging_ import logger
from unittest import mock
if get_device_and_import_modules() == DeviceType.ios:
    import reminders
else:
    reminders = mock.Mock()


def add_reminder_from_url(url: Url):
    r = reminders.Reminder()
    short_podname = url.parser.get_podcast_short_name()
    episode_number = url.parser.get_current_episode_number()
    r.title = url.description
    r.notes = f'{short_podname} #{episode_number} - {url.url}'
    r.save()
    logger.info(f'Reminder added for {r.title}')
