FROM node:7.4.0-alpine
ENV PYTHONUNBUFFERED 1

RUN echo 'http://mirrors.aliyun.com/alpine/v3.4/main/' > /etc/apk/repositories
RUN echo 'http://mirrors.aliyun.com/alpine/v3.4/community/' >> /etc/apk/repositories

RUN apk update && apk add bash 
RUN npm config set registry https://registry.npm.taobao.org
RUN npm i -g webpack bower gulp grunt-cli sails pm2