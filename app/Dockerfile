FROM node:14.16.1

RUN mkdir -p /frontend
COPY . /frontend

WORKDIR /frontend
RUN npm install

EXPOSE 3000

CMD if [ ${APP_MODE} = production ];\
    then\
    npm install -g serve &&\
    npm run build &&\
    serve -s build;\
    else\
    npm start;\
    fi