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
app.addLabel("title", "Data visualization")
app.setLabelBg("title", "white")
app.setLabelFg("title", "black")

app.addTextArea("Data")
app.setTextAreaHeight("Data", 10)

# link the buttons to the function called press
app.addButtons(["Submit", "Cancel"], press)


canvas = app.addCanvas("c1")
canvas.create_rectangle(1000, 0, 1316, 208)

app.setSize("Fullscreen")

# start the GUI
app.go()
