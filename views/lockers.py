
from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify,url_for,flash

from views.forms import LockerAdd, AreaAdd, ConfirmDelete

from controllers import (
    add_new_locker,
    get_lockers_available,
    get_locker_id,
    get_all_lockers,
    delete_locker,
    update_key,
    update_locker_type,
    update_locker_status,
    create_log
)

locker_views = Blueprint('locker_views', __name__, template_folder='../templates')

@locker_views.route("/locker", methods=['GET'])
def index():
    form = LockerAdd()
    return render_template('locker.html', form=form)

@locker_views.route("/locker/manage", methods=['GET'])
def manage_locker():
    lockerData = get_all_lockers()
    return render_template('manage_locker.html', lockerData=lockerData)

@locker_views.route('/locker/<id>/delete', methods=['GET'])
def render_confirm_delete(id):
    locker = get_locker_id(id)

    if not locker:
        flash('Locker does not exist')
        return redirect(url_for('.manage_locker'))
    
    return render_template('delete_locker.html',locker = locker, form = ConfirmDelete() )

@locker_views.route("/locker", methods=['POST'])
def add_locker():
    form = LockerAdd() # create form object
    if form.validate_on_submit:
        data = request.form # get data from form submission
        new_locker = add_new_locker(locker_code=data['locker_code'], locker_type=data['locker_type'], status=data['status'], key=data['key'])
        if not new_locker:
            return redirect(url_for('locker_views.index'))
            #jsonify({"message":"Locker already exist or some error has occurred"}),400
       
    return redirect(url_for('.return_locker_area', id = new_locker.locker_code))
    #jsonify({"data":new_locker.toJSON()}),201


@locker_views.route('/locker/<id>/confirmed', methods=['POST'])
def remove_area(id):
    form = ConfirmDelete()
    if form.validate_on_submit:
        locker = delete_locker(id)
        if not locker:
            flash("Locker doesn't exist")
            return redirect(url_for('.manage_locker'))
        flash('Locker deleted !')
    return redirect(url_for('.manage_locker'))

@locker_views.route("/locker/<id>/edit", methods=['GET'])
def render_edit_lockers(id):
    locker = get_locker_id(id)

    if not locker:
        flash('Locker does not exist')
        return redirect(url_for('.render_area_page'))

    form = LockerAdd()
    form.locker_code.data = locker.locker_code
    form.locker_code.render_kw = {'disabled':''}
    form.locker_type.default = locker.locker_type
    form.status.default = locker.status
    form.key.default = locker.key
    form.submit.label.text = "Update Locker"
    return render_template('locker.html', form=form, updateMode=True)

@locker_views.route("/locker/<id>/update", methods=['POST'])
def update_lockers(id):
    locker = get_locker_id(id)

    if not locker:
        flash('Locker does not exist')
        return redirect(url_for('.render_area_page'))

    form = LockerAdd()
    if form.validate_on_submit: 
        locker_type = request.form.get("locker_type")
        status = request.form.get("status")
        key = request.form.get("key")

        if locker.locker_type != locker_type and locker_type  is not None:
             if not update_locker_type(id,locker_type):
                flash("Error updating LockerType")
                return redirect(url_for('.manage_locker'))  

        if locker.status != status and status is not None:
             if not update_locker_status(id,status):
                flash("Error updating status")
                return redirect(url_for('.manage_locker'))  

        if locker.key != key and key is not None:
            if not update_key(id,key):
                flash("Error updating key")
                return redirect(url_for('.manage_locker'))  

   
    return render_template('locker.html', form=form, updateMode=True)


@locker_views.route('/locker/<id>/area', methods=['GET'])
def return_locker_area(id):
    area =  AreaAdd()
    area.locker_code.data = id
    area.l_code.data = id
    return render_template('locker_area.html',form = area)

@locker_views.route('/lockers/get/available', methods=['GET'])
def get_available_lockers():
    locker_list = get_lockers_available()

    if not locker_list:
        return jsonify({"message":"No available lockers"}),200

    return jsonify({"data":locker_list}),200

@locker_views.route('/lockers/get/<id>', methods=['GET'])
def get_id_locker(id):
    locker = get_locker_id(id)

    if not locker:
        return jsonify({"message":"Locker not found"}),404

    return jsonify({"data":locker.toJSON()}),200

@locker_views.route('/lockers/get/all',methods=['GET'])
def return_all_lockers():
    locker_list = get_all_lockers()
    if not locker_list:
        return jsonify({"error":"No lockers available"}),404
    return jsonify({"data":locker_list}),200
