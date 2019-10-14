# Hello, hackseq19!

Welcome to hackseq19!
This year is going to be a lot of fun.
We'll be building a tool that will make it easier to test bioinformatics software and throwing it at open source software to find real bugs.

## Before you arrive

While there's nothing you have to do (besides get excited!), if you want to get a head start, I'd suggest:

1. Take a look at the [Hypothesis](https://hypothesis.readthedocs.io/en/latest/index.html) documentation, which is the tool on which Hypothesis-Bio is based.
2. Make sure you have Python 3 and git installed.
   If you're new to Python and/or git, don't worry at all.
3. [Email me](mailto:benjamin_lee@college.harvard.edu) your GitHub username so I can add you to the repository (and [create an account](https://github.com/join)) if you haven't already.
4. Join the hackseq19 Slack and the `p10-hypo` channel.
5. Read the [README](https://github.com/Lab41/hypothesis-bio/blob/master/README.md) and [CONTRIBUTING](https://github.com/Lab41/hypothesis-bio/blob/master/CONTRIBUTING.md) files, which have more background information.

## Some ideas for what to work on

I ([Benjamin](https://github.com/Benjamin-Lee)) have put up a basic project scaffold (documentation generator, continuous integration, _etc._) to help get things started.
However, there's still a ton of things to do in order to create the Hypothesis-Bio project.
Here's a non-exhaustive list:

- First and foremost, we need strategies for generating test cases.
  As a starter example, I've created a strategy that generates DNA sequences and put a demonstration of it in the README.
  If you work with a type of biological data that doesn't have a strategy for generating it yet, please feel free to contribute it via a pull request.
  Alternatively, create an [issue](https://github.com/Lab41/hypothesis-bio/issues?q=is%3Aissue+is%3Aopen+label%3A%22new+strategy%22) with the `new strategy` tag so that we can keep track of the idea.

- We'll also need plenty of documentation, tutorials, and examples.
  These can all be written in [Markdown](https://guides.github.com/features/mastering-markdown/), a simple method for marking up text.
  For more information on how to write documentation, take a look at the [CONTRIBUTING](https://github.com/Lab41/hypothesis-bio/blob/master/CONTRIBUTING.md) file.

- Write the paper!
  I want to make sure that everyone gets academic credit for their hard work, so I'm planning on writing a paper.
  A short paper (such as a _Bioinformatics_ application note) is definitely within reach after a weekend of hard work.

- For people with experience in Conda, packaging the project with a recipe.yml would be a great help.

- Go bug hunting!
  There's plenty of open-source bioinformatics software that would appreciate the help.
  If you find a bug, post it as an issue on their repository and let us know that you found one so we can record it.

- If you have creative skills, we could definitely use a logo.
  The Hypothesis project has a [logo](https://github.com/HypothesisWorks/hypothesis/blob/master/brand/dragonfly-rainbow.svg), so you could try to modify it to make it more biological.
  Alternatively, if you're feeling ambitious, you could try to design one from scratch.

- Anything else you think would be cool!
