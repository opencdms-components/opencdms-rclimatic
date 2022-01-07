import logging
import os.path
from opencdms_process.process.climatol import windrose
from opencdms import MidasOpen
from pygeoapi.process.base import BaseProcessor, ProcessorExecuteError
from io import BytesIO
import base64


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
    'links': [],
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
        'windrose': {
            'title': 'Windrose chart',
            'description': 'Return a chart with windrose visualization.',
            'schema': {
                'type': 'object',
                'contentMediaType': 'application/json'
            }
        }
    },
    'example': {
        'inputs': {
            'src_id': 838,
            'period': 'hourly',
            'year': 1991,
            'elements': ['wind_speed', 'wind_direction'],
        }
    }
}


class WindroseDataProcessor:
    def __init__(self, filters):
        self.filters = filters

    def generate_chart(self, base64_encoded=False):
        connection = os.path.join(
            "/home/faysal/PycharmProjects", "opencdms-test-data", "data"
        )

        session = MidasOpen(connection)
        obs = session.obs(**self.filters)
        image = windrose(obs)
        buffered = BytesIO()
        image.save(buffered, format="PNG")

        if base64_encoded:
            bas64_bytes = base64.b64encode(buffered.getvalue())

            returned_image = f'data:image/png;base64,{bas64_bytes.decode("utf-8")}'
        else:
            returned_image = image

        return returned_image


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
        mimetype = 'application/json'
        filters = {
            'src_id': 838,
            'period': 'hourly',
            'year': 1991,
            'elements': ['wind_speed', 'wind_direction'],
        }

        if not {'src_id', 'period', 'year', 'elements'} - set(data.keys()):
            filters = data

        windrose_chart = WindroseDataProcessor(filters)\
            .generate_chart(base64_encoded=True)

        return mimetype, {
            'windrose': windrose_chart
        }

    def __repr__(self):
        return '<WindroseProcessor> {}'.format(self.name)
