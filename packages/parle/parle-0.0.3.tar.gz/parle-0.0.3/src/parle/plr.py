from revolutionhtl.nxTree import is_leaf, count_leafs
from networkx import dfs_postorder_nodes
from itertools import chain, combinations, product
from pandas import DataFrame
from revolutionhtl.lca_rmq import LCA
import numpy as np

def plr_disimilarity_normalized(T_i, T_j, mu_i, mu_j, n_species, S_matrix, alpha,
                                labelAttr= 'label', eventAttr= 'event'):
    disimilarity= plr_disimilarity_raw(T_i, T_j, mu_i, mu_j, S_matrix,
                                       alpha, labelAttr, eventAttr)
    m_genes= count_leafs(T_i)
    diameter= compute_diamter(n_species, m_genes, alpha)
    return disimilarity/diameter

def plr_disimilarity_raw(T_i, T_j, mu_i, mu_j, S_matrix, alpha,
                         labelAttr= 'label', eventAttr= 'event'):
    d_ij= _plr_asymmetric(T_i, T_j, mu_i, mu_j, S_matrix, alpha, labelAttr, eventAttr)
    d_ji= _plr_asymmetric(T_j, T_i, mu_j, mu_i, S_matrix, alpha, labelAttr, eventAttr)
    return d_ij+d_ji

def plr_disimilarity_components(T_i, T_j, mu_i, mu_j, n_species, S_matrix, alpha,
                                labelAttr= 'label', eventAttr= 'event'):
    # Compute equivalent nodes
    E_ij= _compute_equivalent_nodes(T_i, T_j, labelAttr)
    E_ji= _compute_equivalent_nodes(T_j, T_i, labelAttr)
    # Compute path distance
    d_path_ij= _plr_path_component_asymmetric(T_i, T_j, mu_i, mu_j, E_ij, S_matrix, labelAttr)
    d_path_ji= _plr_path_component_asymmetric(T_j, T_i, mu_j, mu_i, E_ji, S_matrix, labelAttr)
    d_path= d_path_ij+d_path_ji
    # Compute label distance
    d_lbl_ij= _plr_lbl_component_asymmetric(T_i, T_j, E_ij, eventAttr)
    d_lbl_ji= _plr_lbl_component_asymmetric(T_j, T_i, E_ji, eventAttr)
    d_lbl= d_lbl_ij+d_lbl_ji
    # Compute raw parle distance
    d_raw= alpha*d_path + (1-alpha)*d_lbl
    # Compute normalization
    m_genes= count_leafs(T_i)
    diameter= compute_diamter(n_species, m_genes, alpha)
    d_prl= d_raw/diameter
    return d_path, d_lbl, d_raw, n_species, m_genes, alpha, diameter, d_prl

def compute_diamter(n, m, alpha):
    """
    n = number of species
    m = number of genes
    """
    return 2*alpha*(n-2)*(m-1) + 2*(1-alpha)*(m-1)

def compute_S_matrix(S, labelAttr='label'):
    M= _init_S_matrix(S, labelAttr)
    descendants= dict()
    for x_node in dfs_postorder_nodes(S, S.u_lca):
        x_label= S.nodes[x_node][labelAttr]
        if is_leaf(S, x_node):
            # Track descendants
            descendants[x_label]= {x_label}
        else:
            Y= set((S.nodes[y][labelAttr] for y in S[x_node]))
            # Distance from x to descendants: P_xz= P_yz + 1
            for y_label in Y:
                for z_label in descendants[y_label]:
                    M.loc[x_label,z_label]= M.loc[y_label,z_label] + 1
                    M.loc[z_label,x_label]= M.loc[x_label,z_label]
            # Distance between two descendants z and z1: P_zz1= P_xz + P_xz1
            for y_label,y1_label in combinations(Y, 2):
                for z_label,z1_label in product(descendants[y_label], descendants[y1_label]):
                    M.loc[z_label, z1_label]= M.loc[x_label,z_label] + M.loc[x_label,z1_label]
                    M.loc[z1_label, z_label]= M.loc[z_label, z1_label]
            # Track descendants
            descendants[x_label]= set(chain.from_iterable((descendants[y_label]
                                                          for y_label in Y))) .union( {x_label} )
    return M.loc

