import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// 認証が不要なパス
const publicPaths = ['/login', '/register', '/public-slides'];

export function middleware(request: NextRequest) {
  // パス名を取得
  const pathname = request.nextUrl.pathname;

  // 認証が不要なパスの場合はスキップ
  if (publicPaths.some(path => pathname.startsWith(path)) || pathname === '/') {
    return NextResponse.next();
  }

  // トークンがない場合はログインページにリダイレクト
  const token = request.cookies.get('token')?.value;
  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

// マッチャーを具体的なパスに変更
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