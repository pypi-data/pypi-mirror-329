desc_def= """
"""

hello="""
         .
._  _.._.| _
[_)(_][  |(/,
|            """

if __name__ == "__main__":
    import argparse
    from importlib.metadata import version

    V_plr= version('parle')
    txt= f"parle.simulate_reconciliations V{V_plr}"

    parser = argparse.ArgumentParser(prog= 'parle.simulate_reconciliations',
                                     description=f'{txt}\n{desc_def}',
                                     usage='python -m parle.simulate_reconciliations species_tree n_genes n_recons <optional arguments>',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                    )

    parser.add_argument('species_tree',
                        help= '[str or int] .txt file containing a species tree in nhx format or number of species to simulate by "random merges".',
                       )

    parser.add_argument('n_genes',
                        help= '[int] maximum number of genes per species.',
                        type= int,
                       )

    parser.add_argument('n_recons',
                        help= '[int] number of rows in output table.',
                        type= int,
                       )

    parser.add_argument('-a', '--a',
                        help= '[float | Default: 0.7] a parameter for cherry probability (P0*exp(-a*d_path).',
                        type= float,
                        default= 0.7,
                       )

    parser.add_argument('-p0', '--p0',
                        help= '[float | Default: 1] p0 parameter for cherry probability (P0*exp(-a*d_path).',
                        type= float,
                        default= 1,
                       )

    parser.add_argument('-ps', '--ps',
                        help= '[float | Default: 0.5] probability of choosing speciation when applicable.',
                        type= float,
                        default= 0.7,
                       )

    parser.add_argument('-s', '--seed',
                        help= '[int | Default: None] seed for random decisions.',
                        type= int,
                        default= None,
                       )

    parser.add_argument('-m', '--mode',
                        help= '[str | Default: pairs] mode for output reconciliation table. Choices: pairs, list',
                        type= str,
                        choices= ['pairs', 'list'],
                        default= 'list',
                       )

    parser.add_argument('-o', '--output_prefix',
                        help= '[str | Default: plr.] Prefix for output files.',
                        type= str,
                        default= 'plr.',
                       )

    args= parser.parse_args()

    print(f'{hello}V{V_plr}\n\n')

    ############
    # Simulate #
    ############
    from .plr import _compute_S_matrix
    from .utils import txt_map
    from .random_reconciliation import get_random_n_genes, random_filogeny, random_reconciliation
    from revolutionhtl.nxTree import induced_leafs
    from revolutionhtl.nhx_tools import read_nhx, get_nhx
    import pandas as pd
    from tqdm import tqdm
    import random as py_random
    import numpy.random as np_random

    py_random.seed(args.seed)
    np_random.seed(args.seed)

    # Species tree
    #-------------
    create_sTree= args.species_tree.isdigit()
    if create_sTree:
        args.species_tree= int(args.species_tree)
        Ts, species= random_filogeny(args.species_tree)
    else:
        with open(args.species_tree) as F:
            nhx= F.read().replace('\n','').strip()
        Ts= read_nhx(nhx)
        Ts.root= 1
        Ts.planted_root= 0
    species= induced_leafs(Ts, Ts.root)
    Ms= _compute_S_matrix(Ts, 'label')

    # Reconciliations
    #----------------
    if args.mode=='pairs':
        df_recons= []
        for i in tqdm(range(args.n_recons), total= args.n_recons):
            genes, sigma= get_random_n_genes(species, args.n_genes)
            Tg_i, mu_i= random_reconciliation(genes, Ts, sigma, Ms,
                                              p_speciation=args.ps,
                                              p0_cherry= args.p0,
                                              a_cherry=args.a,
                                              )
            Tg_j, mu_j= random_reconciliation(genes, Ts, sigma, Ms,
                                              p_speciation=args.ps,
                                              p0_cherry= args.p0,
                                              a_cherry=args.a,
                                              )
            df_recons+= [[Tg_i, Tg_j, mu_i, mu_j]]
        df_recons= pd.DataFrame(df_recons, columns= ['tree_i', 'tree_j', 'mu_i', 'mu_j'])
        df_recons.tree_i= df_recons.tree_i.apply(lambda T: get_nhx(T, name_attr= 'label', root=T.root))
        df_recons.tree_j= df_recons.tree_j.apply(lambda T: get_nhx(T, name_attr= 'label', root=T.root))
        df_recons.mu_i= df_recons.mu_i.apply(txt_map)
        df_recons.mu_j= df_recons.mu_j.apply(txt_map)

    elif args.mode=='list':
        genes, sigma= get_random_n_genes(species, args.n_genes)
        df_recons= []
        for i in tqdm(range(args.n_recons), total= args.n_recons):
            Tg, mu= random_reconciliation(genes, Ts, sigma, Ms,
                                          p_speciation=args.ps,
                                          p0_cherry= args.p0,
                                          a_cherry=args.a,
                                         )
            df_recons+= [[i, Tg, mu]]
        df_recons= pd.DataFrame(df_recons, columns= ['id', 'tree', 'mu'])
        df_recons.tree= df_recons.tree.apply(lambda T: get_nhx(T, name_attr= 'label', root=T.root))
        df_recons.mu= df_recons.mu.apply(txt_map)

    ################
    # Save results #
    ################
    print('Writting output file...')

    if create_sTree:
        Ts_nhx= get_nhx(Ts, name_attr= 'label', root=Ts.root)
        opath= f"{args.output_prefix}species_tree.{args.mode}.nhx"
        with open(opath, 'w') as F:
            F.write(Ts_nhx+'\n')
        print(f"Written to {opath}")

    opath= f"{args.output_prefix}random_reconciliations.{args.mode}.tsv"
    df_recons.to_csv(opath, sep='\t', index= False)
    print(f"Written to {opath}")

    print("\nPLR reconciliations were generated without any problem")
    print("------------------------------------------------------\n")
