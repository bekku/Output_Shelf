interface LikeStatus {
  has_liked: boolean;
}

export async function toggleLike(slideId: number): Promise<void> {
  const token = localStorage.getItem('token');
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/api/slides/${slideId}/like`,
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error('いいねの更新に失敗しました');
  }
}

export async function getLikeStatus(slideId: number): Promise<LikeStatus> {
  const token = localStorage.getItem('token');
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/api/slides/${slideId}/like`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error('いいねの状態の取得に失敗しました');
  }

  return response.json();
}
