from googletrans import Translator
# translator = Translator()
# translation = translator.translate("खर्चा जोड़े",dest='en')
# print(translation.text)

def translate(msg,lang):
    translator = Translator()
    translation = translator.translate(msg,dest=lang)
    return translation.text

text = translate("*Welcome User* \nWhat do you want to do?\n\n• *Add an Expense* 📝\n• *Delete an Expense* ❌\n• *Change Budget Amount* 💰\n• *Send Report* 📊","hi")
print(text)

