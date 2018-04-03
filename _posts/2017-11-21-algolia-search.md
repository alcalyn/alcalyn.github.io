---
title: Algolia Search
tags:
    - php
excerpt: blah.
---

{% include toc title="Summary" %}

I just added a search input to documentation about a PHP library.

## Why ?

I first written the whole documentation in the project README.md, so easy to CTRL+F.

Then it has become bigger. Having a very long readme is not a problem for me,
and it's better to CTRL+F in a single page.

But there was also a second repository with a second readme,
so I decided to merge both documentations to a single website, made with Jekyll.


## How ?

The Jekyll documentation is hosted by Github pages, and it's only generated HTML
files, and Javascript, spread on multiple pages.
So I wasn't possible anymore to ctrl+F the whole documentation.

I found Algolia, a search service with a free community plan.

His advantage is that it can return results in a few milliseconds,
for every character typed in search input.
Test it here: <https://eole-io.github.io/sandstone-doc/get-started>.

But I'm getting lost between all these tools: DocSearch, docsearch-scraper,
instantsearch.js, jekyll-algolia, algoliasearch-jekyll...

In this article, I'll describe how I finally integrated my search input,
which tools I used, and tools I tried and finally not used.




{% include ccby %}
