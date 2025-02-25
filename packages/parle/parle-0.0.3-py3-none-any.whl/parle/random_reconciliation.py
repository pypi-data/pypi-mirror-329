from revolutionhtl.nxTree import set_sparce_matrix, LCA, get_dad

from networkx import DiGraph
from random import randint
from numpy.random import choice
from math import exp

_kCoin= 10000
coin= lambda : randint(0,_kCoin)/_kCoin

def random_filogeny(n_leaves):
    """
    Buttom-up generation of a random tree with n_leaves.
    Algorithm: random joining.
    """
    leafs= list(range(n_leaves))

    T= DiGraph()
    T.add_nodes_from(leafs)

    Q= list(leafs)
    idx= n_leaves

    while len(Q) > 1:
        x0,x1= choice(Q, 2, replace= False)

        T.add_node(idx)
        T.add_edges_from([(idx, x0), (idx, x1)])

        Q.remove(x0)
        Q.remove(x1)
        Q.append(idx)
        idx+=1

    T.root= Q.pop()
    T.planted_root= idx
    T.add_node(idx)
    T.add_edge(idx, T.root)

    set_sparce_matrix(T)

    for x in T:
        T.nodes[x]['label']= x

    return T, leafs

def get_genes(species, n_genes_per_species):
    """
    Generates a list of genes together with the
    species mapping
    """
    genes= list()
    sigma= dict()
    idx= 0

    for x in species:
        for _ in range(n_genes_per_species):
            genes.append(idx)
            sigma[idx]= x
            idx+= 1
    return genes, sigma

def get_random_n_genes(species, max_genes_per_species):
    """
    Generates a list of genes together with the
    species mapping
    """
    genes= list()
    sigma= dict()
    idx= 0

    for x in species:
        ngenes= randint(1, max_genes_per_species)
        for _ in range(ngenes):
            genes.append(idx)
            sigma[idx]= x
            idx+= 1
    return genes, sigma

def random_reconciliation(genes, Ts, sigma, Ms, p_speciation= 0.5, p0_cherry=1, a_cherry=0.7):
    """
    Algorithm: random_joining_reconciliation
    """
    Tg= DiGraph()
    Tg.add_nodes_from(genes)
    mu= sigma.copy()

    for x in genes:
        Tg.nodes[x]['label']= x

    idx= max(genes)+1
    Q= list(genes)
    while len(Q) > 1:
        x0,x1= choose_cherry(Q, mu, Ms, p0_cherry, a_cherry)

        Tg.add_node(idx)
        Tg.add_edges_from([(idx, x0), (idx, x1)])

        y, event= choose_map(Ts, (mu[x0], mu[x1]), Ms, p_speciation)
        mu[idx]= y
        Tg.nodes[idx]['event']= event
        Tg.nodes[idx]['label']= idx

        Q.remove(x0)
        Q.remove(x1)
        Q.append(idx)
        idx+=1

    Tg.root= Q.pop()
    Tg.planted_root= idx
    Tg.add_node(idx)
    Tg.add_edge(idx, Tg.root)

    set_sparce_matrix(Tg)

    return Tg, mu

def choose_cherry(Q, mu, Ms, p0_cherry, a_cherry):
    f= False
    while not f:
        x0,x1= choice(Q, 2, replace= False)
        d= Ms[mu[x0],mu[x1]]
        f=  coin() <= p0_cherry*exp(-a_cherry*d)
    return x0,x1

def choose_map(Ts, ch_mu, Ms, p_speciation):
    y0= LCA(Ts, ch_mu)
    if y0 in ch_mu:
        event= 'D'
    else:
        event= choice(['S','D'], p= [p_speciation, 1-p_speciation])
    return y0, event

def get_ancestors(T, x, root= None):
    if root==None:
        root= T.root
    L= [x]
    while x!=root:
        x= get_dad(T, x)
        L.append( x )
    return L




