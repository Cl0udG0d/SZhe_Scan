from flask import Flask, request,render_template, render_template_string
from jinja2 import Template

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xca\x0c\x86\x04\x98@\x02b\x1b7\x8c\x88]\x1b\xd7"+\xe6px@\xc3#\\'


@app.route('/ssti')
def ssti():
    if request.values.get('name'):
        name = request.values.get('name')
        template = "<p>{name}<p1>".format(name=name)
        return render_template_string(template)

        # template = Template('<p>%s<p1>' %name)
        # return template.render()

        # template = "<p>{{ name }}<p1>"
        # return render_template_string(template, name=name)
    else:
        return render_template_string('<p>输入name值</p>')

if __name__ == '__main__':
    app.run()