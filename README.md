# personal webpage :-)

This repository generates a static HTML webpage with:

- The Jinja2 templating engine.
- The TailwindCSS utility framework.

### Dependencies

```sh
$ cd site/
$ poetry install     # Install Python dependencies (Jinja2).
$ cd styles/
$ yarn install       # Install JavaScript dependencies (TailwindCSS).
```

### Building

```sh
$ ./compile.py full  # To regenerate the entire site.
$ ./compile.py       # Regenerate the HTML but skip the TailwindCSS build step.
```

### Assets

Some external assets are included.

- GitHub Icon from GitHub.
- Icons from HeroIcons (MIT).
