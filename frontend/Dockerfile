FROM node:16.16-bullseye

WORKDIR /app

COPY package.json yarn.lock tsconfig.json ./
COPY next.config.js next.config.js
RUN yarn install

COPY .env.local .env.local
COPY pages ./pages
COPY public ./public
COPY styles ./styles
COPY comps ./comps


CMD ["yarn", "dev"]  # start doesnt work, ill fix it later