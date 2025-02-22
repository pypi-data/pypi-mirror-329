# Tilly

CLI for easily creating Today I Learned posts, inspired by [Simon Willison](https://til.simonwillison.net).

Check this [tilly-pub.github.io](https://tilly-pub.github.io) website that was genereated using Tilly :)


## Installation

```
uv venv .venv
source .venv/bin/activate
uv pip install tilly
```

## tilly commands

<!-- cli-help starts -->
```bash
Usage: tilly [OPTIONS] COMMAND [ARGS]...

  TIL (Today I Learned) Command Line Interface.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  build           Build database tils.db.
  config          List config.
  copy-templates  Copy default templates to current repo for customization.
  gen-static      Generate static site from tils.db using datasette.
  hello           Say hello.
  list-plugins    List all available plugins.
  serve           Serve tils.db using datasette or the generated static...
```
<!-- cli-help ends -->


## Usage

Create a repo (or clone a repo from github):

```
git init
```

Add a TIL:

```
mkdir example # this will be the topic of your TIL.
echo "# My first TIL with tilly" > example/first-til.md
```

Commit your work:

```
git add .
git commit -m "adding first til"
```

Build the local `tils.db`:

```
tilly build
```

Serve you tils locally:

```
tilly serve
```

Generate a static site in the docs folder:

```
tilly config -l --output-folder docs
tilly gen-static
```

The static site can also be served locally:

```
tilly serve --static
```

You can now publish your static site to [Github](https://pages.github.com).
Don't forget to configure the source folder `docs` in your repository's GitHub Pages settings.


## Customize the default templates

Your can overwrite the default templates by first making a copy of the default templates:

```
tilly copy-templates
```

Change the templates to your liking, then generate your static site:

```
tilly gen-static --template-dir templates
```

Customized templates can also be served locally:

```
tilly serve --template-dir templates
```

## Tilly plugins

Tilly's plugin system allows additional features to be implemented as Python code which can be wrapped up in a separate Python package. The underlying mechanism uses [pluggy](https://pluggy.readthedocs.io/en/stable/).

### Available plugins

- [tilly-sitemap](https://github.com/tilly-pub/tilly-sitemap): Generate `robots.txt` and `sitemap.xml` for [tilly](https://github.com/tilly-pub/tilly) sites.

### Creating your own Tilly plugin

You can easily create your own plugin by running the following command:

```
uvx cookiecutter gh:tilly-pub/tilly-plugin
```

This command runs cookiecutter and will use our [`tilly-plugin`](https://github.com/tilly-pub/tilly-plugin) cookiecutter to setup a new project.



# Development, building and publishing


```
uv venv .venv --python=3.11
source .venv/bin/activate
uv pip install .
uv pip install -r requirements-dev.txt
./build.sh
./publish.sh
```

## TODO

- add search to the static site
- document tilly-plugin creation
- add related article links using vector embeddings
- support TILs with multiple categories
- it should be possible to store the template folder in the config

## DONE

- created cookiecutter tilly-plugin repo
- create plugin for generating sitemaps
- example github actions workflow for publishing [tilly static pages](https://tilly-pub.github.io/tilly/github-actions-workflow/)
- add tests
- update `README.md` with latest `tilly` cli commands/options (`python update_readme.py`)
