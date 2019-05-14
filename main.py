import tkinter as tk
import random as rdm
from math import sqrt
import tkinter.ttk as ttk


# List of all fuctions for the software #######################################
def redraw_cities_squares():
    "called if spinbox for cities square size is changed"
    my_gui.size_cities = int(my_gui.cities_square_size_sb.get())
    my_gui.canvas.delete("all")
    my_map.draw_cities(my_gui)


def assign_nb_cities():
    "called if spinbox for number of cities is changed"
    my_gui.nb_cities = int(my_gui.nb_cities_spinbox.get())
    my_gui.canvas.delete("all")
    my_map.list_of_cities(my_gui)
    my_map.draw_cities(my_gui)


def assign_mutation_rate():
    "called if spinbox for mutation rate is changed"
    my_gui.mutation_rate = float(my_gui.mutation_rate_sb.get())


def assign_pop_size():
    "called if spinbox of size of the population is changed"
    my_gui.pop_size = int(my_gui.pop_size_spinbox.get())


def draw_population_road(i):
    "called by generate_initial_list_of_roads function"
    if i >= 0:
        my_gui.canvas.delete("all")
        my_map.draw_cities(my_gui)
        my_gui.initial_list_of_roads[i].draw_road(my_gui)
        my_gui.canvas.after(1, draw_population_road, i-1)


def generate_initial_list_of_roads():
    "used to generate a list of objects Population"
    my_gui.initial_list_of_roads = []
    for i in range(my_gui.pop_size):
        my_gui.initial_list_of_roads.append(Population(my_map, my_gui))
    draw_population_road(len(my_gui.initial_list_of_roads)-1)
###############################################################################


# Class of list of generations ################################################
class list_of_generations(object):

    def __init__(self, my_gui, my_map):
        self.gen_ongoing = 0
        self.list_of_generations = []

    def go_from_gen_x_to_gen_y()

# Class to deal with generations ##############################################
class Generations(object):

    def __init__(self, population_of_roads):
        self.generation_number = 0
        self.population_sorted = None

    def sorting_of_population(self):
        self.population_sorted = sorted(population_of_roads,
                                        key=population_of_roads.road_lenght)
        print(self.population_sorted)

###############################################################################


# Class to create the map with cities in red squares ##########################
class Map(object):

    def __init__(self, gui):
        self.list_cities = []
        self.list_of_cities(gui)
        self.draw_cities(gui)

    def draw_cities(self, gui):
        "draw red squares for each cities"
        for i in range(len(self.list_cities)):
            gui.canvas.create_oval(
                    self.list_cities[i][0]-gui.size_cities,
                    self.list_cities[i][1]-gui.size_cities,
                    self.list_cities[i][0]+gui.size_cities,
                    self.list_cities[i][1]+gui.size_cities, fill="red")

    def list_of_cities(self, gui):
        "create a list containing all cities positions [x, y]"
        gui.canvas.delete("all")
        self.list_cities = []
        i = 0
        while i < gui.nb_cities:
            x = rdm.randrange(10, gui.canvas_size-10, 1)
            y = rdm.randrange(10, gui.canvas_size-10, 1)
            if [x, y] not in self.list_cities:
                self.list_cities.append([x, y])
                i += 1
###############################################################################


