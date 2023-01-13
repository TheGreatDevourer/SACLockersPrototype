from flask import Blueprint, redirect, render_template


from controllers import (
    get_all_logs
    )

@log.route('/log', methods=['GET'])
def Log_page():
    return render_template('log.html', log = get_all_logs())
