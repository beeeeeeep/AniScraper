import socket
from typing import List
import xmlrpc.client
import re


class RTorrentSCGI:
    def __init__(self, socket_path: str) -> None:
        self.socket_path = socket_path

    @staticmethod
    def __value(value):
        if isinstance(value, str):
            type = "string"
        elif isinstance(value, int) or isinstance(value, float):
            type = "double"
        elif isinstance(value, bool):
            type = "boolean"
            value = "1" if value else "0"
        return f"<value><{type}>{value}</{type}></value>"

    @staticmethod
    def __params(params: List[str]):
        if len(params) == 0:
            return ""
        params_xml = "".join(list(map(lambda x: f"<param>{RTorrentSCGI.__value(x)}</param>", params)))
        return f"<params>{params_xml}</params>"

    def request(self, request: str, *params: str):
        request_xml = f'<?xml version="1.0"?><methodCall><methodName>{request}</methodName>'\
            f'{self.__params(params)}</methodCall>'
        headers = {
            "CONTENT_LENGTH": str(len(request_xml)),
            "CONTENT_TYPE": "text/xml",
            "SCGI": "1"
        }
        headers_scgi = "".join([f"{x}\x00{y}\x00" for x, y in headers.items()])
        headers_scgi = f"{len(headers_scgi)}:{headers_scgi}"
        request_body = f"{headers_scgi},{request_xml}"

        print(request_body)

        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(self.socket_path)
            sock.send(request_body.encode("UTF-8"))
            return self.parse_response(sock.makefile())
        finally:
            if sock:
                sock.close()
        
    def parse_response(self, response):
        p, u = xmlrpc.client.getparser()

        response_text = ""

        while True:
            data = response.read(1024)
            if not data:
                break
            response_text += data

        response_header, response_body = re.split(r"\n *?\n", response_text, maxsplit=1)

        p.feed(response_body)
        p.close()
        response.close()

        return u.close()
