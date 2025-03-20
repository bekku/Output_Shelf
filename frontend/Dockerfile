FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install
RUN npm install react-icons

COPY . .

EXPOSE 3000

# CMD ["npm", "run", "dev"]
CMD ["npm", "run", "production"]