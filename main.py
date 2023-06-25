from flask import Flask, render_template, request, escape,session
from panic import vovels
from DBcm import UseDataBase, ConnectionError, CredentialsError
from checker import check_logged_in

app = Flask(__name__)

app.config['dbconfig'] = {
                            'host':'127.0.0.1',
                            'user':'root',
                            'password':'Aa1234567890',
                            'database':'vsearchlogDB',
                        }

@app.route('/login')
def do_login()->str:
    session['logged_in'] = True
    return 'You are now logged in.'

@app.route('/logout')
def do_logout()->str:
    session.pop('logged_in')
    return 'You are now logged out.'


def log_request(req:'flask_request', res:str)->None:
    # with open('vsearch.log','a') as log:
    #     print(req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')
    with UseDataBase(app.config['dbconfig']) as cursor:
        _sql = """insert into log
            (phrase,letters,ip,browser_string, results)
            values
            (%s,%s,%s,'Chrome',%s)"""
        cursor.execute(_sql,(req.form['phrase'],
                             req.form['letters'],
                             req.remote_addr,
                             res))

@app.route('/search4', methods=['POST'])
def do_search()->str:
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = vovels(phrase,letters)
    try:
        log_request(request,results)
    except Exception as err:
        print('error: ',str(err))
    return render_template('results.html',the_phrase=phrase,
                           the_letters = letters,
                           the_title=title,
                           the_results=results)
@app.route('/')
@app.route('/entry')
def entry_page()->'html':
    return render_template('entry.html', the_title='Welcome to search4letters on the web!')


@app.route('/viewlog')
@check_logged_in
def view()->'html':
    try: 
        with UseDataBase(app.config['dbconfig']) as cursor:
            _sql = """select phrase, letters, ip, browser_string, results from log"""
            cursor.execute(_sql)
            content = cursor.fetchall()
            titles = ('Phrase', 'Letters', 'Remote_addr','User_agent', 'Results')
        return render_template('viewlog.html',
                                the_title = 'View_log',
                                the_row_titles = titles,
                                the_data = content,)
    except ConnectionError as err:
        print('Error with DB: ',str(err))
    except CredentialsError as err:
        print("Credentials are not right: ",str(err))
    except Exception as err:
        print("Error: ",str(err))
    return 'Error'
   

app.secret_key = 'YouWillNeverGuessMySecretKey'         

if __name__=="__main__":
    app.run(debug=True)