# Channel 4 Test App
# Flask server

# Imports
import os
import flask
from flask import Flask, redirect, render_template, request, url_for
import openai

# Get OpenAI API key
openai.api_key = "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"

# Declarations
app = Flask(__name__)

# Functions


# Performs a request to ChatGPT
# Returns the response to the query
def do_gpt(text, temp=0.5):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        temperature=temp
    )

    return response.choices[0].text


# Processes the Mood Search
# returns the string for the web client to display
def do_search(req):
    # get all values from the form
    mood_text = req.form.get("mood-text")
    show_count = int(req.form.get("mood-count"))
    emotion_count = 0

    # process free-text entry
    count = 0

    if mood_text != '':
        emotion_list = do_gpt("Summarise the following as a comma separated array of emotions: '" +
                             mood_text +
                             "' that can be parsed in Python")

        emotion_list = emotion_list.split(",")

        for a in emotion_list:
            count += 1

    if mood_text == '' or count == 0:
        if req.form.get("mood-happy") == "on":
            mood_text = "happy"
        if req.form.get("mood-sad") == "on":
            mood_text = "sad"
        if req.form.get("mood-lonely") == "on":
            mood_text = "lonely"
        if req.form.get("mood-naughty") == "on":
            mood_text = "naughty"

    # pluralise show(s)
    text_show = "show"

    if show_count > 1:
        text_show += "s"

    # form the text block to send to ChatGPT
    response = do_gpt("Hey ChatGPT - I'm feeling " +
                      mood_text +
                      ". Can you recommend " +
                      str(show_count) +
                      " " +
                      text_show +
                      " on Channel 4 to help me?")

    # return the response
    return response


@app.route("/", methods=("GET", "POST"))
def index():

    # Handle POST requests
    if request.method == "POST":
        response = do_search(request)

        return redirect(url_for("index", result=response))

    result = request.args.get("result")
    return render_template("index.html", result=result)


# Main
if __name__ == '__main__':
    app.run()