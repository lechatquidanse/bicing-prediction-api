"""
REST Action with HTTP method GET to handle query of station's availabilities predictions
"""
import json

from flask import request
from injector import inject

from infrastructure.request.flask.ByDateTimeInPeriodFilterConverter import ByDateTimeInPeriodFilterConverter
from user_interface.rest.flask.response.FlaskPredictByStationIdsResponse import FlaskPredictByStationIdsResponse


@inject
def post(request_filter_converter: ByDateTimeInPeriodFilterConverter, data_provider,
         response: FlaskPredictByStationIdsResponse):
    data = json.loads(request.data)

    station_ids = data['station_ids']
    by_filter = request_filter_converter.to_python(data['filter'])

    view = data_provider.collection(station_ids, by_filter)

    return response.from_view(view)
