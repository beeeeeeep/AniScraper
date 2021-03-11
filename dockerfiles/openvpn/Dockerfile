FROM dperson/openvpn-client

ARG OPENVPN_PROFILE_PATH

ENV OPENVPN_PROFILE_PATH $OPENVPN_PROFILE_PATH

WORKDIR /

ADD ${OPENVPN_PROFILE_PATH} /vpn/vpn.conf

ADD vpn_credentials.conf /vpn/vpn_credentials.conf

ADD vpn-ca.crt /vpn/vpn-ca.crt

RUN cat /vpn/vpn.conf
