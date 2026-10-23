# Privacy Preserving In-Context-Learning Framework for Large Language Models

Publication summary and citation record; follow the source links for the original work.

- Authors: Bishnu Bhusal; Manoj Acharya; Ramneet Kaur; Colin Samplawski; Anirban Roy; Adam D. Cobb; Rohit Chadha; Susmit Jha
- Year: 2026
- Type: Conference paper
- Publication status: published
- Paper page: https://bishnubhusal.com.np/publications/bhusal2026aaai/
- Scholarly identifier: https://doi.org/10.1609/aaai.v40i42.40838
- Venue or repository: Proceedings of the AAAI Conference on Artificial Intelligence
- DOI: 10.1609/aaai.v40i42.40838
- arXiv: https://arxiv.org/abs/2509.13625
- Topics: Differential privacy; Large language models; In-context learning; Private text generation

## Source links

- [Full paper (HTML)](<https://arxiv.org/html/2509.13625>)
- [Read PDF](<https://bishnubhusal.com.np/assets/pdf/aaai26.pdf>)
- [Publication source](<https://doi.org/10.1609/aaai.v40i42.40838>)
- [Code and resources](<https://github.com/bhusalb/privacy-preserving-icl>)

## Contribution summary

Presents a differentially private prediction framework that generates synthetic text by aggregating clipped per-token logits from inference over private records, without fine-tuning the underlying language model. A blending operation combines private and public inference to improve utility in the evaluated in-context-learning tasks.

## When to read this work

Read this when exploring how to use sensitive examples for language-model predictions or synthetic demonstrations with differential privacy, particularly when updating model weights is undesirable.

## Abstract

Large language models (LLMs) have significantly transformed natural language understanding and generation, but they raise privacy concerns due to potential exposure of sensitive information. Studies have highlighted the risk of information leakage, where adversaries can extract sensitive information embedded in the prompts. In this work, we introduce a novel private prediction framework for generating high-quality synthetic text with strong privacy guarantees. Our approach leverages the Differential Privacy (DP) framework to ensure worst-case theoretical bounds on information leakage without requiring any fine-tuning of the underlying models. The proposed method performs inference on private records and aggregates the resulting per-token output distributions. This enables the generation of longer and coherent synthetic text while maintaining privacy guarantees. Additionally, we propose a simple blending operation that combines private and public inference to further enhance utility. Empirical evaluations demonstrate that our approach outperforms previous state-of-the-art methods on in-context-learning (ICL) tasks, making it a promising direction for privacy-preserving text generation while maintaining high utility.

## Questions about this work

### Can private in-context learning work without fine-tuning?

This method generates differentially private synthetic demonstrations while leaving the underlying language model's weights unchanged. It clips and aggregates private next-token logits and blends private and public inference. The released synthetic demonstrations can then be reused for in-context learning through DP post-processing.

Source: [Approach — Private prediction and synthetic demonstrations](<https://arxiv.org/html/2509.13625#Sx5>)

### What access to the language model does the method require?

The method requires access to the full token-level logit distribution at each decoding step. The experiments use the instruction-tuned Gemma 1.1 2B model. An interface that returns only generated text does not provide the inputs required by this algorithm.

Source: [Experiments — Model access and setup](<https://arxiv.org/html/2509.13625#Sx6>)

### How does generating longer text affect the privacy budget?

Private synthetic generation incurs privacy cost for each generated token, so the accounting must cover the complete generation. Reusing already released DP synthetic text is post-processing. The paper identifies the per-token privacy cost as a limitation compared with private fine-tuning, which accounts for privacy during training.

Source: [Limitations](<https://arxiv.org/html/2509.13625#Sx11>)

## Tutorials and reading guides

- [Privacy-preserving in-context learning: synthetic demonstrations and privacy budgets](<https://bishnubhusal.com.np/blog/2026/privacy-preserving-in-context-learning/>) — How clipped logits, public context, and private token sampling can produce reusable ICL demonstrations, with careful accounting for privacy boundaries.

## Cite this work

[Download BibTeX](<https://bishnubhusal.com.np/publications/bhusal2026aaai/cite.bib>) · [Download RIS](<https://bishnubhusal.com.np/publications/bhusal2026aaai/cite.ris>)

```bibtex
@inproceedings{bhusal2026aaai,
  title = {Privacy Preserving In-Context-Learning Framework for Large Language Models},
  author = {Bhusal, Bishnu and Acharya, Manoj and Kaur, Ramneet and Samplawski, Colin and Roy, Anirban and Cobb, Adam D. and Chadha, Rohit and Jha, Susmit},
  booktitle = {Proceedings of the AAAI Conference on Artificial Intelligence},
  volume = {40},
  number = {42},
  pages = {35303--35312},
  year = {2026},
  month = mar,
  doi = {10.1609/aaai.v40i42.40838},
  url = {https://doi.org/10.1609/aaai.v40i42.40838},
  eprint = {2509.13625},
  archiveprefix = {arXiv}
}
```
