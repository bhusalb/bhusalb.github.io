---
layout: page
permalink: /research/
title: research
description: A guide to Bishnu Bhusal's work on automated differential privacy verification, private language models, and security, with papers and open-source tools.
nav: true
nav_order: 1
---

My research develops tools for reasoning about privacy and security, from formal guarantees for randomized programs to privacy-preserving language models. This guide connects practical research questions to the papers and software that address them.

## Find a starting point

| Your question                                                                             | Start here                                                                   |
| ----------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Can I automatically verify privacy for a streaming algorithm with multiple stored values? | [DiPAut and the CCS 2023 paper](/publications/chadha2023ccs/)                |
| How can I verify a program that samples Gaussian noise?                                   | [DipApprox, CCS 2025](/publications/bhusal2025ccs/)                          |
| How can a solver reason about constraints containing integrals?                           | [∫dReal, OOPSLA 2025](/publications/rivera2025oopsla/)                       |
| Can an LLM use sensitive examples without fine-tuning while bounding information leakage? | [Private in-context learning, AAAI 2026](/publications/bhusal2026aaai/)      |
| How does gradient clipping affect Muon's matrix update?                                   | [Inner Momentum for DP-Muon, 2026 preprint](/publications/bhusal2026dpmuon/) |
| How can deception change an attacker's decisions during a ransomware attack?              | [Strategic deception, GameSec 2024](/publications/neupane2024gamesec/)       |
| How well do privacy labels communicate data practices?                                    | [Privacy nutrition labels, HCII 2025](/publications/bhusal2025hcii/)         |

New to these topics? The [research tutorials](/blog/) introduce the ideas with worked examples. For exact assumptions, proofs, experiments, and limitations, follow the original paper links.

{% for topic in site.data.research.topics %}

<section id="{{ topic.id }}" markdown="1">

## {{ topic.title }}

{{ topic.description }}

{% for key in topic.papers %}
{% assign paper = site.data.publications | where: "key", key | first %}
{% if paper %}

### [{{ paper.title }}]({{ '/publications/' | append: key | append: '/' | relative_url }})

{% if paper.summary != blank %}{{ paper.summary }}{% endif %}

{% if paper.when_to_read != blank %}**Read this when:** {{ paper.when_to_read }}{% endif %}

{% if paper.code %}[Code]({{ paper.code }}) · {% endif %}[Paper and citation]({{ '/publications/' | append: key | append: '/' | relative_url }})

{% endif %}
{% endfor %}

</section>
{% endfor %}

## Research software

These repositories accompany the linked papers. Their documentation describes installation, dependencies, and experiments.

- [DiPAut](https://github.com/bhusalb/DiPAut): differential privacy checking for the online randomized algorithms modeled in the [CCS 2023 paper](/publications/chadha2023ccs/). A [versioned software artifact](/publications/bhusal2023dipaut/) is also available.
- [DipApprox](https://github.com/bhusalb/approximate-dp): approximate privacy verification for the program class studied in [CCS 2025](/publications/bhusal2025ccs/).
- [Privacy-preserving ICL](https://github.com/bhusalb/privacy-preserving-icl): implementation accompanying the [AAAI 2026 paper](/publications/bhusal2026aaai/).
- [Ransomware game simulation](https://github.com/bhusalb/gt-ransomware-simulation): simulation code for the [GameSec 2024 paper](/publications/neupane2024gamesec/).
- [Privacy label review materials](https://github.com/bhusalb/privacy-label-review-paper): materials accompanying the [HCII 2025 paper](/publications/bhusal2025hcii/).

## Stay connected

Follow new explanations through the [RSS feed](/feed.xml), browse [all publications](/publications/), or follow my [Google Scholar profile](https://scholar.google.com/citations?user=Dkp-woMAAAAJ). For research discussions and collaborations, contact [bhusalb@missouri.edu](mailto:bhusalb@missouri.edu).
