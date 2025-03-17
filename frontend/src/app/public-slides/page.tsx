'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useSearchParams, useRouter } from 'next/navigation';
import Pagination from '../components/Pagination';

interface Slide {
  id: number;
  title: string;
  content: string;
  is_public: boolean;
  owner_email: string;
  owner_username: string;
  created_at: string;
  updated_at: string;
}

export default function PublicSlides() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [slides, setSlides] = useState<Slide[]>([]);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [slidePreviews, setSlidePreviews] = useState<{ [key: number]: string }>({});

  // URLからページ番号を取得
  const currentPage = Number(searchParams.get('page')) || 1;

  useEffect(() => {
    fetchSlides();
  }, [currentPage]);

  // スライドコンテンツをページに分割する関数
  const splitContentIntoPages = (content: string) => {
    // SVGコンテンツかどうかを確認
    if (content.trim().startsWith('<svg')) {
      // SVGコンテンツの場合は、そのまま1ページとして扱う
      return content;
    }

    // ページ区切りとなる可能性のあるタグやクラスを探す
    // 一般的なパターン: <div class="page">...</div> または <section>...</section>
    const pagePattern = /<div[^>]*class="[^"]*page[^"]*"[^>]*>[\s\S]*?<\/div>|<section[^>]*>[\s\S]*?<\/section>/g;
    const matches = content.match(pagePattern);

    if (matches && matches.length > 0) {
      return matches[0]; // 最初のページのみを返す
    } else {
      // ページ区切りが見つからない場合は、コンテンツ全体を1ページとして扱う
      return content;
    }
  };

  const fetchSlides = async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/public-slides?page=${currentPage}`
      );

      if (!response.ok) {
        throw new Error('スライドの取得に失敗しました');
      }

      const data = await response.json();
      setSlides(data[0]); // スライドのリスト
      setTotalPages(data[1]); // 総ページ数

      // 各スライドの最初のページをプレビューとして抽出
      const previews: { [key: number]: string } = {};
      data[0].forEach((slide: Slide) => {
        previews[slide.id] = splitContentIntoPages(slide.content);
      });
      setSlidePreviews(previews);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handlePageChange = (page: number) => {
    // URLのクエリパラメータを更新
    const params = new URLSearchParams(searchParams.toString());
    params.set('page', page.toString());
    router.push(`?${params.toString()}`);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">読み込み中...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">公開スライド</h1>

      {error && (
        <div className="p-4 mb-6 text-sm text-red-700 bg-red-100 rounded-lg" role="alert">
          {error}
        </div>
      )}

      {slides.length === 0 ? (
        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <svg
            className="mx-auto h-12 w-12 text-gray-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 13h6m-3-3v6m-9 1V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z"
            />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-gray-900">公開スライドがありません</h3>
          <p className="mt-1 text-sm text-gray-500">
            現在公開されているスライドはありません。
          </p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {slides.map((slide) => (
              <div
                key={slide.id}
                className="bg-white overflow-hidden shadow rounded-lg border border-gray-200"
              >
                <div className="p-5">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <svg
                        className="h-6 w-6 text-gray-400"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                        />
                      </svg>
                    </div>
                    <div className="ml-5 w-0 flex-1">
                      <h3 className="text-lg font-medium text-gray-900 truncate">{slide.title}</h3>
                      <div className="mt-1 flex items-center">
                        <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                          公開
                        </span>
                        <span className="ml-2 text-sm text-gray-500">
                          {new Date(slide.updated_at).toLocaleDateString()}
                        </span>
                      </div>
                      <div className="mt-1 text-xs text-gray-500">
                        作成者: {slide.owner_username || slide.owner_email.split('@')[0]}
                      </div>
                    </div>
                  </div>
                  {/* スライドプレビュー表示エリア */}
                  <div className="mt-4 border rounded-md p-2 overflow-hidden" style={{ height: '180px' }}>
                    <div className="prose prose-sm max-w-none overflow-hidden flex items-center justify-center h-full">
                      <div
                        style={{
                          transform: 'scale(0.4)',
                          transformOrigin: 'center',
                          width: '250%',
                          height: '250%',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center'
                        }}
                      >
                        {slidePreviews[slide.id]?.trim().startsWith('<svg') ? (
                          // SVGコンテンツの場合
                          <div
                            className="svg-container"
                            style={{
                              width: '100%',
                              height: '100%',
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'center'
                            }}
                            dangerouslySetInnerHTML={{ __html: slidePreviews[slide.id] || '' }}
                          />
                        ) : (
                          // 通常のHTMLコンテンツの場合
                          <div dangerouslySetInnerHTML={{ __html: slidePreviews[slide.id] || '' }} />
                        )}
                      </div>
                    </div>
                  </div>
                </div>
                <div className="bg-gray-50 px-5 py-3 flex justify-between">
                  <Link
                    href={`/slides/${slide.id}`}
                    className="text-sm font-medium text-indigo-600 hover:text-indigo-500"
                  >
                    表示
                  </Link>
                  <Link
                    href={`/slides/${slide.id}?slideshow=true`}
                    className="text-sm font-medium text-indigo-600 hover:text-indigo-500"
                  >
                    スライドショー
                  </Link>
                </div>
              </div>
            ))}
          </div>
          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            onPageChange={handlePageChange}
          />
        </>
      )}
    </div>
  );
}