import torch
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv
import pandas as pd

class GNN(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = GCNConv(1,8)
        self.conv2 = GCNConv(8,2)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        return self.conv2(x, edge_index)

def predict():
    df = pd.read_csv("data/transactions.csv")
    vendors = list(df.vendor.unique())
    idx = {v:i for i,v in enumerate(vendors)}
    x = torch.ones((len(vendors),1))
    edges = [[idx[v], idx[v]] for v in df.vendor]
    edge_index = torch.tensor(edges).t()
    model = GNN()
    out = model(x, edge_index)
    return out.argmax(dim=1).tolist()
