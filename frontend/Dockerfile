FROM node:16.16-bullseye

WORKDIR /app

COPY package.json yarn.lock tsconfig.json ./
COPY next.config.js next.config.js

COPY .env.local .env.local
COPY pages ./pages
COPY public ./public
COPY styles ./styles
COPY comps ./comps

RUN yarn install
RUN yarn build
CMD ["yarn", "start"]
# CMD ["yarn", "dev"]  -> For development