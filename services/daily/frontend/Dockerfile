# Stage 2 - Serve frontend
FROM nginx:alpine

# Arg set when building with:
# docker build --build-arg URL="http://localhost:8000/reports/" -t daily-frontend .
ARG URL="http://localhost:8000/reports/"


# Replace all this when we build the frontend properly
# sed for `        var url = "http://localhost:8000/reports/"`
# and change it to URL
COPY ./public /usr/share/nginx/html
RUN sed -i "s|http://localhost:8000/reports/|$URL|g" /usr/share/nginx/html/index.html
