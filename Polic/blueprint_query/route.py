from flask import Blueprint, render_template, request, redirect, url_for, current_app
from db_work import select, call_proc
from access import login_required, group_required
from sql_provider import SQLProvider
import os
from db_context_manager import DBContextManager

blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))



report_list = [
    {'rep_name':"Отчет о количестве посещений у каждого врача за заданный период", 'rep_id':'1'}
]


report_url = {
    '1': {'create_rep':'bp_query.create_rep1', 'view_rep':'bp_query.view_rep1'}
}


@blueprint_query.route('/', methods=['GET', 'POST'])
def start_query():
    if request.method == 'GET':
        return render_template('menu_query.html', report_list=report_list)
    else:
        rep_id = request.form.get('rep_id')
        if request.form.get('create_rep'):
            url_rep = report_url[rep_id]['create_rep']
        else:
            url_rep = report_url[rep_id]['view_rep']
        return redirect(url_for(url_rep))
    # из формы получает номер отчета и какую кнопку

@blueprint_query.route('/create_rep1', methods=['GET', 'POST'])
@group_required
def create_rep1():
    if request.method == 'GET':
        return render_template('report_create.html')
    else:
        rep_year = request.form.get('Byear')
        rep_month = request.form.get('Bmonth')
        rep_name = request.form.get('Dname')
        if rep_year and rep_name and rep_month:
           check = provider.get('rep.sql', Byear=rep_year,Bmonth=rep_month, Dname=rep_name)
           product_result, schema = select(current_app.config['dbconfig'], check)
           check2= provider.get('rep2.sql', Byear=rep_year,Bmonth=rep_month, Dname=rep_name)
           product_result2, schema = select(current_app.config['dbconfig'], check2)
           if product_result[0][0] < product_result2[0][0]:
                res = call_proc(current_app.config['dbconfig'], 'DatePaci', rep_year,rep_month, rep_name)
                return render_template('report_created.html')
           else:
               return render_template('report_exists.html')
        else:
            return "Repeat input"


@blueprint_query.route('/view_rep1', methods=['GET', 'POST'])
@group_required
def view_rep1():
    if request.method == 'GET':
        return render_template('view_rep1.html')
    else:
        rep_year = request.form.get('Byear')
        rep_month = request.form.get('Bmonth')
        rep_name = request.form.get('Dname')
        if rep_year and rep_name and rep_month:
                _sql = provider.get('rep1.sql', Byear=rep_year,Bmonth=rep_month, Dname=rep_name)
                product_result, schema = select(current_app.config['dbconfig'], _sql)
                return render_template('result_rep1.html', schema = ['Имя врача','Количество приемов'], result = product_result)
        else:
            return "Repeat input"

