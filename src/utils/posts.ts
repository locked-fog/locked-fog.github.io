import type { CollectionEntry } from 'astro:content';

export const POSTS_PER_PAGE = 20;

export function getVisibleSortedPosts(posts: CollectionEntry<'posts'>[], isProd: boolean) {
  return posts
    .filter((post) => !post.data.draft || !isProd)
    .sort((a, b) => b.data.pubDate.getTime() - a.data.pubDate.getTime());
}

export function getPageHref(page: number) {
  return page <= 1 ? '/' : `/page/${page}/`;
}
