FROM python

RUN echo "deb [trusted=yes] https://deb.jesec.io/ devel main" | tee /etc/apt/sources.list.d/jesec.list && \
    apt update && \
    apt install -y flood

CMD flood -h 0.0.0.0
