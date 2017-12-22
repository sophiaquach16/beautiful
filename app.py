from sanic import Sanic
from sanic.response import text
from sanic_session import InMemorySessionInterface
from sanic_jinja2 import SanicJinja2
import data.db

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
    products = data.db.ProductsAcessor('data/db.json')
    products.load()
    return jinja.render('admin_product_list.html', request, items=products.items) # render is returning the webpage


@app.route("/admin/product/<id>")
def view_product(request, id):
    products = data.db.ProductsAcessor('data/db.json')
    products.load()
    return jinja.render('admin_product.html', 
                        request, 
                        productId=id, 
                        company=products.items[id].company,
                        name=products.items[id].name,
                        price=products.items[id].price,
                        size=products.items[id].size,
                        unit=products.items[id].unit,
                        description=products.items[id].description
                        )


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