"""
Trainer to create a model
"""
from pandas import DataFrame
from sklearn.model_selection import train_test_split
import xgboost as xgb

from infrastructure.data_mining.xgboost.XGBRegresser import XGBRegresser


class XGBoostDataTrainer:
    EARLY_STOP = 50
    RANDOM_STATE = 42
    VAL_RATIO = 0.3

    def __init__(self, regresser: XGBRegresser):
        self._regresser = regresser

    def train(self, data_frame: DataFrame, params: list = None):
        data_y = data_frame.iloc[:, 0]
        data_x = data_frame.iloc[:, 1:]
        x_train, x_val, y_train, y_val = train_test_split(data_x, data_y, test_size=self.VAL_RATIO,
                                                          random_state=self.RANDOM_STATE)

        data_train = xgb.DMatrix(x_train, y_train)
        data_validate = xgb.DMatrix(x_val, y_val)
        watchlist = [(data_train, 'train'), (data_validate, 'validate')]

        # if None == params:
        #     params = self._regresser.randomized_search_cv(X_train, y_train, X, Y)
        #
        #     logging.critical('PPPPAAAARRRAMS', params)
        params = {'objective': 'reg:linear', 'subsample': 0.8, 'colsample_bytree': 0.85, 'seed': 42,
                  'max_depth': 23,
                  'n_estimators': 364}

        return xgb.train(params, data_train, evals=watchlist, early_stopping_rounds=self.EARLY_STOP,)
