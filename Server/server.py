from Code.interaction import *
from Code.errors import *
from Code.routes import *
from flask import Flask, request, send_file, jsonify
from io import BytesIO





serverapp = Flask(__name__)
serverapp.config["DEBUG"] = True



@serverapp.route('/storage_health', methods=['GET'])
def server_healthcheck():
    return exhaust_wrapper(healthcheck, None)


@serverapp.route('/create_folder', methods=['GET','POST'])
def server_create_folder():
    return exhaust_wrapper(create_folder, request)



@serverapp.route('/upload_file', methods=['POST'])
def server_upload_file():
    return exhaust_wrapper(upload_file, request)


@serverapp.route('/create_element', methods=['POST'])
def server_create_element():
    return exhaust_wrapper(create_element, request)



@serverapp.route('/download_file', methods=['GET','POST'])
def server_download_file():
    result, status_code = exhaust_wrapper(download_file, request)
    if status_code != 200:
        return result, status_code
    else:
        return send_file(BytesIO(result['file']),
                     attachment_filename=result['name'],
                     as_attachment=True,
                     mimetype=result['mimetype'])



@serverapp.route('/delete', methods=['GET','POST', 'DELETE'])
def server_delete():
    return exhaust_wrapper(delete, request)


@serverapp.route('/delete_object', methods=['GET','POST', 'DELETE'])
def server_delete_anything():
    return exhaust_wrapper(delete_anything, request)


@serverapp.route('/list_contents', methods=['GET','POST'])
def server_list_contents():
    result, status_code = exhaust_wrapper(list_contents, request)
    if status_code != 200:
        return result, status_code
    else:
        return jsonify(result), status_code




# serverapp.run(host='0.0.0.0', debug=True)

