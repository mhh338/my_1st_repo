"""
utils.py
--------
Helper classes/functions for a CGCNN (Crystal Graph Convolutional Neural
Network) tutorial.

*** PROVENANCE ***
The imports, the `Data` dataclass, the `Batch` dataclass, `collate_fn`, and
the first few lines of `MaterialsDataset.__init__` below are transcribed
directly from screenshots of the real notebook. Everything else (the rest
of `__init__`, `__getitem__`, `GaussianExpansion`, `plot_sample`) is
reconstructed to be consistent with those confirmed pieces and the imports
they pull in (ase.neighborlist.neighbor_list, ase.visualize.plot.plot_atoms,
networkx) plus the previously-observed fact that, after __init__ runs,
`dataset.data` gains four new columns: "atoms", "edge_src", "edge_dst",
"edge_len".

*** WHAT'S STILL A GUESS ***
Your raw JSON's field names for atomic numbers / positions / cell / pbc,
and the target property's field name. These are auto-detected from common
candidates below (edit CANDIDATE_KEYS if none match — it'll raise an error
listing your real keys).
"""

import functools
import json
import time
from dataclasses import dataclass

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np
import torch
import torch.nn as nn
import torch_scatter
from ase import Atoms
from ase.data import chemical_symbols
from ase.data.colors import jmol_colors
from ase.neighborlist import neighbor_list
from ase.visualize.plot import plot_atoms
from torch.utils.data import DataLoader, Dataset


# --------------------------------------------------------------------------- #
# Config: candidate field names to auto-detect in your JSON entries
# --------------------------------------------------------------------------- #

CANDIDATE_KEYS = {
    "numbers": ("numbers", "atomic_numbers", "Z"),
    "positions": ("positions", "coords", "cart_coords", "xyz"),
    "cell": ("cell", "lattice", "lattice_vectors"),
    "pbc": ("pbc",),
    "target": ("target", "bulk_modulus", "K_VRH", "y", "label", "property", "bulk_mod"),
}

MAX_ATOMIC_NUMBER = 100  # size of the one-hot node feature vector


def _find_key(entry, field):
    for k in CANDIDATE_KEYS[field]:
        if k in entry:
            return k
    return None


def _get_target(entry):
    key = _find_key(entry, "target")
    if key is None:
        raise KeyError(
            f"Could not auto-detect the target property. Available keys: "
            f"{list(entry.keys())}. Add your target's field name to "
            "CANDIDATE_KEYS['target'] at the top of utils.py."
        )
    return entry[key]


def _make_atoms(entry):
    """Builds an ase.Atoms object from a raw JSON entry."""
    num_key = _find_key(entry, "numbers")
    pos_key = _find_key(entry, "positions")
    cell_key = _find_key(entry, "cell")
    pbc_key = _find_key(entry, "pbc")

    if num_key is None or pos_key is None:
        raise KeyError(
            "Could not auto-detect atomic numbers/positions in a dataset "
            f"entry. Available keys were: {list(entry.keys())}. Edit "
            "CANDIDATE_KEYS at the top of utils.py to add your actual field "
            "name(s)."
        )

    return Atoms(
        numbers=entry[num_key],
        positions=entry[pos_key],
        cell=entry[cell_key] if cell_key else None,
        pbc=entry[pbc_key] if pbc_key else (cell_key is not None),
    )


# --------------------------------------------------------------------------- #
# Distance expansion (SchNet/CGCNN-style Gaussian edge embedding)
# --------------------------------------------------------------------------- #

class GaussianExpansion:
    """Expands a scalar distance into `num_gaussians` evenly spaced Gaussian
    basis functions between 0 and `cutoff`."""

    def __init__(self, cutoff, num_gaussians):
        self.centers = np.linspace(0, cutoff, num_gaussians)
        self.width = self.centers[1] - self.centers[0] if num_gaussians > 1 else cutoff

    def expand(self, distances):
        distances = np.asarray(distances, dtype=float)
        return np.exp(-((distances[..., None] - self.centers) ** 2) / (self.width ** 2))


# --------------------------------------------------------------------------- #
# Data / Batch containers  (confirmed from notebook screenshots)
# --------------------------------------------------------------------------- #

@dataclass
class Data:
    """
    Class to contain graph attributes.

    N and M are the number of nodes and edges in the graph, respectively.

    Parameters
    ----------
    node_feat: Tensor
        The node features as a (N, n_node_feats) Tensor.
    edge_feat: Tensor
        The edge features as a (M, n_edge_feats) Tensor.
    edge_src: LongTensor
        The index of the central node for each edge.
    edge_dst: LongTensor
        The index of the destination node for each edge.
    target: Tensor
        The target property to learn.
    atoms: Atoms
        An ase atoms object.
    """

    node_feat: torch.Tensor
    edge_feat: torch.Tensor
    edge_src: torch.LongTensor
    edge_dst: torch.LongTensor
    target: torch.Tensor
    atoms: Atoms


