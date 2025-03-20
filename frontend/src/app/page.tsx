'use client';

import { useEffect, useState } from 'react';
import { useAuth } from './contexts/AuthContext';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import Pagination from './components/Pagination';

interface Slide {
  id: number;
  title: string;
  content: string;
  is_public: boolean;
  owner_id: string;
  owner_username: string;
  created_at: string;
  updated_at: string;
  likes: number;
  views: number;
}

export default function Home() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { isAuthenticated, isLoading } = useAuth();
  const [slides, setSlides] = useState<Slide[]>([]);
  const [filteredSlides, setFilteredSlides] = useState<Slide[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [slidePreviews, setSlidePreviews] = useState<{ [key: number]: string }>({});
  const [searchQuery, setSearchQuery] = useState('');
  const [totalPages, setTotalPages] = useState(1);
  const [sortBy, setSortBy] = useState('created_at');

  // URLからページ番号を取得
  const currentPage = Number(searchParams.get('page')) || 1;

  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      fetchSlides();
    } else if (!isLoading && !isAuthenticated) {
      setLoading(false);
    }
  }, [isLoading, isAuthenticated, currentPage, sortBy]);

  // 検索クエリが変更されたときにスライドをフィルタリング
  useEffect(() => {
    if (slides.length > 0) {
      if (searchQuery.trim() === '') {
        setFilteredSlides(slides);
      } else {
        const query = searchQuery.toLowerCase();
        const filtered = slides.filter(slide =>
          slide.title.toLowerCase().includes(query)
        );
        setFilteredSlides(filtered);
      }
    }
  }, [searchQuery, slides]);

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
      const token = localStorage.getItem('token');
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/slides?` +
        new URLSearchParams({
          page: currentPage.toString(),
          sort_by: sortBy,
          per_page: '18'
        }).toString(),
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error('スライドの取得に失敗しました');
      }

      const data = await response.json();
      setSlides(data[0]);
      setFilteredSlides(data[0]);
      setTotalPages(data[1]);

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

  const handleDeleteSlide = async (slideId: number) => {
    if (!confirm('このスライドを削除してもよろしいですか？')) {
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/slides/${slideId}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('スライドの削除に失敗しました');
      }

      // 成功したら、スライドリストから削除したスライドを除外
      setSlides(slides.filter(slide => slide.id !== slideId));
      setFilteredSlides(filteredSlides.filter(slide => slide.id !== slideId));

      // プレビューからも削除
      const newPreviews = { ...slidePreviews };
      delete newPreviews[slideId];
      setSlidePreviews(newPreviews);
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handlePageChange = (page: number) => {
    // URLのクエリパラメータを更新
    const params = new URLSearchParams(searchParams.toString());
    params.set('page', page.toString());
    router.push(`?${params.toString()}`);
  };

  const handleSortChange = (newSortBy: string) => {
    setSortBy(newSortBy);
    setSearchQuery('');
    const params = new URLSearchParams(searchParams.toString());
    params.set('page', '1');
    params.set('sort_by', newSortBy);
    router.push(`?${params.toString()}`);
  };

  if (isLoading || loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">読み込み中...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <h1 className="text-4xl font-extrabold text-gray-900 sm:text-5xl sm:tracking-tight lg:text-6xl">
            Codebase Slide Share へようこそ
          </h1>
          <p className="mt-5 max-w-xl mx-auto text-xl text-gray-500">
            HTMLやSVG形式で記載されたコードベースのスライド情報を管理するWebアプリです。
          </p>
          <div className="mt-8 flex justify-center">
            <div className="inline-flex rounded-md shadow">
              <Link
                href="/login"
                className="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
              >
                ログイン
              </Link>
            </div>
            <div className="ml-3 inline-flex">
              <Link
                href="/register"
                className="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-indigo-600 bg-white hover:bg-gray-50"
              >
                アカウント登録
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">マイスライド</h1>
        <div className="flex items-center space-x-4">
          <select
            value={sortBy}
            onChange={(e) => handleSortChange(e.target.value)}
            className="block pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
          >
            <option value="created_at">新着順</option>
            <option value="likes">いいね順</option>
            <option value="views">閲覧数順</option>
          </select>
          <Link
            href="/slides/new"
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700"
          >
            新規スライド作成
          </Link>
        </div>
      </div>

      {/* 検索ボックス */}
      <div className="mb-6">
        <div className="relative">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="スライドタイトルで検索..."
            className="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
          />
          <div className="absolute inset-y-0 right-0 flex items-center pr-3">
            <svg
              className="h-5 w-5 text-gray-400"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
              aria-hidden="true"
            >
              <path
                fillRule="evenodd"
                d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                clipRule="evenodd"
              />
            </svg>
          </div>
        </div>
      </div>

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
          <h3 className="mt-2 text-sm font-medium text-gray-900">スライドがありません</h3>
          <p className="mt-1 text-sm text-gray-500">新しいスライドを作成してみましょう。</p>
          <div className="mt-6">
            <Link
              href="/slides/new"
              className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              新規スライド作成
            </Link>
          </div>
        </div>
      ) : filteredSlides.length === 0 ? (
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
          <h3 className="mt-2 text-sm font-medium text-gray-900">検索結果がありません</h3>
          <p className="mt-1 text-sm text-gray-500">検索条件を変更してみてください。</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {filteredSlides.map((slide) => (
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
                        <span
                          className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                            slide.is_public
                              ? 'bg-green-100 text-green-800'
                              : 'bg-yellow-100 text-yellow-800'
                          }`}
                        >
                          {slide.is_public ? '公開' : '非公開'}
                        </span>
                        <span className="ml-2 text-sm text-gray-500">
                          {new Date(slide.updated_at).toLocaleDateString()}
                        </span>
                      </div>
                      <div className="mt-1 text-xs text-gray-500">
                        作成者: {slide.owner_username}
                      </div>
                    </div>
                  </div>
                  {/* プレビュー部分をクリッカブルに */}
                  <Link href={`/slides/${slide.id}`}>
                    <div className="mt-4 border rounded-md p-2 overflow-hidden cursor-pointer hover:bg-gray-50 transition-colors duration-200" style={{ height: '180px' }}>
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
                            <div dangerouslySetInnerHTML={{ __html: slidePreviews[slide.id] || '' }} />
                          )}
                        </div>
                      </div>
                    </div>
                  </Link>
                  {/* 統計情報の表示 */}
                  <div className="mt-4 flex items-center justify-between text-sm text-gray-500">
                    <div className="flex items-center space-x-4">
                      <div className="flex items-center">
                        <svg className="w-5 h-5 mr-1" fill="currentColor" viewBox="0 0 20 20">
                          <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                          <path fillRule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clipRule="evenodd" />
                        </svg>
                        <span>{slide.views}</span>
                      </div>
                      <div className="flex items-center">
                        <svg className="w-5 h-5 mr-1" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd" />
                        </svg>
                        <span>{slide.likes}</span>
                      </div>
                    </div>
                    <span className="text-sm text-gray-500">
                      {new Date(slide.updated_at).toLocaleDateString()}
                    </span>
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
                  {/* 編集と削除ボタンはマイスライドページのみに表示 */}
                  {location.pathname === '/' && (
                    <>
                      <Link
                        href={`/slides/${slide.id}/edit`}
                        className="text-sm font-medium text-indigo-600 hover:text-indigo-500"
                      >
                        編集
                      </Link>
                      <button
                        onClick={() => handleDeleteSlide(slide.id)}
                        className="text-sm font-medium text-red-600 hover:text-red-500"
                      >
                        削除
                      </button>
                    </>
                  )}
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
