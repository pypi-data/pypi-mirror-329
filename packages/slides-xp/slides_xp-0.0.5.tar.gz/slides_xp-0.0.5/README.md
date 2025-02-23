# Slides XP

A simple but flexible markdown slide-show viewer.

## Running

```sh
sxp <directories to serve>
```

## Theming

You can use the `--theme` option to specify the a built-in theme, or a path to
a directory containing CSS theme files.

The built-in themes are:

* `default`
* `xp`

### Python-generated slides

Python files that end with `.slide.py` can be used to generate slides using
Python, which is useful for custom themed slides. The file should include a
`render` function that returns a `pyhtml` tag.

### Custom CSS

A theme directory should contain (at least) these files:

* `main.css`: main stylesheet. Always loaded.
* `slide.css`: stylesheet for slide pages.
* `picker.css`: stylesheet for slide picker page.

These stylesheets are mounted at the `/theme` endpoint.

Within these stylesheets, the following classes can be selected.

* `.highlight`: code blocks
* `.slide-content`: slide content
* `.picker-box`: slide picker
* `.picker-item`: slide within slide picker

And the following variables are available:

* `--hl-comment`: code block highlighting, comment
* `--hl-doc`: code block highlighting, documentation
* `--hl-keyword`: code block highlighting, keyword
* `--hl-var`: code block highlighting, variable
* `--hl-func`: code block highlighting, function
* `--hl-type`: code block highlighting, type
* `--hl-string`: code block highlighting, string
