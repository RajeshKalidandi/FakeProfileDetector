import torch
import torch.nn as nn
import torch.nn.functional as F
import dgl
from dgl.nn import GraphConv

class GNNModel(nn.Module):
    def __init__(self, in_feats, hidden_size, num_classes):
        super(GNNModel, self).__init__()
        self.conv1 = GraphConv(in_feats, hidden_size)
        self.conv2 = GraphConv(hidden_size, num_classes)

    def forward(self, g, features):
        x = F.relu(self.conv1(g, features))
        x = self.conv2(g, x)
        return x

def train_gnn_model(graph, features, labels, epochs=100, lr=0.01):
    model = GNNModel(features.shape[1], 16, 2)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    
    for epoch in range(epochs):
        model.train()
        logits = model(graph, features)
        loss = F.cross_entropy(logits, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if epoch % 10 == 0:
            print(f'Epoch {epoch}: Loss {loss.item():.4f}')
    
    return model
