import json
import uuid

class Product:
    id = ""
    price = 0.00
    company = ""
    code = ""
    name = ""
    size = 0
    unit = ""
    description = "Lol"

class ProductsAcessor: # what you are going to use to connect your product objects with the json file
    def __init__(self, file_path):
        self.file_path = file_path # where is the json file you want to connect to 
        self.items = {} # dictionary of items, representation of all items in the json file
    
    def load(self): # read all items in the json file and create products
        data = json.load(open(self.file_path)) # first step is opening the file path, returns a stream
        # data will be your dictionary representing the json file, it copies the physical location in the memory
        for item in data["products"]: # for each item in the products key
            self.__add_from_json(item) # each item is a dictionary

    def __add_from_json(self, value): # value is item, a dictionary (the parameter)
        key = value["id"] # key is the dictionary's id value
        product = Product()
        product.id = key
        product.price = value["price"]
        product.company = value["company"]
        product.name = value["name"]
        product.size = value["size"]
        product.unit = value["unit"]
        product.description = value["description"]
        self.items[key] = product 
        # self.items is a dictionary of items, in this dictionary, key: item's id, value: product

    def save(self): # creates a new empty array of data
        item_data = []
        for key in self.items:
            item_data.append(self.items[key].__dict__) # add in the item_data a dictionary that is built from the item
            # located at this key, .__dict__ takes your class and converts it into a dictionary of data
        data = json.load(open(self.file_path)) # open your file 
        data["products"] = item_data # replace the value stored at the product key by item_data
        json.dump(data, open(self.file_path, mode="w"), indent=4, sort_keys=True)
        

    def add(self, p): # adding to a new product in memory collection
        if p.id is "":
            p.id = str(uuid.uuid4())
        elif p.id in self.items: # check if any of the items in the json file have this same key
            raise Exception("Already has a product with this ID")
        self.items[p.id] = p

    def delete(self, productId):
        del self.items[productId]


pa = ProductsAcessor("db.json")
pa.load() # called only once in the web app, started at initialization in app

# pa.delete("ec709316-2f8a-4080-92d6-084d0c497467") this deletes
# pa.items["ec709316-2f8a-4080-92d6-084d0c497467"].name = "Super Potato Item" this modifies
# pa.items["ec709316-2f8a-4080-92d6-084d0c497467"].price = 225 this modifies

# these bottom two methods can be called many times, each together
# pa.add(pa.items["ec709316-2f8a-4080-92d6-084d0c497467"])

pa.save()