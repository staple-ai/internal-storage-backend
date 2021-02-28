
from Code.interaction import *
from Code.errors import *
from flask import Flask, request, send_file
from werkzeug.exceptions import BadRequest, HTTPException
import traceback, sys



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
    db_online = healtcheck_root_exists()
    status_code = 200 if db_online else 500
    message = "Document Storage Server is working" if db_online else "Root folder not accessible"
    return message, status_code


def create_folder(req):
    path = req.form['path']
    uid = add_element(path)
    return 'Folder created successfully!', 200

def upload_file(req):
    uploaded_file = req.files['file']
    path = req.form['path']
    if uploaded_file.filename != '':
        print('Uploading File')
        contents = uploaded_file.read()
        add_element(path, contents)
        return 'File uploaded successfully!', 200
    else:
    	raise NoFileSent()


def download_file(req):
    path = req.form['path']
    file = get_file(path)
    return file, 200


def delete(req):
    kind = req.form['type']
    path = req.form['path']
    if kind.lower() == 'file':
        uid = delete_file(path)
    elif kind.lower() == 'folder':
        uid = delete_folder(path)
    else:
        return "Please provide a valid type -  'folder' or 'file'", 400
    return "Deleted {0} '{1}' successfully".format(kind,path) , 200

def list_contents(req):
    path = req.form['path']
    contents = get_folder_contents(path)
    return contents, 200


