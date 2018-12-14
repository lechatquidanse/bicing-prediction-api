"""
Abstract representation of station data used for data mining (data training and prediction thanks to a model)
"""
from pandas import (DataFrame, get_dummies)


class StationData:
    ENCODED_COLUMNS = ['Month', 'DayOfWeek', 'Hour']

    def _date_transform(self, data_frame: DataFrame) -> DataFrame:
        # extract a few features from datetime
        data_frame['Year'] = data_frame.index.year
        data_frame['Month'] = data_frame.index.month
        data_frame['WeekOfYear'] = data_frame.index.weekofyear
        data_frame['DayOfWeek'] = data_frame.index.weekday
        data_frame['Hour'] = data_frame.index.hour
        data_frame['Minute'] = data_frame.index.minute

        # one hot encoder for categorical variables
        for column in self.ENCODED_COLUMNS:
            data_frame[column] = data_frame[column].astype('category')

        return get_dummies(data_frame, columns=self.ENCODED_COLUMNS)
