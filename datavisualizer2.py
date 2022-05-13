# import the library
from appJar import gui
import re



# handle button events
def press(button):
    if button == "Cancel":
        app.stop()
    else:
        try:
            s = '[test1]   bhj [test2]'
            result = re.search('[(.*)]', s)
            print(result.group(1))

            data = app.getTextArea("Data")
            data = data.replace("[", "")
            data = data.replace("]", "")
            data = data.replace(" ", "")
            data = data.split(",")
            data = [int(x) for x in data]

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

app.addLabel("title", "Data visualization | [First block (6+14)], [FlwBlock (14)]")
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
