# Sphinx Documentation of echemdb-unitpackage

This documentation is automatically built and uploaded to GitHub Pages.

To build and see the documentation locally, type:

```sh
pixi run doc
```

Serve the documentation via

```sh
python -m http.server 8880 -b localhost --directory generated/html &
```

Then open http://localhost:8880/ with your browser.

Some MD files can be interactively edited in jupyter

```sh
pixi run jupyter lab
```
