from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify,flash,url_for


from controllers import (
    get_all_logs
    )

log = Blueprint('log', __name__, template_folder='../templates')

@log.route('/log', methods=['GET'])
def Log():
    jls_extract_var = 'log.html'
    return render_template(jls_extract_var, log = get_all_logs())

