'use client';

import { useEffect, useState, useCallback } from 'react';
import { useParams } from 'next/navigation';
import { useAuth } from '@/app/contexts/AuthContext';
import Link from 'next/link';
import { Slide } from '@/app/types';
import { splitContentIntoPages } from '@/app/utils/slide';

export default function SlideDetail() {
  const params = useParams();
  const id = params.id as string;
  const { user } = useAuth();
  const [slide, setSlide] = useState<Slide | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [pages, setPages] = useState<string[]>([]);
  const [isSlideshow, setIsSlideshow] = useState(false);
  const [isLiked, setIsLiked] = useState(false);

  const nextPage = useCallback(() => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  }, [currentPage, totalPages]);

  const prevPage = useCallback(() => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  }, [currentPage]);

  const fetchSlide = useCallback(async () => {
    try {
      setIsLoading(true);
      const token = localStorage.getItem('token');
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/slides/${id}`,
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
      setSlide(data);
      const pageContents = splitContentIntoPages(data.content);
      console.log('Split content into pages:', {
        totalPages: pageContents.length,
        firstPage: pageContents[0]?.substring(0, 100)
      });
      setPages(pageContents);
      setTotalPages(pageContents.length);

      // 表示時にビューカウントをインクリメント
      const incrementView = async () => {
        try {
          await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/slides/${id}/view`, {
            method: 'POST',
          });
        } catch (error) {
          console.error('Failed to increment view count:', error);
        }
      };
      incrementView();
    } catch (error) {
      console.error('Error fetching slide:', error);
      setError(error instanceof Error ? error.message : 'スライドの取得に失敗しました');
    } finally {
      setIsLoading(false);
    }
  }, [id]);

  useEffect(() => {
    if (id) {
      fetchSlide();
    }
  }, [id, fetchSlide]);

  // URLクエリパラメータを確認して、slideshow=trueの場合は自動的にスライドショーモードを開始
  useEffect(() => {
    const searchParams = new URLSearchParams(window.location.search);
    if (searchParams.get('slideshow') === 'true' && !isLoading && slide) {
      setIsSlideshow(true);
    }
  }, [isLoading, slide]);

  // キーボードイベントのリスナーを追加
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight') {
        nextPage();
      } else if (e.key === 'ArrowLeft') {
        prevPage();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [nextPage, prevPage]);

  // スライドショーを開始する
  const startSlideshow = () => {
    setIsSlideshow(true);
  };

  // スライドショーを終了する
  const exitSlideshow = () => {
    setIsSlideshow(false);
  };

  const handleLike = async () => {
    if (!user) {
      alert('いいねするにはログインが必要です。');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/slides/${id}/like`,
        {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      const data = await response.json();
      setIsLiked(data.liked);
      setSlide(prev => prev ? {
        ...prev,
        likes: data.liked ? prev.likes + 1 : prev.likes - 1
      } : null);
    } catch (error) {
      console.error('Failed to toggle like:', error);
    }
  };

  // スライドの所有者かどうかを判定する関数
  const isOwner = () => {
    return slide && user && slide.owner_id === user.id;
  };

  if (isLoading) {
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
            className="w-full h-full flex items-center justify-center"
            style={{
              maxWidth: '90vw',
              maxHeight: '90vh',
              margin: 'auto'
            }}
          >
            {(() => {
              const adjustedPageIndex = currentPage - 1;
              const currentContent = pages[adjustedPageIndex] || '';
              return currentContent.trim().startsWith('<svg') ? (
                <div
                  className="svg-container"
                  style={{
                    width: '100%',
                    height: '100%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    overflow: 'hidden'
                  }}
                  dangerouslySetInnerHTML={{ __html: currentContent }}
                />
              ) : (
                <div
                  className="html-container"
                  style={{
                    width: '100%',
                    height: '100%',
                    overflow: 'auto',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}
                  dangerouslySetInnerHTML={{ __html: currentContent }}
                />
              );
            })()}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 overflow-auto"
      style={{ height: '100vh' }}
    >
      <div className="mb-6 flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">{slide?.title}</h1>
        <div className="flex space-x-4">
          <Link href="/" className="text-indigo-600 hover:text-indigo-500">
            ホームに戻る
          </Link>
          {isOwner() && (
            <Link
              href={`/slides/${slide.id}/edit`}
              className="text-indigo-600 hover:text-indigo-500"
            >
              編集
            </Link>
          )}
        </div>
      </div>

      <div className="mt-4 flex items-center justify-between border-t pt-4">
        <div className="flex items-center space-x-6">
          <div className="flex items-center text-gray-500">
            <svg className="w-5 h-5 mr-1" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
              <path fillRule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clipRule="evenodd" />
            </svg>
            <span>{slide?.views || 0} 回視聴</span>
          </div>
          <button
            onClick={handleLike}
            className={`flex items-center space-x-2 px-4 py-2 rounded-md ${
              isLiked ? 'bg-pink-500 text-white' : 'bg-gray-100 text-gray-500'
            }`}
          >
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd" />
            </svg>
            <span>{slide?.likes || 0}</span>
          </button>
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
              style={{
                height: 'auto',
                maxHeight: 'none',
                overflowY: 'visible',
                padding: '1rem',
                border: '1px solid #e5e7eb',
                borderRadius: '0.375rem'
              }}
              dangerouslySetInnerHTML={{ __html: pages[currentPage - 1] || '' }}
            />
          </div>
        </div>
      </div>

      {/* スライド作成者情報 */}
      <div className="mt-4 text-sm text-gray-500">
        作成者: {slide?.owner_username}
        <span className="mx-2">•</span>
        作成日: {slide && new Date(slide.created_at).toLocaleDateString()}
        {slide?.updated_at !== slide?.created_at && (
          <>
            <span className="mx-2">•</span>
            更新日: {new Date(slide?.updated_at).toLocaleDateString()}
          </>
        )}
      </div>
    </div>
  );
}