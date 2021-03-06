![](https://img.shields.io/pypi/v/whatlies)
![](https://img.shields.io/pypi/pyversions/whatlies)
![](https://img.shields.io/github/license/rasahq/whatlies)
[![Downloads](https://pepy.tech/badge/whatlies)](https://pepy.tech/project/whatlies)

<img src="docs/logo.png" width=255 height=255 align="right">

# whatlies

A library that tries to help you to understand (note the pun).

> "What lies in word embeddings?"

This small library offers tools to make visualisation easier of both
word embeddings as well as operations on them.

Feedback is welcome.

<img src="docs/square-logo.svg" width=200 height=200 align="right">

## Produced

This project was initiated at [Rasa](https://rasa.com) as a by-product of
our efforts in the developer advocacy and research teams. It's an open source project
and community contributions are very welcome!

## Features

This library has tools to help you understand what lies in word embeddings. This includes:

- simple tools to create (interactive) visualisations
- an api for vector arithmetic that you can visualise
- support for many dimensionality reduction techniques like pca, umap and tsne
- support for many language backends including spaCy, fasttext, tfhub, huggingface and bpemb
- lightweight scikit-learn featurizer support for all these backends

## Installation

You can install the package via pip;

```bash
pip install whatlies
```

This will install the base dependencies. Depending on the
transformers and language backends that you'll be using you
may want to install more. Here's all the possible installation
settings you could go for.

```bash
pip install whatlies[tfhub]
pip install whatlies[transformers]
```

If you want it all you can also install via;

```bash
pip install whatlies[all]
```

Note that this will install dependencies but it
**will not** install all the language models you might
want to visualise. For example, you might still
need to manually download spaCy models if you intend
to use that backend.

## Getting Started

For a quick overview, check out our introductory video on
[youtube](https://www.youtube.com/watch?v=FwkwC7IJWO0&list=PL75e0qA87dlG-za8eLI6t0_Pbxafk-cxb&index=9&t=0s). More
in depth getting started guides can be found on the [documentation page](https://rasahq.github.io/whatlies/).

## Examples

The idea is that you can load embeddings from a language backend
and use mathematical operations on it.

```python
from whatlies import EmbeddingSet
from whatlies.language import SpacyLanguage

lang = SpacyLanguage("en_core_web_md")
words = ["cat", "dog", "fish", "kitten", "man", "woman",
         "king", "queen", "doctor", "nurse"]

emb = EmbeddingSet(*[lang[w] for w in words])
emb.plot_interactive(x_axis=emb["man"], y_axis=emb["woman"])
```

![](docs/gif-zero.gif)

You can even do fancy operations. Like projecting onto and away
from vector embeddings! You can perform these on embeddings as
well as sets of embeddings.  In the example below we attempt
to filter away gender bias using linear algebra operations.

```python
orig_chart = emb.plot_interactive('man', 'woman')

new_ts = emb | (emb['king'] - emb['queen'])
new_chart = new_ts.plot_interactive('man', 'woman')
```

![](docs/gif-one.gif)

There's also things like **pca** and **umap**.

```python
from whatlies.transformers import Pca, Umap

orig_chart = emb.plot_interactive('man', 'woman')
pca_plot = emb.transform(Pca(2)).plot_interactive(x_label='pca_0', y_label='pca_1')
umap_plot = emb.transform(Umap(2)).plot_interactive(x_label='umap_0', y_label='umap_1')

pca_plot | umap_plot
```

![](docs/gif-two.gif)

## Documentation

To learn more and for a getting started guide, check out the [documentation](https://rasahq.github.io/whatlies/).

## Similar Projects

There are some projects out there who are working on similar tools and we figured it fair to mention and compare them here.

##### Julia Bazińska & Piotr Migdal Web App

The original inspiration for this project came from [this web app](https://lamyiowce.github.io/word2viz/) and [this pydata talk](https://www.youtube.com/watch?v=AGgCqpouKSs). It is a web app that takes a while to slow
but it is really fun to play with. The goal of this project is to make it
easier to make similar charts from jupyter using different language backends.


##### Tensorflow Projector

From google there's the [tensorflow projector project](https://projector.tensorflow.org/). It offers
highly interactive 3d visualisations as well as some transformations via tensorboard.

- The tensorflow projector will create projections in tensorboard, which you can also load
into jupyter notebook but whatlies makes visualisations directly.
- The tensorflow projector supports interactive 3d visuals, which whatlies currently doesn't.
- Whatlies offers lego bricks that you can chain together to get a visualisation started. This
also means that you're more flexible when it comes to transforming data before visualising it.

##### Parallax

From Uber AI Labs there's [parallax](https://github.com/uber-research/parallax) which is described
in a paper [here](https://arxiv.org/abs/1905.12099). There's a common mindset in the two tools;
the goal is to use arbitrary user defined projections to understand embedding spaces better.
That said, some differences that are worth to mention.

- It relies on bokeh as a visualisation backend and offers a lot of visualisation types
(like radar plots). Whatlies uses altair and tries to stick to simple scatter charts.
Altair can export interactive html/svg but it will not scale as well if you've drawing
many points at the same time.
- Parallax is meant to be run as a stand-alone app from the command line while Whatlies is
meant to be run from the jupyter notebook.
- Parallax gives a full user interface while Whatlies offers lego bricks that you can chain
together to get a visualisation started.
- Whatlies relies on language backends to fetch word embeddings. Parallax allows you to instead
fetch raw files on disk.
- Parallax has been around for a while, Whatlies is more new and therefore more experimental.

## Local Development

If you want to develop locally you can start by running this command.

```bash
make develop
```

### Documentation

This is generated via

```
make docs
```

### Citation
Please use the following citation when you found `whatlies` helpful for any of your work (find the `whatlies` paper [here](http://arxiv.org/abs/2009.02113)):
```
@misc{Warmerdam2020whatlies,
	Archiveprefix = {arXiv},
	Author = {Vincent D. Warmerdam and Thomas Kober and Rachael Tatman},
	Eprint = {2009.02113},
	Primaryclass = {cs.CL},
	Title = {Going Beyond T-SNE: Exposing \texttt{whatlies} in Text Embeddings},
	Year = {2020}
}
```
