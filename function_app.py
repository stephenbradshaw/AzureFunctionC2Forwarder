import azure.functions as func
import logging
import os
import requests 
import urllib3

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


DEBUG=os.getenv('DEBUG', False) 
TESTPATH=os.getenv('TESTPATH', '/b8af860c6c7f78d5cbcaa86c8f11b268cd0c0295')
PROTOCOL=os.getenv('PROTOCOL', 'http')



@app.route(route="{*path}")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    if DEBUG:
        logging.info('Entering handler function')
    host=os.getenv('DESTINATION')
    timeout = int(os.getenv('TIMEOUT', 20)) # override using TIMEOUT env variable
    rpath = req.route_params.get('path')
    path = f'{PROTOCOL}://{host}/{rpath}'
    data = req.get_body()   
    headers=dict(req.headers)
 
    if DEBUG:
        logging.info(f'URL: {path}, Data: {data}, Method: {req.method}')
        logging.info(f'Request headers: {headers}')

    if f'/{rpath}' == TESTPATH:
        return func.HttpResponse(f'OK')

    if not 'accept-encoding' in [a.lower() for a in headers.keys()]:
        headers['Accept-Encoding'] = urllib3.util.SKIP_HEADER # stop requests from adding this header
    try:
        r = requests.request(req.method, path, params=req.params, stream=True, 
                            headers=headers, allow_redirects=False, 
                            data=data, timeout=timeout)
        rdata = r.raw.read()
        if DEBUG:
            logging.info(f'Response headers: {str(dict(r.headers))}')
            logging.info(f'Length of response data: {len(rdata)}')
        return func.HttpResponse(body=rdata, status_code=r.status_code, headers=r.headers)
    except Exception as e:
        # change these responses to remove indicators
        if DEBUG:
            return func.HttpResponse(f'Error: {str(e)}')
        else:
            return func.HttpResponse('Error')

