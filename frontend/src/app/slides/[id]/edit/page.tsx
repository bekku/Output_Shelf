'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useAuth } from '@/app/contexts/AuthContext';
import Link from 'next/link';

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

export default function EditSlide() {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [isPublic, setIsPublic] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [preview, setPreview] = useState(false);
  const [fetchLoading, setFetchLoading] = useState(true);
  const params = useParams();
  const router = useRouter();
  const { isAuthenticated, isLoading: authLoading } = useAuth();
  const slideId = params.id;

  useEffect(() => {
    if (slideId && isAuthenticated) {
      fetchSlide();
    }
  }, [slideId, isAuthenticated]);

  const fetchSlide = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/slides/${slideId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.status === 404) {
        setError('スライドが見つかりません');
        setFetchLoading(false);
        return;
      }

      if (response.status === 403) {
        setError('このスライドを編集する権限がありません');
        setFetchLoading(false);
        return;
      }

      if (!response.ok) {
        throw new Error('スライドの取得に失敗しました');
      }

      const data: Slide = await response.json();

      // スライドが自分のものでない場合は編集不可
      const userEmail = localStorage.getItem('user_email');
      if (data.owner_email !== userEmail) {
        setError('このスライドを編集する権限がありません');
        setFetchLoading(false);
        return;
      }

      setTitle(data.title);
      setContent(data.content);
      setIsPublic(data.is_public);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setFetchLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/slides/${slideId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          title,
          content,
          is_public: isPublic,
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'スライドの更新に失敗しました');
      }

      // 更新成功後、スライド詳細ページにリダイレクト
      router.push(`/slides/${slideId}`);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  if (authLoading || fetchLoading) {
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
    router.push('/login');
    return null;
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

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="md:grid md:grid-cols-3 md:gap-6">
        <div className="md:col-span-1">
          <div className="px-4 sm:px-0">
            <h3 className="text-lg font-medium leading-6 text-gray-900">スライド編集</h3>
            <p className="mt-1 text-sm text-gray-600">
              HTMLやSVG形式でスライドコンテンツを編集できます。
            </p>
            <div className="mt-6">
              <button
                type="button"
                onClick={() => setPreview(!preview)}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700"
              >
                {preview ? 'エディタに戻る' : 'プレビュー'}
              </button>
            </div>
            <div className="mt-4">
              <Link
                href={`/slides/${slideId}`}
                className="text-indigo-600 hover:text-indigo-500"
              >
                編集をキャンセル
              </Link>
            </div>
          </div>
        </div>
        <div className="mt-5 md:mt-0 md:col-span-2">
          {error && (
            <div className="p-4 mb-6 text-sm text-red-700 bg-red-100 rounded-lg" role="alert">
              {error}
            </div>
          )}

          {preview ? (
            <div className="shadow sm:rounded-md sm:overflow-hidden">
              <div className="px-4 py-5 bg-white space-y-6 sm:p-6">
                <h2 className="text-xl font-bold">{title || 'タイトルなし'}</h2>
                <div
                  className="border p-4 rounded-md min-h-[400px]"
                  dangerouslySetInnerHTML={{ __html: content }}
                />
              </div>
            </div>
          ) : (
            <form onSubmit={handleSubmit}>
              <div className="shadow sm:rounded-md sm:overflow-hidden">
                <div className="px-4 py-5 bg-white space-y-6 sm:p-6">
                  <div>
                    <label htmlFor="title" className="block text-sm font-medium text-gray-700">
                      タイトル
                    </label>
                    <input
                      type="text"
                      name="title"
                      id="title"
                      value={title}
                      onChange={(e) => setTitle(e.target.value)}
                      required
                      className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                    />
                  </div>

                  <div>
                    <label htmlFor="content" className="block text-sm font-medium text-gray-700">
                      コンテンツ (HTML/SVG)
                    </label>
                    <div className="mt-1">
                      <textarea
                        id="content"
                        name="content"
                        rows={15}
                        value={content}
                        onChange={(e) => setContent(e.target.value)}
                        required
                        className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 mt-1 block w-full sm:text-sm border border-gray-300 rounded-md font-mono"
                        placeholder="<div>スライドコンテンツをここに入力</div>"
                      />
                    </div>
                    <p className="mt-2 text-sm text-gray-500">
                      HTMLまたはSVG形式でスライドコンテンツを入力してください。
                    </p>
                  </div>

                  <div className="flex items-start">
                    <div className="flex items-center h-5">
                      <input
                        id="is_public"
                        name="is_public"
                        type="checkbox"
                        checked={isPublic}
                        onChange={(e) => setIsPublic(e.target.checked)}
                        className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
                      />
                    </div>
                    <div className="ml-3 text-sm">
                      <label htmlFor="is_public" className="font-medium text-gray-700">
                        公開する
                      </label>
                      <p className="text-gray-500">
                        チェックを外すと、あなただけがこのスライドを閲覧できます。
                      </p>
                    </div>
                  </div>
                </div>
                <div className="px-4 py-3 bg-gray-50 text-right sm:px-6">
                  <button
                    type="submit"
                    disabled={isLoading}
                    className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    {isLoading ? '更新中...' : '更新'}
                  </button>
                </div>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}