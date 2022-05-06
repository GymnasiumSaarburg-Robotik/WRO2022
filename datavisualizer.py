# import the library
from appJar import gui


# handle button events
def press(button):
    if button == "Cancel":
        app.stop()
    else:
        data = app.getTextArea("Data")



# create a GUI variable called app
app = gui("Login Window", "400x200")
app.setBg("white")
app.setFont(18)

# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("title", "Welcome to appJar")
app.setLabelBg("title", "white")
app.setLabelFg("title", "black")

app.addTextArea("Data")

# link the buttons to the function called press
app.addButtons(["Submit", "Cancel"], press)

app.addGoogleMap("m1")
app.setGoogleMapSize("m1", "300x500")

# start the GUI
app.go()
