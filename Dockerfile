FROM node:14-alpine

# install dependencies
WORKDIR /app/svelte
COPY ./svelte/rollup.config.js .
COPY ./svelte/package.json .
RUN npm install

COPY ./svelte/public public
COPY ./svelte/src src
RUN npm run-script build

FROM python:3.9.1

WORKDIR /app

COPY ./data ./data
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY --from=0 ./app/svelte/public/ /app/svelte/public/
COPY *.py ./

CMD ["python", "runping.py"]