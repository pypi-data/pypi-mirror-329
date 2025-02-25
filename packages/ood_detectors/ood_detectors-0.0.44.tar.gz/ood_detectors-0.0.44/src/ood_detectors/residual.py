import numpy as np
from sklearn.covariance import EmpiricalCovariance
import torch
import tqdm


class Residual(torch.nn.Module):
    """
    Residual class for outlier detection.

    Args:
        dims (int): Number of dimensions to consider for outlier detection. Default is 512.
        u (int): Mean value for data centering. Default is 0.

    Attributes:
        dims (int): Number of dimensions to consider for outlier detection.
        u (int): Mean value for data centering.
        name (str): Name of the Residual instance.

    Methods:
        fit(data, *args, **kwargs): Fit the Residual model to the given data.
        predict(data, *args, **kwargs): Predict the outlier scores for the given data.
        to(device): Move the Residual model to the specified device.
        state_dict(): Get the state dictionary of the Residual model.
        load_state_dict(state_dict): Load the state dictionary into the Residual model.

    """

    def __init__(self, dims=512, u=0):
        super().__init__()
        self.dims = dims
        self.u = u
        self.name = "Residual"
        self.ns = torch.tensor([])
        self.device = "cpu"

    def fit(self, data, *args, collate_fn=None, **kwargs):
        """
        Fit the Residual model to the given data.

        Args:
            data (array-like or torch.Tensor or torch.utils.data.DataLoader): Input data for fitting the model.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            list: An empty list.

        """
            
        if isinstance(data, (list, tuple)):
            data = torch.tensor(data, dtype=torch.float32)
        elif isinstance(data, torch.utils.data.Dataset):
            if collate_fn is None and getattr(data, 'collate_fn', None) is not None:
                collate_fn = data.collate_fn
            if collate_fn is None:
                data = torch.vstack([x for x, *_ in data])
            else:
                data = torch.vstack([collate_fn([d])for d in data])
        feat_dim = data.shape[-1]
        if self.dims is None:
            self.dims = 1000 if feat_dim >= 2048 else 512 
        if self.dims <= 1:
            self.dims = int(feat_dim * self.dims)
        if self.dims < 2:
            self.dims = 2
    
        x = data.to(self.device) - self.u

        n_samples = x.shape[0]
        cov_matrix = (x.T @ x) / n_samples 

        eig_vals_torch, eigen_vectors_torch = torch.linalg.eigh(cov_matrix)

        sorted_indices_torch = torch.argsort(eig_vals_torch, descending=True)

        self.ns = eigen_vectors_torch[:, sorted_indices_torch[self.dims:]].contiguous().to(torch.float32)
        return [-1]

    def forward(self, x):
        return torch.linalg.norm((x - self.u) @ self.ns, dim=-1)

    def predict(self, data, batch_size=1024, *args, collate_fn=None, **kwargs):
        """
        Predict the outlier scores for the given data in batches.

        Args:
            data (array-like, torch.Tensor, torch.utils.data.DataLoader, or torch.utils.data.Dataset): Input data for predicting the outlier scores.
            batch_size (int): The size of the batches to use for prediction.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            numpy.ndarray: Outlier scores for the input data.
        """
        if isinstance(data, (list, tuple, np.ndarray)):
            data = torch.tensor(data, dtype=torch.float32)
            dataset = torch.utils.data.TensorDataset(data)
            data_loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=False, drop_last=False)
        elif isinstance(data, torch.Tensor):
            dataset = torch.utils.data.TensorDataset(data)
            data_loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=False, drop_last=False)
        elif isinstance(data, torch.utils.data.Dataset):
            if collate_fn is None and getattr(data, 'collate_fn', None) is not None:
                collate_fn = data.collate_fn
            data_loader = torch.utils.data.DataLoader(data, batch_size=batch_size, shuffle=False, collate_fn=collate_fn, drop_last=False)
        elif isinstance(data, torch.utils.data.DataLoader):
            data_loader = data
        else:
            raise TypeError("Unsupported data type: {}".format(type(data)))

        scores = []
        for (batch,) in data_loader:
            batch = batch.to(self.device)
            batch_scores = self.forward(batch)
            scores.append(batch_scores.detach().cpu().numpy().squeeze())
        return np.concatenate(scores)

    def to(self, device):
        """
        Move the Residual model to the specified device.

        Args:
            device: Device to move the model to.

        """
        self.ns = self.ns.to(device)
        self.device = device
        return self

    def state_dict(self):
        """
        Get the state dictionary of the Residual model.

        Returns:
            dict: State dictionary of the Residual model.

        """
        return {"dims": self.dims, "u": self.u, "ns": self.ns}

    def load_state_dict(self, state_dict):
        """
        Load the state dictionary into the Residual model.

        Args:
            state_dict (dict): State dictionary to load into the Residual model.

        Returns:
            self: Loaded Residual model.

        """
        self.dims = state_dict["dims"]
        self.u = state_dict["u"]
        self.ns = state_dict["ns"]
        return self


class ResidualX():
    def __init__(self, dims=0.5, k=2, subsample=0.5):
        super().__init__()
        self.ood_detectors = [Residual(dims=dims) for _ in range(k)]
        self.subsample = subsample
        self.name = f"Residualx{k}"
        self.device = "cpu"

    def to(self, device):
        self.device = device
        return self
    
    def load_state_dict(self, state_dict):
        for ood_detector, state_dict in zip(self.ood_detectors, state_dict):
            ood_detector.load_state_dict(state_dict)
        return self
    
    def state_dict(self):
        return [ood_detector.state_dict() for ood_detector in self.ood_detectors]
    
    def fit(self, data, *args, verbose=True, **kwargs):
        samples = int(len(data) * self.subsample)
        splits = [np.random.permutation(len(data))[:samples] for _ in range(0, len(data)-1)] + [np.arange(len(data))]
        if verbose:
            iter = tqdm.tqdm(list(zip(self.ood_detectors, splits)))
        else:
            iter = zip(self.ood_detectors, splits)

        loss = []
        collate_fn = kwargs.get('collate_fn', None)
        for ood_detector, split in iter:
            if isinstance(data, (list, tuple)):
                data_split = [data[i] for i in split]
            elif isinstance(data, torch.Tensor):
                data_split = data[split]
            elif isinstance(data, torch.utils.data.Dataset):
                if collate_fn is None and getattr(data, 'collate_fn', None) is not None:
                    collate_fn = data.collate_fn
                    kwargs['collate_fn'] = collate_fn
                data_split = torch.utils.data.Subset(data, split)
            if isinstance(data, np.ndarray):
                data_split = data[split]
            loss.append(ood_detector.fit(data_split, *args, **kwargs))
        return loss

    
    def predict(self, x, *args, reduce=True, verbose=True, **kwargs):
        if verbose:
            iter = tqdm.tqdm(self.ood_detectors)
        else:
            iter = self.ood_detectors
        
        if reduce:
            return np.stack([ood_detector.predict(x,*args, **kwargs) for ood_detector in iter]).mean(axis=0)
        else:
            return np.stack([ood_detector.predict(x,*args, **kwargs) for ood_detector in iter])
        
    def forward(self, x, *args, reduce=True, verbose=True, **kwargs):
        if verbose:
            iter = tqdm.tqdm(self.ood_detectors)
        else:
            iter = self.ood_detectors

        if reduce:
            return torch.stack([ood_detector(x,*args, **kwargs) for ood_detector in iter]).mean(axis=0)
        else:
            return torch.stack([ood_detector(x,*args, **kwargs) for ood_detector in iter])
    
    