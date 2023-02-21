from flask import Flask, render_template, request

app = Flask(__name__)

gestures = ["Rock", "Palm", "No"]   # All possible gestures, constant variables.
availableGestures = gestures    # All gestures that shall be possible to chose from in the interface. List may change during run.

# All custom pick able keys in the interface.
customKeys = [
    {'keyCode': "0xAD", 'keyName': "Volume Mute key"},
    {'keyCode': "0xAE", 'keyName': "Volume Down key"},
    {'keyCode': "0xAF", 'keyName': "Volume Up key"},
    {'keyCode': "0xB0", 'keyName': "Next Track key"},
    {'keyCode': "0xB1", 'keyName': "Previous Track key"},
    {'keyCode': "0xB2", 'keyName': "Stop Media key"},
    {'keyCode': "0xB3", 'keyName': "Play/Pause Media key"}
] # Keys found at: https://learn.microsoft.com/sv-se/windows/win32/inputdev/virtual-key-codes?redirectedfrom=MSDN

data = []  # Array to manage the dataset.


# Navigates to the main HTML page in templates.
@app.route('/')
def index():
    # Render the template with the data
    return render_template('index.html', data=data, availableGestures=availableGestures, customKeys=customKeys)


# Navigates to the HTML page in templates for adding a new entry.
@app.route('/addRowPage/')
def addRowPage():
    return render_template('addRowPage.html', availableGestures=availableGestures, customKeys=customKeys)


# Adds a new entry into the data set.
@app.route("/addRow/", methods=['POST'])
def addRow():

    if len(availableGestures) <= 0:
        return index()

    _name = request.form['name']
    _gesture = request.form['gesture']
    _key = request.form['key']

    if _gesture not in availableGestures:
        return addRowPage()

    data.append({'name': _name, 'gesture': _gesture, 'key': _key})
    availableGestures.remove(_gesture)

    return index()


# Removes an entry in the dataset.
@app.route("/removeElement/", methods=['POST'])
def removeElement():

    _gesture = request.form['gesture']

    for d in data:
        if _gesture == d.get('gesture'):
            availableGestures.append(_gesture)
            data.remove(d)

    return index()


if __name__ == '__main__':
    app.run(debug=True)
