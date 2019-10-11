#!/usr/bin/python
import json
from bson import json_util
import bottle
from bottle import route, run, request, abort

# set up URI paths for REST service
@route('/currentTime', method='GET')
def get_currentTime():
    dateString=datetime.datetime.now().strftime("%Y-%m-%d")
    timeString=datetime.datetime.now().strftime("%H:%M:%S")
    string="{\"date\":"+dateString+",\"time\":"+timeString+"}"
    return json.loads(json.dumps(string, indent=4, default=json_util.default))

if __name__ == '__main__':
  #app.run(debug=True)
  run(host='localhost', port=8080)