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
    print("I get to here")

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        temperature=temp,
    )

    return response.choices[0].text


# Processes the Mood Search
# returns the string for the web client to display
def do_search(req):
    # get all values from the form
    mood_select = req.form['mood-select']
    mood_text = req.form['mood-text']
    show_count = req.form['mood-count']

    # abort if showCount is out of bounds
    if show_count < 1 or show_count > 5:
        return "Error: show count out of bounds"

    # process free-text entry
    if mood_text != '':
        emotion_count = int(do_gpt("How many emotions are in the following text: '" & mood_text & "'"))

        if emotion_count < 1:
            return "Error: no recognised emotions listed"
        else:
            return do_gpt("Hey ChatGPT - I'm feeling " &
                          mood_text &
                          ". Can you recommend " &
                          show_count &
                          " shows on Channel 4 to help me?")

    # process selected emotions
    print(mood_select)
    print(req.form['mood-happy'])
    print(req.form['mood-sad'])
    print(req.form['mood-lonely'])
    print(req.form['mood-naughty'])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/gpt", methods=("GET", "POST"))
def post_gpt():

    # Handle POST requests
    if request.method == "POST":
        response = do_search(request)

        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


# Main
if __name__ == '__main__':
    app.run(debug=True)