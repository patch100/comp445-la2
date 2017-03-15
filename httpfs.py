import json
import os
import re
import socket
import threading
import argparse

from dicttoxml import dicttoxml
from request import request
from response import response

def run_server(host, port, dir):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        listener.bind((host, port))
        listener.listen(5)
        if args.v:
            print('Echo server is listening at', port)
        while True:
            conn, addr = listener.accept()
            threading.Thread(target=handle_client, args=(conn, addr, dir)).start()
    finally:
        listener.close()


def handle_client(conn, addr, dir):
    if args.v:
        print 'New client from', addr
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                if args.v:
                    print 'data unreadable from: ', addr
                break
            request = parseRequest(data)

            cwd = dir

            if args.v:
                print 'Working dir is: ' + cwd, addr

            # if no file specified, list files
            if request.getMethod() == "GET" and not request.filename:
                if args.v:
                    print 'Listing files for: ', addr
                files = os.listdir(cwd)
                content_type = request.getHeader("Accept")[1]
                output = formatData(content_type, files)
                r = response("200 OK", content_type, output)
                if args.v:
                    print r.toString(), addr
                conn.sendall(r.toString())

            # return contents of file
            elif request.getMethod() == "GET" and request.filename:
                if args.v:
                    print 'reading file: ' + request.filename, addr
                if os.path.isfile(cwd + "/" + request.filename):
                    if args.v:
                        print 'file found: ', addr
                    file = open(cwd + "/" + request.filename)
                    r = response("200 OK", "text/plain", file.read())
                    file.close()
                else:
                    if args.v:
                        print 'file not found: ', addr
                    r = response("404 Not Found", "", "")

                if args.v:
                    print r.toString(), addr
                conn.sendall(r.toString())

            # overwrite file with body of request
            elif request.getMethod() == "POST" and request.filename:
                if args.v:
                    print 'writing file : ' + request.filename, addr
                filename = os.path.join(dir,request.filename)
                file = open(filename, 'w+')
                file.write(request.getBody())
                file.close()
                r = response("201 Created", "", "")
                if args.v:
                    print r.toString(), addr
                conn.sendall(r.toString())
            else:
                if args.v:
                    print 'bad request from: ', addr
                r = response("400 Bad Request", "", "")
                if args.v:
                    print r.toString(), addr
                conn.sendall(r.toString())

            break

    finally:
        conn.close()

def parseRequest(data):
    search = re.search('(GET|POST) \/(\w+.\w+)? (HTTP\/\d.\d)(?:\\r\\n)?\s*((?:\w+-?\w+: .*\s)*)(?:\\r\\n)?(\s?.*)?', data)
    method = search.group(1)
    directory = search.group(2)
    headers = re.findall('\s+\w+-?\w+: .*(?:\\r\\n)?', search.group(4))
    r = request(method, directory)
    r.setBody(search.group(5))

    for h in headers:
        separator = re.search('\s+(\w+-?\w+): (.*)(?:\\r\\n)?', h)
        r.addHeader((separator.group(1), separator.group(2)))

    return r

def formatData(content_type, files):
    data = {}
    data["files"] = []
    for f in files:
        data["files"].append(f)

    if "application/json" in content_type:
        return json.dumps(data)
    elif "xml" in content_type:
        return dicttoxml(data, custom_root='files', attr_type=False)
    elif "html" in content_type:
        html = "<!doctype html><html lang=en><head><meta charset=utf-8><title>Files</title></head><body><ul>"
        for f in files:
            html += "<li>"+f+"</li>"
        html += "</ul></body></html>"
        return html
    else:
        return str(data)

def checkIfDir (string):
    if os.path.isdir(string):
        return string
    else:
        raise argparse.ArgumentTypeError('The path passed is not a directory. Make sure you use the full path')

parser = argparse.ArgumentParser(description='Socket based HTTP fileserver')

# optional arguments
parser.add_argument("-v", help="enable verbosity", action='store_true')
parser.add_argument("-d", help="directory on server", type=checkIfDir)
parser.add_argument("-p", help="specify server port", type=int)

args = parser.parse_args()
port = args.p if args.p else 8080
dir = args.d if args.d else "files"
run_server('', port, dir)
