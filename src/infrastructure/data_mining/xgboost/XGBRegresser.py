"""
Regresser to find best parameters to use to create model
"""
from pandas import DataFrame, Series
from sklearn.model_selection import RandomizedSearchCV
from xgboost.sklearn import XGBRegressor as XGBRegressorBase
import scipy.stats as st


class XGBRegresser:
    PARAMS_SK = {'objective': 'reg:linear', 'subsample': 0.8, 'colsample_bytree': 0.85, 'seed': 42}

    def randomized_search_cv(self, x_train: DataFrame, y_train: Series, x_test: DataFrame, y_test: Series):
        skrg = XGBRegressorBase(**self.PARAMS_SK)

        skrg.fit(x_train, y_train)

        params_grid = {'n_estimators': st.randint(100, 500), 'max_depth': st.randint(6, 30)}
        search_sk = RandomizedSearchCV(skrg, params_grid, cv=5, random_state=1, n_iter=20)
        search_sk.fit(x_test, y_test)

        return {**self.PARAMS_SK, **search_sk.best_params_}
