# alcalyn-blog

Personal blog built with [Hugo](https://gohugo.io) and the [Rusty Poison](https://github.com/RustyDaemon/rusty-poison) theme.

## Requirements

- [Hugo extended](https://gohugo.io/installation/) (v0.168 or later)
- Git
- Node.js (the theme builds its CSS with Tailwind, and the search index with Pagefind)

## Run locally

Clone the repository with its theme submodule:

```bash
git clone --recurse-submodules <repo-url>
cd alcalyn-blog
```

If you already cloned without `--recurse-submodules`:

```bash
git submodule update --init --recursive
```

Install the npm dependencies:

```bash
npm install
```

Start the development server:

```bash
hugo server
```

Then open http://localhost:1313. The site reloads automatically when files change.

To also show drafts and future-dated posts while writing:

```bash
hugo server -D -F
```

## Write a new post

The site is bilingual (English and French). Each post is a page bundle with one file per language, and its images next to them:

```bash
hugo new content posts/my-new-post/index.en.md
hugo new content posts/my-new-post/index.fr.md
```

New posts are created with `draft = true`. Remove that line (or set it to `false`) to publish the post.

Insert images with the Markdown syntax, the caption goes in the title: `![Alt text](image.png "Caption")`.
A post or project image (`featuredImage`) lives in `static/images/`.

## Build

```bash
npm run build
```

The static site is generated in `public/`, with its search index.
The search is not available with `hugo server`: to try it, build and serve `public/` on http://localhost:8000:

```bash
npm run preview
```
