from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime
from datetime import date
from dataDb import Database
from lang import languages
from googletrans import Translator

app = Flask(__name__)
count = 0

menu_option = ['add', 'delete', 'budget', 'language', 'report']
select_cat = ['food', 'travel', 'rent', 'entertainment', 'shopping']
greet = ["hello", "hi", "what's up", "yo", "greetings!", "greet", "greeting"]


@app.route("/webhook", methods=['POST'])
def reply():
    db = Database()
    incoming = request.form.get('Body').lower()
    incoming_msg = translate(incoming, "en").lower()
    print(incoming_msg)
    sender_info = request.form.get('From').split(':')
    sender_info = int(sender_info[-1])
    response = MessagingResponse()
    message = response.message()
    responded = False
    words = incoming_msg.split()

    if incoming_msg in greet:
        if db.check_for_account(number=sender_info) == True and db.check_lang(number=sender_info) == True:
            reply = "*Welcome User* \nWhat do you want to do?\n\n• *Add an Expense* 📝\n• *Delete an Expense* ❌\n• *Change Budget Amount* 💰\n• *Change Language* 💬\n• *Send Report* 📊"
            reply_trs = translate(reply, db.read_language(number=sender_info))
            message.body(reply_trs)
            responded = True
        elif db.check_for_account(number=sender_info) == False:
            reply = "Looks like you are not registered! \nDo you want to register? 🤔"
            message.body(reply)
            responded = True

        else:
            reply = "Please select any regional language to continue.\n"
            message.body(reply)
            responded = True

    if len(words) == 1 and incoming_msg in languages.keys():
        db.add_language(number=sender_info, language=languages[incoming_msg])
        reply = "Language updated Successfully!\nPlease type Hello to get started"
        message.body(reply)
        responded = True

    if len(words) == 1 and "yes" in incoming_msg:
        name_string = "Please enter your name"

        message.body(name_string)
        responded = True

    if len(words) == 1 and "no" in incoming_msg:
        reply = "Ok. Have a nice day! 😄"
        message.body(reply)
        responded = True

    elif len(words) > 1 and (words[0] in menu_option or words[1] in menu_option):
        if db.check_for_account(sender_info) == True and db.check_for_field(field='budget', number=sender_info) == True:
            if 'add' in words:
                db.create_temp_menu(number=sender_info,
                                    label="menu", data="add")
                reply = "Select a Category\n\n• *Food* 🍕\n• *Travel* 🏖️\n• *Rent* 🏠\n• *Entertainment* 🎬\n• *Shopping* 🛍️"
                reply_trs = translate(
                    reply, db.read_language(number=sender_info))
                message.body(reply_trs)
                responded = True
            if 'delete' in words:
                db.create_temp_menu(number=sender_info,
                                    label="menu", data="delete")
                reply = "Type Expense Name <space> Date Added"
                reply_trs = translate(
                    reply, db.read_language(number=sender_info))
                message.body(reply_trs)
                responded = True
            if 'budget' in words:
                db.create_temp_menu(number=sender_info,
                                    label="menu", data="budget")
                reply = "Please type your monthly expense budget"
                reply_trs = translate(
                    reply, db.read_language(number=sender_info))
                message.body(reply_trs)
                responded = True
            if 'language' in words:
                db.create_temp_menu(number=sender_info,
                                    label="menu", data="language")
                reply = "Type in any regional language\n"
                reply_trs = translate(
                    reply, db.read_language(number=sender_info))
                message.body(reply_trs)
                responded = True
            if 'report' in words:
                db.create_temp_menu(number=sender_info,
                                    label="menu", data="report")
                reply = "Please type a date range in the format: dd/mm/yy"
                reply_trs = translate(
                    reply, db.read_language(number=sender_info))
                message.body(reply_trs)
                responded = True

        elif db.check_for_account(sender_info) == True or db.check_for_field(field='budget', number=sender_info) == False:
            db.create_temp_menu(number=sender_info,
                                label="menu", data="budget")
            reply = "Looks like you didn't specify your expense budget! Let's quickly add one!\nPlease type your monthly expense budget"
            reply_trs = translate(reply, db.read_language(number=sender_info))
            message.body(reply_trs)
            responded = True

        else:
            reply = "Sorry I didn't get that! Please try again 😕"
            reply_trs = translate(reply, db.read_language(number=sender_info))
            message.body(reply_trs)
            responded = True

    elif len(words) == 1 and words[-1].isnumeric() == True:
        if db.read_temp_menu(number=sender_info, label="menu") == 'budget':
            amt = int(words[0])
            db.add_budget(budget=amt, number=sender_info)
            reply = "Budget Added Successfully! 🎉\nPlease type Hello to get started"
            reply_trs = translate(reply, db.read_language(number=sender_info))
            message.body(reply_trs)
            responded = True
        else:
            reply = "Please select a valid option 🙄"
            reply_trs = translate(reply, db.read_language(number=sender_info))
            message.body(reply_trs)
            responded = True

    elif len(words) == 1 and words[0] in select_cat:
        if 'food' in words:
            db.create_temp_menu(number=sender_info,
                                label="category", data="food")
            reply = "Please type expense name <space> price"
            reply_trs = translate(reply, db.read_language(number=sender_info))
            message.body(reply_trs)
            responded = True
        if 'travel' in words:
            db.create_temp_menu(number=sender_info,
                                label="category", data="travel")
            reply = "Please type expense name <space> price"
            reply_trs = translate(reply, db.read_language(number=sender_info))
            message.body(reply_trs)
            responded = True
        if 'rent' in words:
            db.create_temp_menu(number=sender_info,
                                label="category", data="rent")
            reply = "Please type expense name <space> price"
            reply_trs = translate(reply, db.read_language(number=sender_info))
            message.body(reply_trs)
            responded = True
        if 'entertainment' in words:
            db.create_temp_menu(number=sender_info,
                                label="category", data="entertainment")
            reply = "Please type expense name <space> price"
            reply_trs = translate(reply, db.read_language(number=sender_info))
            message.body(reply_trs)
            responded = True
        if 'shopping' in words:
            db.create_temp_menu(number=sender_info,
                                label="category", data="shopping")
            reply = "Please type expense name <space> price"
            reply_trs = translate(reply, db.read_language(number=sender_info))
            message.body(reply_trs)
            responded = True

    elif len(words) > 1 and words[-1].isnumeric() == True:
        label = words[0]
        price = int(words[-1])
        if db.read_temp_menu(number=sender_info, label="menu") == 'add':
            category = db.read_temp_menu(number=sender_info, label="category")
            db.per_field_spend(number=sender_info,
                               catagory=category, field=label, amount=price)
            total_spend = db.check_totalSpend(number=sender_info)
            check_budget = db.check_budget(number=sender_info)
            if total_spend >= check_budget:
                reply = "Expense Added Successfully! 🎉\n🔴 *Alert* 🔴\n\nYou have reached you're monthly expense limit!\nWe advice you to *reduce* your expending"
                reply_trs = translate(
                    reply, db.read_language(number=sender_info))
                message.body(reply_trs)
                responded = True

            else:
                reply = "Expense Added Successfully! 🎉"
                reply_trs = translate(
                    reply, db.read_language(number=sender_info))
                message.body(reply_trs)
                responded = True
        else:
            reply = "Please select a valid option 🙄"
            reply_trs = translate(reply, db.read_language(number=sender_info))
            message.body(reply_trs)
            responded = True

    elif len(words) > 1 and is_date_format(words[-1]) == True:
        label = words[0]
        date_1 = words[0]
        date_2 = words[-1]
        print(date_1, date_2)
        amt = words[1]
        read = db.read_temp_menu(number=sender_info, label='menu')
        print(read)
        if (read == 'delete'):
            # if is_expense_exist(label,date_2) == True:
            if db.delete_perfield_spend(number=sender_info, field=label, date=date_2, amt=amt) == False:
                # delete_expense(label,date_2)
                reply = "Sorry! Expense does not exist! Try again 😕"
                reply_trs = translate(
                    reply, db.read_language(number=sender_info))
                message.body(reply_trs)
                responded = True
            else:
                reply = "Expense Deleted Successfully! 👌"
                reply_trs = translate(
                    reply, db.read_language(number=sender_info))
                message.body(reply_trs)
                responded = True

        elif (read == 'report'):
            # if is_date_valid(date_1, date_2) == True:
            # send_report(date_1, date_2)
            print(f"date - {date_1,date_2}")
            data_report = db.report(
                number=sender_info, date1=date_1, date2=date_2)
            start_date = date_1
            end_date = date_2
            month_budget = data_report['budget']
            total_spend = data_report['totalSpend']
            food = data_report['catgoryTotalSpend']['food']
            travel = data_report['catgoryTotalSpend']['travel']
            rent = data_report['catgoryTotalSpend']['rent']
            entertainment = data_report['catgoryTotalSpend']['entertainment']
            shoping = data_report['catgoryTotalSpend']['shopping']
            money_l = data_report['moneyLeft']

            reply = f"*Here is your report* 📊\n\n1. *Starting Date* 📅: {start_date}\n\n2. *Ending Date* 📅: {end_date}\n\n3. *Monthly Budget* 💰: {month_budget}\n\n4. *Total Spend* 🤑: {total_spend}\n\n5. *Category Wise Spending*: \n\n- *Food* 🍕: {food}\n\n- *Travel* 🏖️: {travel}\n\n- *Rent* 🏠: {rent}\n\n- *Entertainment* 🎬: {entertainment}\n\n- *Shopping* 🛍️: {shoping}\n\n6. *Money Left* 💵: {money_l}"
            reply_trs = translate(
                reply, db.read_language(number=sender_info))
            message.body(reply_trs)
            responded = True
            # else:
            #     reply = "Please enter a valid date range"
            #     reply_trs = translate(
            #         reply, db.read_language(number=sender_info))
            #     message.body(reply_trs)
            #     responded = True
        else:
            reply = "Please select a valid option 🙄"
            reply_trs = translate(reply, db.read_language(number=sender_info))
            message.body(reply_trs)
            responded = True

    elif len(words) > 1 and db.check_for_account(number=sender_info) == False:
        db.add_account(number=sender_info, name=incoming_msg)
        reply = "User Added Successfully! 🎉\nPlease type hello to get started"
        reply_trs = translate(reply, db.read_language(number=sender_info))
        message.body(reply_trs)
        responded = True

    if not responded:
        reply = "Sorry! I didn't get that.\nPlease try again! 😕"
        reply_trs = translate(reply, db.read_language(number=sender_info))
        message.body(reply_trs)

    return str(response)


def translate(msg, lang):
    translator = Translator()
    translation = translator.translate(msg, dest=lang)
    return translation.text


def is_date_format(date):
    format = "%d/%m/%Y"
    try:
        res = bool(datetime.strptime(date, format))
        return res
    except ValueError:
        return False


if __name__ == "__main__":
    app.run(debug=True)
