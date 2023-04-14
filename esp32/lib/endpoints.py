import json

# Add new get endpoints here and 
# Please add documentation on how to use the endpoint
def GET_REQUEST(request):
    
    # Description:
    # Test home page 
    #
    #
    if request['path'] == '/':
        html = """<!DOCTYPE html>
            <html>
            <head> <title>Pico W</title> </head>
            <body> <h1>Pico W</h1>
            <p>Hello World</p>
            </body>
            </html>
            """
        response = {
            'message': html,
            'code': '200 OK\r\n'
        }
        return response
    
    # Description:
    # Test get request
    #
    #
    elif request['path'] == '/hello':
        response = {
            'message': 'Hello From the GET request',
            'code': '200 OK\r\n'
        }
        return response
    
    # Description:
    # Error response when path doesn't get a match
    #
    #
    else:
        response = {
            'message': ('error: no GET endpoint configured for ' + request['path']),
            'code': '404 Not-Found\r\n'
        }
        return response

# Add new post endpoints here
def POST_REQUEST(request, data):
    if data == {}:
        data = None
    else:
        data = json.loads(data)
        
    # Description:
    # returns the json body that was send in the request for testing
    # 
    #
    if request['path'] == '/hello':
        response = {
            'message': 'Hello from the Post. You sent: ' + json.dumps(data),
            'code': '200 OK\r\n'
        }
        return response
    
    # Description:
    # Error response when path doesn't get a match
    #
    #
    else:
        response = {
            'message': ('error: no POST endpoint configured for ' + request['path']),
            'code': '404 Not-Found\r\n'
        }
        return response