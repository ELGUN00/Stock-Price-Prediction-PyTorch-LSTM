import yfinance as yahooFinance
from sklearn.preprocessing import MinMaxScaler
import torch
import backend.lstm as lstm
from copy import deepcopy as dc
import numpy as np

class Predict:
    def __init__(self, ticket) -> None:
        self.ticket = ticket
        self.lookback=10
        self.hidden_size = 16
        self.model = lstm.LSTM(1,self.hidden_size,1)
        self.scaler = MinMaxScaler()
        self.model.load_state_dict(torch.load(f'./backend/models/rnn_{self.ticket}.pth'))
        self.model.eval()


    def set_data(self):
        self.data = yahooFinance.Ticker(self.ticket).history(f'{self.lookback}d')
        self.lookback_days_list = self.data['Close'].to_list()
        self.data  =self.scaler.fit_transform(self.data[['Close']])
        self.data = torch.from_numpy(self.data).reshape((-1,self.lookback,1)).float()
    
    def predict(self):
        self.set_data()
        with torch.no_grad():
            predicted = self.model(self.data.to(self.model.device)).numpy()
        predictions = predicted.flatten()

        dummies = np.zeros((predictions.shape[0], self.lookback+1))
        dummies[:, 0] = predictions
        dummies = self.scaler.inverse_transform(dummies)
        predictions = dc(dummies[:, 0])
        return {
            'status': 'OK',
            'lookback_days':self.lookback_days_list,
            'prediction': predictions[0]}
    