# Class for the roads, list of cities randomly selected from the list #########
# of cities in the map.
class Population(object):

    def __init__(self, the_map, gui):
        """Initialise the length of the road and randomly select the order
        of the road"""
        self.road_order = rdm.sample(the_map.list_cities,
                                     len(the_map.list_cities))
        self.road_lenght = self.lenght_of_road()

    def draw_road(self, gui):
        "Draw on the canvas the link between the cities"
        for i in range(len(self.road_order)-1):
            gui.canvas.create_line(self.road_order[i][0],
                                   self.road_order[i][1],
                                   self.road_order[i+1][0],
                                   self.road_order[i+1][1], fill="green")
            gui.canvas.create_line(self.road_order[-1][0],
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
###############################################################################


# Gui class ###################################################################
class MyGui(object):

    def __init__(self, root):
        "windows dimensions and others container widgets dimensions"
        self.initial_height = 624
        self.initial_width = 772
        self.canvas_size = 600
        root.geometry(f"{self.initial_width}x{self.initial_height}+1200+10")
        root.title("The SalesMan Problem solved with genetic")
        root.resizable(width=False, height=False)

        "variables related to cities"
        self.size_cities = 1
        self.nb_cities = 25

        "variables related to mutation rate and other reproductive stuff"
        self.pop_size = 12
        self.mutation_rate = 0.00

        """initialisation of initial list of roads to be transmitted to class"
        Generation"""
        self.initial_list_of_roads = []

        "functions to create widgets"
        self.getMainWidgets(root)
        self.getLabelsWidgets(root)
        self.getEntryWidgets(root)
        self.getButtonWidgets(root)
        self.getSpinboxWidgets(root)
        self.refresh_info()

    def refresh_info(self):
        "Refresh informations of labels every 100 ms"
        self.windows_geometry["text"] = root.winfo_geometry()
        self.windows_geometry.after(100, self.refresh_info)

    def getMainWidgets(self, root):
        "Initialisation of canvas"
        self.canvas = tk.Canvas(root, height=self.canvas_size,
                                width=self.canvas_size, bg="dark grey")
        self.canvas.grid(row=0, column=0, rowspan=2)

        "Initialisation of frames on the right position of canvas"
        self.frame = tk.Frame(root, bg="red")
        self.frame.grid(row=0, column=1, sticky=tk.NSEW)
        self.buttonframe = tk.Frame(root, bg="light blue")
        self.buttonframe.grid(row=1, column=1, sticky=tk.NSEW)

    def getLabelsWidgets(self, root):
        "Initialisation of labels widgets related to positionning of windows"
        self.windows_geometry = tk.Label(root, text="test")
        self.windows_geometry.grid(row=2, column=1)

        "initialisation of label widgets related to variables of the problem"
        self.FrameVariablesTitle = tk.Label(self.frame,
                                            text="Problem variables")
        self.FrameVariablesTitle.grid(row=0, column=0, columnspan=2,
                                      sticky=tk.EW)
        self.size_cities_label = tk.Label(self.frame, text="Size cities: ")
        self.size_cities_label.grid(row=1, column=0, sticky=tk.EW)
        self.number_of_cities_label = tk.Label(self.frame,
                                               text="Nb of Cities: ")
        self.number_of_cities_label.grid(row=2, column=0, sticky=tk.EW)
        self.mutation_rate_label = tk.Label(self.frame, text="Mutation rate: ")
        self.mutation_rate_label.grid(row=3, column=0, sticky=tk.EW)
        self.population_size_label = tk.Label(self.frame, text="Pop. Size: ")
        self.population_size_label.grid(row=4, column=0, sticky=tk.EW)
        "Empty labels to separate variables from buttons"

        "initialisation of label widgets related to launch of solving problem"
        self.FrameButtonsTitle = tk.Label(self.buttonframe, text="Buttons???")
        self.FrameButtonsTitle.grid(row=0, column=0, sticky=tk.NSEW)

    def getEntryWidgets(self, root):
        "Initialisation of all entry widgets"
        pass

    def getButtonWidgets(self, root):
        "Initialisation of all buttons widgets"
        self.generation_of_initial_population = tk.Button(
                self.buttonframe,
                text="Generate list of roads",
                width=20,
                command=generate_initial_list_of_roads)
        self.generation_of_initial_population.grid(row=1, column=0)

        self.sorting_of_population_test_button = tk.Button(
                self.buttonframe,
                text="test sorting of roads",
                width=20,
                command=start)
        self.sorting_of_population_test_button.grid(row=2, column=0)

    def getSpinboxWidgets(self, root):
        "initiation spinbox related to size of the square of the cities"
        self.spinbox1Val = tk.StringVar(self.frame, value=self.size_cities)
        self.cities_square_size_sb = ttk.Spinbox(self.frame,
                                                 from_=0, to=4,
                                                 increment=1,
                                                 width=5,
                                                 textvariable=self.spinbox1Val,
                                                 command=redraw_cities_squares)
        self.cities_square_size_sb.grid(row=1, column=1)

        "initialisation of spinbox related to the number of cities on the map"
        self.spinbox2Val = tk.StringVar(self.frame, value=self.nb_cities)
        self.nb_cities_spinbox = ttk.Spinbox(self.frame, from_=10, to=250,
                                             increment=1, width=5,
                                             textvariable=self.spinbox2Val,
                                             command=assign_nb_cities)
        self.nb_cities_spinbox.grid(row=2, column=1)

        "initialisation of spinbox related to the mutation rate"
        self.spinbox3Val = tk.StringVar(self.frame, value=self.mutation_rate)
        self.mutation_rate_sb = ttk.Spinbox(self.frame, from_=0, to=1,
                                            increment=0.01, width=5,
                                            textvariable=self.spinbox3Val,
                                            command=assign_mutation_rate)
        self.mutation_rate_sb.grid(row=3, column=1)

        "Initialisation of spinbox related to the population size"
        self.spinbox4Val = tk.StringVar(self.frame, value=self.pop_size)
        self.pop_size_spinbox = ttk.Spinbox(self.frame, from_=12, to=3000,
                                            increment=3, width=5,
                                            textvariable=self.spinbox4Val,
                                            command=assign_pop_size)
        self.pop_size_spinbox.grid(row=4, column=1)
###############################################################################


# Main Program (To clean)######################################################
if __name__ == "__main__":
    root = tk.Tk()
    my_gui = MyGui(root)
    my_map = Map(my_gui)
    root.mainloop()
###############################################################################

