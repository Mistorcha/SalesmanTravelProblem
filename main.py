import tkinter as tk
import random as rdm
from math import sqrt


# Class to create the map with cities in red squares ##########################
class Map(object):

    def __init__(self, nb_cities, map_height, map_width):
        self.nb_cities = nb_cities
        self.map_height = map_height
        self.map_width = map_width
        self.list_cities = []

    def draw_cities(self):
        for i in range(len(self.list_cities)):
            can.create_rectangle(self.list_cities[i][0]-3,
                                 self.list_cities[i][1]-3,
                                 self.list_cities[i][0]+3,
                                 self.list_cities[i][1]+3, fill="red")
        print(self.list_cities)

    def list_of_cities(self):
        can.delete("all")
        self.list_cities = []
        i = 0
        while i < self.nb_cities:
            x = rdm.randrange(10, self.map_width-10, 10)
            y = rdm.randrange(10, self.map_height-10, 10)
            if [x, y] not in self.list_cities:
                self.list_cities.append([x, y])
                i += 1
        self.draw_cities()
###############################################################################


# Class for the roads, list of cities randomly selected from the list #########
# of cities in the map.
class Population(object):

    def __init__(self, other):
        """Initialise the length of the road and randomly select the order
        of the road"""
        self.road_lenght = 0
        self.road_order = rdm.sample(other.list_cities, len(other.list_cities))

    def draw_road(self):
        "Draw on the canvas the link between the cities"
        print(test.road_order)
        for i in range(len(self.road_order)-1):
            can.create_line(self.road_order[i][0],
                            self.road_order[i][1],
                            self.road_order[i+1][0],
                            self.road_order[i+1][1], fill="green")
            can.create_line(self.road_order[-1][0],
                            self.road_order[-1][1],
                            self.road_order[0][0],
                            self.road_order[0][1], fill="green")

    def square_root(self, i):
        "Used to calculate the length between two cities"
        dx = abs(self.road_order[i][0] -
                 self.road_order[i+1][0])
        dy = abs(self.road_order[i][1] -
                 self.road_order[i+1][1])
        return sqrt(dx * dx + dy * dy)

    def lenght_of_road(self):
        "Measure the length of the road using self.square_root"
        self.road_lenght = 0
        for i in range(len(self.road_order)-1):
            self.road_lenght += self.square_root(i)
        self.road_lenght += self.square_root(-1)
        print(self.road_lenght)
###############################################################################


# Assignation of variables ####################################################
hgt = 800
wdt = 800
nbc = 25
###############################################################################

# Main Program (To clean)######################################################
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry(f"{wdt}x{hgt+50}+50+50")
    can = tk.Canvas(root, height=hgt, width=wdt, bg="dark grey")
    can.grid(row=0, column=0, columnspan=2)
    testMap = Map(nbc, hgt, wdt)
    testMap.list_of_cities()
    test = Population(testMap)
    but3 = tk.Button(root, text="draw road", command=test.draw_road)
    but3.grid(row=1, column=0)
    but4 = tk.Button(root, text="Lenght road", command=test.lenght_of_road)
    but4.grid(row=1, column=1)
    root.mainloop()
###############################################################################
