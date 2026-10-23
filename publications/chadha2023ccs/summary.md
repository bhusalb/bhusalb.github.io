# Deciding Differential Privacy of Online Algorithms with Multiple Variables

Publication summary and citation record; follow the source links for the original work.

- Authors: Rohit Chadha; A. Prasad Sistla; Mahesh Viswanathan; Bishnu Bhusal
- Year: 2023
- Type: Conference paper
- Publication status: published
- Paper page: https://bishnubhusal.com.np/publications/chadha2023ccs/
- Scholarly identifier: https://doi.org/10.1145/3576915.3623170
- Venue or repository: Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security
- DOI: 10.1145/3576915.3623170
- arXiv: https://arxiv.org/abs/2309.06615
- Topics: Differential privacy; Formal verification; Online algorithms; DiP automata; Decision procedures

## Source links

- [Publication source](<https://doi.org/10.1145/3576915.3623170>)
- [Code and resources](<https://github.com/bhusalb/DiPAut>)

## Contribution summary

Extends DiP automata to online randomized algorithms with multiple real-valued storage variables. The paper characterizes when an automaton is Dε-differentially private for some D and every ε > 0, proves that deciding this property is PSPACE-complete, and implements an algorithm that also computes a suitable D.

## When to read this work

Read this when studying automated privacy verification for algorithms that process a stream of inputs, or when comparing the expressiveness and complexity of automata-based privacy analyses.

## Abstract

We consider the problem of checking the differential privacy of online randomized algorithms that process a stream of inputs and produce outputs corresponding to each input. This paper generalizes an automaton model called DiP automata to describe such algorithms by allowing multiple real-valued storage variables. A DiP automaton is a parametric automaton whose behavior depends on the privacy budget ε. An automaton A will be said to be differentially private if, for some D, the automaton is Dε-differentially private for all values of ε > 0. We identify a precise characterization of the class of all differentially private DiP automata. We show that the problem of determining if a given DiP automaton belongs to this class is PSPACE-complete. Our PSPACE algorithm also computes a value for D when the given automaton is differentially private. The algorithm has been implemented, and experiments demonstrating its effectiveness are presented.

## Cite this work

[Download BibTeX](<https://bishnubhusal.com.np/publications/chadha2023ccs/cite.bib>) · [Download RIS](<https://bishnubhusal.com.np/publications/chadha2023ccs/cite.ris>)

```bibtex
@inproceedings{chadha2023ccs,
  title = {Deciding Differential Privacy of Online Algorithms with Multiple Variables},
  author = {Chadha, Rohit and Sistla, A. Prasad and Viswanathan, Mahesh and Bhusal, Bishnu},
  booktitle = {Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security},
  series = {CCS '23},
  pages = {1761--1775},
  year = {2023},
  month = nov,
  publisher = {Association for Computing Machinery},
  address = {New York, NY, USA},
  isbn = {9798400700507},
  doi = {10.1145/3576915.3623170},
  url = {https://doi.org/10.1145/3576915.3623170},
  eprint = {2309.06615},
  archiveprefix = {arXiv},
  keywords = {automata, decision procedure, differential privacy, verification}
}
```
