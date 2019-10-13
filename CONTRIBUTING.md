# Contributing

Thanks for contributing to Hypothesis-Bio!
Every little bit helps and it's always appreciated.

There are a bunch of ways to contribute:

## Types of Contribution

### File bug reports

Please report any bugs to our [issue tracker](https://github.com/Lab41/hypothesis-bio/issues).
If you are reporting a bug, please provide as much information as you can including:

1. Hypothesis-Bio version
2. Hypothesis version
3. Python version
4. OS and version
5. How to reproduce the error

### Write documentation

Hypothesis-Bio could always use more documentation.
The documentation is contained in:

1. [Docstrings](https://www.python.org/dev/peps/pep-0257/) in the source code.

   These docstrings are the source of the documentation about each strategy.
   They're written in Markdown and contain a list of each argument's meaning, usage examples, and information about what exactly is being generated.
   The docstrings are rendered by the website into the full API documentation.

2. The README.md and CONTRIBUTING.md files.
   These files contain the key information for using and working on Hypothesis-Bio.
   Specifically, the README file is used both as the project's homepage on GitHub and landing page on the documentation website.

3. A documentation website.
   In addition to containing the rendered docstrings and README/CONTRIBUTING files, the site also (should) contain tutorials and additional information.
   To get the site up an running, you'll need a copy of [Node](https://nodejs.org/en/).
   Then, inside the `docs/` directory, run `npm i` and `npm run dev` to set up a development server.
   The site is built with [Vuepress](https://vuepress.vuejs.org), a simple static site generator whose configuration is defined in [`docs/.vuepress/config.js`](https://github.com/Lab41/hypothesis-bio/blob/master/docs/.vuepress/config.js).

### Add new strategies

### Add unit tests

## How to contribute

Ready to contribute to Hypothesis-Bio?
Here's how to set up your local environment for development:

1.  Fork the `hypothesis-bio` repo on GitHub.

2.  Clone your fork locally:

    ```shell
    $ git clone git@github.com:your_name_here/hypothesis_bio.git
    ```

3.  Install your local copy into a virtualenv.

    ```shell
    $ cd hypothesis-bio/
    $ virtualenv env
    $ source env/bin/activate
    (env) $ pip install -e .
    (env) $ pip install -r requirements-dev.txt
    ```

4.  Create a branch for local development:

    ```shell
    $ git checkout -b name-of-your-bugfix-or-feature
    ```

    Now you can make your changes locally.

5.  When you're done making changes, check that your changes pass flake8, mypy, black, and isort:

    ```shell
    (env) $ mypy hypothesis_bio/
    (env) $ black hypothesis_bio/
    (env) $ isort hypothesis_bio/*
    (env) $ flake8
    ```

    Also, run your code through our test suite to ensure nothing breaks:

    ```shell
    (env) $ pytest
    ```

6.  Commit your changes and push your branch to GitHub:

    ```shell
    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature
    ```

7.  Submit a pull request through the GitHub website.
