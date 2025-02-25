from .plr import plr_disimilarity_raw, compute_S_matrix, plr_disimilarity_normalized, plr_disimilarity_components
from .errors import NonUniqueNodeLabels

from revolutionhtl.nhx_tools import read_nhx
from revolutionhtl.nxTree import count_leafs

from pandas import DataFrame, read_csv
from itertools import combinations
from networkx import dfs_postorder_nodes

def compute_plr_dataframe_all_vs_all(df, Ts, alpha= None):
    # Check input dataframe
    _check_labels_all_vs_all(df, Ts)
    # Compute parameters
    S_matrix= compute_S_matrix(Ts)
    n_species= count_leafs(Ts)
    if alpha==None:
        alpha= 1/n_species
    # Compute distance
    df_distances= []
    for i,j in combinations(df.index, 2):
        d_plr= plr_disimilarity_normalized(df.loc[i,'tree'], df.loc[j,'tree'],
                                           df.loc[i,'mu'], df.loc[j,'mu'],
                                           n_species, S_matrix, alpha)
        df_distances+= [[f"{i}-vs-{j}", d_plr]]
    df_ret= DataFrame(df_distances, columns= ['trees', 'distance'])
    return df_ret

def compute_plr_dataframe_rows(df, Ts, alpha= None):
    # Check input dataframe
    _check_labels_rows(df, Ts)
    # Compute parameters
    S_matrix= compute_S_matrix(Ts)
    n_species= count_leafs(Ts)
    if alpha==None:
        alpha= 1/n_species
    # Compute distance
    d_plr= lambda row: plr_disimilarity_normalized(row.tree_i, row.tree_j, row.mu_i, row.mu_j,
                                                   n_species, S_matrix, alpha)
    df_ret= DataFrame(dict(OG= df.OG, distance=df.apply(d_plr, axis= 1)))
    return df_ret

component_columns= ['path_dist', 'lbl_dist', 'raw_distance', 'n_species',
                    'm_genes', 'alpha', 'diameter', 'normalized_distance']
def compute_plr_components_dataframe_rows(df, Ts, alpha= None):
    # Check input dataframe
    _check_labels_rows(df, Ts)
    # Compute parameters
    S_matrix= compute_S_matrix(Ts)
    n_species= count_leafs(Ts)
    if alpha==None:
        alpha= 1/n_species
    # Compue distance
    df_prl= lambda row: plr_disimilarity_components(row.tree_i, row.tree_j,
                                                    row.mu_i, row.mu_j,
                                                    n_species, S_matrix, alpha)
    df_ret= DataFrame(list(map(list, df.apply(df_prl, axis= 1).values)),
                      columns= component_columns)
    df_ret['OG']= df.OG

    return df_ret[ ['OG']+component_columns ]

def check_label_uniqueness(T, labelAttr):
    nodes= list(dfs_postorder_nodes(T, T.u_lca))
    labels= set((T.nodes[x][labelAttr] for x in nodes))
    return len(nodes)==len(labels)

def load_df_all_vs_all(path, treeCol= 'tree', muCol= 'mu'):
    df= read_csv(path, sep='\t')
    df[treeCol]= df[treeCol].apply(read_nhx)
    df[muCol]= df[muCol].apply(_txtMu_2_dict)
    return df

def load_df_rows(path, tree_i_Col= 'tree_i', tree_j_Col= 'tree_j', mu_i_Col= 'mu_i', mu_j_Col= 'mu_j'):
    df= read_csv(path, sep='\t')
    df[tree_i_Col]= df[tree_i_Col].apply(read_nhx)
    df[tree_j_Col]= df[tree_j_Col].apply(read_nhx)
    df[mu_i_Col]= df[mu_i_Col].apply(_txtMu_2_dict)
    df[mu_j_Col]= df[mu_j_Col].apply(_txtMu_2_dict)
    return df

def _txtMu_2_dict(txt):
    return dict(map(lambda x: x.split(':'), txt.split(',')))

txt_map= lambda X: ','.join((f"{a}:{b}" for a,b in X.items()))

def _check_labels_all_vs_all(df, Ts):
    if not check_label_uniqueness(Ts, 'label'):
        raise NonUniqueNodeLabels('Labels of species tree are not unique')
    if not df.tree.apply(lambda T: check_label_uniqueness(T, labelAttr)).all():
        raise NonUniqueNodeLabels('There are gene trees with non unique albels')

def _check_labels_rows(df, Ts):
    if not check_label_uniqueness(Ts, 'label'):
        raise NonUniqueNodeLabels('Labels of species tree are not unique')
    if not df.tree_i.apply(lambda T: check_label_uniqueness(T, 'label')).all():
        raise NonUniqueNodeLabels('There are gene trees with non-unique labels')
    if not df.tree_j.apply(lambda T: check_label_uniqueness(T, 'label')).all():
        raise NonUniqueNodeLabels('There are gene trees with non-unique labels')
