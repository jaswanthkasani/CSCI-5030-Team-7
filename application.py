from os import terminal_size
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from hunspell import Hunspell
import string
import sys
import langDetect


app = Flask(__name__, template_folder="templates")
app.config["TEMPLATES_AUTO_RELOAD"] = True

h = Hunspell()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form["submit_button"] == "submit":
            if not request.form.get("text"):
                error = "Please provide a text to check"
                return render_template("index.html", error=error)
            text = request.form.get("text")
            punc = '''!()-[]{};:"\,<>./?@#$%^&*_~'''
            for element in text:
                if element in punc:
                    text = text.replace(element, "")
            words = text.split()
            misspelled = []
            # Amir
            # this function check if text in english or not
            isEng = langDetect.detect(words)
            notEng = ""
            if not(langDetect.detect(words)):
                notEng = "The text is not in English."
            else:
                notEng = "The text is in English."

            suggestions = ""
            # end Amir
            if (isEng):
                for word in words:
                    if h.spell(word) == True:
                        continue
                    misspelled.append(word)
                suggestions = dict.fromkeys(misspelled)
                for key in suggestions:
                    suggestions[key] = h.suggest(key)

            return render_template("/index.html", text=text, misspelled=misspelled, suggestions=suggestions, notEng=notEng)

        elif request.form["submit_button"] == "clear":
            return render_template("/index.html")

        elif request.form["submit_button"] == "example":

            example_dict = {
                1: 'What can I do with this?',
                2: "As you can easily notice the second block of text looks more realistic.",
                3: "Sam is looking for a job.",
                4: "I need to buy some things from IKEA.",
                5: "I hope to visit Peru again in the future."
            }

            #rand_num = random.randint(0, len(example_arr))
            example_text = example_dict[1]
            print(example_text)
            return render_template("/index.html", example_text=example_text)

    else:
        return render_template("/index.html")


if __name__ == "__main__":

    app.run()