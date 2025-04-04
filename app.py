from flask import Flask, render_template


class App:
    def __init__(self):
        self.app = Flask(__name__)


    def create_website(self, movies):
        """renders index.html using movies list of dictionaries"""
        @self.app.route('/')
        def index():
            return render_template('index.html', movies=movies)


        self.app.run(debug=False)
