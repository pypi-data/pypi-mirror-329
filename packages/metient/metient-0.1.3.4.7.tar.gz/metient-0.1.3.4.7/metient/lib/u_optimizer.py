import torch
from metient.util import vertex_labeling_util as vutil
from metient.util import data_extraction_util as dutil
from torch.distributions.binomial import Binomial
import numpy as np
import pandas as pd
import numpy as np

from metient.lib.projection import fit_F
from metient.util.globals import MIN_VARIANCE

class ObservedClonesSolver:
    def __init__(self, num_sites, num_internal_nodes, ref, var, omega, idx_to_observed_sites,
                 input_T, G, node_collection, weights, config, estimate_observed_clones, ordered_sites):
        self.ref = ref
        self.var = var
        self.omega = omega
        self.input_T = input_T
        self.G = G
        self.weights = weights
        self.config = config
        self.num_sites = num_sites
        self.num_internal_nodes = num_internal_nodes
        self.node_collection = node_collection
        self.estimate_observed_clones = estimate_observed_clones
        self.idx_to_observed_sites = idx_to_observed_sites
        self.ordered_sites = ordered_sites
    
    def run(self):
        if not self.estimate_observed_clones:
            T, G, L, node_collection = vutil.full_adj_matrix_from_internal_node_idx_to_sites_present(self.input_T, self.G, self.idx_to_observed_sites, 
                                                                                                     self.num_sites, self.config['identical_clone_gen_dist'],
                                                                                                     self.node_collection, self.ordered_sites)
            return None, self.input_T, T, G, L, node_collection, self.num_internal_nodes, self.idx_to_observed_sites

        # return fit_u_map(self)
        return self._fit_u_mle()

    def _fit_u_mle(self):
        """
        Fits the observed clone proportions matrix U using the projection algorithm (finds an MLE estimate of U)
        """
        V, R = self.var, self.ref
        V_hat = V + 1
        T_hat = V + R + 2
        W = V_hat*(1 - V_hat/T_hat) / (T_hat*self.omega)**2
        W = np.maximum(MIN_VARIANCE, W)
        

        parents = self._convert_adjmatrix_to_parents()
        print("parents\n", parents)

        # Convert inputs to float64
        V = V.detach().numpy().astype(np.float64).T
        R = R.detach().numpy().astype(np.float64).T
        W = W.detach().numpy().astype(np.float64).T
        omega = self.omega.detach().numpy().astype(np.float64).T

        F, U, F_llh = fit_F(parents, 
                            V, 
                            R,
                            omega,
                            W)

        U = torch.from_numpy(U).T
        return self._build_full_tree_with_witness_nodes(U)

    def _convert_adjmatrix_to_parents(self):
        """
        Converts the input adjacency matrix to a parent array
        ( a numpy array where each index represents a node, and the value at that index represents
        that nodes direct ancestor (parent) in the tree)
        """
        # Add germline root to the tree
        new_T = np.zeros((self.input_T.shape[0] + 1, self.input_T.shape[0] + 1))
        new_T[1:, 1:] = self.input_T
        new_T[0, 1] = 1  # New root connects to old root
        adj = np.copy(new_T)
        np.fill_diagonal(adj, 0)
        return np.argmax(adj[:,1:], axis=0)

    def _build_full_tree_with_witness_nodes(self, U):
        """
        Attaches witness nodes to the inputted tree using the observed clone proportions matrix U

        Args:
            U: Observed clone proportions matrix (num_sites x num_internal_nodes)
            u_solver: ObservedClonesSolver object

        Returns:
            U: Observed clone proportions matrix (num_sites x num_internal_nodes)
            input_T: Input tree (num_internal_nodes x num_internal_nodes)
            T: Expanded tree, which includes internal nodes and leaf/witness nodes (num_tree_nodes x num_tree_nodes)
            G: Genetic distance matrix (num_tree_nodes x num_tree_nodes)
            L: Leaf node labels (num_sites x num_leaf_nodes)
            node_collection: Node collection that contains info on all nodes
            num_internal_nodes: Number of internal nodes
            idx_to_observed_sites: Node index to observed sites
        """
        with torch.no_grad():
            full_T, full_G, L, idx_to_observed_sites, node_collection = vutil.full_adj_matrix_using_inferred_observed_clones(U, self.input_T, self.G, self.num_sites, 
                                                                                                                            self.config['identical_clone_gen_dist'],
                                                                                                                            self.node_collection, self.ordered_sites)
            # Remove any leaf nodes that aren't detected at > U_CUTOFF in any sites. These are not well estimated
            U_no_normal = U[:,1:] # first column is normal cells
            removal_indices = []
            for node_idx in range(U_no_normal.shape[1]):
                children = vutil.get_child_indices(self.input_T, [node_idx])
                if node_idx not in idx_to_observed_sites and len(children) == 0:
                    removal_indices.append(node_idx)
            # print("node indices not well estimated", removal_indices)

            U, input_T, T, G, node_collection, idx_to_observed_sites = vutil.remove_leaf_indices_not_observed_sites(removal_indices, U, self.input_T, 
                                                                                                                    full_T, full_G, node_collection, idx_to_observed_sites)
            num_internal_nodes = self.num_internal_nodes - len(removal_indices)
            
        return U, input_T, T, G, L, node_collection, num_internal_nodes, idx_to_observed_sites






