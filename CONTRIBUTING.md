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

### Add new strategies

### Add unit tests

## How to contribute

Ready to contribute to Hypothesis-Bio?
Here's how to set up your local environment for development:

1.  Fork the `hypothesis_bio` repo on GitHub.
2.  Clone your fork locally:
    ```shell
    $ git clone git@github.com:your_name_here/hypothesis_bio.git
    ```
3.  Install your local copy into a virtualenv.

    ```shell
    $ cd hypothesis_bio/
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

5.  When you're done making changes, check that your changes pass flake8, mypy, black, and isort.

    ```shell
    $ mypy hypothesis-bio/
    $ black hypothesis-bio/
    $ isort hypothesis-bio/*
    $ flake8 hypothesis-bio/
    ```

6.  Commit your changes and push your branch to GitHub::

    ```shell
    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature
    ```

7.  Submit a pull request through the GitHub website.
