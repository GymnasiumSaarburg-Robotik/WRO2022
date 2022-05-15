# import the library
from appJar import gui
import re

# handle button events
def press(button):
    if button == "Cancel":
        app.stop()
    else:
        try:
            data = app.getTextArea("Data")
            data = re.findall('\[(.*?)\]', data)
            first = True
            for block in data:
                if first:
                    block = block.replace("175, 193, 33, 42, 82, 7, ", "")
                block = block.replace("1, 0, ", "", 1)
                blockAsStringList = block.split(",")
                blockAsStringList = blockAsStringList[:-4]
                data = [int(x) for x in blockAsStringList]
                first = False
                summed_data = []
                c1 = app.getCanvas("c1")

                num_hash = 0
                for i in range(len(data)):
                    num_hash += data[i]
                    if i % 2 != 0:
                        summed_data.append(num_hash)
                        num_hash = 0

                for i in range(1, int(len(summed_data) / 4) + 1):
                    base_index = i * 4 - 1
                    offset = 1000

                    x_center = offset + summed_data[base_index - 3]
                    y_center = summed_data[base_index - 2]
                    width = summed_data[base_index - 1]
                    height = summed_data[base_index]

                    c1.create_rectangle(
                        x_center - int(width / 2),
                        y_center - int(height / 2),
                        x_center + int(width / 2),
                        y_center + int(height / 2)
                    )
        except:
            app.errorBox("Fehler", "Daten invalide. Kopf entfernen")


app = gui("Login Window", "400x200")
app.setBg("white")

app.addLabel("title", "Data visualization | Remove head before usage")
app.setLabelBg("title", "white")
app.setLabelFg("title", "black")

app.addTextArea("Data")
app.setTextAreaHeight("Data", 10)
app.addButtons(["Submit", "Cancel"], press)

canvas = app.addCanvas("c1")
# outside box
canvas.create_rectangle(1000, 0, 1316, 208)

app.setSize("Fullscreen")
app.go()
