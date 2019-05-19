import tkinter as tk
import random as rdm
from math import sqrt
import tkinter.ttk as ttk
import time as time


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
    my_gui.generation_of_initial_population["state"] = "active"


def assign_mutation_rate():
    "called if spinbox for mutation rate is changed"
    my_gui.mutation_rate = float(my_gui.mutation_rate_sb.get())


def assign_pop_size():
    "called if spinbox of size of the population is changed"
    my_gui.pop_size = int(my_gui.pop_size_spinbox.get())


def assign_bn_generations():
    "called if spinbox for number of generations to run is changed"
    my_gui.nb_generations_to_run = int(my_gui.nb_generations_sb.get())


def assign_time_between_gen():
    my_gui.time_between_gen = int(my_gui.time_between_gen_sb.get())


def draw_population_road(i):
    "called by generate_initial_list_of_roads function"
    if i >= 0:
        my_gui.canvas.delete("all")
        my_map.draw_cities(my_gui)
        my_gui.list_of_roads[i].draw_road(my_gui)
        my_gui.canvas.after(1, draw_population_road, i-1)


def generate_initial_list_of_roads():
    "used to generate a list of objects Population"
    my_generations.list_of_roads = []
    for i in range(my_gui.pop_size):
        my_generations.list_of_roads.append(Population(my_map, my_gui))
    my_gui.information_label["text"] = f"Generation of initial population done\
, {len(my_generations.list_of_roads)} roads generated"
    my_gui.generation_of_initial_population["state"] = "disabled"
    my_gui.nb_cities_spinbox["state"] = "disabled"
    my_gui.pop_size_spinbox["state"] = "disabled"
    my_gui.nb_generations_sb["state"] = "active"
    my_gui.sorting_of_population_test_button["state"] = "active"
    if my_generations.list_of_roads_sort is None:
        my_generations.sorting_of_population()


def start():
    my_gui.sorting_of_population_test_button["state"] = "disabled"
    my_generations.drawing_graph = 1
    try:
        a.draw_graph()
    except:
        pass
    my_generations.go_from_gen_x_to_gen_y(my_gui.nb_generations_to_run)
    my_gui.information_label["text"] = f"                                \
                                                    "


def start_stop_graphs():
    global a
    try:
        if a.toplevel.winfo_exists():
            a.toplevel.destroy()
        else:
            a = Extend(root, my_gui)
    except:
        a = Extend(root, my_gui)
###############################################################################


