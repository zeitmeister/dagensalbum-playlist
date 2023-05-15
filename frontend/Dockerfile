FROM node:18-alpine
ENV NODE_ENV=production
RUN mkdir /app
RUN mkdir /app/logs

WORKDIR /app

COPY ["package.json", "package-lock.json*", "./"]
COPY dagensalbum.log ./logs/
RUN npm install --production

COPY . .

CMD ["npm", "start"]
