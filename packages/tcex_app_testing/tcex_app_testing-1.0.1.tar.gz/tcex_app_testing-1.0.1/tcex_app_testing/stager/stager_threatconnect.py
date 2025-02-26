"""TcEx Framework Module"""

# standard library
import logging

# first-party
from tcex_app_testing.render.render import Render
from tcex_app_testing.requests_tc import TcSession

_logger = logging.getLogger(__name__.split('.', maxsplit=1)[0])


class StagerThreatconnect:
    """Stages the Redis Data"""

    def __init__(self, session: TcSession):
        """Initialize class properties."""
        self.session = session
        self.log = _logger

        # available fields for different types of tc endpoints
        self.fields = {}

    def stage(self, threatconnect_data) -> dict:
        """Stage data in ThreatConnect."""
        staged_data = {}
        for root_key, root_value in threatconnect_data.items():
            staged_data.setdefault(root_key, {})
            for key, data in root_value.items():
                if key in staged_data:
                    ex_msg = f'ThreatConnect variable {key} is already staged.'
                    raise RuntimeError(ex_msg)
                staged_data[root_key][f'{key}'] = self.stage_data(root_key, data)

        return staged_data

    def stage_data(self, ioc_type, data):
        """Stage data in ThreatConnect."""
        self.session.log_curl = True

        params = {'fields': self.get_fields(ioc_type)}
        response = self.session.post(f'/v3/{ioc_type}', json=data, params=params)
        if not response.ok:
            error_msg = [
                f'Error staging data: {data}',
                f'Url: {response.request.url}',
                f'Method: {response.request.method}',
                f'Text: {response.text}',
                f'Status Code: {response.status_code}',
            ]

            error_msg = '\n'.join(error_msg)
            self.log.error(f'step=setup, event=staging-{ioc_type}-data, message={error_msg}')
            Render.panel.failure(error_msg)

        response_json = response.json()
        return response_json.get('data', response_json)

    def get_fields(self, type_):
        """Return fields for the provided type."""
        fields = self.fields.get(type_.lower(), [])
        if fields:
            return fields
        response = self.session.options(f'/v3/{type_}/fields', params={})
        fields = [field.get('name') for field in response.json().get('data', [])]
        self.fields[type_.lower()] = fields
        return fields

    def cleanup(self, staged_data: dict):
        """Cleanup staged data in ThreatConnect."""
        for root_key, root_value in staged_data.items():
            for data in root_value.values():
                response = self.session.delete(f'/v3/{root_key}/{data.get("id")}')
                if not response.ok:
                    Render.panel.error(f'Failed to cleanup data {data} in ThreatConnect.')
                    self.log.error(
                        f'step=cleanup, '
                        f'event=cleanup-{root_key}-data, '
                        f'message=Failed to cleanup data {data} in ThreatConnect.'
                    )
