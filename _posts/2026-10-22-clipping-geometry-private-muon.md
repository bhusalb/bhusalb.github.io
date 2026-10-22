---
layout: post
title: "Why gradient clipping changes Muon's geometry: a two-dimensional example"
date: 2026-10-22 09:00:00 -0600
author: Bishnu Bhusal
description: "A runnable Python example shows how unequal per-example clipping rotates a matrix's polar factor, motivating the DP-Muon-IM preprint."
tags: [differential-privacy, optimization, language-models, python]
categories: [research]
related_papers: [bhusal2026dpmuon]
related_posts: false
sitemap: true
og_image: /assets/img/research/private-muon.png
og_image_alt: "Why gradient clipping changes Muon’s geometry: a two-dimensional example — Bishnu Bhusal"
twitter_card: summary_large_image
permalink: /blog/2026/clipping-geometry-private-muon/
---

Per-example gradient clipping changes more than an update's size. Although clipping multiplies each example's gradient by a nonnegative scalar, different examples generally receive different scalars. Their average can therefore point in a different direction or, for matrix-valued gradients, have different singular-vector geometry.

Our preprint [*Inner Momentum for Differentially Private Muon*]({{ '/publications/bhusal2026dpmuon/' | relative_url }}) investigates why this matters for Muon and proposes a history-based correction before clipping. This tutorial uses the preprint's abstract to describe its motivation and reported scope. The calculation below is an independent illustration, not a reproduction of its algorithm, theoretical bounds, or experiments. The source is available on [arXiv](https://arxiv.org/abs/2610.02738).

## Why a matrix optimizer notices clipping

A matrix A can be written using a singular value decomposition as U Sigma V-transpose. For a nonsingular square matrix, its orthogonal polar factor is Q = U V-transpose. This retains singular-vector information while replacing singular values by one. Muon's orthogonalization is motivated by an approximation to this polar factor.

Multiplying A by the same positive scalar changes its singular values but preserves Q. That invariance can make clipping seem harmless at first: if clipping just scales the update, why would the orthogonalized update change?

The missing distinction is the order of operations. Private training clips individual examples before averaging them. If their clipping multipliers differ, the clipped mean need not be a scalar multiple of the original mean. Orthogonalization can therefore see a different input geometry even before privacy noise is added.

## Two matrices are enough

Consider two illustrative per-example matrix gradients:

$$
G_1=\begin{pmatrix}4&0\\0&0\end{pmatrix},\qquad
G_2=\begin{pmatrix}0&1\\0&1\end{pmatrix}.
$$

Their arithmetic mean is

$$
A=\frac{G_1+G_2}{2}
=\begin{pmatrix}2&0.5\\0&0.5\end{pmatrix}.
$$

Clip each matrix to Frobenius norm at most 1. The Frobenius norm is the square root of the sum of squared entries. The clipping operation multiplies G by min(1, 1 / norm(G)), leaving a zero matrix unchanged.

The two norms are 4 and square-root-of-2, so the clipping multipliers are 0.25 and approximately 0.707107. After clipping each example and then averaging, the result is

$$
B=\begin{pmatrix}0.5&0.353553\ldots\\0&0.353553\ldots\end{pmatrix}.
$$

B is not a common rescaling of A. Its first column shrank more than its second because the examples contributing to those columns had different norms. This reweighting occurs before we add any noise or run any approximate orthogonalization routine.

## Compute the polar-factor rotation

For a real 2-by-2 matrix with entries a, b, c, d and positive determinant, its polar factor has a convenient closed form:

$$
Q=\frac{1}{\sqrt{(a+d)^2+(c-b)^2}}
\begin{pmatrix}a+d&b-c\\c-b&a+d\end{pmatrix}.
$$

Its rotation angle is atan2(c − b, a + d). Both means in this example have positive determinants, so the formula applies even though the individual example matrices are rank deficient.

| Matrix sent to orthogonalization | Polar-factor rotation |
| :------------------------------- | --------------------: |
| Original mean A                  |    −11.309932 degrees |
| Mean of clipped examples B       |    −22.500000 degrees |
| Common rescaling 0.25A           |    −11.309932 degrees |

The unequal clipping changes the polar rotation by about 11.19 degrees. Common positive rescaling leaves it unchanged. The Frobenius distance between the two polar factors is approximately 0.275762. These are deterministic properties of the chosen matrices, not measured training improvements.

Download [clipping_polar_geometry.py]({{ '/assets/code/clipping_polar_geometry.py' | relative_url }}) and run it with Python's standard library:

```sh
python3 clipping_polar_geometry.py
```

The script prints the clipping multipliers, both means, their rotations, and the common-rescaling control. It intentionally handles only the positive-determinant 2-by-2 case needed here. It is not a general SVD implementation or a private optimizer.

## The connection to inner momentum

The preprint proposes averaging each sampled example's Muon gradient over the current model and a short history of recent models before clipping. This places the temporal averaging inside the per-example computation. It differs from simply smoothing a batch update after clipping has already reweighted its contributors.

A useful algebraic view separates common scaling from the part that changes geometry. Write a clipped mean as the average of alpha-i times G-i, where alpha-i is an example's clipping multiplier. If alpha-bar and G-bar are their respective averages, then

$$
\frac1n\sum_i\alpha_iG_i
=\bar\alpha\bar G+
\frac1n\sum_i(\alpha_i-\bar\alpha)(G_i-\bar G).
$$

The first term is a common rescaling. The second is a covariance-like residual that captures the association between gradient structure and clipping multipliers. The abstract describes a distortion bound using such a residual. The identity alone does not prove that any particular temporal averaging scheme reduces it.

The abstract also states that a finite Newton–Schulz iteration preserves the input polar factor under specified spectral conditions. That statement needs those conditions; this example's exact closed form does not test a finite-iteration implementation.

## What the preprint reports

The abstract reports GPT-2 fine-tuning on E2E and DART at epsilon values 1, 2, 4, and 8. It states that DP-Muon-IM improves BLEU and ROUGE-L over DP-Muon in every seed-matched comparison in those experiments, and reports 2–4% lower pre-noise polar error in non-private diagnostics. These are the authors' reported results for the preprint's evaluation, not a guarantee for other models or datasets.

This illustrative calculation adds no privacy noise and performs no training. Clipping alone is insufficient to establish differential privacy. A private implementation must analyze the full mechanism, including its noise, sampling, history dependence, and privacy accounting.

## When to cite this work

Cite [*Inner Momentum for Differentially Private Muon*]({{ '/publications/bhusal2026dpmuon/' | relative_url }}) when discussing its proposed per-example history averaging, its analysis of clipping-induced polar distortion, or comparisons to DP-Muon-IM. Identify it as an arXiv preprint and consult the current version for the exact assumptions and implementation. The elementary matrix example here explains the motivation; it does not establish the proposed method's effectiveness.