@dataclass
class Batch:
    """
    Class to contain batched graph attributes.

    N and M are the number of nodes and edges across all batched graphs,
    respectively. G is the number of graphs in the batch.

    Parameters
    ----------
    node_feat: Tensor
        The node features as a (N, n_node_feats) Tensor.
    edge_feat: Tensor
        The edge features as a (M, n_edge_feats) Tensor.
    edge_src: LongTensor
        The index of the central node for each edge.
    edge_dst: LongTensor
        The index of the destination node for each edge.
    target: Tensor
        The target property to learn, as a (G, 1) Tensor.
    batch: LongTensor
        The graph to which each node belongs, as a (N,) Tensor.
    """

    node_feat: torch.Tensor
    edge_feat: torch.Tensor
    edge_src: torch.LongTensor
    edge_dst: torch.LongTensor
    target: torch.Tensor
    batch: torch.LongTensor

    def to(self, device, non_blocking=False):
        for k, v in self.__dict__.items():
            self.__dict__[k] = v.to(device=device, non_blocking=non_blocking)


def collate_fn(dataset):
    """
    Collate a list of Data objects and return a Batch.

    Parameters
    ----------
    dataset: MaterialsDataset
        The dataset to batch (or a list of Data objects, as passed by a
        DataLoader).

    Returns
    -------
    Batch
        A batched dataset.
    """
    batch = Batch([], [], [], [], [], [])
    base_idx = 0
    for i, data in enumerate(dataset):
        batch.node_feat.append(data.node_feat)
        batch.edge_feat.append(data.edge_feat)
        batch.edge_src.append(data.edge_src + base_idx)
        batch.edge_dst.append(data.edge_dst + base_idx)
        batch.target.append(data.target)
        batch.batch.extend([i] * len(data.node_feat))
        base_idx += len(data.node_feat)

    return Batch(
        node_feat=torch.cat(batch.node_feat),
        edge_feat=torch.cat(batch.edge_feat),
        edge_src=torch.cat(batch.edge_src),
        edge_dst=torch.cat(batch.edge_dst),
        batch=torch.LongTensor(batch.batch),
        target=torch.stack(batch.target),
    )


# --------------------------------------------------------------------------- #
# Dataset  (first 3 lines of __init__ confirmed from notebook screenshot)
# --------------------------------------------------------------------------- #

class MaterialsDataset(Dataset):
    def __init__(self, filename, cutoff=4, num_gaussians=40):
        """
        A dataset of materials properties.

        Parameters
        ----------
        filename: str
            The path to the dataset.
        cutoff: float
            The cutoff radius for searching for neighbors.
        num_gaussians: float
            The number of gaussian functions used in the edge
            embedding expansion.
        """
        with open(filename) as f:
            self.data = json.load(f)
        self.cutoff = cutoff
        self.num_gaussians = num_gaussians

        # --- everything below this point is reconstructed ---
        self.gdf = GaussianExpansion(cutoff, num_gaussians)

        # Precompute the graph (once) for every material, using ase's
        # periodic-boundary-aware neighbor search, and stash the results
        # back onto each entry -> matches the "atoms/edge_src/edge_dst/
        # edge_len" columns you saw in pd.DataFrame(dataset.data).
        for entry in self.data:
            atoms = _make_atoms(entry)
            i, j, d = neighbor_list("ijd", atoms, cutoff)
            entry["atoms"] = atoms
            entry["edge_src"] = i
            entry["edge_dst"] = j
            entry["edge_len"] = d

    def __len__(self):
        return len(self.data)

    @functools.lru_cache(maxsize=None)
    def __getitem__(self, idx):
        entry = self.data[idx]
        atoms = entry["atoms"]
        edge_src = entry["edge_src"]
        edge_dst = entry["edge_dst"]
        edge_len = entry["edge_len"]
        target = _get_target(entry)

        # one-hot node features from atomic number
        node_feat = np.zeros((len(atoms), MAX_ATOMIC_NUMBER), dtype=np.float32)
        for k, z in enumerate(atoms.numbers):
            node_feat[k, int(z) - 1] = 1.0

        # gaussian-expanded edge features
        edge_feat = self.gdf.expand(edge_len)

        return Data(
            node_feat=torch.tensor(node_feat, dtype=torch.float32),
            edge_feat=torch.tensor(edge_feat, dtype=torch.float32),
            edge_src=torch.LongTensor(edge_src),
            edge_dst=torch.LongTensor(edge_dst),
            target=torch.tensor([float(target)], dtype=torch.float32),
            atoms=atoms,
        )


# --------------------------------------------------------------------------- #
# Visualization
# --------------------------------------------------------------------------- #

