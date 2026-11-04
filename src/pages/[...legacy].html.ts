import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
  const posts = await getCollection('blog', ({ data }) => !data.draft);
  const paths: { params: { legacy: string }; props: { targetSlug: string; title: string } }[] = [];

  for (const post of posts) {
    for (const oldPath of post.data.legacyPaths || []) {
      const clean = oldPath.replace(/^\/+/, '').replace(/\.html$/i, '');
      if (clean) {
        paths.push({
          params: { legacy: clean },
          props: { targetSlug: post.id, title: post.data.title },
        });
      }
    }
  }
  return paths;
}

export const GET: APIRoute = ({ props }) => {
  const { targetSlug, title } = props as { targetSlug: string; title: string };
  const rawBase = import.meta.env.BASE_URL;
  const base = rawBase === '/' ? '' : rawBase.replace(/\/$/, '');
  const targetUrl = `${base}/posts/${targetSlug}/`;

  const html = `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Redirecting to ${title}</title>
    <link rel="canonical" href="${targetUrl}" />
    <meta http-equiv="refresh" content="0; url=${targetUrl}" />
    <script>window.location.replace(${JSON.stringify(targetUrl)});</script>
  </head>
  <body style="font-family: system-ui, sans-serif; padding: 2rem;">
    <p>Redirecting to <a href="${targetUrl}">${title}</a>...</p>
  </body>
</html>`;

  return new Response(html, {
    headers: { 'Content-Type': 'text/html; charset=utf-8' },
  });
};
