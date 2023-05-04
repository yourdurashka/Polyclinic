import json
from flask import Flask, url_for, render_template, redirect, json, session
from auth.route import blueprint_auth
from blueprint_query.route import blueprint_query
from blueprint_report.route import blueprint_report
from basket.route import blueprint_order
from typing import List, Callable
from access import group_required
from access import login_required

app = Flask(__name__)
app.secret_key = 'SuperKey'

app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_report, url_prefix='/reports')
app.register_blueprint(blueprint_query, url_prefix='/query')
app.register_blueprint(blueprint_order, url_prefix='/order')

app.config['db_config'] = json.load(open('data_files/dbconfig.json'))
app.config['access_config'] = json.load(open('configs/access.json'))

with open ('data_files/dbconfig.json', 'r') as f:
    db_config = json.load(f)
app.config['dbconfig'] = db_config

with open('configs/access.json', 'r') as f:
    access_config = json.load(f)
    app.config['access_config'] = access_config

with open('data_files/cache.json', 'r') as f:
    cache_config = json.load(f)
    app.config['cache_config'] = cache_config


@app.route('/', methods=['GET', 'POST'])
def menu_choice():
    if 'user_id' in session:
        print(1)
        if session.get('user_group', None):
            return render_template('internal_user_menu.html')
        else:
            return render_template('external_user_menu.html')
    else:
        return redirect(url_for('bp_auth.start_auth'))

def add_blueprint_access_hadler(app: Flask, blueprint_names: List[str], handler: Callable) -> Flask:
    for view_func_name, view_func in app.view_functions.items():#цикл по всем доступным разработчикам
        print('view_func_name = ', view_func_name)#Имя функции
        print('view_func = ', view_func)#Сама функция
        view_func_parts = view_func_name.split('.')
        if len(view_func_parts) > 1:
            view_blueprint = view_func_parts[0]#Имя блюпринта
            if view_blueprint in blueprint_names:
                view_func = handler(view_func)#Функция оборачивается в декоратор
                app.view_functions[view_func_name] = view_func
    return app

@app.route('/exit')
@login_required
def exit_func():
    session.clear()
    return 'До свиданья, заходите еще раз'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)