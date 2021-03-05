
from Code.interaction import *
from Code.errors import *
from flask import Flask, request, send_file
from werkzeug.exceptions import BadRequest, HTTPException
import traceback, sys, psycopg2


def exhaust_wrapper(func, req):
    message, code = function_exception_wrapper(func, req)
    print("Flushing stream...")
    a = request.stream
    print(type(a))
    print(a)
    try:
        a.truncate(0)
        print("Could truncate")
    except:
        print("Could not truncate")
    try:
        a.exhaust()
        print("Could exhaust")
    except:
        print("Could not exhaust")
    # environ['wsgi.input'].read()
    return message, code

def exhaust_request(req):
    a = request.stream
    print(type(a))
    print(a)
    try:
        a.truncate(0)
        print("Could truncate")
    except:
        print("Could not truncate")
    try:
        a.exhaust()
        print("Could exhaust")
    except:
        print("Could not exhaust")


def function_exception_wrapper(func, req):
    try:
        response, status_code = func(req)
        return response, status_code
    except (NoSuchFolder, NoSuchFile, ElementAlreadyExists, DatabaseError, UnknownServerError, NoFileSent) as er:
        return er.message, er.code
    except HTTPException as e:
        print("werkzeug")
        traceback.print_exc(file=sys.stdout)
        print("code", e.code,"name", e.name,"description", e.description,)
        return e.name, e.code
    except:
        traceback.print_exc(file=sys.stdout)
        return "Internal Server Error", 500

def healthcheck(req):
    exhaust_request(req)
    db_online = healtcheck_root_exists()
    status_code = 200 if db_online else 500
    message = "Document Storage Server is working" if db_online else "Root folder not accessible"
    return message, status_code


def create_folder(req):
    if request.method == 'POST':
        path = req.form['path']
        force = True if req.form.get('force', 'False').lower() == 'true' else False
    elif request.method == 'GET':
        path = request.args.get('path')
        force = True if req.args.get('force', 'False').lower() == 'true' else False
    exhaust_request(req)
    uid = add_element(path, force = force)
    return 'Folder created successfully!', 200

def upload_file(req):
    uploaded_file = req.files['file']
    path = req.form['path']
    force = True if req.form.get('force', 'False').lower() == 'true' else False


    if uploaded_file.filename != '':
        print('Uploading File')
        contents = uploaded_file.read()
        exhaust_request(req)
        add_element(path, contents, force)
        return 'File uploaded successfully!', 200
    else:
        exhaust_request(req)
        raise NoFileSent()



def create_element(req):
    path = req.form['path']
    force = True if req.form.get('force', 'False').lower() == 'true' else False

    uploaded_file = req.files.get('file', None)
    file_upload = uploaded_file is not None and uploaded_file.filename != ''
    contents = uploaded_file.read() if file_upload else None

    exhaust_request(req)
    print('Uploading File')
    add_element(path, contents, force)
    if file_upload:
        return 'File uploaded successfully!', 200
    else:
        return 'Folder created successfully!', 200


def download_file(req):
    if request.method == 'POST':
        path = req.form['path']
    elif request.method == 'GET' or request.method == 'DELETE':
        path = request.args.get('path')
    exhaust_request(req)
    file = get_file(path)
    return file, 200


def delete(req):
    if request.method == 'POST':
        kind = req.form['type']
        path = req.form['path']
    elif request.method == 'GET' or request.method == 'DELETE':
        kind = request.args.get('type')
        path = request.args.get('path')
    exhaust_request(req)
    if kind.lower() == 'file':
        uid = delete_file(path)
    elif kind.lower() == 'folder':
        uid = delete_folder(path)
    else:
        return "Please provide a valid type -  'folder' or 'file'", 400
    return "Deleted {0} '{1}' successfully".format(kind,path) , 200


def delete_anything(req):
    if request.method == 'POST':
        path = req.form['path']
    elif request.method == 'GET' or request.method == 'DELETE':
        path = request.args.get('path')
    exhaust_request(req)
    try:
        generic_delete(path)
    except psycopg2.OperationalError as e:
        print("OperationalError")

    return "Deleted '{0}' successfully".format(path) , 200


def list_contents(req):
    if request.method == 'POST':
        path = req.form['path']
    elif request.method == 'GET':
        path = request.args.get('path')
    exhaust_request(req)
    contents = get_folder_contents(path)
    return contents, 200


