"""
In charge of response handle for predictions by station
"""
from flask import jsonify
from pandas import DataFrame, DatetimeIndex

from application.use_case.query.StationAvailabilitiesPredictionByDateTimeInPeriodFilterView import \
    StationAvailabilitiesPredictionByDateTimeInPeriodFilterView


class FlaskPredictByStationIdResponse:
    def from_view(self, view: StationAvailabilitiesPredictionByDateTimeInPeriodFilterView):
        return jsonify({'station_id': view.station_id(),
                        'predictions': self._predictions_by_date_time(view.predictions(),
                                                                      view.by_filter().to_date_time_index())})

    @staticmethod
    def _predictions_by_date_time(predictions: DataFrame, date_time: DatetimeIndex) -> dict:
        predictions_by_date_time = DataFrame(data=predictions, index=date_time)
        predictions_by_date_time.index = predictions_by_date_time.index.strftime('%Y-%m-%d %H:%M:%S')

        predictions = predictions_by_date_time.to_dict()

        if len(predictions) == 0:
            return {}

        return next(iter(predictions.values()))
