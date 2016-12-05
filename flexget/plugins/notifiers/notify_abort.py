from __future__ import unicode_literals, division, absolute_import
from builtins import *  # noqa pylint: disable=unused-import, redefined-builtin

import logging

from flexget import plugin
from flexget.event import event

__name__ = 'notify_abort'
log = logging.getLogger(__name__)


class NotifyAbort(object):
    schema = {
        'type': 'object',
        'properties': {
            'to': {'type': 'array', 'items':
                {'allOf': [
                    {'$ref': '/schema/plugins?group=notifiers'},
                    {'maxProperties': 1,
                     'error_maxProperties': 'Plugin options within notify_abort plugin must be indented '
                                            '2 more spaces than the first letter of the plugin name.',
                     'minProperties': 1}]}}
        },
        'required': ['to'],
        'additionalProperties': False
    }

    def on_task_abort(self, task, config):
        if task.silent_abort:
            return

        title = 'Task {{ task_name }} has aborted!'
        message = 'Reason: {{ task.abort_reason }}'
        notify_config = {'to': config['to'],
                         'scope': 'task',
                         'title': title,
                         'message': message}
        log.debug('sending abort notification')
        plugin.get_plugin_by_name('notify').instance.send_notification(task, notify_config)


@event('plugin.register')
def register_plugin():
    plugin.register(NotifyAbort, __name__, api_ver=2)
