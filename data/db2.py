import json
import uuid

class User:
    def __init__(self):
        self.id = ""
        self.name = ""
        self.email = ""
        self.number_and_street = ""
        self.city = ""
        self.province_or_state = ""
        self.password = "pw"

class UsersAcessor: 
    def __init__(self, file_path):
        self.file_path = file_path  
        self.temp_items = {} 
    
    def load(self):
        data = json.load(open(self.file_path)) 

        for user in data["users"]: 
            self.__add_from_json(user) 

    def __add_from_json(self, value): 
        key = value["id"] 
        user = User()
        user.id = key
        user.name = value["name"]
        user.email = value["email"]
        user.number_and_street = value["number_and_street"]
        user.city = value["city"]
        user.province_or_state = value["province_or_state"]
        user.password = value["password"]
        self.temp_items[key] = user 

    def save(self): # creates a new empty array of data
        temp_item_data = []
        for key in self.temp_items:
            temp_item_data.append(self.temp_items[key].__dict__) # add in the item_data a dictionary that is built from the item
            # located at this key, .__dict__ takes your class and converts it into a dictionary of data
        data = json.load(open(self.file_path)) # open your file 
        data["users"] = temp_item_data # replace the value stored at the product key by item_data
        json.dump(data, open(self.file_path, mode="w"), indent=4, sort_keys=True)
        

    def add(self, p): # adding to a new product in memory collection
        if p.id is "":
            p.id = str(uuid.uuid4())
        elif p.id in self.temp_items: # check if any of the items in the json file have this same key
            raise Exception("Already has a product with this ID")
        self.temp_items[p.id] = p

    def delete(self, userId):
        del self.temp_items[userId]