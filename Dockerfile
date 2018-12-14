#########################################
###### Bicing MACHINE LEARNING API ######
#########################################
FROM python:3.7 AS bicing_machine_learning_api

WORKDIR /var/www/bicing-prediction-api

COPY requirements.txt ./
RUN mkdir -p .pip \
    && pip install --upgrade pip \
    && pip --cache-dir=.pip install -r requirements.txt

RUN git clone --recursive https://github.com/dmlc/xgboost \
    && cd xgboost; make -j4

COPY ./config ./config
COPY ./features ./features
COPY ./src ./src

EXPOSE 9090
CMD ["python", "/var/www/bicing-prediction-api/src/app.py"]

ENV PYTHONPATH "${PYTHONPATH}:/var/www/bicing-prediction-api/src/"
ENV PYTHONPATH "${PYTHONPATH}:/var/www/bicing-prediction-api/config/"

#########################################
######## Bicing API for dev env ########
#########################################
FROM bicing_machine_learning_api AS bicing_machine_learning_api_env_dev

COPY requirements_dev.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements_dev.txt
