// 表示回数をインクリメントする関数
export const incrementViewCount = async (slideId: number): Promise<void> => {
  try {
    await fetch(`${process.env.NEXT_PUBLIC_API_URL}/slides/${slideId}/view`, {
      method: 'POST',
      credentials: 'include',
    });
  } catch (error) {
    console.error('Error incrementing view count:', error);
  }
};

// いいねの状態を切り替える関数
export const toggleLike = async (slideId: number): Promise<{ message: string }> => {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/slides/${slideId}/like`, {
    method: 'POST',
    credentials: 'include',
  });

  if (!response.ok) {
    throw new Error('Failed to toggle like');
  }

  return response.json();
};

// いいねの状態を取得する関数
export const getLikeStatus = async (slideId: number): Promise<{ has_liked: boolean }> => {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/slides/${slideId}/like-status`, {
    credentials: 'include',
  });

  if (!response.ok) {
    throw new Error('Failed to get like status');
  }

  return response.json();
};