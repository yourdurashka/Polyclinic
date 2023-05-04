import os
import json
from flask import Blueprint, request, render_template, current_app, session, redirect, url_for
from cache.wrapper import fetch_from_cache
from db_context_manager import DBContextManager
from db_work import select_dict, select
from sql_provider import SQLProvider

blueprint_order = Blueprint('bp_order', __name__, template_folder='templates', static_folder='static')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_order.route('/', methods=['GET', 'POST'])
def order_index():
    db_config = current_app.config['dbconfig']
    cache_config = current_app.config['cache_config']
    cached_select = fetch_from_cache('all_items_cached', cache_config)(select_dict)
    if request.method == 'GET':
        sql = provider.get('all_items.sql') #имеющиеся товары
        user_id = session.get('user_id')
        _sql3 = provider.get('pac_inf.sql', user_id=user_id)
        inf_result, schema = select(current_app.config['dbconfig'], _sql3)
        print('inf_result HERE', inf_result)
        print("HERE!!! вот здесь")
        items = cached_select(db_config, sql) #селектим товары из бд
        print('item', items)
        basket_items = session.get('basket', {})
        return render_template('basket_order_list.html', items=items, basket=basket_items, result=inf_result, schema=['Имя пациента','Паспортные данные','Адрес']) #передаем item из бд, вставляем в колонки в html
    else:
        id_doc = request.form['id_doc'] #получили айди товара на кот нажали
        sql = provider.get('select_item.sql', id_doc=id_doc)
        print('sql', sql)
        print("HERE!!!")
       # date_visit = request.form.get('date_visit')
        input_time = request.form.get('input_time')
       # print("date_visit = ",date_visit)
        print("input_time = ", input_time)
        item = select_dict(db_config, sql)[0]
        date_visit=item['date_visit']
        print("date_visit = ", date_visit)
        user_id = session.get('user_id')
        _sql2=provider.get('check.sql', doc_id=id_doc, date_visit=date_visit, input_time=input_time)
        result, schema = select(current_app.config['dbconfig'], _sql2)
        _sql4=provider.get('check2.sql', doc_id=id_doc, date_visit=date_visit, input_time=input_time, user_id=user_id)
        result2, schema = select(current_app.config['dbconfig'], _sql4)
        print("RESALT",result)
        if result[0][0]==0 and result2[0][0]==0:
            add_to_basket(id_doc, item) #добавляем в корзину
        return redirect(url_for('bp_order.order_index'))



def add_to_basket(id_doc:str, item:dict):
    curr_basket =session.get('basket', {}) #достаем текущую корзину которая есть
    input_time = request.form.get('input_time')
    print("input_time = ", input_time)
    print('aaaaa',curr_basket)
    date_visit = request.form.get('date_visit')
    print("date_visitHERE = ", date_visit)
    if id_doc in curr_basket:
        curr_basket[id_doc]['amount'] = curr_basket[id_doc]['amount'] + 1
    else:
        curr_basket[id_doc] ={
                'doc_name': item['doc_name'],
                'spec': item['spec'],
                'date_visit': item['date_visit'],
                'amount': 1,
                'input_time': input_time}
        session['basket'] = curr_basket
        session.permanent = True
    return True
#тело транзакции - инсерт, селект
@blueprint_order.route('/save_order', methods=['GET', 'POST'])
def save_order():
    user_id = session.get('user_id')
    current_basket = session.get('basket', {}) #что находится в сессии
    print('LLLL', current_basket)
    order_id = save_order_with_list(current_app.config['dbconfig'], user_id, current_basket)
    print('order id HERE1 = ',order_id)
    if order_id:
        session.pop('basket')
        return render_template('order_created.html', order_id=order_id)
    #else:
        # return 'Что-то пошло не так'

def save_order_with_list(dbconfig: dict, user_id: int, current_basket: dict):
    with DBContextManager(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан') #курсор создает в КМ, инит - сооздание нового экзм,
        _sql1 = provider.get('insert_order.sql', user_id=user_id)
        result1 = cursor.execute(_sql1)
        print("result1 = ",result1)
        if result1 == 1:        #если успешно
            print("ID = ",user_id)
            _sql2 = provider.get('select_order_id.sql', user_id=user_id)
            print("sql2 = ",_sql2)
            cursor.execute(_sql2)
            order_id = cursor.fetchall()[0][0] #массив
            print('order_idHERE= ', order_id)
            if order_id:
                print("IF",order_id)
                for key in current_basket: # извлекается ключ
                    print("KEY ==",key, current_basket[key]['amount'])
                    doc_name = current_basket[key]['doc_name']
                    spec = current_basket[key]['spec']
                    date_visit = current_basket[key]['date_visit']
                    input_time=current_basket[key]['input_time']
                    print("FOR = ", order_id)
                  #  insert orders_list values(NULL, '$order_id', '$id_doc', '$doc_name', '$spec', '$input_date', '$amount')
                   # insert orders_list values(NULL, '$order_id', '$id_doc', '$doc_name', '$spec', '$date_visit', '$user_id')
                    _sql3 = provider.get('insert_order_list.sql', order_id=order_id, id_doc=key, doc_name=doc_name, spec=spec, date_visit=date_visit, user_id=user_id, input_time=input_time)
                    print(_sql3)
                    print("FOR11", order_id)
                    cursor.execute(_sql3)
                    print("FOR", order_id)
                return order_id

@blueprint_order.route('/clear-basket')
def clear_basket():
    if 'basket' in session:
        session.pop('basket')
    return redirect(url_for('bp_order.order_index'))