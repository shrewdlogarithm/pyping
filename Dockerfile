FROM node:14-alpine

# install dependencies
WORKDIR /app
COPY rollup.config.js ./
COPY package*.json ./
RUN npm install

COPY ./public ./public
COPY ./data ./data
COPY ./src ./src
RUN npm run-script build

FROM python:3.9.1

WORKDIR /app

COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY --from=0 ./app/public/ /app/public/
COPY --from=0 ./app/data/ /app/data/
COPY *.py ./

CMD ["python", "runping.py"]