# Class to deal with generations ##############################################
class Generations(object):

    def __init__(self, my_generations, my_gui, my_map):
        "initialisation of all variables"
        self.generation_number = my_generations.gen_ongoing
        self.population = my_generations.list_of_roads
        self.population_sorted = my_generations.list_of_roads_sort
        "let's go with the functions"
        self.main(my_generations, my_gui)

    def selection_of_fittest_parents_in_trio(self, a, b, c):
        "create a list with the 3 potential parents"
        trio_of_parents = [a, b, c]
        "list used to sort them by length"
        trio_of_parents_length = []
        for i in trio_of_parents:
            trio_of_parents_length.append(i.lenght_of_road())
        y = sorted(trio_of_parents, key=lambda parent: parent.lenght_of_road())
        return [y[0], y[1]]

    def reproduction(self, parent_a, parent_b):
        "select half of the parent_a, starting random, and fill with parent_b"
        new_kid = Population(my_map, my_gui)
        beg = rdm.randrange(len(parent_a.road_order))
        new_kid.road_order = []
        for i in range(beg, beg + len(parent_a.road_order)//2):
            if i >= len(parent_a.road_order):
                i -= len(parent_a.road_order)
            new_kid.road_order.append(parent_a.road_order[i])
        for i in parent_b.road_order:
            if i not in new_kid.road_order:
                new_kid.road_order.append(i)
        return new_kid

    def mutation(self, kid):
        "inverse two consecutive cities in the road"
        iterator = 0
        m_kid = kid
        for changed in range(len(m_kid.road_order)):
            if rdm.random() < my_gui.mutation_rate:
                iterator += 1
                changed_with = int(rdm.random() * len(m_kid.road_order))

                city_1 = m_kid.road_order[changed]
                city_2 = m_kid.road_order[changed_with]
                m_kid.road_order[changed] = city_2
                m_kid.road_order[changed_with] = city_1
        return m_kid

    def main(self, my_generations, my_gui):
        """start by creating a list of roads that will be destroyed
        not to touch the self.population list that might be usefull in the
        futur"""
        temp_list_of_roads = self.population[:]
        rdm.shuffle(temp_list_of_roads)
        new_list_of_roads = []
        while temp_list_of_roads:
            two_winners = self.selection_of_fittest_parents_in_trio(
                     temp_list_of_roads.pop(),
                     temp_list_of_roads.pop(),
                     temp_list_of_roads.pop())
            new_list_of_roads.append(two_winners[0])
            new_list_of_roads.append(two_winners[1])
            kid_of_winners = self.reproduction(two_winners[0], two_winners[1])
            kid_mutated = self.mutation(kid_of_winners)
            new_list_of_roads.append(kid_mutated)
        my_generations.list_of_roads = new_list_of_roads
###############################################################################


# Class of list of generations ################################################
class List_of_generations(object):

    def __init__(self, my_gui, my_map):
        "number of the previous generation before creating the new one"
        self.gen_ongoing = 0
        self.list_of_generations = []
        "this is the list of the road for each generations"
        self.list_of_roads = []
        self.list_of_roads_sort = None
        self.gen_of_min_road = None
        self.shortest_road = 1000000000000000000
        "Used to draw_graph or not"
        self.drawing_graph = 0

    def sorting_of_population(self):
        "used to sort a complete population depending of the road length"
        road_length = []
        for i in self.list_of_roads:
            road_length.append(i.lenght_of_road())
        self.list_of_roads_sort = sorted(self.list_of_roads,
                                         key=lambda pop: pop.lenght_of_road())
        if self.shortest_road > self.list_of_roads_sort[0].road_lenght:
            self.shortest_road = self.list_of_roads_sort[0].road_lenght
            self.gen_of_min_road = self.gen_ongoing

    def go_from_gen_x_to_gen_y(self, x):
        if x > 0:
            self.gen_ongoing += 1
            time.sleep(my_gui.time_between_gen/1000)
            self.sorting_of_population()
            self.list_of_generations.append(Generations(self, my_gui, my_map))
            my_gui.canvas.delete("all")
            redraw_cities_squares()
            self.list_of_roads_sort[0].draw_road(my_gui)
            if x == 1:
                my_gui.sorting_of_population_test_button["state"] = "active"
                self.drawing_graph = 0
            my_gui.information_label["text"] = f"Generation nb: \
{self.gen_ongoing}, shortest\
 road : {round(self.list_of_roads_sort[0].lenght_of_road())}.\
 Shortest road found at gen : {self.gen_of_min_road}"
            my_gui.canvas.after(1, self.go_from_gen_x_to_gen_y, x-1)
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
        return self.road_lenght
###############################################################################


# test for other gui class to extend the first one#############################
class Extend(object):

    def __init__(self, root, my_gui):
        "initialisation of size variables for the windows"
        self.h = my_gui.initial_height*2//3
        self.w = my_gui.initial_width
        self.dw = my_gui.initial_width+10
        "creation of the new windows"
        self.toplevel = tk.Toplevel()
        self.toplevel.title("Graph test")
        self.toplevel.geometry(f"{self.w}x{self.h}+{self.dw}+0")
        self.toplevel.resizable(width=False, height=False)
        "functions to create the differents widgets"
        self.getMainWidgets()
        "start drawing immediatly"
        self.draw_graph()

    def getMainWidgets(self):
        self.canvas = tk.Canvas(self.toplevel, width=self.w, height=self.h,
                                bg="black")
        self.canvas.grid(row=0, column=0, columnspan=4)

    def draw_graph(self):
        tempo = my_generations.list_of_generations
        self.canvas.create_line(10, 378, 10, 20, arrow=tk.LAST, fill="white")
        self.canvas.create_line(10, 378, 764, 378, arrow=tk.LAST, fill="white")
        if my_generations.drawing_graph == 1:
            self.canvas.delete("all")
            self.canvas.create_line(10, 378, 10, 20,
                                    fill="white", arrow=tk.LAST)
            self.canvas.create_line(10, 378, 764, 378,
                                    fill="white", arrow=tk.LAST)
            point_every_x_gens = len(tempo) // 754 + 1
            for i in range(0, len(tempo), point_every_x_gens):
                j = point_every_x_gens
                hauteur = tempo[i].population_sorted[0].lenght_of_road()
                hauteur_maxi = tempo[0].population_sorted[0].lenght_of_road()
                hauteur = (hauteur/hauteur_maxi)
                hauteur = (1-hauteur)*368 + 20
                self.canvas.create_line(i//j+20, hauteur, i//j + 21, hauteur,
                                        fill="white")
            self.canvas.after(250, self.draw_graph)
###############################################################################


# Gui class ###################################################################
class MyGui(object):

    def __init__(self, root):
        "windows dimensions and others container widgets dimensions"
        self.initial_height = 624
        self.initial_width = 772
        self.canvas_size = 600
        root.geometry(f"{self.initial_width}x{self.initial_height}+10+10")
        root.title("The SalesMan Problem solved with genetic")
        root.resizable(width=False, height=False)

        "variables related to cities"
        self.size_cities = 1
        self.nb_cities = 25

        "variables related to mutation rate and other reproductive stuff"
        self.pop_size = 1200
        self.mutation_rate = 0.01

        """initialisation of initial list of roads to be transmitted to class"
        Generation"""
        self.initial_list_of_roads = []

        "variables related to passing of generations"
        self.time_between_gen = 0
        self.nb_generations_to_run = 100

        "functions to create widgets"
        self.getMainWidgets(root)
        self.getLabelsWidgets(root)
        self.getEntryWidgets(root)
        self.getButtonWidgets(root)
        self.getSpinboxWidgets(root)
        """self.refresh_info()"""

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
        self.FrameButtonsTitle.grid(row=0, column=0, sticky=tk.NSEW,
                                    columnspan=2)
        self.nb_of_generations_to_do_label = tk.Label(self.buttonframe,
                                                      text="Nb Gen to go: ")
        self.nb_of_generations_to_do_label.grid(row=2, column=0, sticky=tk.EW)
        self.time_between_gen_label = tk.Label(self.buttonframe,
                                               text="Time btwn gen: ")
        self.time_between_gen_label.grid(row=3, column=0, sticky=tk.EW)

        "initialisation of labels related to progress of solution"
        self.information_label = tk.Label(root, text="Waiting, \
please select Problem variables paremeters then generate list of roads")
        self.information_label.grid(row=2, column=0, sticky=tk.W)

    def getEntryWidgets(self, root):
        "Initialisation of all entry widgets"
        pass

    def getButtonWidgets(self, root):
        "Initialisation of quit button"
        self.quit_button = tk.Button(root, text="Quit", command=root.quit)
        self.quit_button.grid(row=2, column=1, sticky=tk.EW)
        "Initialisation of all buttons widgets"
        self.generation_of_initial_population = tk.Button(
                self.buttonframe,
                text="Generate list of roads",
                width=20,
                command=generate_initial_list_of_roads)
        self.generation_of_initial_population.grid(row=1, column=0,
                                                   columnspan=2)

        self.sorting_of_population_test_button = tk.Button(
                self.buttonframe,
                text="go for n generations",
                width=20, state="disabled",
                command=start)
        self.sorting_of_population_test_button.grid(row=4, column=0,
                                                    columnspan=2)
        self.graph_button = tk.Button(self.buttonframe, text="Graph",
                                      width=20, command=start_stop_graphs)
        self.graph_button.grid(row=5, column=0, columnspan=2)

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
        self.mutation_rate_sb = ttk.Spinbox(self.frame, from_=0.001, to=0.03,
                                            increment=0.002, width=5,
                                            textvariable=self.spinbox3Val,
                                            command=assign_mutation_rate)
        self.mutation_rate_sb.grid(row=3, column=1)

        "Initialisation of spinbox related to the population size"
        self.spinbox4Val = tk.StringVar(self.frame, value=self.pop_size)
        self.pop_size_spinbox = ttk.Spinbox(self.frame, from_=12, to=30000,
                                            increment=3, width=5,
                                            textvariable=self.spinbox4Val,
                                            command=assign_pop_size)
        self.pop_size_spinbox.grid(row=4, column=1)
        "initialisation of spinbox for the number of generations to run"
        self.spinbox5Val = tk.StringVar(self.buttonframe,
                                        value=self.nb_generations_to_run)
        self.nb_generations_sb = ttk.Spinbox(self.buttonframe, from_=100,
                                             to=20000,
                                             increment=100, width=5,
                                             state="disabled",
                                             textvariable=self.spinbox5Val,
                                             command=assign_bn_generations)
        self.nb_generations_sb.grid(row=2, column=1)
        "initialisation of spinbox for time in ms between generations"
        self.spinbox6Val = tk.StringVar(self.buttonframe, value=0)
        self.time_between_gen_sb = ttk.Spinbox(self.buttonframe, from_=0,
                                               to=1000, increment=50, width=5,
                                               textvariable=self.spinbox6Val,
                                               command=assign_time_between_gen)
        self.time_between_gen_sb.grid(row=3, column=1)
###############################################################################


# Main Program (To clean)######################################################
if __name__ == "__main__":
    root = tk.Tk()
    my_gui = MyGui(root)
    a = Extend(root, my_gui)
    a.toplevel.destroy()
    my_map = Map(my_gui)
    my_generations = List_of_generations(my_gui, my_map)
    root.mainloop()
    root.destroy()
###############################################################################
