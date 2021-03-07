FROM python

ADD ./dockerfiles/deluged/start.sh /start.sh

RUN chmod +x /start.sh

RUN apt update && \
    apt install -y deluged deluge-web

CMD ["/start.sh"]