def _plr_asymmetric(T_i, T_j, mu_i, mu_j, S_matrix, alpha, labelAttr, eventAttr):
    E_ij= _compute_equivalent_nodes(T_i, T_j, labelAttr)
    d_ij= lambda x: _d_ij(x, T_i, T_j, mu_i, mu_j, E_ij, S_matrix,
                          alpha, labelAttr, eventAttr)
    return sum(map(d_ij, dfs_postorder_nodes(T_i, source= T_i.u_lca)))

def _plr_path_component_asymmetric(T_i, T_j, mu_i, mu_j, E_ij, S_matrix, labelAttr):
    d_path_ij= lambda x: _d_path(x, T_i, T_j, mu_i, mu_j, E_ij, S_matrix, labelAttr)
    return sum(map(d_path_ij, dfs_postorder_nodes(T_i, source= T_i.u_lca)))

def _plr_lbl_component_asymmetric(T_i, T_j, E_ij, eventAttr):
    d_lbl_ij= lambda x: _d_lbl(x, T_i, T_j, E_ij, eventAttr)
    return sum(map(d_lbl_ij, dfs_postorder_nodes(T_i, source= T_i.u_lca)))

def _d_ij(x, T_i, T_j, mu_i, mu_j, E_ij, S_matrix, alpha, labelAttr, eventAttr):
    d_path= _d_path(x, T_i, T_j, mu_i, mu_j, E_ij, S_matrix, labelAttr)
    d_lbl= _d_lbl(x, T_i, T_j, E_ij, eventAttr)
    return alpha*d_path + (1-alpha)*d_lbl

def _d_path(x, T_i, T_j, mu_i, mu_j, E_ij, S_matrix, labelAttr):
    return S_matrix[mu_i[T_i.nodes[x][labelAttr]], mu_j[T_j.nodes[E_ij[x]][labelAttr]]]

def _d_lbl(x, T_i, T_j, E_ij, eventAttr):
    return T_i.nodes[x][eventAttr] != T_j.nodes[E_ij[x]][eventAttr]

def _compute_equivalent_nodes(T_i, T_j, labelAttr):
    E_ij= _init_E_ij(T_i, T_j, labelAttr)
    induced_leafs= dict()
    for i_node in dfs_postorder_nodes(T_i):
        if is_leaf(T_i, i_node):
            # Add induced leaf
            induced_leafs[i_node]= { E_ij[ i_node ] }
        else:
            # compute induced leafs
            induced_leafs[i_node]= set(chain.from_iterable((induced_leafs[x] for x in T_i[i_node])))
            # compute LCA in T_j
            E_ij[i_node]= LCA(T_j, induced_leafs[i_node])
    return E_ij

def _init_S_matrix(S, labelAttr):
    index= [S.nodes[x][labelAttr] for x in dfs_postorder_nodes(S, S.u_lca)]
    N= len(index)
    return DataFrame(np.zeros((N,N)), columns= index, index= index)

def _init_E_ij(T_i, T_j, labelAttr):
    # Check leafs
    i_leafs= _label_2_leaf(T_i, labelAttr)
    j_leafs= _label_2_leaf(T_j, labelAttr)
    if set(i_leafs) != set(j_leafs):
        raise ValueError('The leafs of the trees are not the same')
    # Init E_ij
    return {x : j_leafs[x_label] for x_label,x in i_leafs.items()}

_label_2_leaf= lambda T, attr: {T.nodes[x][attr] : x for x in _leafs_iterator(T)}
_leafs_iterator= lambda T: (x for x in T if is_leaf(T, x))
