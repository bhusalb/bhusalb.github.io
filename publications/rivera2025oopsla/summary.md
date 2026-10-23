# Checking δ-Satisfiability of Reals with Integrals

Publication summary and citation record; follow the source links for the original work.

- Authors: Cody Rivera; Bishnu Bhusal; Rohit Chadha; A. Prasad Sistla; Mahesh Viswanathan
- Year: 2025
- Type: Journal article
- Publication status: published
- Paper page: https://bishnubhusal.com.np/publications/rivera2025oopsla/
- Scholarly identifier: https://doi.org/10.1145/3720446
- Venue or repository: Proc. ACM Program. Lang.
- DOI: 10.1145/3720446
- Topics: Formal verification; δ-satisfiability; Numerical integration; Synthesis; ∫dReal

## Source links

- [Publication source](<https://doi.org/10.1145/3720446>)

## Contribution summary

Extends δ-decision procedures over the reals to constraints containing integrals of user-specified functions. The ∫dReal implementation builds on dReal and is evaluated on fairness, privacy, utility, and parameter-synthesis problems.

## When to read this work

Read this when a verification or synthesis task reduces to real-valued constraints involving probability integrals, including privacy-mechanism utility and algorithmic fairness.

## Abstract

Many synthesis and verification problems can be reduced to determining the truth of formulas over the real numbers. These formulas often involve constraints with integrals in them. To this end, we extend the framework of δ-decision procedures with techniques for handling integrals of user-specified real functions. We implement this decision procedure in the tool ∫dReal, which is built on top of dReal. We evaluate ∫dReal on a suite of problems that include formulas verifying the fairness of algorithms and the privacy and the utility of privacy mechanisms and formulas that synthesize parameters for the desired utility of privacy mechanisms. The performance of the tool in these experiments demonstrates the effectiveness of ∫dReal.

## Cite this work

[Download BibTeX](<https://bishnubhusal.com.np/publications/rivera2025oopsla/cite.bib>) · [Download RIS](<https://bishnubhusal.com.np/publications/rivera2025oopsla/cite.ris>)

```bibtex
@article{rivera2025oopsla,
  title = {Checking δ-Satisfiability of Reals with Integrals},
  author = {Rivera, Cody and Bhusal, Bishnu and Chadha, Rohit and Sistla, A. Prasad and Viswanathan, Mahesh},
  journal = {Proc. ACM Program. Lang.},
  volume = {9},
  number = {OOPSLA1},
  articleno = {105},
  pages = {704--729},
  year = {2025},
  month = apr,
  publisher = {Association for Computing Machinery},
  doi = {10.1145/3720446},
  url = {https://doi.org/10.1145/3720446},
  keywords = {integrals, synthesis, theory of reals, verification, δ-satisfiability}
}
```
