# Stage 1 - the build process
FROM node:20 AS build-deps
WORKDIR /usr/src/app

# Copy 'package.json' and 'package-lock.json' (if available)
COPY package*.json ./

# Install project dependencies
RUN npm install

# Bundle app source
COPY . .

# Build for production.
RUN npm run build

# Stage 2 - the production environment
FROM nginx:1.17.9-alpine

# Copy nginx configuration
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

# Copy build output from Stage 1
COPY --from=build-deps /usr/src/app/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
