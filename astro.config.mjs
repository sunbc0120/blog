import { defineConfig } from 'astro/config';
import { unified } from '@astrojs/markdown-remark';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

// Set ASTRO_BASE="/" if migrating from sunbc0120.github.io/blog to root sunbc0120.github.io
const BASE_PATH = process.env.ASTRO_BASE ?? '/blog';
const normalizedBase = BASE_PATH === '/' ? '' : BASE_PATH.replace(/\/$/, '');

/**
 * Converts ```mermaid fenced blocks into <figure class="mermaid-figure"> before Shiki runs,
 * storing the raw diagram source in data-mermaid-src so client-side Mermaid can re-render
 * seamlessly across Day and Night theme switches.
 */
function remarkMermaid() {
  return (tree) => {
    function walk(node) {
      if (!node || !Array.isArray(node.children)) return;
      for (let i = 0; i < node.children.length; i++) {
        const child = node.children[i];
        if (child.type === 'code' && child.lang === 'mermaid') {
          const escapedAttr = child.value
            .replace(/&/g, '&amp;')
            .replace(/"/g, '&quot;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
          const escapedText = child.value
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
          node.children[i] = {
            type: 'html',
            value: `<figure class="mermaid-figure"><div class="mermaid-stage" data-mermaid-src="${escapedAttr}"><pre class="mermaid">${escapedText}</pre></div></figure>`,
          };
        } else {
          walk(child);
        }
      }
    }
    walk(tree);
  };
}

/**
 * Automatically prefixes root-relative /images/... and internal links in Markdown/MDX
 * with `base` (e.g. `/blog`) so posts stay portable between `/blog` and `/`.
 */
function rehypePrefixBase() {
  return (tree) => {
    if (!normalizedBase) return;
    function walk(node) {
      if (!node || typeof node !== 'object') return;
      if (node.type === 'element' && node.properties) {
        for (const attr of ['src', 'href']) {
          const val = node.properties[attr];
          if (
            typeof val === 'string' &&
            val.startsWith('/') &&
            !val.startsWith('//') &&
            !val.startsWith(normalizedBase + '/') &&
            val !== normalizedBase
          ) {
            node.properties[attr] = `${normalizedBase}${val}`;
          }
        }
      }
      if (Array.isArray(node.children)) {
        for (const child of node.children) walk(child);
      }
    }
    walk(tree);
  };
}

export default defineConfig({
  site: 'https://sunbc0120.github.io',
  base: BASE_PATH,
  trailingSlash: 'ignore',
  devToolbar: { enabled: false },
  server: {
    host: '::',
    port: 4321,
    allowedHosts: true,
  },
  vite: {
    server: {
      allowedHosts: true,
    },
    preview: {
      allowedHosts: true,
    },
  },
  integrations: [mdx(), sitemap()],
  markdown: {
    processor: unified({
      remarkPlugins: [remarkMermaid, remarkMath],
      rehypePlugins: [
        [rehypeKatex, { strict: false, trust: true }],
        rehypePrefixBase,
      ],
    }),
    syntaxHighlight: 'shiki',
    shikiConfig: {
      themes: {
        light: 'github-light',
        dark: 'github-dark-dimmed',
      },
      defaultColor: false,
      wrap: false,
    },
  },
});
