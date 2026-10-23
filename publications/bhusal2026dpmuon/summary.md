# Inner Momentum for Differentially Private Muon

Publication summary and citation record; follow the source links for the original work.

- Authors: Bishnu Bhusal; Minh Vu; Ben Southworth; Geigh Zollicoffer; Rohit Chadha; Manish Bhattarai
- Year: 2026
- Type: Preprint
- Publication status: preprint
- Paper page: https://bishnubhusal.com.np/publications/bhusal2026dpmuon/
- Scholarly identifier: https://arxiv.org/abs/2610.02738
- Venue or repository: arXiv preprint arXiv:2610.02738
- arXiv: https://arxiv.org/abs/2610.02738
- Topics: Differential privacy; Private optimization; Muon; Gradient clipping; Language-model fine-tuning

## Source links

- [Full paper (HTML)](<https://arxiv.org/html/2610.02738>)
- [Publication source](<https://arxiv.org/abs/2610.02738>)

## Contribution summary

Studies how unequal per-example clipping factors can distort the singular-vector geometry used by Muon. The proposed inner-momentum method averages each sampled example's gradients across the current and recent models before clipping. The preprint gives a distortion analysis and reports improved BLEU and ROUGE-L over DP-Muon in seed-matched private GPT-2 fine-tuning on E2E and DART at ε ∈ {1, 2, 4, 8}.

## When to read this work

Read this when studying differentially private optimizers, gradient-clipping geometry, or the interaction between Muon's orthogonalization and private language-model fine-tuning.

## Abstract

Differentially private training clips each per-example gradient before adding noise. This clipping is radial for each example, yet unequal clipping factors can distort the relative singular-vector geometry of their average. Muon is particularly exposed to this effect, since its update is an approximate polar factor UV^T that depends only on the singular vectors that clipping can shift. To curb this degradation, we propose averaging each sampled example’s Muon gradient over the current model and a short history of recent models before clipping. The clipped batch matrix then separates into a common rescaling and a covariance residual R between sampled gradients and clipping values, bounding the clipping-induced distortion directly. We further show that a finite Newton-Schulz iteration preserves the polar factor of its input under these spectral conditions, confirming that our correction survives orthogonalization. In private GPT-2 fine-tuning on E2E and DART at epsilon in 1, 2, 4, 8, DP-Muon-IM improves BLEU and ROUGE-L over DP-Muon in every seed-matched comparison, and non-private diagnostics show 2-4% lower pre-noise polar error.

## Questions about this work

### Does inner momentum require an additional privacy budget?

Under the paper's conditions, history averaging adds no private releases. The baseline per-run privacy accounting applies when the sampling rule, clipping radius, noise calibration, release denominator, and number of releases are unchanged. Theorem 4 uses add/remove adjacency and a valid Poisson-sampled Gaussian accountant, with a fixed public history length and decay.

Source: [Section 4.3 — Training procedure and Theorem 4](<https://arxiv.org/html/2610.02738#S4.SS3>)

### Where was DP-Muon-IM evaluated?

The preprint evaluates private GPT-2-small fine-tuning on E2E and DART at ε values 1, 2, 4, and 8. It reports higher BLEU and ROUGE-L than DP-Muon in all 24 seed-matched comparisons: two datasets, four privacy budgets, and three seeds.

Source: [Section 5.2 — Utility across privacy budgets](<https://arxiv.org/html/2610.02738#S5.SS2>)

### What is the computational cost of inner momentum?

The method stores recent pre-update model states and evaluates each sampled example's gradient at the current and selected past states. Per-step computation grows linearly with the maximum history length, and storing those model states adds memory cost.

Source: [Section 4.3 — Cost](<https://arxiv.org/html/2610.02738#S4.SS3>)

## Tutorials and reading guides

- [Why gradient clipping changes Muon's geometry: a two-dimensional example](<https://bishnubhusal.com.np/blog/2026/clipping-geometry-private-muon/>) — A runnable Python example shows how unequal per-example clipping rotates a matrix's polar factor, motivating the DP-Muon-IM preprint.

## Cite this work

[Download BibTeX](<https://bishnubhusal.com.np/publications/bhusal2026dpmuon/cite.bib>) · [Download RIS](<https://bishnubhusal.com.np/publications/bhusal2026dpmuon/cite.ris>)

```bibtex
@article{bhusal2026dpmuon,
  title = {Inner Momentum for Differentially Private Muon},
  author = {Bhusal, Bishnu and Vu, Minh and Southworth, Ben and Zollicoffer, Geigh and Chadha, Rohit and Bhattarai, Manish},
  journal = {arXiv preprint arXiv:2610.02738},
  year = {2026},
  month = oct,
  eprint = {2610.02738},
  archiveprefix = {arXiv},
  primaryclass = {cs.LG},
  url = {https://arxiv.org/abs/2610.02738}
}
```
