import { useState, useEffect } from 'react';
import { Card, CardContent, Typography, CardActions, Button, IconButton, Box } from '@mui/material';
import { Favorite, FavoriteBorder, Visibility } from '@mui/icons-material';
import Link from 'next/link';
import { toggleLike, getLikeStatus } from '../api/slidesApi';

interface SlideCardProps {
  id: number;
  title: string;
  content: string;
  isPublic: boolean;
  ownerUsername: string;
  likes: number;
  views: number;
  isOwner?: boolean;
  onDelete?: (id: number) => void;
}

export default function SlideCard({ id, title, content, ownerUsername, likes, views, isOwner, onDelete }: SlideCardProps) {
  const [likeCount, setLikeCount] = useState(likes);
  const [hasLiked, setHasLiked] = useState(false);

  useEffect(() => {
    const checkLikeStatus = async () => {
      try {
        const status = await getLikeStatus(id);
        setHasLiked(status.has_liked);
      } catch (error) {
        console.error('Failed to check like status:', error);
      }
    };

    checkLikeStatus();
  }, [id]);

  const handleLikeClick = async () => {
    try {
      await toggleLike(id);
      setHasLiked(!hasLiked);
      setLikeCount(prev => hasLiked ? prev - 1 : prev + 1);
    } catch (error) {
      console.error('Failed to toggle like:', error);
    }
  };

  return (
    <Card variant="outlined" sx={{ mb: 2 }}>
      <CardContent>
        <Typography variant="h5" component="div">
          {title}
        </Typography>
        <Typography sx={{ mb: 1.5 }} color="text.secondary">
          作成者: {ownerUsername}
        </Typography>
        <Typography variant="body2">
          {content.length > 100 ? `${content.substring(0, 100)}...` : content}
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mr: 2 }}>
            <Visibility fontSize="small" sx={{ mr: 0.5 }} />
            <Typography variant="body2">{views}</Typography>
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            {hasLiked ?
              <Favorite fontSize="small" sx={{ mr: 0.5, color: 'red' }} /> :
              <FavoriteBorder fontSize="small" sx={{ mr: 0.5 }} />
            }
            <Typography variant="body2">{likeCount}</Typography>
          </Box>
        </Box>
      </CardContent>
      <CardActions>
        <Button size="small" component={Link} href={`/slides/${id}`}>
          詳細を見る
        </Button>
        <IconButton size="small" onClick={handleLikeClick} aria-label="いいね">
          {hasLiked ? <Favorite color="error" /> : <FavoriteBorder />}
        </IconButton>
        {isOwner && (
          <Button size="small" color="error" onClick={() => onDelete && onDelete(id)}>
            削除
          </Button>
        )}
      </CardActions>
    </Card>
  );
}