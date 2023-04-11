from pymongo import MongoClient
from datetime import datetime
from datetime import date as dt
import os
from dotenv import load_dotenv
load_dotenv('./.env')
print(os.environ.get('DATABASE'))


class Database:
    def __init__(self):
        self.client = MongoClient(os.environ.get('DATABASE'))
        self.db = self.client["clientDB"]
        self.collection = self.db["client_data"]
        self.food = self.db["food"]
        self.travel = self.db["travel"]
        self.rent = self.db["rent"]
        self.entertainment = self.db["entertainment"]
        self.shopping = self.db["shopping"]
        self.temp_collection = self.db["temp"]
        self.catMap = {
            'food': self.food,
            'travel': self.travel,
            'rent': self.rent,
            'entertainment': self.entertainment,
            'shopping': self.shopping
        }

    # check existence of account and return value in boolean
    def check_for_account(self, number):
        """check for account exist or not"""
        found = self.collection.find_one({"number": number})
        if found is None:
            return False
        return True

    # add account
    def add_account(self, number, name):
        self.collection.insert_one(
            {"number": number, "name": name})

    ########################################## ---ADD AND CHECK BUDGET-----#################################

    # add_budget
    def add_budget(self, budget, number):
        """add user budget field"""
        budget_d = self.collection.update_one(
            {"number": number}, {"$set": {"budget": budget}})

    def check_budget(self, number):
        test = self.collection.find_one(
            {"number": number, "budget": {"$exists": True}}, {"_id": 0, "budget": 1})
        if test is None:
            return False
        return test["budget"]

    # --Add catagory budget
    def catagory_budget(self, number, catagory, amount):
        self.collection.update_one(
            {"number": number}, {"$inc": {f"catgBudget.{catagory}": amount}})

    def update_Catagory_budget(self, number, catagory, amount):
        self.collection.update_one({"number": number, f"catgBudget.{catagory}": {"$exists": True}},
                                   {"$inc": {f"catgBudget.{catagory}": -amount}})

    # check for existence of field basically parent field

    def check_for_field(self, field, number):
        """check for field and return True if exist"""
        field_c = self.collection.find_one(
            {"number": number, f"{field}": {"$exists": True}})
        if field_c is None:
            return False
        else:
            return True

    ############################################## --ADD SPEND --##############################################

    def per_field_spend(self, number, catagory, field, amount):
        date = datetime.now()
        find = self.collection.find_one({"number": number}, {"_id": 1})
        id = find["_id"]
        cat_check = self.catMap[catagory].find_one({"_id": id})
        if cat_check is not None:
            transaction = {
                "transaction_name": field,
                "amount": amount,
                "date": date
            }
            self.catMap[catagory].update_one(
                {"_id": id}, {"$push": {"transaction": transaction}})
        else:
            self.catMap[catagory].insert_one({"_id": id, "transaction": [{
                "transaction_name": field,
                "amount": amount,
                "date": date
            }]})
        self.catagory_total_spend(
            number=number, amount=amount, catagory=catagory)
        self.total_spend(number, amount)
