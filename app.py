from sanic import Sanic
from sanic.response import text, redirect
from sanic_session import InMemorySessionInterface
from sanic_jinja2 import SanicJinja2
import data.db
import data.db2

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


@app.route("/user/account/create")
def view_account_create(request):
    return jinja.render('user_account_create.html', request)

@app.route("/user/controllers/account-create", methods=['POST'])
def controller_account_create(request):
    user_data = request.form
    user = data.db2.User()
    user.name = user_data["name"][0]
    user.email = user_data["email"][0]
    user.number_and_street = user_data["address"][0]
    user.city = user_data["city"][0]
    user.province_or_state = user_data["province"][0]
    user.password = user_data["password"][0]

    users = data.db2.UsersAcessor('data/db.json')
    users.load()
    users.add(user)
    users.save()
    return redirect(app.url_for('view_login'))
    
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


@app.route("/admin/product-update/<id>", methods=['GET'])
def view_product_update(request, id):
    products = data.db.ProductsAcessor('data/db.json')
    products.load()
    return jinja.render('admin_product_update.html', 
                        request, 
                        product=products.items[id],
                        productId=id, 
                        )

@app.route("/user/controllers/logging-in", methods=['POST'])
def controller_account_login(request):
    users = data.db2.UsersAcessor('data/db.json')
    users.load()

    user_data = request.form
    email = user_data["email"][0]
    if (email in users.temp_items) == False:
        return redirect(app.url_for('view_login'))
    correct_pw = users.temp_items[email].password
    if (correct_pw == user_data["password"][0]):
        return redirect(app.url_for('view_logged_in'))
    else: 
        return redirect(app.url_for('view_login'))

@app.route("/user/account")
def view_logged_in(request):
    return jinja.render('user_home.html', request)


@app.route("/user/controllers/product-update/<id>", methods=['POST'])
def controller_product_update(request, id):
    product_data = request.form

    products = data.db.ProductsAcessor('data/db.json')
    products.load()
    
    products.items[id].name = product_data["name"][0]
    products.items[id].company = product_data["company"][0]
    products.items[id].price = float(product_data["price"][0])
    products.items[id].size = float(product_data["size"][0])
    products.items[id].unit = product_data["unit"][0]
    products.items[id].description = product_data["description"][0]

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