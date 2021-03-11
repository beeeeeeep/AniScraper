FROM httpd

WORKDIR /

RUN apt update && \
    apt install -y git build-essential apache2-dev

RUN git clone https://github.com/nascheme/scgi

RUN cd scgi/apache2 && make && \
echo "\
LoadModule proxy_module /usr/local/apache2/modules/mod_proxy.so\n\
LoadModule proxy_scgi_module /usr/local/apache2/modules/mod_proxy_scgi.so\n\
\
ProxyPass /RPC2 scgi://openvpn:5050\n" >> /usr/local/apache2/conf/httpd.conf
