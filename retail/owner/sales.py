import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import csv

# Load data
dataset_path = '/Users/abbasmammadov/Downloads/store-sales-time-series-forecasting/train.csv'


def single_store(store_id, family):       
    df = pd.read_csv(dataset_path)
    df = df[df['family'] == family]
    df = df[df['store_nbr'] == store_id]
    # df = df[:300]
    # df = df[:10000]
    # Filter data
    # df = df[(df['sales'] > 4000) & (df['sales'] < 20000)]

    df = df[df['date'] < '2017-08-13']
    print('1 day')
    print(df)

    print(df.shape)
    # Preprocessing
    scaler = MinMaxScaler(feature_range=(-1, 1))
    df['sales'] = scaler.fit_transform(df['sales'].values.reshape(-1, 1))

    # Create sequences
    def create_inout_sequences(input_data, tw):
        inout_seq = []
        L = len(input_data)
        for i in range(L-tw):
            train_seq = torch.FloatTensor(input_data[i:i+tw]).view(-1, tw, 1)
            train_label = torch.FloatTensor(input_data[i+tw:i+tw+1])
            inout_seq.append((train_seq, train_label))
        return inout_seq


    train_window = 30
    train_inout_seq = create_inout_sequences(df['sales'].values, train_window)
    # train_inout_seq = torch.tensor(train_inout_seq)
    # print(type(train_inout_seq))
    # print(train_inout_seq)
    # Define LSTM model
    device='cpu'
    class LSTM(nn.Module):
        def __init__(self, input_dim, hidden_dim, num_layers, output_dim):
            super(LSTM, self).__init__()
            self.hidden_dim = hidden_dim
            self.num_layers = num_layers
            self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
            self.linear = nn.Linear(hidden_dim, output_dim)

        def forward(self, x):
            h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).to(x.device)
            # h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim)
            
            c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).to(x.device)
            # c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim)
            
            out, (hn, cn) = self.lstm(x, (h0, c0))
            out = self.linear(out[:, -1, :])
            return out


    # Hyperparameters
    input_dim = 1
    hidden_dim = 64
    num_layers = 1
    output_dim = 1
    learning_rate = 0.001
    num_epochs = 30

    model = LSTM(input_dim=input_dim, hidden_dim=hidden_dim, output_dim=output_dim, num_layers=num_layers)
    model = model.to(device)
    criterion = torch.nn.MSELoss(reduction='mean')
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    losses = []
    # Training
    # single_loss = 0.0
    for epoch in range(num_epochs):
        for seq, labels in train_inout_seq:
            optimizer.zero_grad()
            # move the input and labels to GPU
            seq = seq.to(device)
            labels = labels.to(device)
            y_pred = model(seq)
            single_loss = criterion(y_pred.view(-1), labels)
            single_loss.backward()
            optimizer.step()
            
            losses.append(single_loss.item())

        # if epoch % 10 == 0:
        print(f'Epoch {epoch} loss: {single_loss.item()}')

    # Predictions
    fut_pred = 1
    test_inputs = df['sales'][-train_window:].tolist()

    model.eval()

    # for i in range(fut_pred):
    #     with torch.no_grad():
    #         test_inputs.append(model(seq).item())

    for i in range(fut_pred):
        seq = torch.FloatTensor(test_inputs[-train_window:]).view(-1, train_window, 1).to(device)
        # seq = torch.FloatTensor(test_inputs[-train_window:])
        with torch.no_grad():
            model.hidden = (torch.zeros(1, 1, model.hidden_dim),
                            torch.zeros(1, 1, model.hidden_dim))
            test_inputs.append(model(seq).item())

    actual_predictions = scaler.inverse_transform(np.array(test_inputs[train_window:]).reshape(-1, 1))

    # plot losses
    plt.plot(losses)
    plt.title('training loss')

    # change them back to dataframe
    df_pred = pd.DataFrame(actual_predictions, columns=['predictions'])
    print(df_pred)
    return df_pred


stores = [6, 8]
families = ["POULTRY", "SEAFOOD"]

result = {}


for store in stores:
    for family in families:
        print('RUNNING STORE: ', store, ' FAMILY: ', family)
        predicted = single_store(store, family)
        result[f'store_{store}_family_{family}'] = predicted
        print('---------------------------------')

with open('result.csv', 'w') as f:
    #write the header
    f.write("store,family,predictions\n")
    for key in result.keys():
        key_split = key.split('_')
        res = key_split[1] + ',' + key_split[3] + ',' + str(result[key]) + "\n"
        f.write(res)
        
