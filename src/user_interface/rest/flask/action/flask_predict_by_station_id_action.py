import uuid

from flask import request
from injector import inject

from application.use_case.data_provider.StationAvailabilitiesPredictionByDateTimeInPeriodFilterDataProvider import \
    StationAvailabilitiesPredictionByDateTimeInPeriodFilterDataProvider

from infrastructure.request.flask.ByDateTimeInPeriodFilterConverter import ByDateTimeInPeriodFilterConverter
from user_interface.rest.flask.response.FlaskPredictByStationIdResponse import FlaskPredictByStationIdResponse


@inject
def get(station_id: uuid,
        request_filter_converter: ByDateTimeInPeriodFilterConverter,
        data_provider: StationAvailabilitiesPredictionByDateTimeInPeriodFilterDataProvider,
        response: FlaskPredictByStationIdResponse):

    view = data_provider.collection(station_id, request_filter_converter.to_python(request.args.get('filter')))

    return response.from_view(view)
