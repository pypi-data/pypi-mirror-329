# PARLE: Path Analysis, Reconciliation, and Label Evaluation

This tool computes the path-label reconciliation (PLR) dissimilarity measure. ([see abstract](https://gitlab.com/jarr.tecn/recondist)).

**Reference:** López Sánchez A., Ramírez-Rafael J. A., Flores Lamas A., Hernandez-Rosales M., Lafond M. (2024) **The Path-Label Reconciliation (PLR) Dissimilarity
Measure for Gene Trees** (currently under review at the [WABI 2024 conference](https://algo-conference.org/2024/wabi/)).

# Installation

```bash
pip install parle
```

# Synopsis of the tool

This code is a command-line tool designed to generate and compare reconciled gene trees with a given species tree, accounting for evolutionary events. It uses a proposed semi-metric *PLR* to quantify differences between reconciled gene trees, considering discrepancies in tree topology, gene-species mapping, and speciation/duplication events.

This tool supports benchmarking and validation by simulating reconciliations and comparing results with metrics like *LRF* and *ELRF*. The tool aims to enhance phylogenetic reconciliation by providing a refined and efficient method for comparing reconciled gene trees.

The tool can be used with the following syntax:

```bash
# Compute disimilarity
python -m parle gene_trees species_tree <optional arguments>

# Compute distance
python -m parle.simulate_reconciliations species_tree n_genes n_recons <optional arguments>


```

For detailed usage information, you can access the help documentation of the modules:

```bash
python -m parle -h
python -m parle.simulate -h
```

# Tutorial

We will see how to generate and analyze datasets for 10 species, maximum 2 gene per species, and 20 gene trees/pairs of gene trees. These numbers can be modified.

The species tree can be simulated by PARLE or can be inputed as a .nhx file.

## To Generate Data

Generate a list of reconciliations with the same species tree and set of genes for all the reconciliations:

```bash
python -m parle.simulate 10 2 20
```

Output files: `plr.species_tree.list.nhx`, `plr.random_reconciliations.list.tsv`

---

Generate pairs of reconciliations with the same species tree for all the reconciliations and pair-specific sets of genes:

```bash
python -m parle.simulate 10 2 20 -m pairs
```

Output files: `plr.species_tree.pairs.nhx`, `plr.random_reconciliations.pairs.tsv`.

---

To use an external species tree use the name of the file instead of `5`, an example, if you have a file `species_tree.nhx` with the content `((((((16,17)15,14)7,6)5,((10,11)9,8)4)3,((18,19)13,12)2)1)0;`, then you can use the commands:

```bash
python -m parle.simulate species_tree.nhx 1 10
python -m parle.simulate species_tree.nhx 1 10 -m pairs
```

## To Compute Distances

Compute distances of pairs of trees sorted by rows:

```bash
python -m parle plr.random_reconciliations.list.tsv plr.species_tree.list.nhx
```

Compute distances for all possible pairs of gene trees in a list:

```bash
python -m parle plr.random_reconciliations.list.tsv plr.species_tree.list.nhx -m all_vs_all
```

## Visualization

- For gene tree visualization we recomend [itol](itol.embl.de/).
- For trees reconciliation we recommend [REvolutionH-tl](pypi.org/project/revolutionhtl/).

# Additional Information

- The tool uses the PLR metric, which is designed to compare reconciled gene trees by taking into account all three components of reconciliations (tree topology, gene-species map, and event labeling) as well as duplication clusters.

- The metric is linear-time computable, making it suitable for large datasets.
- For more detailed documentation and examples, please refer to the project documentation within the repository.