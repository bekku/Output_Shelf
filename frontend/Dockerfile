FROM node:20-alpine AS builder

# build tools の追加
RUN apk add --no-cache \
    python3 \
    make \
    g++ \
    && npm install -g npm

WORKDIR /app
RUN mkdir -p /app/.next
RUN mkdir -p /app/node_modules

COPY package*.json ./

RUN npm install
RUN npm install react-icons @mui/material @emotion/react @emotion/styled @mui/icons-material
RUN npm install --save-dev @types/node @types/react @types/react-dom @types/js-cookie

COPY . .

# ビルド時の環境変数を引数として受け取る
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

# ビルド
RUN npm run build

# 本番環境で実行
CMD ["npx", "next", "start"]
