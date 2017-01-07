FROM frolvlad/alpine-python3

#RUN apk --update add python3 && rm -f /var/cache/apk/*
RUN adduser -S bot
RUN mkdir /bot
WORKDIR /bot
COPY . /bot/spylist
WORKDIR /bot/spylist
RUN pip install -r requirements.txt
USER bot