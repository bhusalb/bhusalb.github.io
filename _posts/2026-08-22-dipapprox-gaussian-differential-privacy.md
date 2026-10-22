---
layout: post
title: "DipApprox: verifying differential privacy with Gaussian noise"
date: 2026-08-22 10:00:00 -0600
display_order: 3
author: Bishnu Bhusal
description: "Inside our CCS 2025 paper: how DipApprox uses certified integration, Gaussian tail bounds, and probability intervals to prove or refute differential privacy."
tags: [differential-privacy, formal-verification, gaussian-mechanisms]
categories: [research]
related_papers: [bhusal2025ccs]
related_posts: false
sitemap: true
og_image: /assets/img/research/dipapprox-ccs25.png
og_image_alt: "DipApprox: verifying differential privacy with Gaussian noise — inside our ACM CCS 2025 paper"
twitter_card: summary_large_image
permalink: /blog/2026/dipapprox-gaussian-differential-privacy/
---

A program can add Gaussian noise and still fail its intended differential privacy guarantee. The answer depends on what the program releases, how its branches interact, and how it reuses random values. Establishing privacy therefore requires reasoning about the complete computation.

In our CCS 2025 paper, [*Approximate Algorithms for Verifying Differential Privacy with Gaussian Distributions*]({{ '/publications/bhusal2025ccs/' | relative_url }}), we develop a way to automate that reasoning for a defined class of programs. Our tool, **DipApprox** (styled **DiPApprox** in the paper), computes probability intervals with certified error bounds and uses them to prove privacy, find a violation, or report that the current precision is insufficient.

