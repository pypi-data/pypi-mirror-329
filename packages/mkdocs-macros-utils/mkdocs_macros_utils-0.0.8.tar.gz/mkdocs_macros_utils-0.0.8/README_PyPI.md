# mkdocs-macros-utils

[mkdocs-macros-utils](https://7rikazhexde.github.io/mkdocs-macros-utils/) is [mkdocs-macros-plugin](https://mkdocs-macros-plugin.readthedocs.io/en/latest/) based project that provides macros to extend cards, code blocks, etc, in MkDocs documents.

[![pages-build-deployment](https://github.com/7rikazhexde/mkdocs-macros-utils/actions/workflows/pages/pages-build-deployment/badge.svg?branch=gh-pages)](https://github.com/7rikazhexde/mkdocs-macros-utils/actions/workflows/pages/pages-build-deployment) [![DOCS](https://img.shields.io/badge/Docs-Click%20Here-blue?colorA=24292e&colorB=0366d6&logo=github)](https://7rikazhexde.github.io/mkdocs-macros-utils/)

## Features

- **Link Card**: Create link cards with images and descriptions, etc
- **Gist Code Block**: Embed and syntax-highlight code from GitHub Gists
- **X/Twitter Card**: Embed tweets with proper styling and dark mode support

## Usage

### Install `mkdocs-macros-utils`

```bash
# For pip
pip install mkdocs-macros-utils

# For poetry
poetry add mkdocs-macros-utils
```

### Config settings

1. Add the plugin to your `mkdocs.yml`

    ```yaml
    plugins:
      - macros:
          modules: [mkdocs_macros_utils]

    markdown_extensions:
      - attr_list
      - md_in_html

    extra:
      debug:
        link_card: false  # Set to true for debug logging
        gist_codeblock: false
        x_twitter_card: false

    extra_css:
      - stylesheets/macros-utils/link-card.css
      - stylesheets/macros-utils/gist-cb.css
      - stylesheets/macros-utils/x-twitter-link-card.css

    extra_javascript:
      - javascripts/macros-utils/x-twitter-widget.js
    ```

1. Start the development server

    ```bash
    poetry run mkdocs serve
    ```

The plugin will automatically create the required directories and copy CSS/JS files during the build process.

## Documentation

For detailed usage and examples, please see the [documentation](https://7rikazhexde.github.io/mkdocs-macros-utils/).

## License

MIT License - see the [LICENSE](./LICENCE) file for details.
