import torch
from torch_scatter import scatter
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, GATConv
from torch_geometric.graphgym.register import register_stage
from torch_geometric.graphgym.config import cfg

class G2(nn.Module):
    """
    Gradient Gating for Deep Multi-Rate Learning on Graphs
    arxiv: https://arxiv.org/pdf/2210.00513
    code https://github.com/tk-rusch/gradientgating
    """

    def __init__(self, conv, p=2., conv_type='GCN', activation=nn.ReLU()):
        super(G2, self).__init__()
        self.conv = conv
        self.p = p
        self.activation = activation
        self.conv_type = conv_type

    def forward(self, X, edge_index):
        n_nodes = X.size(0)
        if self.conv_type == 'GAT':
            X = F.elu(self.conv(X, edge_index)).view(n_nodes, -1, 4).mean(dim=-1)
        else:
            X = self.activation(self.conv(X, edge_index))
        gg = torch.tanh(scatter((torch.abs(X[edge_index[0]] - X[edge_index[1]]) ** self.p).squeeze(-1),
                                edge_index[0], 0, dim_size=X.size(0), reduce='mean'))

        return gg


class G2_GNN_original(nn.Module):
    def __init__(self, nfeat, nhid, nclass, nlayers, conv_type='GCN', p=2., drop_in=0, drop=0, use_gg_conv=True):
        super(G2_GNN_original, self).__init__()
        self.conv_type = conv_type
        self.enc = nn.Linear(nfeat, nhid)
        self.dec = nn.Linear(nhid, nclass)
        self.drop_in = drop_in
        self.drop = drop
        self.nlayers = nlayers
        if conv_type == 'GCN':
            self.conv = GCNConv(nhid, nhid)
            if use_gg_conv == True:
                self.conv_gg = GCNConv(nhid, nhid)
        elif conv_type == 'GAT':
            self.conv = GATConv(nhid,nhid,heads=4,concat=True)
            if use_gg_conv == True:
                self.conv_gg = GATConv(nhid,nhid,heads=4,concat=True)
        else:
            print('specified graph conv not implemented')

        if use_gg_conv == True:
            self.G2 = G2(self.conv_gg,p,conv_type,activation=nn.ReLU())
        else:
            self.G2 = G2(self.conv,p,conv_type,activation=nn.ReLU())

    def forward(self, data):
        X = data.x
        n_nodes = X.size(0)
        edge_index = data.edge_index
        X = F.dropout(X, self.drop_in, training=self.training)
        X = torch.relu(self.enc(X))

        for i in range(self.nlayers):
            if self.conv_type == 'GAT':
                X_ = F.elu(self.conv(X, edge_index)).view(n_nodes, -1, 4).mean(dim=-1)
            else:
                X_ = torch.relu(self.conv(X, edge_index))
            tau = self.G2(X, edge_index)
            X = (1 - tau) * X + tau * X_
        X = F.dropout(X, self.drop, training=self.training)

        return self.dec(X)


class G2_GNN_Stack_Stage(nn.Module):
    """
    Gradient Gating for Deep Multi-Rate Learning on Graphs
    arxiv: https://arxiv.org/pdf/2210.00513

    No need for GNNLayer or GeneralLayer
    """

    def __init__(self, dim_in, dim_out, num_layers):
        super(G2_GNN_Stack_Stage, self).__init__()
        self.num_layers = num_layers
        nhid = dim_out
        self.conv_type = cfg.gnn.layer_type  # You can set this dynamically based on your requirement
        # self.convs = nn.ModuleList([self.build_conv_layer(nhid) for _ in range(num_layers)])
        # self.G2s = nn.ModuleList([G2(self.build_conv_layer(nhid), p=2., conv_type=self.conv_type, activation=nn.ReLU()) for _ in range(num_layers)])
        if self.conv_type == 'gcnconv':
            self.conv_gg = GCNConv(nhid, nhid)
        elif self.conv_type == 'gatconv':
            self.conv_gg = GATConv(nhid,nhid,heads=4,concat=True)
        else:
            raise NotImplementedError('Specified graph conv not implemented')

        p = 2
        self.G2 = G2(self.conv_gg, p, self.conv_type, activation=nn.ReLU())

    def forward(self, batch):
        X = batch.x
        n_nodes = X.size(0)
        edge_index = batch.edge_index

        for i in range(self.num_layers):
            if self.conv_type == 'gatconv':
                X_ = F.elu(self.conv_gg(X, edge_index)).view(n_nodes, -1, 4).mean(dim=-1)
            else:
                X_ = torch.relu(self.conv_gg(X, edge_index))
            tau = self.G2(X, edge_index)
            X = (1 - tau) * X + tau * X_

        batch.x = F.dropout(X, cfg.gnn.dropout, training=self.training)
        return batch


register_stage('g2_gnn', G2_GNN_Stack_Stage)