def fit_u_map(u_solver):
    
    # We're learning eta, which is the mixture matrix U (U = softmax(eta)), and tells us the existence
    # and anatomical locations of the extant clones (U > U_CUTOFF)
    #eta = -1 * torch.rand(num_sites, num_internal_nodes + 1) # an extra column for normal cells
    eta = torch.ones(u_solver.num_sites, u_solver.num_internal_nodes + 1) # an extra column for normal cells
    eta.requires_grad = True 
    u_optimizer = torch.optim.Adam([eta], lr=u_solver.config['lr'])

    B = vutil.mutation_matrix_with_normal_cells(u_solver.input_T)
    print("B\n", B)
    i = 0
    u_prev = eta
    u_diff = 1e9
    while u_diff > 1e-6 and i < 300:
        u_optimizer.zero_grad()
        U, u_loss, nll, reg = compute_u_loss(eta, u_solver.ref, u_solver.var, u_solver.omega, B, u_solver.weights)
        u_loss.backward()
        u_optimizer.step()
        u_diff = torch.abs(torch.norm(u_prev - U))
        u_prev = U
        i += 1

    print_U(U, B, u_solver.node_collection, u_solver.ordered_sites, u_solver.ref, u_solver.var)

    return build_tree_with_witness_nodes(U, u_solver)

# Adapted from PairTree
def calc_llh(F_hat, R, V, omega_v):
    '''
    Args:
        F_hat: estimated subclonal frequency matrix (num_nodes x num_mutation_clusters)
        R: Reference allele count matrix (num_samples x num_mutation_clusters)
        V: Variant allele count matrix (num_samples x num_mutation_clusters)
    Returns:
        Data fit using the Binomial likelihood (p(x|F_hat)). See PairTree (Wintersinger et. al.)
        supplement section 2.2 for details.
    '''

    N = R + V
    S, K = F_hat.shape

    for matrix in V, N, omega_v:
        assert(matrix.shape == (S, K-1))

    P = torch.mul(omega_v, F_hat[:,1:])

    bin_dist = Binomial(N, P)
    F_llh = bin_dist.log_prob(V) / np.log(2)
    assert(not torch.any(F_llh.isnan()))
    assert(not torch.any(F_llh.isinf()))

    llh_per_sample = -torch.sum(F_llh, axis=1) / S
    nlglh = torch.sum(llh_per_sample) / (K-1)
    return nlglh

def compute_u_loss(eta, ref, var, omega, B, weights):
    '''
    Args:
        eta: raw values we are estimating of matrix U (num_sites x num_internal_nodes)
        ref: Reference matrix (num_anatomical_sites x num_mutation_clusters). Num. reads that map to reference allele
        var: Variant matrix (num_anatomical_sites x num_mutation_clusters). Num. reads that map to variant allele
        omega: VAF to subclonal frequency correction 
        B: Mutation matrix (shape: num_internal_nodes x num_mutation_clusters)
        weights: Weights object

    Returns:
        Loss to score the estimated proportions of each clone in each site
    '''
    
    # Using the softmax enforces that the row sums are 1, since the proprtions of
    # clones in a given site should sum to 1
    U = torch.softmax(eta, dim=1)
    # print("eta", eta)
    #print("U", U)

    # 1. Data fit
    F_hat = (U @ B)
    nlglh = calc_llh(F_hat, ref, var, omega)
    # 2. Regularization to make some values of U -> 0
    reg = torch.sum(eta) # l1 norm 
    clone_proportion_loss = (weights.data_fit*nlglh + weights.reg*reg)
    
    return U, clone_proportion_loss, weights.data_fit*nlglh, weights.reg*reg

def print_U(U, B, node_collection, ordered_sites, ref, var):
    cols = ["GL"]+[";".join([str(i)]+node_collection.get_node(i).label[:2]) for i in range(len(node_collection.get_nodes())) if not node_collection.get_node(i).is_witness]
    U_df = pd.DataFrame(U.detach().numpy(), index=ordered_sites, columns=cols)

    print("U\n", U_df)
    F_df = pd.DataFrame((var/(ref+var)).numpy(), index=ordered_sites, columns=cols[1:])
    print("F\n", F_df)
    Fhat_df = pd.DataFrame(0.5*(U @ B).detach().numpy()[:,1:], index=ordered_sites, columns=cols[1:])
    print("F hat\n", Fhat_df)