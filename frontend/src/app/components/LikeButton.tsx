'use client';

import { useState, useEffect } from 'react';
import { toggleLike, getLikeStatus } from '../services/slideService';
import { FaHeart, FaRegHeart } from 'react-icons/fa';

interface LikeButtonProps {
  slideId: number;
  initialLikes: number;
}

export default function LikeButton({ slideId, initialLikes }: LikeButtonProps) {
  const [hasLiked, setHasLiked] = useState(false);
  const [likes, setLikes] = useState(initialLikes);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchLikeStatus = async () => {
      try {
        const { has_liked } = await getLikeStatus(slideId);
        setHasLiked(has_liked);
      } catch (error) {
        console.error('Error fetching like status:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchLikeStatus();
  }, [slideId]);

  const handleLikeClick = async () => {
    try {
      await toggleLike(slideId);
      setHasLiked(!hasLiked);
      setLikes(prev => hasLiked ? prev - 1 : prev + 1);
    } catch (error) {
      console.error('Error toggling like:', error);
    }
  };

  if (isLoading) {
    return <span>Loading...</span>;
  }

  return (
    <button
      onClick={handleLikeClick}
      className="flex items-center gap-1 text-sm"
      aria-label={hasLiked ? "Unlike slide" : "Like slide"}
    >
      {hasLiked ? (
        <FaHeart className="text-red-500" />
      ) : (
        <FaRegHeart />
      )}
      <span>{likes}</span>
    </button>
  );
}