from flask import Blueprint, render_template, request, redirect, url_for, current_app
from access import login_required, group_required
import os
from db_work import select
from sql_provider import SQLProvider

blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql')) #Создается словарь

@blueprint_report.route('/', methods=['GET', 'POST'])
@login_required
def start_report():
    return render_template('menu_report.html')

@blueprint_report.route('/otchet1', methods=['GET', 'POST'])
@group_required
def otchet1():
    if request.method == 'GET':
        return render_template('otchet1_form.html')
    else:
        input_name = request.form.get('name_doc')
        if input_name:
            _sql = provider.get('otchet1.sql', input_name=input_name) # передаются в качестве параметра - имя ключа + значение параметра
            otchet1_result, schema = select(current_app.config['dbconfig'], _sql)
            return render_template('pb_result.html', schema=['Имя пациента','Паспорт','Адрес','Дата рождения','Дата создания карты'], result=otchet1_result)


@blueprint_report.route('/pac', methods=['GET', 'POST'])
@group_required
def pac():
    if request.method == 'GET':
        return render_template('pac_form.html')
    else:
        input_name = request.form.get('pac_name')
        if input_name:
            _sql = provider.get('pac.sql', input_name=input_name) # передаются в качестве параметра - имя ключа + значение параметра
            pac_result, schema = select(current_app.config['dbconfig'], _sql)
            return render_template('pb_result.html', schema=['Имя пациента','Паспорт','Адрес','Дата рождения','Дата создания карты'], result=pac_result)
        else:
            return "Repeat input"

@blueprint_report.route('/doc', methods=['GET', 'POST'])
@group_required
def doc():
    if request.method == 'GET':
        return render_template('doc_form.html')
    else:
        input_name = request.form.get('doc_name')
        if input_name:
            _sql = provider.get('doc.sql', input_name=input_name) # передаются в качестве параметра - имя ключа + значение параметра
            doc_result, schema = select(current_app.config['dbconfig'], _sql)
            return render_template('db_result.html', schema=['Имя врача','Специальность','Адрес','Паспорт','Дата рождения','Дата приема на работу','Дата увольнения'], result=doc_result)
        else:
            return "Repeat input"

@blueprint_report.route('/otchet2', methods=['GET', 'POST'])
@group_required
def otchet2():
    if request.method == 'GET':
        return render_template('otchet2_form.html')
    else:
        input_data = request.form.get('input_data')
        if input_data:
            _sql = provider.get('otchet2.sql', input_data=input_data) # передаются в качестве параметра - имя ключа + значение параметра
            otchet2_result, schema = select(current_app.config['dbconfig'], _sql)
            return render_template('dd_result.html', schema=['Номер кабинета','Дата приема','Имя врача','Количество пациентов явившихся на прием','Всего записавшихся на прием'], result=otchet2_result)
        else:
            return "Repeat input"

@blueprint_report.route('/appointment', methods=['GET', 'POST'])
@login_required
def timetable():
        columns=["Имя врача","Специальность","Дата приема","Номер кабинета"]
        if request.method == 'GET':
            _sql = provider.get('timetable.sql')
            tt_result, schema = select(current_app.config['dbconfig'], _sql)
            return render_template('tt.result.html', schema=columns, result=tt_result)