#
#
###################################### --DELETE PARTICULER SPEND----################################################################
#

    def delete_perfield_spend(self, number, field, amt, date):
        amount = int(amt)
        tempd = date.split('/')
        dt = datetime(int(tempd[2]), int(tempd[1]), int(tempd[0]))
        dt_2 = datetime(int(tempd[2]), int(tempd[1]),
                        int(tempd[0]), 23, 59, 59)
        find = self.collection.find_one({"number": number}, {"_id": 1})
        if find is not None:
            id = find["_id"]
            for catg in self.catMap:
                catData = self.catMap[catg].find_one(
                    {"_id": id, "transaction.transaction_name": field, "transaction.amount": amount,
                     "transaction.date": {"$gte": dt, "$lte": dt_2}}, {"_id": 0})
                if catData is not None:
                    temp = []
                    temp_amount = 0
                    for item in catData['transaction']:
                        item['date']
                        if item['transaction_name'] == field and item['amount'] == amount and item['date'] > dt and item['date'] < dt_2:
                            temp_amount = temp_amount+item['amount']
                            temp.append(item)
                    self.catMap[catg].update_one(
                        {"_id": id}, {"$pull": {"transaction": {"$in": temp}}})
                    self.update_total_spend(number=number, amount=temp_amount)
                    self.update_Catagory_total_spend(
                        number=number, catagory=catg, amount=temp_amount)
                    return True
            return False

    ################################################ --ADD, UPDATE AND CHECK PERFIELD SPEND------####################################################################
    def catagory_total_spend(self, number, catagory, amount):
        self.collection.update_one(
            {"number": number}, {"$inc": {f"catgTotalSpend.{catagory}": amount}})

    def update_Catagory_total_spend(self, number, catagory, amount):
        self.collection.update_one({"number": number, f"catgTotalSpend.{catagory}": {"$exists": True}},
                                   {"$inc": {f"catgTotalSpend.{catagory}": -amount}})
    #################################################### --ADD ,UPDATE AND CHECK TOTAL SPEND---###################################################################

    def total_spend(self, number, amount):
        if not self.check_for_field(field="total_spend", number=number):
            self.collection.update_one(
                {"number": number}, {"$set": {"total_spend": amount}})
        else:
            self.collection.update_one(
                {"number": number}, {"$inc": {"total_spend": amount}})
        print(self.collection.find_one({"number": number, f"total_spend": {"$exists": True}},
                                       {"_id": 0, "total_spend": 1}))

    def update_total_spend(self, number, amount):
        self.collection.update_one(
            {"number": number}, {"$inc": {"total_spend": -amount}})

    def check_totalSpend(self, number):
        test = self.collection.find_one({"number": number, "total_spend": {
            "$exists": True}}, {"_id": 0, "total_spend": 1})
        if test is None:
            return False
        return test["total_spend"]

    ##################################################### --ADD AND READ TEMP DATA----#############################################################################

    def create_temp_menu(self, number, label, data):
        test = self.temp_collection.find_one({"number": number})
        if test is not None:
            self.temp_collection.update_one(
                {"number": number}, {"$set": {f"{label}": data}})
        else:
            self.temp_collection.insert_one(
                {"number": number, f"{label}": data})

    def read_temp_menu(self, number, label):
        data = self.temp_collection.find_one(
            {"number": number, f"{label}": {"$exists": True}}, {f"{label}": 1})
        if data is not None:
            self.temp_collection.update_one(
                {"number": number}, {"$unset": {f"{label}": data[f"{label}"]}})
            return data[f"{label}"]

    ##################################################### --Store and Language ---########################################################################################

    def add_language(self, number, language):
        data = self.collection.update_one(
            {"number": number}, {"$set": {"language": language}})

    def check_lang(self, number):
        data = self.collection.find_one(
            {"number": number, "language": {"$exists": True}})
        if data is None:
            return False
        else:
            return True

    def read_language(self, number,):
        data = self.collection.find_one({"number": number}, {'language': 1})
        return data['language']

    ###########################################

    def per_field_over_spend(self, number, field, amount):
        self.collection.update_one(
            {"number": number}, {"$push": {"catgOverSpend": {field: amount}}})

    def update_perfield_total_spend(self, number, field, amount):
        self.collection.update_one({"number": number, f"catgOverSpend.{field}": {"$exists": True}},
                                   {"$inc": {f"catgTotalSpend.$.{field}": -amount}})

    def report(self, number, date1, date2):
        tempd1 = date1.split('/')
        tempd2 = date2.split('/')
        dt = datetime(int(tempd1[2]), int(tempd1[1]), int(tempd1[0]))
        dt_2 = datetime(int(tempd2[2]), int(tempd2[1]),
                        int(tempd2[0]), 23, 59, 59)
        print(dt, dt_2)
        find = self.collection.find_one({"number": number})
        tmpDic = {}
        if find is not None:
            id = find["_id"]
            totelSpend = 0
            catagoryTotalSpend = {}
            # catMoneyLeft = {}
            for catg in self.catMap:
                catData = self.catMap[catg].find_one(
                    {"_id": id, "transaction.date": {"$gte": dt, "$lte": dt_2}}, {"_id": 0})
                catSpend = 0
                if catData is not None:
                    cat = []
                    for item in catData['transaction']:
                        if item['date'] > dt and item['date'] < dt_2:
                            catSpend = catSpend+item['amount']
                            totelSpend = totelSpend+item['amount']
                            cat.append(item)
                    catagoryTotalSpend[catg] = catSpend
                else:
                    catagoryTotalSpend[catg] = 0
            tmpDic['catgoryTotalSpend'] = catagoryTotalSpend
            tmpDic['moneyLeft'] = find['budget']-totelSpend
            tmpDic['budget'] = find['budget']
            tmpDic['totalSpend'] = totelSpend
            tmpDic["number"] = find['number']
            tmpDic["name"] = find['name']
            return tmpDic
