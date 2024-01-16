from datetime import datetime

from flask import Flask, render_template, request, flash, redirect, url_for, \
    abort
from requests.exceptions import RequestException
from page_analyzer.cfg import SECRET_KEY
from page_analyzer.database import get_all_urls, get_url_by_name, \
    get_url_by_id, insert_url, insert_url_checking_result, \
    get_url_checking_results
from page_analyzer.url_checks import validate_url, get_ceo_data

FLASH_MESSAGES = {
    'zero_len': {'message': 'URL обязателен',
                 'type': 'danger'},
    'too_long': {'message': 'URL превышает 255 символов',
                 'type': 'danger'},
    'wrong': {'message': 'Некорректный URL',
              'type': 'danger'},
    'exists': {'message': 'Страница уже существует',
               'type': 'info'},
    'success': {'message': 'Страница успешно добавлена',
                'type': 'success'},
    'check_success': {'message': 'Страница успешно проверена',
                      'type': 'success'},
    'check_failed': {'message': 'Произошла ошибка при проверке',
                     'type': 'danger'}
}

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY


@app.route("/")
def start_page():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.post("/urls")
def add_url():
    input_url = request.form['url']
    validation_result = validate_url(input_url)
    error = validation_result['error']

    if error is None:
        url_data = {
            'url': validation_result['url'],
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        url_id = insert_url(url_data)
        flash(FLASH_MESSAGES['success']['message'],
              FLASH_MESSAGES['success']['type'])

        return redirect(url_for('show_url_page', id_=url_id))

    if error == 'exists':
        flash(FLASH_MESSAGES[error]['message'],
              FLASH_MESSAGES[error]['type'])
        url = get_url_by_name(validation_result['url'])
        return redirect(url_for('show_url_page', id_=url['id']))

    flash(FLASH_MESSAGES[error]['message'],
          FLASH_MESSAGES[error]['type'])

    return render_template('index.html'), 422


@app.get("/urls")
def show_urls():
    urls = get_all_urls()
    return render_template('urls_table.html', rows=urls)


@app.route("/urls/<int:id_>")
def show_url_page(id_):
    url_data = get_url_by_id(id_)

    if not url_data:
        abort(404)

    return render_template('url_info.html', url=url_data)


@app.post("/urls/<int:id_>/checks")
def check_url(id_):
    url_data = get_url_by_id(id_)
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        checking_result = get_ceo_data(url_data['name'])
        checking_result['url_id'] = id_
        checking_result['created_at'] = created_at

        insert_url_checking_result(checking_result)

        flash(FLASH_MESSAGES['check_success']['message'],
              FLASH_MESSAGES['check_success']['type'])
    except RequestException:
        flash(FLASH_MESSAGES['check_failed']['message'],
              FLASH_MESSAGES['check_failed']['type'])

    checks_data = get_url_checking_results(id_)

    return render_template('url_info.html', url=url_data,
                           checks=checks_data)