I worked on this paper with **Rohit Chadha, A. Prasad Sistla, and Mahesh Viswanathan**. This visual walkthrough explains the method, its limits, and selected results. [Read the paper]({{ '/assets/pdf/ccs25.pdf' | relative_url }}), [browse the code](https://github.com/bhusalb/approximate-dp), or [download the citation]({{ '/publications/bhusal2025ccs/cite.bib' | relative_url }}).

## From a randomized program to a privacy answer

Consider a program that samples one noisy threshold and compares several independently perturbed queries against it. Even though the noise draws are independent, the comparison outcomes share the threshold. Computing the probability of a particular output sequence requires accounting for that shared random value.

This is the challenge behind examples such as Gaussian variants of the **Sparse Vector Technique (SVT)**. SVT answers threshold questions while limiting how many positive answers it releases. The program's output is discrete, but the random choices leading to it range over the real line.

DipApprox follows the program's execution paths, expresses their probabilities as integrals, and encloses those probabilities in intervals. It then checks the differential privacy inequalities using the bounds.

<figure>
  <img src="{{ '/assets/img/research/dipapprox-verification-pipeline.svg' | relative_url }}" width="640" height="820" class="img-fluid" loading="lazy" data-zoomable alt="DipApprox pipeline: a program and finite inputs produce execution paths, bounded integrals and tail bounds, probability intervals, and privacy-gap bounds, ending in DP, Not_DP, or Unknown.">
  <figcaption><strong>Figure 1.</strong> The verification pipeline. Both integration error and probability in the tails remain accounted for in the final bounds.</figcaption>
</figure>

The formal program class, **DiPGauss**, has finite input and output domains and is loop-free. Fixed bounded loops can be unrolled. Its presented syntax includes Gaussian and Laplace sampling; the underlying probability-approximation argument extends to suitable distributions with computable densities and finite means and variances. The prototype has additional restrictions, including support for comparisons among sampled values. These assumptions define what a successful check establishes.

## Why a Gaussian tail cannot simply be ignored

For an elementary example, suppose a program releases whether a query value plus Gaussian noise exceeds a fixed threshold:

$$
b=\mathbf{1}\{q+Z>T\},\qquad Z\sim\mathcal{N}(0,\sigma^2).
$$

The probability of releasing 1 is an integral of the Gaussian density from $$T-q$$ to infinity. More complicated programs introduce multiple random values and branch conditions, producing nested integrals. A numerical estimate alone is insufficient when a privacy inequality is close to its boundary.

Our approach separates a bounded integration region from its tails. It computes the bounded-region contribution with an error bound, then adds a bound on the probability outside that region. For multiple samples, the tail contribution accounts for the event that at least one draw falls outside its allowed window.

<figure>
  <img src="{{ '/assets/img/research/dipapprox-gaussian-tails.svg' | relative_url }}" width="640" height="490" class="img-fluid" loading="lazy" data-zoomable alt="A standard Gaussian split at minus two and plus two standard deviations: about 95.45 percent of its mass is in the center, and 4.55 percent is in the two tails combined. The tail mass must be bounded, not discarded.">
  <figcaption><strong>Figure 2.</strong> An illustrative integration window, chosen to make the tails visible. The paper's experiments use a wider Gaussian window of four standard deviations, not the two-standard-deviation window shown here. Tail truncation error is a numerical quantity, separate from the privacy parameter δ.</figcaption>
</figure>

The theory uses tail inequalities, including Chernoff and Chebyshev bounds. The implementation uses **FLINT** for rigorous arithmetic and integral computation. A computed value is represented by a ball enclosure—a midpoint together with an error radius—rather than an unqualified floating-point estimate.

The resulting probability interval contains the true probability. The paper's approximation interface can request an interval of width at most $$2^{-\rho}$$, where increasing $$\rho$$ asks for finer precision. Numerical approximation therefore does not weaken a certified privacy conclusion: uncertainty remains explicit in the bounds.

## Checking privacy without enumerating every output event

Differential privacy compares the program's output distributions on neighboring inputs. Let $$p_u(o)$$ denote the probability of output $$o$$ on input $$u$$. For a fixed privacy budget $$\varepsilon_{\mathrm{prv}}$$, define the directed privacy gap

$$
\Delta(u,u')=
\sum_o\max\left\{
p_u(o)-e^{\varepsilon_{\mathrm{prv}}}p_{u'}(o),\;0
\right\}.
$$

The program satisfies $$(\varepsilon_{\mathrm{prv}},\delta)$$-differential privacy when this gap is at most $$\delta$$ for every required ordered adjacent pair. With symmetric adjacency, both directions matter.

Why sum only positive terms? The output event that maximizes the privacy violation includes exactly the outputs with positive contributions. This replaces checking every subset of the finite output space with a sum over individual outputs. Lemma 2 in the paper establishes the equivalence.

DipApprox computes lower and upper bounds on this gap. For each pair, an upper bound at or below $$\delta$$ proves the inequality; a lower bound above $$\delta$$ proves a violation. An interval crossing the boundary is inconclusive at the current precision. Equivalently, the largest gap over all required pairs must be at most $$\delta$$; the figure illustrates bounds on that maximum.

<figure>
  <img src="{{ '/assets/img/research/dipapprox-privacy-intervals.svg' | relative_url }}" width="640" height="500" class="img-fluid" loading="lazy" data-zoomable alt="Illustrative bounds on the maximum privacy gap against delta equal to 0.10: 0.04 to 0.08 certifies privacy, 0.12 to 0.16 certifies a violation, and 0.08 to 0.13 is inconclusive.">
  <figcaption><strong>Figure 3.</strong> Three possible relationships between a certified interval and the privacy boundary. The numbers illustrate the decision rule; they are not experimental measurements or recommended privacy settings. A program-wide DP answer requires checking every pair in the specified adjacency relation; one violating pair is enough for Not_DP.</figcaption>
</figure>

The paper distinguishes the mechanism's noise-controlling parameter $$\varepsilon$$ from its claimed privacy budget $$\varepsilon_{\mathrm{prv}}$$. They need not be equal. A verification run fixes both, together with $$\delta$$ and the adjacency relation.

## What “almost decidable” means

The qualifier concerns termination at exact boundaries. For a fixed program, noise parameter, privacy budget, and adjacency relation, the theory identifies a finite set of critical $$\delta$$ values. Away from that set, sufficiently precise probability bounds can decide the privacy question. At a critical value, continued refinement may remain inconclusive.

The answers **DP** and **Not_DP** are sound under the model's assumptions. **Unknown** preserves that soundness when the current bounds cannot resolve the inequality. It is neither a privacy certificate nor evidence of a violation. This is also distinct from _approximate differential privacy_, where $$\delta$$ appears in the guarantee itself.

## Making the integrals practical

Nested integration can dominate runtime. The paper uses a dependency graph of integration limits to identify opportunities to separate integrations and reduce nesting while preserving their values. For the studied SVT-Gauss expressions, this optimization limits maximum nesting depth to three, independently of the number of queries.

<figure>
  <img src="{{ '/assets/img/research/dipapprox-optimization.svg' | relative_url }}" width="640" height="620" class="img-fluid" loading="lazy" data-zoomable alt="Paper Table 2, SVT-Gauss with five queries and one selected adjacent pair: optimized integration took 7.9 seconds and reduced maximum nesting depth from six to three; unoptimized integration exceeded the 600-second timeout.">
  <figcaption><strong>Figure 4.</strong> A result from Table 2 of the paper: SVT-Gauss, N = 5, one selected adjacent pair, ε = 0.5, ε_prv = 1.24, and δ = 0.01. The optimized runtime averages three runs on a 1.4 GHz quad-core Intel Core i5 Mac with 8 GB RAM. The unoptimized result is a timeout, not a measured completion time of 600 seconds.</figcaption>
</figure>

The experiments also distinguish **checking one pair** from **verifying all pairs in a finite domain**. For SVT-Gauss with five queries, Table 1 reports 76.7 seconds for all pairs of binary input vectors under the experiment's adjacency relation. For 25 queries, one selected pair took 441.3 seconds, while the all-pair run exhausted memory. In this benchmark, every pair of vectors in $$\{0,1\}^N$$ is considered adjacent; the selected pair is the all-zero vector and the vector with only its final entry set to one.

The tool also detected violations in both Gaussian SVT leaky variants at the parameter settings reported in Table 1. These results demonstrate both proof and falsification on the benchmark programs. They also expose a practical limit: reducing integral depth does not remove the growth in the number of input combinations. The supported mathematical model is not a verification of arbitrary deployed Python or C++ implementations, including their floating-point sampling behavior.

## Explore the artifact

The [code repository](https://github.com/bhusalb/approximate-dp) contains the Python/C++ implementation, examples, and reproduction scripts. For the version associated with CCS 2025, use the [archived artifact on Zenodo](https://doi.org/10.5281/zenodo.16930793).

The repository documents this Docker workflow:

```sh
git clone https://github.com/bhusalb/approximate-dp.git
cd approximate-dp
docker build . -t dpapprox
docker run --rm -it dpapprox
```

Inside the container, start with `python3 src/main.py --help` to inspect the verification options. The documented benchmark entry points are `scripts/benchmark.py` and `scripts/benchmark_unoptimized.py`; `scripts/table_generator.py` generates Tables 1 and 2. Consult the [artifact README](https://github.com/bhusalb/approximate-dp/blob/master/README.md) for the current instructions and select the program, parameters, and input pairs deliberately when interpreting a result.

## Paper and citation

**Bishnu Bhusal, Rohit Chadha, A. Prasad Sistla, and Mahesh Viswanathan.** “Approximate Algorithms for Verifying Differential Privacy with Gaussian Distributions.” **ACM CCS 2025**, pp. 1439–1453. [DOI: 10.1145/3719027.3765043](https://doi.org/10.1145/3719027.3765043).

The [author-hosted extended paper]({{ '/assets/pdf/ccs25.pdf' | relative_url }}) contains the definitions, proofs, and experimental details used here. See Sections 5–6 for the decision procedure and probability approximation, and Section 7 and Tables 1–2 for the results. [Download BibTeX]({{ '/publications/bhusal2025ccs/cite.bib' | relative_url }}) or [RIS]({{ '/publications/bhusal2025ccs/cite.ris' | relative_url }}).

Cite this work when using its probability-approximation method, studying automated privacy verification for its supported Gaussian-sampling programs, or comparing against DipApprox. For foundational differential privacy definitions and composition, see Dwork and Roth's [_The Algorithmic Foundations of Differential Privacy_](https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf).
