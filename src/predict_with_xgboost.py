import numpy as np
import pandas as pd
from util import *
from myXgb import *
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from xgboost.sklearn import XGBRegressor  # wrapper
import scipy.stats as st
import pickle

##############################################################################
# PreHook to configure matplotlib plot and constant definition
config_plot()

N_rows = 30000
parse_dates = ['stated_at']
filename = "/var/www/bicing-prediction/data/slim_19.csv"
encode_cols = ['Month', 'DayofWeek', 'Hour']
val_ratio = 0.3
n_tree = 300
early_stop = 50
bucket_size = "2T"
steps = 2000


test_start_date = '2018-11-20 20:00:00'
unseen_start_date = '2018-12-01 21:00:00'
plot_start = '2018-11-01 16:10:00'

# base parameters
xgb_params = {
    'booster': 'gbtree',
    'objective': 'reg:linear',  # regression task
    'subsample': 0.80,  # 80% of data to grow trees and prevent overfitting
    'colsample_bytree': 0.85,  # 85% of features used
    'eta': 0.1,
    'max_depth': 10,
    'seed': 42}  # for reproducible results

#############################################################################
# xgboost EDA

# df = pre_process(N_rows, parse_dates, filename)
# df = date_transform(df, encode_cols)
#
# print('-----Xgboost Using All Numeric Features-----',
#       '\n---inital model feature importance---')
# fig_allFeatures = xgb_importance(df, val_ratio, xgb_params, n_tree, early_stop, 'All Features')

#############################################################################
# xgboost using only datetime information
df = pre_process(N_rows, parse_dates, filename)

bikes = df["available_bike_number"]

df = pd.DataFrame(bucket_avg(bikes, bucket_size))
df.dropna(inplace=True)
# df.iloc[-1, :].index

# get splited data
df_unseen, df_test, df = xgb_data_split(
    df, bucket_size, unseen_start_date, steps, test_start_date, encode_cols)

print('\n-----Xgboost on only datetime information---------\n')

dim = {'train and validation data ': df.shape,
       'test data ': df_test.shape,
       'forecasting data ': df_unseen.shape}
print(pd.DataFrame(list(dim.items()), columns=['Data', 'dimension']))

# train model
Y = df.iloc[:, 0]
X = df.iloc[:, 1:]

X_train, X_val, y_train, y_val = train_test_split(X, Y, test_size=val_ratio, random_state=42)

X_test = xgb.DMatrix(df_test.iloc[:, 1:])
Y_test = df_test.iloc[:, 0]
X_unseen = xgb.DMatrix(df_unseen)

dtrain = xgb.DMatrix(X_train, y_train)
dval = xgb.DMatrix(X_val, y_val)
watchlist = [(dtrain, 'train'), (dval, 'validate')]

# Grid Search
params_sk = {
    'objective': 'reg:linear',
    'subsample': 0.8,
    'colsample_bytree': 0.85,
    'seed': 42}

skrg = XGBRegressor(**params_sk)

skrg.fit(X_train, y_train)

params_grid = {"n_estimators": st.randint(100, 500),
               #                "colsample_bytree": st.beta(10, 1),
               #                "subsample": st.beta(10, 1),
               #                "gamma": st.uniform(0, 10),
               #                'reg_alpha': st.expon(0, 50),
               #                "min_child_weight": st.expon(0, 50),
               #               "learning_rate": st.uniform(0.06, 0.12),
               'max_depth': st.randint(6, 30)
               }
search_sk = RandomizedSearchCV(skrg, params_grid, cv=5, random_state=1, n_iter=20)  # 5 fold cross validation
search_sk.fit(X, Y)

print("best parameters:", search_sk.best_params_)
print("best score:", search_sk.best_score_)

params_new = {**params_sk, **search_sk.best_params_}

params_new = {'objective': 'reg:linear', 'subsample': 0.8, 'colsample_bytree': 0.85, 'seed': 42, 'max_depth': 23,
              'n_estimators': 364}

model_final = xgb.train(params_new, dtrain, evals=watchlist,
                        early_stopping_rounds=early_stop, verbose_eval=True)

pickle.dump(model, open("/var/www/bicing-prediction/open/pima.pickle.dat", "wb"))
# model_final = pickle.load(open("/var/www/bicing-prediction/open/pima.pickle.dat", "rb"))

#############################################################################
# Forcasting
# prediction to testing data
Y_hat = model_final.predict(X_test)
Y_hat = pd.DataFrame(Y_hat, index=Y_test.index, columns=["predicted"])

# predictions to unseen future data
unseen_y = model_final.predict(X_unseen)
forecasts = pd.DataFrame(
    unseen_y, index=df_unseen.index, columns=["forecasts"])

# plot forcast results using grid search final model
print('-----Xgboost Using Datetime Features Only------',
      '\n---Forecasting from Grid Search---')
forecasts_plot2 = xgb_forecasts_plot(
    plot_start, Y, Y_test, Y_hat, forecasts, 'Grid Search')
