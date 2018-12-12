FROM python:3.7

WORKDIR /var/www/bicing-prediction

COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

RUN git clone --recursive https://github.com/dmlc/xgboost \
    && cd xgboost; make -j4

COPY ./config .
COPY ./src .

EXPOSE 9090
CMD ["python", "/var/www/bicing-prediction/src/app.py"]

ENV PYTHONPATH "${PYTHONPATH}:/var/www/bicing-prediction/src/"
ENV PYTHONPATH "${PYTHONPATH}:/var/www/bicing-prediction/config/"
