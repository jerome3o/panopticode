FROM buildkite/puppeteer:10.0.0

WORKDIR /app
COPY package* ./
RUN npm install
COPY index.js .
RUN mkdir img

CMD [ "npm", "run", "start" ]