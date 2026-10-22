---
layout: post
title: "Privacy-preserving in-context learning: synthetic demonstrations and privacy budgets"
date: 2026-09-08 09:00:00 -0600
display_order: 2
author: Bishnu Bhusal
description: "How clipped logits, public context, and private token sampling can produce reusable ICL demonstrations, with careful accounting for privacy boundaries."
tags: [differential-privacy, language-models, in-context-learning]
categories: [research]
related_papers: [bhusal2026aaai]
related_posts: false
sitemap: true
og_image: /assets/img/research/private-icl.png
og_image_alt: "Privacy-preserving in-context learning: synthetic demonstrations and privacy budgets — Bishnu Bhusal"
twitter_card: summary_large_image
permalink: /blog/2026/privacy-preserving-in-context-learning/
---

In-context learning gives a language model examples inside a prompt, allowing it to perform a task without updating its weights. When those examples contain private records, the prompt becomes part of the privacy problem. A model can repeat sensitive phrases, and simply asking it to paraphrase does not provide a mathematical privacy guarantee.

Our AAAI 2026 paper, [*Privacy Preserving In-Context-Learning Framework for Large Language Models*]({{ '/publications/bhusal2026aaai/' | relative_url }}), studies a different workflow: generate synthetic demonstrations through a differentially private mechanism, then reuse those demonstrations for downstream inference. This tutorial explains the mechanism and the boundary of its guarantee. The [paper PDF]({{ '/assets/pdf/aaai26.pdf' | relative_url }}) and [research code](https://github.com/bhusalb/privacy-preserving-icl) provide the full method.

## What is being protected?

Differential privacy bounds how much an output distribution can change when one protected record changes. The paper uses add/remove adjacency: two datasets are neighbors when one contains one additional prompt record. A mechanism A is (epsilon, delta)-differentially private if, for every neighboring pair and every output event S,

$$
\Pr[A(D)\in S]\leq e^{\varepsilon}\Pr[A(D')\in S]+\delta.
$$

The guarantee concerns distributions, including unlikely outputs. It does not promise that sensitive-looking words can never appear. Delta is an additive allowance in this inequality; it should not be interpreted as the probability that a particular person's record will be exposed. For the formal definition and post-processing property, see Chapter 2 of Dwork and Roth's [_The Algorithmic Foundations of Differential Privacy_](https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf).

The protected unit matters. If one person contributes many prompt records, a record-level guarantee is not automatically the same as a user-level guarantee. Deployment requires choosing the unit of protection before calibrating the mechanism.

## How private demonstrations are generated

The paper's generator consults several private prompts separately. At each decoding step, the language model produces a vector of logits for each prompt, conditioned on the synthetic prefix generated so far. A logit is a score for a possible next token, before conversion into probabilities.

The algorithm recenters and clips each logit vector, then averages the clipped private vectors. Bounding each vector's coordinates controls the influence of one private prompt. Recentering and clipping have different effects: a uniform shift leaves softmax probabilities unchanged, while clipping can change them.

A second branch computes clipped logits using a public prompt and the same synthetic prefix. The algorithm averages the public vector with the private aggregate, then samples a token using temperature-scaled softmax. The paper analyzes this sampling through the exponential mechanism. It does not implement this step by adding Gaussian noise to logits.

The sampled token extends the prefix, and generation continues until an end-of-sequence token or a specified maximum length. The resulting synthetic examples become demonstrations for downstream ICL. No fine-tuning of the underlying language model is required by this workflow.

Public blending is useful because a language model's public context can support task-relevant tokens without another direct consultation of private records. However, blending an unprotected private vector with a public vector does not, by itself, establish privacy. The guarantee depends on the sensitivity bound and randomized sampling together.

## Where composition enters

Every new token can depend on the private prompts. Privacy accounting must therefore cover the whole sequence, including its adaptive dependence on earlier tokens.

A conservative calculation uses basic composition, developed alongside stronger composition results in Chapter 3 of [Dwork and Roth](https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf). If each of T token mechanisms is epsilon-zero DP, with that guarantee holding conditional on every prior transcript, releasing the sequence is at most T times epsilon-zero DP. For example, 40 steps with a per-step budget of 0.02 give an overall bound of 0.8. These numbers illustrate composition; they are not settings or results from the paper.

More refined composition can improve the bound by allowing a nonzero delta. Any implementation must retain the terms and assumptions of the chosen accounting theorem. A useful operating rule is to set a maximum number of private token-generation steps before generation begins. Generating several synthetic examples from the same records also requires accounting across those examples, not just within each one.

Reusing a fixed, privately generated demonstration set is different. If subsequent inference uses only that release and information independent of the protected records, differential privacy's post-processing property adds no privacy cost for those records. Creating a fresh demonstration set by consulting the records again is a new private computation.

## The public branch and the trust boundary

The public branch can depend on the already generated private transcript. For analysis, one fixes that transcript and asks whether the branch makes any additional access to the protected dataset. A public prompt chosen from raw private records, or a model separately fine-tuned on those records without accounting, requires additional analysis.

The mechanism protects what is released through its analyzed output interface. The machine computing raw private logits still sees private prompts. Sending those prompts to a remote inference provider exposes them to that provider unless the deployment establishes a separate protection. Output DP does not make the raw prompts invisible to the service running inference.

Similarly, downstream queries may themselves contain sensitive information. The guarantee for the demonstration records does not automatically cover those queries. Logging raw prompts or intermediate unprotected logits also creates an output channel outside the intended release.

## What the experiments establish

The paper evaluates synthetic demonstrations on AGNews, DBPedia, and TREC classification, plus MIT-G and MIT-D extraction tasks. Its main experiments use Gemma 1.1 2B IT and access to full token logits. At epsilon equal to 1, Table 1 reports better accuracy than the two Gemma-based baselines on three of the five tasks; performance is not uniformly best across all tasks.

These results support studying private prediction as a way to obtain useful demonstrations. They do not establish that arbitrary models, prompts, or application domains will have the same utility. An API exposing only generated text or a few token probabilities may also lack the interface required by the described method.

## When to cite this work

Cite the [AAAI paper]({{ '/publications/bhusal2026aaai/' | relative_url }}) when discussing private synthetic demonstrations for ICL, clipped logit aggregation with public-context blending, or reproducing and comparing this framework. Use the [published DOI](https://doi.org/10.1609/aaai.v40i42.40838) for the article and the [repository](https://github.com/bhusalb/privacy-preserving-icl) for implementation details. General statements about differential privacy or composition should also cite their foundational sources.
