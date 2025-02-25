desc_def= """Computes PLR disimilarity measure between tree reconciliations.
[REFERENCE]

Input
-----
> species_tree
  A .txt file containing a species tree in nhx format.

  Example of species tree: '((A,B)X,(C,D)Y)Z;'
  Note that both leafs and inner nodes of the species tree have a label.
  In the example above the leafs are: A, B, C, D
  and the inner nodes are: X, Y, Z

> gene_trees
  A .tsv file containing gene trees and reconciliation maps.
  - If mode='pairs' (default) the file should contain the columns: tree_i, tree_j, mu_i, mu_j
  - If mode='all_vs_all' the file should contain the columns: tree, mu

  Example of gene tree: '(((a,b)x[event=S],c)y[event=S],d)z[event=D];'
  Note that both leafs and inner nodes of the gene tree have a label,
  furthermore, the inner nodes are associated with an evolutionary event.
  In the example above the leafs are: a, b, c, d
  and the inner nodes are: x, y, z.
  Inner nodes x and y are speciations, while inner node z is a duplication.
  Valid evolutionary events are: 'S' for 'speciation', 'D' for 'duplication'.

  Example of reconciliation map: 'a:A,b:B,c:C,d:D,x:X,y:Z,z:Z'
  This is a map from the nodes of the gene tree to the nodes of the species tree,
  it is comma separated, where the element 'a:A' means 'node a in the gene tree
  maps to node A in the species tree'.
  Te reconciliation map must satisfy the restrictions specified at [REFERENCE]

See extra parameters bellow.
For more examples go to [PYPI WEBSITE]

Output
------
A table containing the PLR disimilarity measure between the input reconciliations.
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
    txt= f"parle V{V_plr}"

    parser = argparse.ArgumentParser(prog= 'parle',
                                     description=f'{txt}\n{desc_def}',
                                     usage='python -m parle gene_trees species_tree <optional arguments>',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                    )

    parser.add_argument('gene_trees',
                        help= '[str] .tsv file containing gene trees and reconciliation maps.',
                        type= str,
                       )

    parser.add_argument('species_tree',
                        help= '[str] .txt file containing a species tree in nhx format.',
                        type= str,
                       )

    parser.add_argument('-a', '--alpha',
                        help= '[float | Default: 1/(number of species)] alpha parameter to balance linear-versus-quadratic components of PLR disimilarity measure.',
                        type= float,
                        default= None,
                       )


    parser.add_argument('-m', '--mode',
                        help= '[str | Default: pairs] mode for comparing reconciliations. Choices: pairs, all_vs_all',
                        type= str,
                        choices= ['pairs', 'all_vs_all'],
                        default= 'pairs',
                       )

    parser.add_argument('-o', '--output_prefix',
                        help= '[str | Default: plr.] Prefix for output files.',
                        type= str,
                        default= 'plr.',
                       )

    parser.add_argument('--break_down',
                        help= '[flag] Use to break down the computation of prl disimilarity.',
                        action= 'store_true',
                       )

    args= parser.parse_args()

    print(f'{hello}V{V_plr}\n\n')

    ###################
    # Read input data #
    ###################
    from revolutionhtl.nhx_tools import read_nhx
    print('Reading data...')

    # Species tree
    with open(args.species_tree) as F:
        nhx= F.read().replace('\n','').strip()
    Ts= read_nhx(nhx)

    # Gene trees
    if args.mode=='pairs':
        from .utils import load_df_rows
        df= load_df_rows(args.gene_trees)
    elif args.mode=='all_vs_all':
        from .utils import load_df_all_vs_all
        df= load_df_all_vs_all(args.gene_trees)

    #####################
    # Compute distances #
    #####################
    print('Computing PLR disimilarity...')
    if args.mode=='pairs':
        if args.break_down:
            from .utils import compute_plr_components_dataframe_rows as computedist
        else:
            from .utils import compute_plr_dataframe_rows as computedist
        df_dist= computedist(df, Ts, alpha= args.alpha)
    elif args.mode=='all_vs_all':
        from .utils import compute_plr_dataframe_all_vs_all
        df_dist= compute_plr_dataframe_all_vs_all(df, Ts, alpha= args.alpha)

    ################
    # Save results #
    ################
    print('Writting output file...')
    opath= f"{args.output_prefix}disimilarity.{args.mode}.tsv"
    df_dist.to_csv(opath, sep='\t', index= False)
    print(f"Written to {opath}")

    print("\nPLR disimilarity was computed without any problem")
    print("-------------------------------------------------\n")
