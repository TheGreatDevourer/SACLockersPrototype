from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify,url_for,flash

from controllers import (
    add_new_student,
    get_all_students,
    get_student_by_id,
    update_student_id,
    update_student_first_name,
    update_student_last_name,
    update_student_phone_number,
    update_student_email,
    update_student_faculty,

    )
from views.forms import StudentAdd 

student_views = Blueprint('student_views', __name__, template_folder='../templates')

@student_views.route('/student',methods=['GET'])
def render_student():
    form = StudentAdd()
    return render_template("student.html",form=form)

@student_views.route('/student', methods=['POST'])
def add_student():
    form = StudentAdd()
    if form.validate_on_submit:
        data = request.form
        student = add_new_student(s_id = data['student_id'], f_name=data['f_name'], l_name=data['l_name'], faculty=data['faculty'],p_no=data['p_no'],email=data['email'])
        if not student:
            flash("Student not created")
            return redirect(url_for('rent_views.rent_page'))
        flash("Success")
        return redirect(url_for('rent_views.rent_page'))

@student_views.route('/student/manage',methods=['GET'])
def render_manage_student():
    studentData = get_all_students()
    return render_template("manage_student.html",studentData=studentData)

@student_views.route("/student/<id>/edit", methods=['GET'])
def render_edit_student(id):
    student = get_student_by_id(id)

    if not student:
        flash('Student does not exist')
        return redirect(url_for('.render_manage_student'))

    form = StudentAdd()
    form.student_id.data = student.student_id
    #form.student_id.render_kw= {'disabled':''}
    form.f_name.data = student.first_name
    form.l_name.data = student.last_name
    form.faculty.data = student.faculty
    form.p_no.data = student.phone_number
    form.email.data = student.email
    form.submit.label.text = "Update Student"
    return render_template('student.html', form=form, updateMode=True)

@student_views.route("/student/<id>/update", methods=['POST'])
def update_student_info(id):
    student = get_student_by_id(id)

    if not student:
        flash('Student does not exist')
        return redirect(url_for('.render_manage_student'))

    form = StudentAdd()
    if form.validate_on_submit: 
        student_id = str(request.form.get("student_id"))
        f_name = str(request.form.get("f_name"))
        l_name = str(request.form.get("l_name"))
        faculty = str(request.form.get("faculty"))
        p_no  = str(request.form.get("p_no"))
        email = str(request.form.get("email"))
        
        if str(student.student_id) != student_id and student_id != "":
             if not update_student_id(id,f_name):
                flash("Error updating StudentID")
                return redirect(url_for('.render_manage_student'))  

        if student.first_name != f_name and f_name != "":
             if not update_student_first_name(id,f_name):
                flash("Error updating First Name")
                return redirect(url_for('.render_manage_student'))  

        if student.last_name != l_name and l_name != "":
            if not update_student_last_name(id,l_name):
                flash("Error updating Last Name")
                return redirect(url_for('.render_manage_student')) 
        if student.faculty != faculty and faculty != "":
             if not update_student_faculty(id,faculty):
                flash("Error updating Faculty")
                return redirect(url_for('.render_manage_student'))
        if student.phone_number != p_no and p_no != "":
             if not update_student_phone_number(id,p_no):
                flash("Error updating Phone")
                return redirect(url_for('.render_manage_student')) 
        if student.email != email and email != "":
             if not update_student_email(id,email):
                flash("Error updating Faculty")
                return redirect(url_for('.render_manage_student')) 
        return redirect(url_for('.render_manage_student'))