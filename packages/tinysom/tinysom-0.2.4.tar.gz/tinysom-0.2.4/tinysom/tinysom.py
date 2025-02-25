#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import scipy.sparse as sp
import scipy.stats as st
import matplotlib.pyplot as plt
import matplotlib as mpl
from tqdm.auto import tqdm


class SOM(object):
    """Self-Organising Map (SOM) training and analysis.

    Attributes
    ----------
    bmus : ndarray
        1D array of Best Matching Units (BMUs) for each training instance.
    wts: ndarray
        SOM weights (codebook). Rows correspond to neurons, columns to
        weights in feature space.
    inertia_: ndarray
        Total squared distance between data points and BMUs.
    quanterr: float
        Mean squared distance between data points and BMUs.
    varexp: ndarray
        Fraction of variance explained: 1 - (quanterr/variance).
    topoerr: ndarray
        Fraction of data for which the BMU is not a neighbour of the 2nd BMU.
    """

    def __init__(self, n_rows, n_cols, topology='hexagonal', neighbourhood='gaussian',
                 metric='euclidean', n_epochs=10, weight_t0_Rmax=0.8, weight_tN_Rmin=0.2,
                 initial='pca', unit_dropout_factor=0., feature_dropout_factor=0.):
        """Class constructor.

        Parameters
        ----------
        n_rows : int
            Number of rows in SOM.
        n_cols : int
            Number of columns in SOM.
        topology : str, optional
            SOM topoplogy. Options are `hexagonal` (default) and `rectangular`.
        neighbourhood : str, optional
            Form of neighbourhood function on SOM. Options are
            `gaussian` (default), `exponential`, `linear`, `bubble`.
        metric : str
            Metric used to calculate BMUs. Options are
            'euclidean' (default) or 'cosine'.
        n_epochs : int, optional
            Number of training epochs. Defaults to 10.
        weight_t0_Rmax : float, optional
            Initial neighbourhood weight at maximum inter-neuron distance.
            Defaults to 0.8.
        weight_tN_Rmin : float, optional
            Final neighbourhood weight at minimum inter-neuron distance.
            Defaults to 0.2.
        initial : str, optional
            Weights initialisation method. Options are
            `pca` (default) or `random`.
        unit_dropout_factor : float, optional
            Fraction of units to drop randomly for each record and
            training epoch.
        feature_dropout_factor : float, optional
            Fraction of features to drop randomly for each record and
            training epoch.
        """

        self.n_rows = n_rows
        self.n_cols = n_cols
        self.topology = topology
        self.neighbourhood = neighbourhood
        self.metric = metric
        self.n_epochs = n_epochs
        self.weight_t0_Rmax = weight_t0_Rmax
        self.weight_tN_Rmin = weight_t0_Rmax
        self.initial = initial
        self.unit_dropout_factor = unit_dropout_factor
        self.units_dropped = None
        self.feature_dropout_factor = feature_dropout_factor
        self.bmus = None
        self.wts = None
        self.inertia_ = -1*np.ones(self.n_epochs)
        self.quanterr = None
        self.varexp = None
        self.topoerr = None
        self.d = None
        self.k = None
        self.umat_sharp = None

        # Generate distance**2, adjacency and U-matrices for neuron array
        self.ixs = np.arange(n_rows*n_cols)
        self.rows, self.cols = self.ixs // n_cols, self.ixs % n_cols
        if 'hex' in self.topology:
            self.topology = 'hexagonal'
            y, x = self.rows*1., self.cols*1.
            x[self.rows%2==1] = x[self.rows%2==1]+0.5
            y = y*np.sqrt(3)/2
        else:
            self.topology = 'rectangular'
            y, x = self.rows*1., self.cols*1.
        self.x = x; self.y = y
        self.d2mat = (x[:,None]-x[None,:])**2 + (y[:,None]-y[None,:])**2
        self.adjmat = np.isclose(self.d2mat, 1).astype(int)

        # Initialise U-matrix in edge list format as easier to work with
        self.adj_i, self.adj_j = np.where(self.adjmat==1)
        self.umat = np.zeros(self.adjmat.sum())

        # Define based on neighbourhood function and neuron distance matrix
        self.make_kernels()

    def calc_BMUs(self, X):
        """Calculate Best-Matching Units (BMUs) for training data array X.

        Parameters
        ----------
            X : ndarray
                Training data, with rows as instances, columns as features.
        """
        if self.metric == 'cosine':
            num = -(X@self.wts.T)
            denom = np.outer(np.linalg.norm(X, axis=1),
                             np.linalg.norm(self.wts, axis=1))
            return num/denom
        elif self.metric == 'euclidean':
            return ((X[:,None]-self.wts)**2).sum(axis=2)
        else:
            print('metric must be cosine or euclidean')
            return None

    def make_kernels(self):
        """Generate kernels for all epochs.

        User-defined kernel weights at the maximum radius Rmax for the
        first epoch, and unit radius R1 at the final epoch.
        """

        dmat = np.sqrt(self.d2mat)
        Rmax = dmat.max()

        # Define kernels based on neighbourhood function
        if self.neighbourhood == 'bubble':
            # Note that the bubble neighbourhood ignores sig_t0_Rmax and sig_tN_Rmin
            Rs = np.linspace(Rmax, 0.5, self.n_epochs)
            self.kernels = np.where(dmat[None,:,:]<=Rs[:,None,None], 1, np.spacing(1))
        elif self.neighbourhood == 'linear':
            sig = (self.weight_t0_Rmax - 1)/Rmax
            alpha_max = (self.weight_tN_Rmin - 1)/sig
            alphas = np.linspace(1, alpha_max, self.n_epochs)
            self.kernels = sig * dmat[None,:,:] * alphas[:,None,None] + 1
        elif self.neighbourhood == 'exponential':
            sig = -Rmax/(2*np.log(self.weight_t0_Rmax))
            alpha_max = -2*sig*np.log(self.weight_tN_Rmin)
            alphas = np.linspace(1, alpha_max, self.n_epochs)
            self.kernels = np.exp(-(dmat[None,:,:]*alphas[:,None,None]/(2*sig)))
        elif self.neighbourhood == 'gaussian':
            sig = -self.d2mat.max()/(2*np.log(self.weight_t0_Rmax))
            alpha_max = -2*sig*np.log(self.weight_tN_Rmin)
            alphas = np.linspace(1, alpha_max, self.n_epochs)
            self.kernels = np.exp(-(self.d2mat[None,:,:]*alphas[:,None,None]/(2*sig)))
        elif self.neighbourhood == 'kmeans':
            self.kernels = np.repeat(np.diag(np.ones(self.n_rows*self.n_cols))[None],
                                     self.n_epochs, axis=0) + np.spacing(1)
        else:
            print('Invalid neighbourhood')
            return None

    def fit(self, X, y=None, verbose=True):
        """Train SOM on input data array X using the batch algorithm.

        Input array X should be in the standard format, i.e.
        rows (axis 0) are instances, columns (axis 1) are features.

        Parameters
        ----------
            X : ndarray
                Training data, with rows as instances, columns as features.
            y : Ignored
                Not used, present here for API consistency by convention.
            verbose : boolean
                Track epochs using tqdm or not.
        """

        # Initialise SOM weights as a random array or using PCA
        n_samp, n_feat = X.shape
        if self.initial == 'random':
            self.wts = np.random.random(size=(self.n_rows*self.n_cols, n_feat))
        elif self.initial == 'pca':
            X_mean = X.mean(axis=0)
            X_zm = X - X_mean
            covmat = (X_zm.T @ X_zm)/n_samp
            eigvals, eigvecs = np.linalg.eigh(covmat)

            # Variance explained by PCs beyond the first two
            resid_variance = eigvals[:-2].sum()

            # Generate Gaussian noise to make up variance
            noise = np.random.normal(loc=0, scale=np.sqrt(resid_variance),
                                     size=(self.n_rows, self.n_cols, n_feat))

            # Ranges of row PCs (for EOF1) and column PCs (for EOF2) over SOM
            row_facs = np.linspace(-eigvals[-1], eigvals[-1], self.n_rows)
            col_facs = np.linspace(-eigvals[-2], eigvals[-2], self.n_cols)
            col_facs, row_facs = np.meshgrid(col_facs, row_facs)

            self.wts = ((row_facs[:,:,None] * eigvecs[:,-1]) +
                        (col_facs[:,:,None] * eigvecs[:,-2]) +
                        noise + X_mean).reshape((self.n_rows*self.n_cols, -1))
        else:
            print('initial must be random or pca')
            return None

        # Calculate initial BMUs
        self.bmus = self.calc_BMUs(X).argmin(axis=1)

        # Make unit dropout boolean mask for all epochs
        if self.unit_dropout_factor > np.spacing(1):
            ijk = (self.n_epochs, X.shape[0], self.n_rows*self.n_cols)
            self.units_dropped = np.random.uniform(size=ijk
                                                   )<=self.unit_dropout_factor

        if verbose:
            epochs = tqdm(range(self.n_epochs))
        else:
            epochs = range(self.n_epochs)
        for i in epochs:
            # Calculate BMU kernel weights
            bmu_kern_wts = self.kernels[i][self.bmus]

            # Calculate numerator (BMU kernel-weighted sum of training data)
            num = (X[:,None]*bmu_kern_wts[:,:,None]).sum(axis=0)

            # Calculate denominator (sum of BMU weights for training data)
            denom = bmu_kern_wts.sum(axis=0)

            # Update weights
            self.wts = num/denom[:,None]

            # Update BMUs for all training vectors
            if self.unit_dropout_factor < np.spacing(1):
                self.bmus = self.calc_BMUs(X).argmin(axis=1)
            else:
                self.bmus = np.where(self.units_dropped[i], np.inf,
                                     self.calc_BMUs(X)).argmin(axis=1)

            # Update inertia array
            self.inertia_[i] = ((X - self.wts[self.bmus])**2).sum()

        # Calculate U-matrix
        if self.metric == 'euclidean':
            self.umat = np.linalg.norm(self.wts[self.adj_i,:] -
                                       self.wts[self.adj_j,:], axis=1)
        else:
            num = (self.wts[self.adj_i,:] * self.wts[self.adj_j,:]).sum(axis=1)
            denom = (np.linalg.norm(self.wts[self.adj_i,:], axis=1) *
                     np.linalg.norm(self.wts[self.adj_j,:], axis=1))
            self.umat = num/denom

        # BMU hits
        self.hitcount = np.bincount(self.bmus)

        # Map quality metrics
        self.quanterr = self.inertia_[-1]/X.shape[0]
        self.varexp = 1 - self.quanterr/X.var(axis=0).sum()

        # Get indices of best and second BMUs and calculate adjacent fraction
        i, j = self.calc_BMUs(X).argsort(axis=1).T[:2]
        self.topoerr = 1 - self.adjmat[i,j].sum()/X.shape[0]

    def predict(self, X):
        """Calculate Best-Matching Units (BMUs) for training data array X.

        Parameters
        ----------
            X : ndarray
                Training data, with rows as instances, columns as features.

        Returns
        -------
            bmus : ndarray
                BMUs.
        """

        if self.wts is None:
            print('Train SOM before classifying')
            return None
        return self.calc_BMUs(X).argmin(axis=1)

    def calc_dumat(self):
        """Calculate distance matrix in feature space over SOM manifold."""

        umat = sp.coo_matrix((self.umat, (self.adj_i, self.adj_j))).tolil()
        self.dumat = sp.csgraph.floyd_warshall(umat, directed=False)

    def plot_umatrix(self, sharp=False, ax=None, figsize=(4,4)):
        """Plot U-matrix."""

        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=figsize)
        else:
            figsize = ax.figure.get_size_inches()
        lw = figsize[0]/25

        if sharp:
            umat = self.umat_sharp
        else:
            umat = self.umat
        if self.topology == 'hexagonal':
            pc = ax.hexbin(self.x[self.adj_i], 2*self.y[self.adj_j]/np.sqrt(3),
                           umat, gridsize=(self.n_cols, self.n_rows//2),
                           ec='w', lw=lw, extent=(0,self.n_cols,0,self.n_rows))
        else:
            pc = ax.scatter(self.x[self.adj_i], self.y[self.adj_j], c=umat,
                            marker='s')
        ax.set_title('U-matrix')
        ax.set_axis_off()
        return ax

    def sharpen_umat(self, d=0.5, k=0.1):
        """Function to sharpen u-matrix differences between neurons.

        Applies sigmoid function to u-matrix distances with weights up to 1 for
        higher quantiles and weights down to 0 for lower quantiles.

        Parameters
        ----------
            d : float
                Median of sigmoid; should be between 0 and 1.
            k : float
                Steepness of sigmoid.
        """

        ps = st.rankdata(self.umat)/self.umat.size
        self.d = d
        self.k = k
        self.umat_sharp = self.umat/(1+np.exp(-(ps-d)/k))

    def plot_component_planes(self, i=None, cmap='viridis_r', figsize=(4,4)):
        """Plot component planes.

        Parameters
        ----------
            i : int, list or ndarray
                Index or indices of neuron weights to visualise.
            cmap : str
                Matplotlib colourmap.
        """

        if i is None:
            to_loop = range(self.wts.shape[1])
        elif isinstance(i, int):
            to_loop = [i]
        else:
            to_loop = i

        # Loop over dimensions of codebook
        for i in to_loop:
            arr = self.wts[:,i].reshape((self.n_rows, self.n_cols))
            fig, ax = plt.subplots(1, 1, figsize=figsize)
            ax.imshow(arr, cmap=cmap)

    def plot_mesh2d(self, ax=None, feature_ixs=None):
        """Plot neuron mesh for 2D features only."""

        if self.wts is None or (self.wts.shape[1]>2 and feature_ixs is None):
            print('Ensure SOM is fitted and model either has two features'
                  'or two feature indices are passed.')
            return None

        adjmat_bool = self.adjmat.astype(bool)
        if feature_ixs is not None:
            wts_toplot = self.wts[:,feature_ixs]
        else:
            wts_toplot = self.wts

        lines = [(wts_toplot[i], j) for i in range(wts_toplot.shape[0])
                 for j in wts_toplot[adjmat_bool[i]]]
        ax.add_collection(mpl.collections.LineCollection(lines, linewidths=0.1, color='r'))
        ax.scatter(wts_toplot[:,0], wts_toplot[:,1], label='TinySOM', color='r', s=2, marker='x')


class SOM_cluster(SOM):
    """Subclass of SOM object for unsupervised clustering.

    Uses SOM twice, first to cluster input data to a general map of arbitrary
    size, and again to the target number of clusters.

    Attributes
    ----------
    labels_: ndarray
        Cluster labels derived from unsupervised clustering.
    """

    def __init__(self, n_clusters, n_rows, n_cols, topology='hexagonal', neighbourhood='gaussian',
                 metric='euclidean', n_epochs=10, weight_t0_Rmax=0.1, weight_tN_Rmin=0.1,
                 initial='pca', unit_dropout_factor=0., feature_dropout_factor=0.):
        """Subclass constructor.

        Parameters
        ----------
            n_clusters : int
                Number of clusters to target for unsupervised clustering.
        """

        super().__init__(n_rows, n_cols, topology, neighbourhood, metric, n_epochs, weight_t0_Rmax,
                         weight_tN_Rmin, initial, unit_dropout_factor, feature_dropout_factor)

        self.n_clusters = n_clusters
        self.neuron_to_label = np.empty(self.n_cols*self.n_rows)
        self.neuron_to_label[:] = np.nan
        self.labels_ = None

    def fit(self, X, y=None):
        """Modified fit function for clustering.

        Input array X should be in the standard format, i.e.
        rows (axis 0) are instances, columns (axis 1) are features.

        Parameters
        ----------
            X : ndarray
                Training data, with rows as instances, columns as features.
            y : Ignored
                Not used, present here for API consistency by convention.
        """

        super().fit(X)

        # A linear SOM instance to cluster the weights vectors
        som = SOM(1, self.n_clusters, neighbourhood='kmeans', n_epochs=100, initial='random')
        som.fit(self.wts)
        self.neuron_to_label[:] = som.bmus
        self.labels_ = som.bmus[self.bmus]

    def predict(self, X):
        """Predict clusters of data.

        Parameters
        ----------
            X : ndarray
                Training data, with rows as instances, columns as features.

        Returns
        -------
            cluster : ndarray
                Predicted cluster labels.
        """

        if np.isnan(self.neuron_to_label).all():
            print('Fit SOM clusterer before predicting')
            return None

        bmus = self.calc_BMUs(X).argmin(axis=1)
        return self.neuron_to_label[bmus]


class SOM_classify(SOM):
    """Subclass of SOM object for supervised classification.
    """

    def __init__(self, n_rows, n_cols, topology='hexagonal', neighbourhood='gaussian',
                 metric='euclidean', n_epochs=10, weight_t0_Rmax=0.1, weight_tN_Rmin=0.1,
                 initial='pca', unit_dropout_factor=0., feature_dropout_factor=0.):
        """Subclass constructor."""

        super().__init__(n_rows, n_cols, topology, neighbourhood, metric,
                         n_epochs, weight_t0_Rmax, weight_tN_Rmin, initial,
                         unit_dropout_factor, feature_dropout_factor)

        self.neuron_to_label = np.empty(self.ixs.size)
        self.neuron_to_label[:] = np.nan

    def fit(self, X, y):
        """Modified fit function for classification.

        Input array X should be in the standard format, i.e.
        rows (axis 0) are instances, columns (axis 1) are features.

        Parameters
        ----------
            X : ndarray
                Training data, with rows as instances, columns as features.
            y : ndarray or list
                Labels of training data for supervised training.
        """

        super().fit(X)

        # Supervised classification
        y = np.array(y)

        # Define mapping from neurons to classes using majority vote
        for ix in self.ixs:
            labels_ix = y[self.bmus==ix]
            values, counts = np.unique(labels_ix, return_counts=True)
            if counts.size > 0:
                self.neuron_to_label[ix] = values[np.argmax(counts)]
            else:
                self.neuron_to_label[ix] = np.nan

        # Backfill nans in neuron_to_label with the closest non-nan neuron
        if np.isnan(self.neuron_to_label).any():
            self.calc_dumat()
            dumat_nonan = np.where(np.isnan(self.neuron_to_label),
                                  np.inf, self.dumat)
            backfill = dumat_nonan.argmin(axis=1)
            self.neuron_to_label = self.neuron_to_label[backfill]

    def predict(self, X):
        """Predict labels of data.

        Parameters
        ----------
            X : ndarray
                Training data, with rows as instances, columns as features.

        Returns
        -------
            labels : ndarray
                Predicted labels.
        """

        if np.isnan(self.neuron_to_label).all():
            print('Fit SOM classifier before predicting')
            return None

        bmus = self.calc_BMUs(X).argmin(axis=1)
        return self.neuron_to_label[bmus]
