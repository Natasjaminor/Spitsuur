
# Tkinter zit standaard in python xy
import Tkinter
root = Tkinter.Tk()

canvas = Tkinter.Canvas(root, width = 300, height = 300)
canvas.pack()

canvas.create_line(0,300,300,300)
canvas.create_line(300,300,300,0)
# nog geen linker verticale lijn en nog geen boven horizontale lijn

for row in range(6): # maakt rijen en kolommen
    for column in range(6):
        canvas.create_line(50 *column, 0, 50 * column, 400)
        canvas.create_line(0, 50 * row, 400, 50 * row)

canvas.create_rectangle(150, 0, 100, 150, fill="purple") # Een auto

root.mainloop()
