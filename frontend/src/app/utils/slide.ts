export const splitContentIntoPages = (content: string) => {
  // 空のコンテンツの場合は空の配列を返す
  if (!content || content.trim() === '') {
    console.log('Empty content provided to splitContentIntoPages');
    return [''];
  }

  // SVGコンテンツかどうかを確認
  if (content.trim().startsWith('<svg')) {
    console.log('SVG content detected');
    // SVGコンテンツの場合は、そのまま1ページとして扱う
    return [content];
  }

  // ページ区切りとなる可能性のあるタグやクラスを探す
  // 一般的なパターン: <div class="page">...</div> または <section>...</section>
  const pagePattern = /<div[^>]*class="[^"]*page[^"]*"[^>]*>[\s\S]*?<\/div>|<section[^>]*>[\s\S]*?<\/section>/g;
  const matches = content.match(pagePattern);

  if (matches && matches.length > 0) {
    console.log(`Found ${matches.length} pages using page pattern`);
    return matches;
  } else {
    console.log('No page divisions found, treating entire content as one page');
    // ページ区切りが見つからない場合は、コンテンツ全体を1ページとして扱う
    return [content];
  }
};