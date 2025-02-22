from typing import *

from quicly.result import QxResult, QxError, QxFinish
from quicly.urlutils import QxUrl
from quicly.conf import QxGlobalConf

import requests


class QxApiClient(object):
  def __init__(self, url: str, signer: Callable = None, **kw):
    self._url = self._process_url(url)
    self._host = self._process_host(url)
    self._session = kw.get('session', requests.Session())
    self._session.headers.update(kw.get('headers', {}))
    self._session.cookies.update(kw.get('cookies', {}))
    self._signer = signer

  @staticmethod
  def _process_url(url: str):
    url = url.strip().strip('/').strip()

    url_t = url.lower()
    if not url_t.startswith('http://') and not url_t.startswith('https://'):
      url = f'http://{url}'
    url.rstrip('/')

    return url

  @staticmethod
  def _process_host(url: str):
    return url.split('//', maxsplit=1)[1].split('/', maxsplit=1)[0]

  @staticmethod
  def mk_url(url: str, path: str = None, params: dict = None) -> str:
    return QxUrl().set_url(url).join_path(path).set_query(params).mk_url()

  def _mk_url(self, path: str = None, params: dict = None) -> str:
    return self.mk_url(self._url, path, params)

  @staticmethod
  def mk_headers(headers: Union[dict, str] = None) -> dict:
    headers = headers if isinstance(headers, dict) else dict()

    headers.update(QxGlobalConf().get('requests', {}).get('headers', {}))

    return headers

  def _mk_headers(self, headers: Union[dict, str] = None) -> dict:
    headers = self.mk_headers(headers)

    headers.setdefault('Host', self._host)
    headers.setdefault('Origin', self._url)

    return headers

  @staticmethod
  def _process_request_data(data: Union[bytes, str, dict, None]):
    return data

  def raw_request(self, method: str, path: str, **kw):
    method = method.upper()
    assert method in ('GET', 'PUT', 'POST', 'PATCH', 'DELETE')
    url = self._mk_url(path, params=kw.get('params', {}))

    headers = self._mk_headers(kw.get('headers'))

    if callable(self._signer):
      headers = self._signer(method, url, headers)

    kw['headers'] = headers
    kw['data'] = self._process_request_data(kw.get('data'))
    kw.setdefault('verify', False)

    res = self._session.request(method, url, **kw)

    return res

  def raw_get(self, path: str, params: dict = None, **kw):
    return self.raw_request('GET', path, params=params, **kw)

  def raw_put(self, path: str, params: dict = None, data: Union[AnyStr, dict, None] = None, **kw):
    return self.raw_request('PUT', path, params=params, data=data, **kw)

  def raw_post(self, path: str, params: dict = None, data: Union[AnyStr, dict, None] = None, **kw):
    return self.raw_request('POST', path, params=params, data=data, **kw)

  def raw_patch(self, path: str, params: dict = None, data: Union[AnyStr, dict, None] = None, **kw):
    return self.raw_request('PATCH', path, params=params, data=data, **kw)

  def raw_delete(self, path: str, params: dict = None, **kw):
    return self.raw_request('DELETE', path, params=params, **kw)

  @staticmethod
  def _decode_response_text(text: AnyStr):
    if isinstance(text, bytes):
      text = text.decode()
    return text

  def _decode_response(self, res: requests.Response):
    if res.status_code == 200:
      ret = QxFinish(data=self._decode_response_text(res.text))
    else:
      ret = QxError(code=res.status_code, data=self._decode_response_text(res.text))
    return ret

  def request(self, method: str, path: str, **kw):
    return self._decode_response(self.raw_request(method, path, **kw))

  def get(self, path: str, params: dict = None, **kw):
    return self._decode_response(self.raw_get(path, params, **kw))

  def put(self, path: str, params: dict = None, data: Union[AnyStr, dict, None] = None, **kw):
    return self._decode_response(self.raw_put(path, params, data, **kw))

  def post(self, path: str, params: dict = None, data: Union[AnyStr, dict, None] = None, **kw):
    return self._decode_response(self.raw_post(path, params, data, **kw))

  def patch(self, path: str, params: dict = None, data: Union[AnyStr, dict, None] = None, **kw):
    return self._decode_response(self.raw_patch(path, params, data, **kw))

  def delete(self, path: str, params: dict = None, **kw):
    return self._decode_response(self.raw_delete(path, params, **kw))
