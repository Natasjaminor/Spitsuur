
# Tkinter zit standaard in python xy
import Tkinter

class Visualization:
    def __init__(self, width, height):
        #self.num_autos = num_autos
        self.max_dim = max(width, height)
        self.width = width
        self.height = height

        #draw canvas
        self.root = Tkinter.Tk()
        self.canvas = Tkinter.Canvas(self.root, width = 500, height = 500)
        self.canvas.pack()
        self.root.update()
       
        x1, y1 = self._map_coords(0, 0)
        x2, y2 = self._map_coords(width, height)
        self.canvas.create_rectangle(x1, y1, x2, y2, fill = "white")

        for i in range(width + 1):
            x1, y1 = self._map_coords(i, 0)
            x2, y2 = self._map_coords(i, height)
            self.canvas.create_line(x1, y1, x2, y2)
        for i in range(height + 1):
            x1, y1 = self._map_coords(0, i)
            x2, y2 = self._map_coords(width, i)
            self.canvas.create_line(x1, y1, x2, y2)

    def _map_coords(self, x, y):
        "Maps grid positions to window positions (in pixels)."
        return (250 + 450 * ((x - self.width / 2.0) / self.max_dim),
                250 + 450 * ((self.height / 2.0 - y) / self.max_dim))

    def done(self):
        mainloop()

a = Visualization(300,300)

<<<<<<< HEAD

gdfgjdfgdfg
dh
dhdh
dh
dfhd
h
=======
bnsdfjbsnbfnsfhbsbf
sdbfsbfsbfmbsfmbsmnfb
sdfsbdfmsbfbsfbsfbk
sdnfbsmnfbmsbfmsbfmbsfmnbsf
sdjfnmsbfmnsbfmsbf
>>>>>>> 8b6a29d65c7339363ef7604bc9c4673de4a5897f
