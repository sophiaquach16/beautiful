from sanic import Sanic
from sanic.response import text, redirect
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


@app.route("/admin/product/create")
def view_product_create(request):
    return jinja.render('admin_product_create.html', request)

@app.route("/admin/controllers/product-create/", methods=['POST'])
def controller_product_create(request):
    product_data = request.form
    product = data.db.Product()
    product.name = product_data["name"][0]
    product.company = product_data["company"][0]
    product.price = float(product_data["price"][0])
    product.size = float(product_data["size"][0])
    product.unit = product_data["unit"][0]
    product.description = product_data["description"][0]

    products = data.db.ProductsAcessor('data/db.json')
    products.load()
    products.add(product)
    products.save()
    return redirect(app.url_for('view_products_list'))

@app.route("/admin/product/<id>", methods=['GET'])
def view_product(request, id):
    products = data.db.ProductsAcessor('data/db.json')
    products.load()
    return jinja.render('admin_product.html', 
                        request, 
                        product=products.items[id],
                        productId=id, 
                        )

@app.route("/admin/controllers/product-delete/<id>", methods=['POST'])
def controller_product_delete(request, id):
    products = data.db.ProductsAcessor('data/db.json')
    products.load()
    if id in products.items:
        products.delete(id)
        products.save()
        return redirect(app.url_for('view_products_list'))
    else:
        return text("This product does not exist", status=404)

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