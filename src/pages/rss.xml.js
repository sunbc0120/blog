import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const posts = (await getCollection('blog', ({ data }) => !data.draft)).sort(
    (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
  );
  const rawBase = import.meta.env.BASE_URL;
  const base = rawBase === '/' ? '' : rawBase.replace(/\/$/, '');

  return rss({
    title: "SUN's Blog",
    description:
      'Notes from hard technical lessons, to remind myself later and help those who may run into the same situation.',
    site: context.site,
    items: posts.map((post) => ({
      title: post.data.title,
      pubDate: post.data.pubDate,
      description: post.data.description,
      link: `${base}/posts/${post.id}/`,
    })),
  });
}
