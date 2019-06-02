from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import matplotlib.pyplot as plt 
import numpy as np
import matplotlib
import os

app = Flask(__name__, static_url_path='')
app.config['UPLOAD_FOLDER'] = './'

# home route
@app.route('/')
def home():
    return render_template('form.html')

@app.route('/success', methods = ['POST'])
def success():
    valuex = request.form['xaxis']
    valuey = request.form['yaxis']

    x = valuex.split(',')
    y = valuey.split(',')

    listx = []
    listy = []

    for i in x:
        listx.append(int(i))
    for j in y:
        listy.append(int(j))

    x = np.array(listx)
    y = np.array(listy)

    plt.clf()
    plt.figure('Graphic')    
    plt.plot(x, y)
    plt.title('Graphic X vs Y')
    plt.xlabel('X Values')
    plt.ylabel('Y Values')
    plt.xticks(rotation = 45)           
    plt.yticks(rotation = 40)
    plt.grid(True)

    i = 0
    while True:
        i += 1
        newname = '%s%s.png'%('graphic', str(i))
        if os.path.exists('./storage/'+ newname):
            continue
        plt.savefig('./storage/'+ newname)
        break

    graphic = 'http://localhost:5000/storage/'+ newname
    graphicvalues = {
        'Xaxis' : valuex,
        'Yaxis' : valuey,
        'graphic' : graphic
    }
    return render_template('result_page.html', graphicvalues = graphicvalues)

@app.route('/storage/<filename>')
def storage(filename):
    return send_from_directory('./storage', filename)

# activate server
if __name__ == '__main__':
    app.run(debug=True)
