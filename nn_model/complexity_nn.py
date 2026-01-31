import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from sklearn.preprocessing import StandardScaler

feature_cols = [
    'param_count',
    'local_statement_count',
    'total_statement_count',
    'local_variable_count',
    'total_variable_count',
    'local_nesting_depth',
    'total_nesting_depth'
]


class NeuralNetwork(nn.Module):
    def __init__(self, input_size):
        super(NeuralNetwork, self).__init__()
        self.layer1 = nn.Linear(input_size, 64)
        self.layer2 = nn.Linear(64, 32)
        self.layer3 = nn.Linear(32, 1)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=0.2)

    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.dropout(x)
        x = self.relu(self.layer2(x))
        x = self.layer3(x)
        return x


def create_scaler(train_ds):

    train_array = np.array([train_ds[col] for col in feature_cols]).T
    scaler = StandardScaler()
    scaler.fit(train_array)
    return scaler


def train_model(num_epochs, train_ds, val_ds):

    input_size = len(feature_cols)
    model = NeuralNetwork(input_size)

    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)

    for epoch in range(num_epochs):
        model.train()
        train_loss = 0.0

        for batch in train_loader:
            inputs = batch['features'].float()
            labels = batch['complexity'].float().unsqueeze(1)

            if inputs.dim() == 3:
                inputs = inputs.squeeze(1)

            optimizer.zero_grad()
            outpus = model(inputs)
            loss = criterion(outpus, labels)

            loss.backward()
            optimizer.step()

            train_loss += loss.item()

        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            val_loader = DataLoader(val_ds, batch_size=32)
        for batch in val_loader:
            inputs = batch['features'].float()
            labels = batch['complexity'].float().unsqueeze(1)

            if inputs.dim() == 3:
                inputs = inputs.squeeze(1)

            outputs = model(inputs)
            loss = criterion(outputs, labels)
            val_loss += loss.item()

        if (epoch + 1) % 10 == 0:
            print(f'Epoch [{epoch+1}/{num_epochs}], '
                  f'Train Loss: {train_loss/len(train_loader):.4f}, '
                  f'Val Loss: {val_loss/len(val_loader):.4f}')

    return model
