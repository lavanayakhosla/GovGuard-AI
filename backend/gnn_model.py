import pandas as pd

def predict():
    try:
        import torch
        from torch_geometric.nn import GCNConv
    except ImportError:
        # fallback for demo / environments without torch
        return {
            "status": "disabled",
            "reason": "torch or torch_geometric not installed"
        }

    class GNN(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.conv1 = GCNConv(1, 8)
            self.conv2 = GCNConv(8, 2)

        def forward(self, x, edge_index):
            x = self.conv1(x, edge_index).relu()
            return self.conv2(x, edge_index)

    df = pd.read_csv("data/transactions.csv")

    vendors = list(df.vendor.unique())
    idx = {v: i for i, v in enumerate(vendors)}

    x = torch.ones((len(vendors), 1))
    edges = [[idx[v], idx[v]] for v in df.vendor]
    edge_index = torch.tensor(edges).t()

    model = GNN()
    out = model(x, edge_index)

    return {
        "status": "ok",
        "result": out.argmax(dim=1).tolist()
    }
