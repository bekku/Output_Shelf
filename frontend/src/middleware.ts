import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// 認証が不要なパス
const publicPaths = ['/login', '/register', '/public-slides'];

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')?.value;
  const { pathname } = request.nextUrl;

  // 認証が不要なパスの場合はスキップ
  if (publicPaths.includes(pathname) || pathname === '/') {
    return NextResponse.next();
  }

  // トークンがない場合はログインページにリダイレクト
  if (!token) {
    const url = new URL('/login', request.url);
    return NextResponse.redirect(url);
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * 以下のパスを除外:
     * - api (API routes)
     * - _next/static (静的ファイル)
     * - _next/image (画像最適化API)
     * - favicon.ico (ファビコン)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};