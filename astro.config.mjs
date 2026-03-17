import { defineConfig } from 'astro/config';
import rehypeKatex from 'rehype-katex';
import remarkMath from 'remark-math';

const site = process.env.SITE_URL ?? 'https://locked-fog.github.io';

function rehypeKatexWithDocumentMacros() {
  return (tree, file) => {
    const transform = rehypeKatex({
      globalGroup: true,
      macros: {},
    });

    return transform(tree, file);
  };
}

export default defineConfig({
  site,
  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeKatexWithDocumentMacros],
  },
});
