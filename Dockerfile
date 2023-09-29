FROM python:3

WORKDIR /stock_price_prediction

COPY . .

# RUN pip install --no-cache-dir -r req.txt
RUN pip install pip --upgrade pip
RUN pip install pandas
RUN pip install --no-cache-dir torch
RUN pip install numpy
RUN pip install scikit-learn
RUN pip install fastapi
RUN pip install  uvicorn

RUN pip install streamlit
RUN pip install yfinance