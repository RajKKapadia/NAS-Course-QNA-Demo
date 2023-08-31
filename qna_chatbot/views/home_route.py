from flask import Blueprint

home = Blueprint(
   'home',
   __name__
)

@home.route('/', methods=['GET', 'POST'])
def home_route():
    return 'Application is working okay.', 200
