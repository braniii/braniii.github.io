# personal webpage :-)

This repository generates a static webpage with:

- [Astro](https://astro.build) v7
- [TailwindCSS](https://tailwindcss.com) v4

### Development

```sh
$ npm install    # Install dependencies.
$ npm run dev    # Start the dev server at localhost:4321.
```

### Building

```sh
$ npm run build      # Build the static site into dist/.
$ npm run preview    # Preview the production build locally.
```

Deployment happens automatically via GitHub Actions on pushes to `master`,
publishing `dist/` to the `gh-pages` branch.

### Content

The page content (publications, software) lives in `src/data/index.json`.

### Assets

Some external assets are included.

- GitHub Icon from GitHub.
- Icons from HeroIcons (MIT).
