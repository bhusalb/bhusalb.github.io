---
layout: post
title: "Verifying differential privacy: a worked example and three routes to automation"
date: 2026-10-22 09:00:00 -0600
author: Bishnu Bhusal
description: "Compute an exact finite-output privacy violation in Python, then connect the calculation to DiPAut, DipApprox, and verification with integrals."
tags: [differential-privacy, formal-verification, python]
categories: [research]
related_papers: [chadha2023ccs, bhusal2025ccs, rivera2025oopsla]
related_posts: false
sitemap: true
og_image: /assets/img/research/verifying-dp.png
og_image_alt: "Verifying differential privacy: a worked example and three routes to automation — Bishnu Bhusal"
twitter_card: summary_large_image
permalink: /blog/2026/verifying-differential-privacy/
---

Adding noise is one ingredient of a private algorithm. Verifying differential privacy means establishing that the complete program satisfies a probability inequality for every neighboring input pair and every observable output event. Branches, repeated comparisons, and reused randomness make that a program-analysis problem.

This tutorial starts with an exact calculation small enough to inspect by hand, then explains the scopes of three research directions: [DiPAut]({{ '/publications/chadha2023ccs/' | relative_url }}), [DipApprox]({{ '/publications/bhusal2025ccs/' | relative_url }}), and [∫dReal]({{ '/publications/rivera2025oopsla/' | relative_url }}). The example is educational code, not an implementation of these tools.

## Checking all output events without enumerating them

Fix neighboring inputs D and D-prime. Let p(y) and q(y) be their output probabilities on a finite output space. Starting from the differential privacy definition in Chapter 2 of Dwork and Roth's [_The Algorithmic Foundations of Differential Privacy_](https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf), the largest directed privacy gap for a fixed epsilon is

$$
\delta_{p\to q}(\varepsilon)
=\max_S\sum_{y\in S}\bigl(p(y)-e^\varepsilon q(y)\bigr)
=\sum_y\max\{p(y)-e^\varepsilon q(y),0\}.
$$

Why does the last expression work? Including an output with a positive contribution increases the gap. Including one with a negative contribution decreases it. The maximizing event therefore contains all outputs whose contributions are positive. Zero contributions may be included or omitted.

This calculation is sometimes called a hockey-stick divergence. For symmetric adjacency, both directions must be checked. The minimum delta needed for this pair is the larger of the p-to-q and q-to-p gaps. A mechanism-wide guarantee then takes the worst case over all neighboring pairs.

## A three-output example

Suppose the output space is {a, b, c}, and epsilon is log(2), so that exp(epsilon) is exactly 2.

| Output | p(y) | q(y) | p(y) − 2q(y) | q(y) − 2p(y) |
| :----- | ---: | ---: | -----------: | -----------: |
| a      | 0.45 | 0.20 |         0.05 |        −0.70 |
| b      | 0.35 | 0.15 |         0.05 |        −0.55 |
| c      | 0.20 | 0.65 |        −1.10 |         0.25 |

In the forward direction, the maximizing event is {a, b}. Its gap is 0.80 − 2 × 0.35 = 0.10. Checking each singleton against delta = 0.05 would miss this combined event: both a and b contribute positive mass.

In the reverse direction, the maximizing event is {c}. Its gap is 0.65 − 2 × 0.20 = 0.25. Consequently, delta = 0.10 is insufficient for symmetric adjacency, even though it passes the forward calculation. For this particular pair, the minimum delta is 0.25.

These intentionally large deltas make the arithmetic visible. They are not recommended deployment parameters. Nor does checking this pair establish a guarantee for a program with other neighboring inputs.

## Run the exact calculation

Download [finite_output_privacy.py]({{ '/assets/code/finite_output_privacy.py' | relative_url }}) and run:

```sh
python3 finite_output_privacy.py
```

The script uses Python's standard-library `Fraction` type, keeping the probabilities and likelihood factor exact. It also independently enumerates all eight output events for this small example to check the maximizing-event calculation. Its output includes:

```text
P -> Q: delta = 1/10; witness = ('a', 'b')
Q -> P: delta = 1/4; witness = ('c',)
Both directions: minimum delta = 1/4
delta = 1/10: passes = False
delta = 1/4: passes = True
```

Using exp(epsilon) = 2 avoids a floating-point approximation of exp(log(2)). For general real epsilon or probabilities obtained from numerical integration, deciding a nearly tight inequality requires explicit numerical error bounds.

## Where the probabilities come from

The toy example supplies its probability table. A verifier must derive that table, or an equivalent characterization, from program semantics. Repeatedly running a program and counting outputs gives estimates; rare outputs and small differences can remain undetected.

Continuous sampling introduces another difficulty. A program can draw Gaussian noise and still have a finite output alphabet, such as a Boolean threshold decision. The probability of each output is then an integral over the random draws leading to it. Multiple branches and dependent thresholds can produce nested integrals. This is where the following approaches address different parts of the problem.

## Three research directions and their scope

**DiPAut: online algorithms with state.** Our [CCS 2023 paper]({{ '/publications/chadha2023ccs/' | relative_url }}) studies a specified class of DiP automata with multiple real-valued storage variables. It characterizes when an automaton is D-epsilon DP for some constant D and all positive epsilon, proves the decision problem PSPACE-complete, and computes a suitable D in the private case. This concerns the defined automaton model, not arbitrary programs. The [implementation](https://github.com/bhusalb/DiPAut) and [archived artifact](https://doi.org/10.5281/zenodo.8332275) support further exploration.

**DipApprox: programs using Gaussian distributions.** Our [CCS 2025 paper]({{ '/publications/bhusal2025ccs/' | relative_url }}) treats the DiPGauss language: loop-free programs with finite input and output domains and supported continuous sampling, including Gaussian and Laplace distributions. It computes probability enclosures through integral approximation and tail bounds. The implementation uses FLINT for rigorous arithmetic. The paper's “almost decidable” result excludes a finite set of delta values for a fixed program, parameters, and adjacency relation; it is not a claim that the verifier always terminates. See the [PDF]({{ '/assets/pdf/ccs25.pdf' | relative_url }}) and [code](https://github.com/bhusalb/approximate-dp).

**∫dReal: constraints containing integrals.** Our [OOPSLA 2025 paper]({{ '/publications/rivera2025oopsla/' | relative_url }}) extends delta-decision procedures to formulas involving integrals of user-specified functions. Its evaluations include privacy, utility, fairness, and parameter synthesis. Here, the delta in “delta-satisfiability” describes a logical relaxation; it is conceptually distinct from the additive delta in differential privacy. The [published article](https://doi.org/10.1145/3720446) defines the supported formulas and procedure.

## When to cite this work

Cite DiPAut for its automaton model, characterization, or verification algorithm; DipApprox for probability approximation and verification of the supported Gaussian-sampling programs; and ∫dReal for reasoning about integral constraints and its applications. Select the paper matching the claim or method you use. This tutorial's rational example is a derivation from the DP definition and does not substitute for those papers' theorems or artifacts.
