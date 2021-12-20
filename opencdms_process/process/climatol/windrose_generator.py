import logging
import os.path
from opencdms_process.process.climatol import windrose
from opencdms import MidasOpen
from pygeoapi.process.base import BaseProcessor, ProcessorExecuteError


LOGGER = logging.getLogger(__name__)

#: Process metadata and description
PROCESS_METADATA = {
    'version': '0.2.0',
    'id': 'windrose-generator',
    'title': {
        'en': 'Windrose Generator'
    },
    'description': {
        'en': 'Generates windrose chart.',
    },
    'keywords': ['windrose-generator', 'opencdms'],
    'links': [{
        'type': 'text/html',
        'rel': 'canonical',
        'title': 'information',
        'href': 'https://example.org/process',
        'hreflang': 'en-US'
    }],
    'inputs': {
        'src_id': {
            'title': 'Source ID',
            'description': 'Source ID of the observation data.',
            'schema': {
                'type': 'integer'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'metadata': None,  # TODO how to use?
            'keywords': ['src_id', 'personal']
        },
        'period': {
            'title': 'Period',
            'description': 'Period of the observation data.',
            'schema': {
                'type': 'string'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'metadata': None,  # TODO how to use?
            'keywords': ['period', 'midas-open']
        },
        'year': {
            'title': 'Year',
            'description': 'Year of the observation data.',
            'schema': {
                'type': 'integer'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'metadata': None,  # TODO how to use?
            'keywords': ['year', 'midas-open']
        },
        'elements': {
            'title': 'Elements',
            'description': 'Elements of the observation data.',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'string'
                }
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'metadata': None,  # TODO how to use?
            'keywords': ['elements', 'midas-open']
        },
    },
    'outputs': {
        'echo': {
            'title': 'Hello, world',
            'description': 'A "hello world" echo with the name and (optional)'
                           ' message submitted for processing',
            'schema': {
                'type': 'object',
                'contentMediaType': 'application/json'
            }
        }
    },
    'example': {
        'inputs': {
            'name': 'World',
            'message': 'An optional message.',
        }
    }
}


class WindroseProcessor(BaseProcessor):
    """Hello World Processor example"""

    def __init__(self, processor_def):
        """
        Initialize object

        :param processor_def: provider definition

        :returns: pygeoapi.process.hello_world.HelloWorldProcessor
        """

        super().__init__(processor_def, PROCESS_METADATA)

    def execute(self, data):
        connection = os.path.join(
            "/code", "opencdms-test-data", "data"
        )
        mimetype = 'application/json'

        filters = {
            'src_id': 838,
            'period': 'hourly',
            'year': 1991,
            'elements': ['wind_speed', 'wind_direction'],
        }

        if not {'src_id', 'period', 'year', 'elements'} - data.keys():
            filters = data

        session = MidasOpen(connection)
        obs = session.obs(**filters)

        return mimetype, {"windrose": windrose(obs)}

    def __repr__(self):
        return '<WindroseProcessor> {}'.format(self.name)
