FROM ubuntu

WORKDIR /

RUN apt update && \
    apt install -y rtorrent

ADD .rtorrent.rc /root/.rtorrent.rc

CMD rtorrent -o system.daemon.set=true
