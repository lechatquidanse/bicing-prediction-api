"""
In charge of response handle for predictions by station
"""
from flask import jsonify
from pandas import DataFrame, DatetimeIndex

from application.use_case.query.StationsAvailabilitiesPredictionByDateTimeInPeriodFilterView import \
    StationsAvailabilitiesPredictionByDateTimeInPeriodFilterView


class FlaskPredictByStationIdsResponse:
    def from_view(self, view: StationsAvailabilitiesPredictionByDateTimeInPeriodFilterView):
        stations = view.data()

        response = []

        for station in stations:
            station_id = station[0]
            status = station[1]
            total_bikes = station[2]
            prediction = view.find_predictions_by_station_id(station_id)

            if prediction is not None:
                response.append({
                    'station_id': station_id,
                    'predictions': self._predictions(prediction.predictions(), view.by_filter().to_date_time_index(),
                                                     status, total_bikes)
                })

        return jsonify(response)

    def _predictions(self, predictions: DataFrame, date_time_index: DatetimeIndex, status: str,
                     total_bikes: float) -> list:
        predictions_by_date_time = self._predictions_by_date_time(predictions, date_time_index)

        return self._predictions_by_station_id(predictions_by_date_time, status, total_bikes)

    @staticmethod
    def _predictions_by_date_time(predictions: DataFrame, date_time: DatetimeIndex) -> dict:
        predictions_by_date_time = DataFrame(data=predictions, index=date_time)
        predictions_by_date_time.index = predictions_by_date_time.index.strftime('%Y-%m-%d %H:%M:%S')

        predictions = predictions_by_date_time.to_dict()

        if len(predictions) == 0:
            return {}

        return next(iter(predictions.values()))

    @staticmethod
    def _predictions_by_station_id(predictions: dict, status: str, total_bikes: float) -> list:
        results = []

        for forecast_at, available_bike_number in predictions.items():
            available_slot_number = total_bikes - available_bike_number
            data = {
                'available_bike_number': available_bike_number,
                'available_slot_number': available_slot_number,
                'status': status,
                'forecast_at': forecast_at
            }
            results.append(data)

        return results
