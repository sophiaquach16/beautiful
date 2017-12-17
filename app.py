from sanic import Sanic
from sanic.response import text
from sanic_session import InMemorySessionInterface
from sanic_jinja2 import SanicJinja2


app = Sanic()
jinja = SanicJinja2(app)
session_interface = InMemorySessionInterface()


@app.middleware('request')
async def add_session_to_request(request):
    # before each request initialize a session
    # using the client's request
    await session_interface.open(request)


@app.middleware('response')
async def save_session(request, response):
    # after each request save the session,
    # pass the response to set client cookies
    await session_interface.save(request, response)


@app.route("/admin/product")
def view_products_list(request):
    return jinja.render('admin_product_list.html', request) # render is returning the webpage


@app.route("/admin/product/<id>")
def view_product(request, id):
    return jinja.render('admin_product.html', request)


@app.route("/admin/login")
def view_login(request):
    return jinja.render('admin_login.html', request)


@app.route("/")
async def index(request):
    # interact with the session like a normal dict
    if not request['session'].get('foo'):
        request['session']['foo'] = 0

    request['session']['foo'] += 1

    return jinja.render('index.html', request, greetings='Hello, sanic!')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)