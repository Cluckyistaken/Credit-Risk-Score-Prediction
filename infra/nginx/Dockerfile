# infra/nginx/Dockerfile
# Minimal nginx image that expects:
# - TLS cert files mounted to /etc/ssl/certs/fullchain.pem and /etc/ssl/private/privkey.pem
# - Optionally /var/www/certbot for ACME challenge
# - Configuration mounted at /etc/nginx/nginx.conf (or build-time copy)

FROM nginx:1.26-alpine

LABEL maintainer="your-team@example.com"

# create directories for certbot/webroot if needed
RUN mkdir -p /var/www/certbot /etc/ssl/certs /etc/ssl/private

# Copy default nginx.conf if you want to bake it in the image.
# If you prefer mounting at runtime, comment this out and mount with -v.
COPY nginx.conf /etc/nginx/nginx.conf

# Expose ports (80 and 443)
EXPOSE 80 443

# Healthcheck (simple)
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD [ "sh", "-c", "wget -q -O - http://127.0.0.1/healthz || exit 1" ]

# Run as non-root in production if you configure users properly (left as default nginx user)
CMD ["nginx", "-g", "daemon off;"]
