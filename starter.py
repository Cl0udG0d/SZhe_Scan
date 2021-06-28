from app import create_app
from flask import render_template

app=create_app()

@app.route("/")
@app.route("/login/")
def index():
    return render_template("login.html")

if __name__ == "__main__":
    app.logger.warning(
        """
        ----------------------------
        |  app.run() => flask run  |
        ----------------------------
        """
    )
    app.logger.warning(
        """
        路由:\n{}
        """.format(app.url_map)
    )
    app.run()
