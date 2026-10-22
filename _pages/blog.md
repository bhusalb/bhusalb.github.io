---
layout: page
permalink: /blog/
title: tutorials
description: Research tutorials by Bishnu Bhusal on differential privacy verification, private in-context learning, and private optimization, with worked examples and links to the original papers.
nav: true
nav_order: 3
sitemap: true
---

Research explanations and worked examples, with links to the original papers and implementations. Each tutorial separates the teaching example from the paper's results and states the assumptions that matter.

[Subscribe via RSS](/feed.xml) · [Explore the research guide](/research/)

<ul class="post-list">
{% for post in site.posts %}
  <li>
    <h2><a class="post-title" href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
    <p>{{ post.description }}</p>
    <p class="post-meta"><time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %-d, %Y" }}</time> · {{ post.content | number_of_words | divided_by: 180 | plus: 1 }} min read</p>
  </li>
{% endfor %}
</ul>