def plot_structure(atoms, edge_src, edge_dst, cutoff=None, target=None):
    """
    Plots a crystal structure: the real atomic structure (via ase's
    plot_atoms) side-by-side with its graph representation (via networkx).

    This is the shared plotting logic used by both `plot_sample` (for a
    sample already inside a MaterialsDataset) and the prediction pipeline
    (for a brand-new structure that isn't part of any dataset) - so both
    code paths always render identically.

    Parameters
    ----------
    atoms : ase.Atoms
        The structure to plot.
    edge_src, edge_dst : array-like of int
        Parallel arrays of neighbor-edge endpoints (as returned by
        ase.neighborlist.neighbor_list("ijd", atoms, cutoff)).
    cutoff : float, optional
        Only used to display in the right panel's title.
    target : float, optional
        If known, displayed in the figure title and printed info. Pass
        None (default) when the target is unknown, e.g. at prediction time.
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # left: real atomic structure
    plot_atoms(atoms, axes[0], radii=0.5, rotation=("10x,10y,10z"))
    axes[0].set_title(f"Structure: {atoms.get_chemical_formula(empirical=True)}")
    axes[0].set_axis_off()

    # legend for the left panel: element -> color, using ase's own jmol
    # colors (the same colors plot_atoms used to draw the structure)
    left_elements = sorted(set(atoms.numbers))
    left_handles = [
        mpatches.Patch(color=jmol_colors[z], label=chemical_symbols[z])
        for z in left_elements
    ]
    axes[0].legend(handles=left_handles, loc="upper right",
                    fontsize=8, framealpha=0.9, title="Elements")

    # right: graph representation
    G = nx.Graph()
    G.add_nodes_from(range(len(atoms)))
    G.add_edges_from(zip(edge_src, edge_dst))

    cmap = mpl.colormaps["tab10"]
    numbers = atoms.numbers
    norm = mpl.colors.Normalize(vmin=min(numbers), vmax=max(numbers))
    node_colors = [cmap(norm(z)) for z in numbers]

    pos = nx.spring_layout(G, seed=0)
    nx.draw(G, pos, ax=axes[1], node_color=node_colors, with_labels=False, node_size=200)
    cutoff_str = f", cutoff={cutoff} Å" if cutoff is not None else ""
    axes[1].set_title(f"Graph ({G.number_of_edges()} edges{cutoff_str})")

    # legend for the right panel: element -> color, using the same tab10
    # colormap used to color the graph's nodes
    right_elements = sorted(set(numbers))
    right_handles = [
        mpatches.Patch(color=cmap(norm(z)), label=chemical_symbols[z])
        for z in right_elements
    ]
    axes[1].legend(handles=right_handles, loc="upper right",
                    fontsize=8, framealpha=0.9, title="Elements")

    title = f"{atoms.get_chemical_formula(empirical=True)}"
    if target is not None:
        title += f"  —  target: {target}"
    fig.suptitle(title)
    plt.tight_layout()
    plt.show()

    print(f"Formula         : {atoms.get_chemical_formula(empirical=True)}")
    print(f"Number of atoms : {len(atoms)}")
    print(f"Number of edges : {len(edge_src)}")
    if target is not None:
        print(f"Target property : {target}")


def plot_sample(dataset, idx=0):
    """
    Plots one sample of a MaterialsDataset: the real atomic structure (via
    ase's plot_atoms) side-by-side with its graph representation (via
    networkx), and prints basic info.
    """
    entry = dataset.data[idx]
    atoms = entry["atoms"]
    edge_src = entry["edge_src"]
    edge_dst = entry["edge_dst"]
    target = _get_target(entry)

    plot_structure(atoms, edge_src, edge_dst, cutoff=dataset.cutoff, target=target)


# --------------------------------------------------------------------------- #
# Model: a single graph convolution layer (message passing + gating)
# --------------------------------------------------------------------------- #

class GraphConvolution(nn.Module):

  def __init__(self, node_feat_dim, edge_feat_dim):
    # 'node_feat_dim' : number of node features
    # 'edge_feat_dim' : number of edge features

    super().__init__()

    # Linear layer used for the gated MLP
    self.lin1 = nn.Linear(
        2 * node_feat_dim + edge_feat_dim,
        2 * node_feat_dim
    )

    # Batch normalization layers
    self.bn1 = nn.BatchNorm1d(2 * node_feat_dim)
    self.bn2 = nn.BatchNorm1d(node_feat_dim)

  # Foward propagation
  def forward(self, node_feat, edge_feat, edge_src, edge_dst):
    # 'node_feat' : node features
    # 'edge_feat' : edge features
    # 'edge_src' : indices of the central nodes for the edges
    # 'edge_dst' : indices of the destination nodes for the edges

    # Concatenating node and edge features along columns
    m = torch.cat([node_feat[edge_src], node_feat[edge_dst], edge_feat], dim=1)
    # Dimension of 'm': [num_edge, 2 * node_embed + edge_embed]

    # Gated MLP
    z = self.lin1(m)
    z = self.bn1(z) # [num_edges, 2 * node_embed]
    z1, z2, = z.chunk(2, dim=1) # Splitting the z matrix into 2 matrix containing half the number of columns, dim will be z1 : [num_edges, node_embed], z2 : [num_edges, node_embed]
    z1 = nn.Sigmoid()(z1)
    z2 = nn.Softplus()(z2)
    z = z1 * z2 # Element-wise multiplication, [num_edges, node_embed]

    # Pooling the features,
    z = torch_scatter.scatter_add(z, edge_src, out=torch.zeros_like(node_feat), dim=0) # [num_nodes, node_embed]

    # Passing through normalization layer
    return nn.Softplus()(self.bn2(z) + node_feat)


# --------------------------------------------------------------------------- #
# Model: full CGCNN (embedding -> stacked graph convolutions -> pooling -> FC)
# --------------------------------------------------------------------------- #

# CGCNN model architecture
class CGCNN(nn.Module):
  def __init__(
    self,
    node_feat_dim,
    edge_feat_dim,
    node_hidden_dim=64,
    num_graph_conv_layers=3,
    fc_feat_dim=128
  ):
    """
    Parameters:
    node_feat_dim (int) : Number of node features from one-hot encoding.
    edge_feat_dim (int) : Number of bond features.
    node_hidden_dim (int) : The number of features in node embedding.
    num_graph_conv_layers (int) : Number of convolution layers (hyperparameter).
    fc_feat_dim (int) : Number of hidden features after pooling.
    """

    super().__init__()

    # Dense layer to transform one-hot encoded node features to embedding
    self.embedding = nn.Linear(node_feat_dim, node_hidden_dim)

    # Setting up the convolutions
    convs = []
    for _ in range(num_graph_conv_layers):
      convs.append(GraphConvolution(node_feat_dim=node_hidden_dim, edge_feat_dim=edge_feat_dim))
    self.convs = nn.ModuleList(convs)

    # Dense layer to turn final node embeddings to the crystal features
    self.conv_to_fc = nn.Sequential(
        nn.Linear(node_hidden_dim, fc_feat_dim), nn.Softplus()
    )

    # Dense layer to get the final target value
    self.fc_out = nn.Linear(fc_feat_dim, 1)

  def forward(self, batch):
    """
    Predicting a target property in a given batch of data.

    Parameters:
    batch : Batch, the data to pass through the network.
    """

    # Getting initial node embedding
    node_feat = self.embedding(batch.node_feat)

    # Apply convolutions
    for conv in self.convs:
      node_feat = conv(node_feat, batch.edge_feat, batch.edge_src, batch.edge_dst)

    # Pooling node vectors
    crys_feat = torch_scatter.scatter_mean(node_feat, batch.batch, dim=0)

    # Passing pooled vector through FC layer with activation function
    crys_feat = self.conv_to_fc(crys_feat)

    # Passing crystal features through final fully-connected layer
    return self.fc_out(crys_feat)


# --------------------------------------------------------------------------- #
# Training / evaluation loops
# --------------------------------------------------------------------------- #

def train(model, dataloader, criterion, optimizer, device):
  """
  Runs one full training epoch: forward pass, loss, backprop, weight update,
  for every batch in `dataloader`. Returns the epoch-averaged (loss, MAE).
  """
  epoch_loss = 0
  epoch_mae = 0

  model.train()

  for i, batch in enumerate(dataloader):
    # Moving the data onto the GPU if available
    batch.to(device)

    # Computing the output
    y_pred = model(batch)
    loss = criterion(y_pred, batch.target)
    mae = nn.L1Loss()(y_pred, batch.target)

    # Computing gradients
    optimizer.zero_grad() # Clearing previous gradients
    loss.backward()
    optimizer.step()

    # Updating the metrics
    epoch_loss += loss.item()
    epoch_mae += mae.item()

  return epoch_loss / len(dataloader), epoch_mae / len(dataloader) # Returning averages of epoch_loss & epoch_mae.


def evaluate(model, dataloader, criterion, device):
  """
  Runs one full evaluation pass (no gradient updates) over `dataloader`.
  Returns the averaged (loss, MAE).
  """
  epoch_loss = 0
  epoch_mae = 0

  model.eval()

  with torch.no_grad():
    for i, batch in enumerate(dataloader):
      batch.to(device)

      # Computing the output
      y_pred = model(batch)
      loss = criterion(y_pred, batch.target)
      mae = nn.L1Loss()(y_pred, batch.target)

      # Updating the metrics
      epoch_loss += loss.item()
      epoch_mae += mae.item()

  return epoch_loss / len(dataloader), epoch_mae / len(dataloader)
