from flask import Flask, render_template, request, escape
from panic import vovels
import mysql.connector

app = Flask(__name__)



@app.route('/search4', methods=['POST'])
def do_search()->str:
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = vovels(phrase,letters)
    log_request(request,results)
    return render_template('results.html',the_phrase=phrase,
                           the_letters = letters,
                           the_title=title,
                           the_results=results)
@app.route('/')
@app.route('/entry')
def entry_page()->'html':
    return render_template('entry.html', the_title='Welcome to search4letters on the web!')


def log_request(req:'flask_request', res:str)->None:
    # with open('vsearch.log','a') as log:
    #     print(req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')
    dbconfig = {
        'host':'127.0.0.1',
        'user':'root',
        'password':'Aa1234567890',
        'database':'vsearchlogDB',
    }

    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _sql = """insert into log
            (phrase,letters,ip,browser_string, results)
            values
            (%s,%s,%s,'Chrome',%s)"""
    cursor.execute(_sql,(req.form['phrase'],
                         req.form['letters'],
                         req.remote_addr,
                        #  str(req.user_agent),
                         res,))
    conn.commit()
    cursor.close()
    conn.close()
            

@app.route('/viewlog')
def view()->'html':
    contents = []
    with open('vsearch.log') as f:
        for line in f:
            contents.append([])
            for item in line.split("|"):
                contents[-1].append(escape(item))
    titles = ('Form Data','Remote_addr', 'User_agent', 'Results')
    return render_template('viewlog.html',the_title='View Log',
                           the_row_titles = titles,
                           the_data=contents)
            

if __name__=="__main__":
    app.run(debug=True)