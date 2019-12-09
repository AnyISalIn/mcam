# build
FROM node:11.12.0-alpine as build-vue
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY ./client/package*.json ./
RUN npm install
COPY ./client .
RUN npm run build:prod

# production
FROM nginx:stable-alpine as production
WORKDIR /app
VOLUME ["/plans"]

ENV PIP_INDEX_URL https://pypi.tuna.tsinghua.edu.cn/simple

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

RUN apk --no-cache add python3 \
                       build-base \
                       python3-dev \
                       supervisor \
                       openssl \
                       git \
                       bash \
                       sudo \
                       py3-pip \
                       jpeg-dev \
                       zlib-dev \
                       freetype-dev \
                       lcms2-dev \
                       openjpeg-dev \
                       tiff-dev \
                       tk-dev \
                       tcl-dev \
                       harfbuzz-dev \
                       fribidi-dev

COPY ./server/requirements.txt ./
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

RUN wget -qO- https://releases.hashicorp.com/terraform/0.12.17/terraform_0.12.17_linux_amd64.zip | busybox unzip -d /usr/local/bin - && chmod +x /usr/local/bin/terraform

RUN echo 'plugin_cache_dir   = "$HOME/.terraform.d/plugin-cache"' > ~/.terraformrc

COPY ./entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]

COPY --from=build-vue /app/dist /usr/share/nginx/html
COPY ./etc/nginx.conf /etc/nginx/conf.d/default.conf

COPY etc/supervisord.conf /etc/supervisord.conf

COPY ./server .
CMD flask init-data && gunicorn -b 0.0.0.0:5000 app:app --daemon --access-logfile access.log --error-logfile error.log && \
      sed -i -e 's/$PORT/'"$PORT"'/g' /etc/nginx/conf.d/default.conf && \
      nginx -g 'daemon off;'