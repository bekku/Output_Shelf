export interface Slide {
  id: number;
  title: string;
  content: string;
  is_public: boolean;
  owner_id: number;
  owner_username: string;
  created_at: string;
  updated_at: string;
  likes: number;
  views: number;
}export interface ApiError {
  message: string;
  status?: number;
}

export interface ApiResponse<T> {
  data: T;
  error?: ApiError;
}

export interface FormError {
  message: string;
  field?: string;
}

