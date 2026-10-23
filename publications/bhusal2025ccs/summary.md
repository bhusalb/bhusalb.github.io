# Approximate Algorithms for Verifying Differential Privacy with Gaussian Distributions

Publication summary and citation record; follow the source links for the original work.

- Authors: Bishnu Bhusal; Rohit Chadha; A. Prasad Sistla; Mahesh Viswanathan
- Year: 2025
- Type: Conference paper
- Publication status: published
- Paper page: https://bishnubhusal.com.np/publications/bhusal2025ccs/
- Scholarly identifier: https://doi.org/10.1145/3719027.3765043
- Venue or repository: Proceedings of the 2025 ACM SIGSAC Conference on Computer and Communications Security
- DOI: 10.1145/3719027.3765043
- arXiv: https://arxiv.org/abs/2509.08804
- Topics: Differential privacy; Formal verification; Gaussian mechanisms; Numerical integration; DipApprox

## Source links

- [Full paper (HTML)](<https://arxiv.org/html/2509.08804>)
- [Read PDF](<https://bishnubhusal.com.np/assets/pdf/ccs25.pdf>)
- [Publication source](<https://doi.org/10.1145/3719027.3765043>)
- [Code and resources](<https://github.com/bhusalb/approximate-dp>)

## Contribution summary

Introduces DipApprox for verifying differential privacy of loop-free probabilistic programs that use Gaussian and other discrete or continuous distributions. It combines numerical integration and tail bounds to approximate probabilities to arbitrary precision, with an almost-decidability result for (ε, δ)-privacy: all but a finite set of δ values are decidable under the paper's assumptions.

## When to read this work

Read this when a privacy mechanism uses Gaussian noise or requires reasoning about both discrete and continuous random choices. The Sparse Vector and Noisy Max evaluations provide concrete verification examples.

## Abstract

The verification of differential privacy algorithms that employ Gaussian distributions is little understood. This paper tackles the challenge of verifying such programs by introducing a novel approach to approximating probability distributions of loop-free programs that sample from both discrete and continuous distributions with computable probability density functions, including Gaussian and Laplace. We establish that verifying (epsilon, delta)-differential privacy for these programs is almost decidable, meaning the problem is decidable for all values of delta except those in a finite set. Our verification algorithm is based on computing probabilities to any desired precision by combining integral approximations, and tail probability bounds. The proposed methods are implemented in the tool, DipApprox, using the FLINT library for high-precision integral computations, and incorporate optimizations to enhance scalability. We validate DipApprox on fundamental privacy-preserving algorithms, such as Gaussian variants of the Sparse Vector Technique and Noisy Max, demonstrating its effectiveness in both confirming privacy guarantees and detecting violations.

## Questions about this work

### Which programs can DipApprox verify?

DipApprox targets loop-free DiPGauss programs with finite input and output domains, including mechanisms that sample from Gaussian and Laplace distributions. The paper's implementation currently supports comparisons among sampled values.

Source: [Section 7 — Implementation and Evaluation, footnote 8](<https://arxiv.org/html/2509.08804#S7>)

### What does almost decidable mean for differential privacy?

For a fixed program, positive rational program parameter and privacy budget, and adjacency relation, privacy verification is decidable for every δ in [0, 1] except a finite set of critical values. The result does not promise a terminating decision at those exceptional values.

Source: [Section 6.1 — Theorem 4](<https://arxiv.org/html/2509.08804#S6.SS1>)

### Does passing one adjacent input pair prove the whole program private?

A successful pair check establishes the privacy inequality for that pair. The full verification algorithm must confirm every pair in the specified adjacency relation. A violating pair refutes privacy; an Unknown result means the current probability bounds are insufficient to decide.

Source: [Section 5 — Verifying Differential Privacy](<https://arxiv.org/html/2509.08804#S5>)

## Tutorials and reading guides

- [DipApprox: verifying differential privacy with Gaussian noise](<https://bishnubhusal.com.np/blog/2026/dipapprox-gaussian-differential-privacy/>) — Inside our CCS 2025 paper: how DipApprox uses certified integration, Gaussian tail bounds, and probability intervals to prove or refute differential privacy.

## Cite this work

[Download BibTeX](<https://bishnubhusal.com.np/publications/bhusal2025ccs/cite.bib>) · [Download RIS](<https://bishnubhusal.com.np/publications/bhusal2025ccs/cite.ris>)

```bibtex
@inproceedings{bhusal2025ccs,
  title = {Approximate Algorithms for Verifying Differential Privacy with Gaussian Distributions},
  author = {Bhusal, Bishnu and Chadha, Rohit and Sistla, A. Prasad and Viswanathan, Mahesh},
  booktitle = {Proceedings of the 2025 ACM SIGSAC Conference on Computer and Communications Security},
  series = {CCS '25},
  pages = {1439--1453},
  year = {2025},
  month = oct,
  publisher = {Association for Computing Machinery},
  doi = {10.1145/3719027.3765043},
  url = {https://doi.org/10.1145/3719027.3765043},
  eprint = {2509.08804},
  archiveprefix = {arXiv},
  keywords = {Differential Privacy, Verification, Gaussian Distribution, Tail Bounds, Approximation Algorithms}
}
```
