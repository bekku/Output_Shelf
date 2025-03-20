'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useAuth } from '@/app/contexts/AuthContext';
import Link from 'next/link';

interface Slide {
  id: number;
  title: string;
  content: string;
  is_public: boolean;
  owner_id: string;
  owner_username: string;
  created_at: string;
  updated_at: string;
}

export default function SlideDetail() {
  const [slide, setSlide] = useState<Slide | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [currentPage, setCurrentPage] = useState(0);
  const [pages, setPages] = useState<string[]>([]);
  const [isSlideshow, setIsSlideshow] = useState(false);
  const params = useParams();
  const router = useRouter();
  const { isAuthenticated } = useAuth();
  const slideId = params.id;

  useEffect(() => {
    if (slideId) {
      fetchSlide();
    }
  }, [slideId]);

  // URLクエリパラメータを確認して、slideshow=trueの場合は自動的にスライドショーモードを開始
  useEffect(() => {
    const searchParams = new URLSearchParams(window.location.search);
    if (searchParams.get('slideshow') === 'true' && !loading && slide) {
      setIsSlideshow(true);
    }
  }, [loading, slide]);

  // キーボードイベントのリスナーを追加
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (isSlideshow) {
        if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'n') {
          nextPage();
        } else if (e.key === 'ArrowLeft' || e.key === 'p') {
          prevPage();
        } else if (e.key === 'Escape') {
          setIsSlideshow(false);
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [isSlideshow, currentPage, pages.length]);

  // スライドショーを開始する
  const startSlideshow = () => {
    setIsSlideshow(true);
  };

  // スライドショーを終了する
  const exitSlideshow = () => {
    setIsSlideshow(false);
  };

  // スライドコンテンツをページに分割する関数
  const splitContentIntoPages = (content: string) => {
    // ページ区切りとなる可能性のあるタグやクラスを探す
    // 一般的なパターン: <div class="page">...</div> または <section>...</section>
    const pagePattern = /<div[^>]*class="[^"]*page[^"]*"[^>]*>[\s\S]*?<\/div>|<section[^>]*>[\s\S]*?<\/section>/g;
    const matches = content.match(pagePattern);

    if (matches && matches.length > 0) {
      return matches;
    } else {
      // SVGコンテンツかどうかを確認
      if (content.trim().startsWith('<svg')) {
        // SVGコンテンツの場合は、そのまま1ページとして扱う
        return [content];
      } else {
        // ページ区切りが見つからない場合は、コンテンツ全体を1ページとして扱う
        return [content];
      }
    }
  };

  const fetchSlide = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers: HeadersInit = {};

      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`http://localhost:8000/api/slides/${slideId}`, {
        headers,
      });

      if (response.status === 404) {
        setError('スライドが見つかりません');
        setLoading(false);
        return;
      }

      if (response.status === 403) {
        setError('このスライドを閲覧する権限がありません');
        setLoading(false);
        return;
      }

      if (!response.ok) {
        throw new Error('スライドの取得に失敗しました');
      }

      const data = await response.json();
      setSlide(data);

      // コンテンツをページに分割
      const pageContents = splitContentIntoPages(data.content);
      setPages(pageContents);
      // 最初のページを表示
      setCurrentPage(0);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // 次のページに進む
  const nextPage = () => {
    if (currentPage < pages.length - 1) {
      setCurrentPage(currentPage + 1);
    }
  };

  // 前のページに戻る
  const prevPage = () => {
    if (currentPage > 0) {
      setCurrentPage(currentPage - 1);
    }
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

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
          <strong className="font-bold">エラー: </strong>
          <span className="block sm:inline">{error}</span>
        </div>
        <div className="mt-4">
          <Link href="/" className="text-indigo-600 hover:text-indigo-500">
            ホームに戻る
          </Link>
        </div>
      </div>
    );
  }

  if (!slide) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded relative" role="alert">
          <strong className="font-bold">注意: </strong>
          <span className="block sm:inline">スライドが見つかりません</span>
        </div>
        <div className="mt-4">
          <Link href="/" className="text-indigo-600 hover:text-indigo-500">
            ホームに戻る
          </Link>
        </div>
      </div>
    );
  }

  // スライドショーモード
  if (isSlideshow) {
    return (
      <div className="fixed inset-0 bg-black flex flex-col">
        {/* ヘッダー部分 */}
        <div className="flex items-center justify-between px-4 py-2 bg-gray-800 text-white">
          <h2 className="text-xl font-bold truncate max-w-md">{slide.title}</h2>
          <div className="flex items-center space-x-4">
            <button
              onClick={exitSlideshow}
              className="ml-4 bg-red-600 text-white px-4 py-1 rounded hover:bg-red-700"
            >
              終了
            </button>
          </div>
        </div>

        {/* スライドコンテンツ */}
        <div className="flex-1 flex items-center justify-center overflow-auto p-4 bg-white">
          <div
            className="max-w-full max-h-full w-full h-full flex items-center justify-center"
          >
            {pages[currentPage]?.trim().startsWith('<svg') ? (
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
                dangerouslySetInnerHTML={{ __html: pages[currentPage] || '' }}
              />
            ) : (
              // 通常のHTMLコンテンツの場合
              <div
                className="html-container"
                style={{ maxWidth: '100%', maxHeight: '100%' }}
                dangerouslySetInnerHTML={{ __html: pages[currentPage] || '' }}
              />
            )}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6 flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">{slide?.title}</h1>
        <div className="flex space-x-4">
          <Link href="/" className="text-indigo-600 hover:text-indigo-500">
            ホームに戻る
          </Link>
          {isAuthenticated && (
            <Link
              href={`/slides/${slide.id}/edit`}
              className="text-indigo-600 hover:text-indigo-500"
            >
              編集
            </Link>
          )}
        </div>
      </div>

      <div className="bg-white shadow overflow-hidden sm:rounded-lg">
        <div className="px-4 py-5 sm:px-6 flex justify-between">
          <div>
            <span
              className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                slide?.is_public ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
              }`}
            >
              {slide?.is_public ? '公開' : '非公開'}
            </span>
            <span className="ml-2 text-sm text-gray-500">
              最終更新: {slide && new Date(slide.updated_at).toLocaleString()}
            </span>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={startSlideshow}
              className="px-3 py-1 rounded bg-indigo-600 text-white hover:bg-indigo-700"
            >
              スライドショー
            </button>
          </div>
        </div>
        <div className="border-t border-gray-200">
          <div className="px-4 py-5 sm:p-6">
            <div
              className="prose max-w-none"
              dangerouslySetInnerHTML={{ __html: pages[currentPage] || '' }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}