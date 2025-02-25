import json
import requests

class HttpError(Exception):
  def __init__(self, message=None, status_code=500):
    super().__init__(message)
    self._status_code = status_code

  def get_status_code(self):
    return self._status_code

class HttpService:
  def __init__(self, base_url: str = None):
    self._base_url = base_url

  def of(self):
    return HttpService(self._base_url)
  
  def on_request_success(self, response: requests.Response):
    pass

  def on_request_error(self, response: requests.Response):
    raise HttpError(response.text, 500)
  
  def get_body(self, body):
    if body is not None:
      if isinstance(body, dict):
        return json.dumps(body)
      elif isinstance(body, str):
        return body
      else:
        raise ValueError('Invalid body type, must be dict or string')
    return None
  
  def get_request_headers(self, options):
    body = options.get('body')
    headers = options.get('headers', {})
    parsed_body = self.get_body(body)

    if parsed_body:
      headers['Content-Length'] = str(len(parsed_body.encode('utf-8')))

    return headers
  
  def request(self, request_options):
    path = request_options.get('path')
    body = request_options.get('body')
    options = {k: v for k, v in request_options.items() if k not in ['path', 'body']}

    parsed_body = self.get_body(body)
    parsed_headers = self.get_request_headers(request_options)

    full_url = f"{self._base_url}/{path}" if self._base_url else path

    try:
      response = requests.request(
        method=options.get('method', 'GET'),
        url=full_url,
        headers=parsed_headers,
        data=parsed_body,
        # **options,
      )
      response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
      raise HttpError(str(http_err), status_code=response.status_code)
    except Exception as err:
      raise HttpError(str(err))

    return {
      'status_code': response.status_code,
      'headers': response.headers,
      'body': response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
    }
