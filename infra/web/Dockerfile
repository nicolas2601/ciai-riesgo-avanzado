# Static SPA. Build dist first (cd app/web && VITE_API_URL=... bun run build), then from the repo root:
# docker build -f infra/web/Dockerfile -t ciai-web:local .
FROM nginxinc/nginx-unprivileged:alpine
COPY infra/web/nginx.conf /etc/nginx/conf.d/default.conf
COPY app/web/dist /usr/share/nginx/html
EXPOSE 8080
