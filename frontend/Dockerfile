FROM node:22-alpine AS build
WORKDIR /app
ARG VITE_API_URL=/api
COPY . .
RUN sed -i "s|http://localhost:3001/api|${VITE_API_URL}|g" src/api.js

FROM node:22-alpine
WORKDIR /app
ENV PORT=3000
EXPOSE 3000
RUN npm install -g serve@14
COPY --from=build /app ./
CMD ["sh", "-c", "serve -l tcp://0.0.0.0:${PORT}"]
