from datetime import datetime


def get_MIME_type(url: str) -> str:
    """
    Получение MIME-типа для формирования заголовка.
    """
    types: dict[str, str] = {'html': r"text\html", "png": 'image', "pdf": "application/pdf"}
    if not url:
        return "text/plain"
    return types[url.split(".")[1]]


class HTTPHeader:
    """
    Реализация п.п. 1.
    """
    def __init__(self, type: str, url: str, status: str, content: bytes):
        self.method = type
        self.path = url
        self.protocol = 'HTTP/1.1'
        self.date = datetime.now().strftime(
            "%A, %d %b %Y %X %Z")
        self.content_type = get_MIME_type(url)
        self.server = 'localhost'
        self.content_length = len(content)
        self.connection = 'keep-alive'
        self.keep_alive = "timeout=5, max=5"
        self.status_code = status

    def get_response(self) -> bytes:
        return f"{self.protocol} {self.status_code}\r\n" \
               f"Connection: {self.connection}\r\n" \
               f"Keep-Alive: {self.keep_alive}\r\n"\
               f"Content-Length: {self.content_length}\r\n" \
               f"Server: {self.server}\r\n" \
               f"Content-Type: {self.content_type}\r\n" \
               f"Date: {self.date}\r\n\r\n".encode()
