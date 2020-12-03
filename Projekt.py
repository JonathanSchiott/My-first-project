"""Jonathan Schiött 2020-12-03
dropbox link with all pictures and files:
https://www.dropbox.com/sh/8k9e0ssc2c8b6fh/AAAcgUIFCH7kmTtRIXhWLkWWa?dl=0"""



# import of modules that will be used in the program:
import pygame as pg
import sys
# start pygame:
pg.init()
# variables for the text, in the TrollBox class:
FONT = pg.font.Font(None, 32)
box_font = pg.font.Font(None, 150)


class ShowASolution:
    def __init__(self, size):
        self.size = size
        self.troll = "T"
        self.start_pos = 0

    def create_matrix(self):
        matrix = []
        for y in range(self.size):
            row = []
            for x in range(self.size):
                row.append("_")
            matrix.append(row)
        return matrix

    def placement(self, matrix):
        y_pos = 0
        x_pos = 0
        while y_pos < self.size:
            while x_pos < self.size + 1:
                # try function to catch when the x_position is outside of the matrix
                try:
                    if self.placement_ok(y_pos, x_pos, matrix):
                        # if current position is placeable, place troll:
                        matrix[y_pos][x_pos] = self.troll
                        # test if the matrix is done:
                        if self.done(matrix):
                            return matrix
                        # if not done, move on to the next row
                        else:
                            y_pos += 1
                            x_pos = 0
                    # if it's not possible to place, test next position:
                    else:
                        x_pos += 1
                # if x_position is outside of matrix:
                except IndexError:
                    # go back to previous row
                    y_pos -= 1
                    # the new x_position will be the one after the placed
                    x_pos = 1 + matrix[y_pos].index(self.troll)
                    # find the placed troll on the previous row:
                    x_remove = matrix[y_pos].index(self.troll)
                    # replace the placed troll with empty
                    matrix[y_pos][x_remove] = "_"

    def placement_ok(self, y_pos, x_pos, matrix):
        for i in range(self.size):
            if i != 0:
                # check rows, columns and diagonals:
                if matrix[y_pos - i][x_pos] == self.troll or \
                        x_pos - i >= 0 and matrix[y_pos - i][x_pos - i] == self.troll or \
                        x_pos + i < len(matrix) and matrix[y_pos - i][x_pos + i] == self.troll or \
                        x_pos + i < len(matrix) and matrix[y_pos][x_pos + i] == self.troll or \
                        x_pos - i >= 0 and matrix[y_pos][x_pos - i] == self.troll:
                    return False
        return True

    # check if done by making a list and checking the length of the list:
    def done(self, matrix):
        control_list = []
        for y in range(self.size):
            for x in range(self.size):
                if matrix[y][x] == self.troll:
                    control_list.append(1)
        if len(control_list) == self.size:
            return True

    # the method that runs the solver:
    def solving_mechanism(self):
        matrix = self.create_matrix()
        done_matrix = self.placement(matrix)
        return done_matrix


"""
This class is largely influenced by the class in the link below:
    https://www.codegrepper.com/code-examples/delphi/how+to+make+a+text+input+box+python+pygame"""


# class that makes boxes that the user can click on to place trolls:
class TrollBox:
    def __init__(self, x, y, w, h, text=''):
        # create rectangle based on the coordinates, width and height:
        self.rect = pg.Rect(x, y, w, h)
        # variables taken from above:
        self.color = pg.Color(255, 255, 255, 255)
        self.txt_surface = box_font.render(text, True, self.color)
        # variable to verify if the troll is placed
        self.active = False
        self.troll_is_placed = False
        # text variable, using in the size input mode
        self.text = text
        # coordinates:
        self.x = x
        self.y = y

    # function that handles events in the box(influenced by the input box class):
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
                # toggle between troll is placed or not
                self.troll_is_placed = not self.troll_is_placed
            else:
                self.active = False

    # function to draw the box on the screen:
    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


# Class for the first screen:
class StartMenu:
    def __init__(self):
        # size:
        self.width = 800
        self.height = 800
        # make screen surface:
        self.screen = pg.display.set_mode((self.width, self.height))
        # font:
        self.myfont = pg.font.SysFont("Helvetica", 15)
        # frames per second variable:
        self.fps = 27
        # create clock to make the screen run:
        self.clock = pg.time.Clock()

    def create_boxes_and_labels(self):
        # creating clickable boxes with the different sized of the board that the user can choose:
        self.box_05 = TrollBox(200, 630, 100, 100, "5")
        self.box_06 = TrollBox(300, 630, 100, 100, "6")
        self.box_07 = TrollBox(400, 630, 100, 100, "7")
        self.box_08 = TrollBox(500, 630, 100, 100, "8")
        # put them in a list:
        self.input_boxes = [self.box_05, self.box_06, self.box_07, self.box_08]
        self.bg_start_screen = pg.transform.scale(pg.image.load("Start_screen.jpg"), (self.width, self.height))
        self.welcome_label = FONT.render("Welcome to angry trolls!", True, (255, 255, 255))
        self.label01 = FONT.render("The game where you are the troll keeper and place trolls in the forest", True,
                              (255, 255, 255))
        self.label02 = FONT.render("Trolls are simple creatures, and as the keeper it's your job to make sure", True,
                              (255, 255, 255))
        self.label03 = FONT.render("that the trolls don't see each other. Luckily for you trolls only see", True,
                              (255, 255, 255))
        self.label04 = FONT.render("straight to the sides, up, down and to the diagonals.", True,
                              (255, 255, 255))
        self.label05 = FONT.render("If a troll sees another troll, they instantly become so angry that", True,
                              (255, 255, 255))
        self.label06 = FONT.render("they all collapse. 'If its not measured it doesn't exist' a wise man once said", True,
                              (255, 255, 255))
        self.label07 = FONT.render("and therefore your performance will be measured.", True,
                              (255, 255, 255))
        self.label08 = FONT.render("Time and the amount of trolls you have placed will be taken into account.", True,
                              (255, 255, 255))
        self.label09 = FONT.render("If you beat the current high score you will earn a spot and eternal fame", True,
                              (255, 255, 255))

        self.start_label = FONT.render("Choice the size of your board to start:", True,
                                  (255, 255, 255))

        high_score01, high_score02, high_score03 = self.high_score.show_high_score()
        # create labels
        self.high_score_label = FONT.render("High score:", True, (255, 255, 255))
        self.high_score01_label = FONT.render(f"1:   {high_score01}", True, (255, 255, 255))
        self.high_score02_label = FONT.render(f"2:   {high_score02}", True, (255, 255, 255))
        self.high_score03_label = FONT.render(f"3:   {high_score03}", True, (255, 255, 255))

    def draw_boxes_and_labels(self):
        # draw text
        self.screen.blit(self.welcome_label, (270, 40))
        self.screen.blit(self.label01, (10, 120))
        self.screen.blit(self.label02, (10, 150))
        self.screen.blit(self.label03, (10, 180))
        self.screen.blit(self.label04, (10, 210))

        self.screen.blit(self.label05, (10, 250))
        self.screen.blit(self.label06, (10, 280))
        self.screen.blit(self.label07, (10, 310))
        self.screen.blit(self.label08, (10, 340))
        self.screen.blit(self.label09, (10, 370))
        self.screen.blit(self.start_label, (200, 600))

        # draw high score:
        self.screen.blit(self.high_score_label, (335, 430))
        self.screen.blit(self.high_score01_label, (335, 455))
        self.screen.blit(self.high_score02_label, (335, 480))
        self.screen.blit(self.high_score03_label, (335, 505))

        for box in self.input_boxes:
            box.draw(self.screen)

    # the start screen::
    def start_screen(self):
        # variable for the running of the window:
        self.run1 = True
        # import and rescale image:
        self.bg_start_screen = pg.transform.scale(pg.image.load("Start_screen.jpg"), (self.width, self.height))
        box = TrollBox(300, 600, 200, 40, "")
        self.high_score = HighScore()
        self.create_boxes_and_labels()
        while self.run1:
            self.screen.blit(self.bg_start_screen, (0, 0))
            # for loop that looks for events from the user:
            for event in pg.event.get():
                # if sats that will close the screen if you press x
                if event.type == pg.QUIT:
                    pg.quit()
                    # exit the program:
                    sys.exit()
                for box in self.input_boxes:
                    box.handle_event(event)
                    # if box is clicked (re-using the variable for troll-placement in the main class)
                    if box.troll_is_placed:
                        # return size
                        return int(box.text)
            self.draw_boxes_and_labels()

            # update and draw on the screen:
            pg.display.update()
            box.draw(self.screen)
            # tick the clock:
            self.clock.tick(self.fps)


# class to keep the high score, not used at the moment
class HighScore:
    def __init__(self):
        pass

    def show_high_score(self):
        # open the file if it exists, otherwise it will create a new one.
        try:
            with open("high_score_file.txt", "r") as file:
                high_score = file.read().splitlines()
                for number in range(len(high_score)):
                    # create a list with all of the high scores:
                    high_score[number] = str(high_score[number])
                # sort them after the biggest one:
                high_score.sort(reverse=True)
        except FileNotFoundError:
            with open("high_score_file.txt", "a+") as file:
                file.write("0\n0\n0")
            with open("high_score_file.txt", "r") as file:
                high_score = file.read().splitlines()
                for number in range(len(high_score)):
                    # create a list with all of the high scores:
                    high_score[number] = str(high_score[number])
        # return the number of high scores that exist:
        return high_score[0], high_score[1], high_score[2]


    def change_high_score(self, score):
        try:
            with open("high_score_file.txt", "r") as file:
                # open high score file and save each line:
                high_score = file.read().splitlines()
                for number in range(len(high_score)):
                    # create a list with all of the high scores:
                    high_score[number] = str(high_score[number])
                # sort them after the biggest one:
                high_score.sort(reverse=True)
                if score > float(high_score[2]):
                    # if the user score is higher than the last one:
                    high_score[2] = str(score)
                    # sort again to make sure that the highest is on top:
                    high_score.sort(reverse=True)
                    # write the new order in to the file:
                    with open("high_score_file.txt", "w") as new_file:
                        for number in high_score:
                            new_file.write(f"{str(number)}\n")
        except FileNotFoundError:
            # if file doesn't exist, create a new one:
            with open("high_score_file.txt", "a+") as file:
                file.write(f"{str(score)}\n0\n0")




# main class that controls the screen of the game:
class MainScreen(TrollBox):
    # super-initializer not here since i want to import everything
    def __init__(self, size):
        self.size = size
        # using the size input to size the screen:
        self.width = ((size * 90) + 225)
        self.height = ((size * 90) + 90)
        # creating a clock
        self.clock = pg.time.Clock()
        # variable for taking time:
        self.start_time = pg.time.get_ticks()
        self.passed_time = 0
        # variable to keep track of fail time:
        self.fail_variable = None
        # frames per second:
        self.fps = 40
        # create screen to run the program in:
        self.screen = pg.display.set_mode((self.width, self.height))
        # list for matrix for the boxes:
        self.troll_boxes_matrix = []
        # variable for the frames per second:
        self.frame = 0
        # font variable
        self.FONT = pg.font.Font(None, 32)
        # font variable
        self.score = 0
        # boolean to control status of game:
        self.win = False
        self.fail = False

    # function to create matrix for the boxes:
    def matrix_maker(self):
        for y in range(self.size):
            # list for rows in matrix:
            row = []
            for x in range(self.size):
                # create boxes with given coordinates for the screen and append to matrix:
                box = TrollBox((x * 90 + 45), (y * 90 + 45), 90, 90)
                row.append(box)
            self.troll_boxes_matrix.append(row)

    # method that controls the timer:
    def timer(self):
        # stop time if the user wins or fails:
        if self.win or self.fail:
            timer_running = False
        else:
            timer_running = True
        if timer_running:
            self.passed_time = pg.time.get_ticks() - self.start_time
        # draw the timer:
        time_label = FONT.render(f"Timer: {self.passed_time / 1000}", True, (255, 255, 255))
        self.screen.blit(time_label, (0, 0))

    # method to place the brown borders around the borders:
    def draw_background(self):
            # get pictures and scale up:
            bg_border = pg.transform.scale(pg.image.load("dirt_picture.png"), (45, 45))
            bg_surface = pg.transform.scale(pg.image.load("grass.jpg"), (self.width, self.height))
            # draw the background:
            self.screen.blit(bg_surface, (0, 0))
            # draw the borders:
            self.screen.blit(bg_border, (0, 0))
            for a in range(self.size * 2 + 1):
                # upper border
                self.screen.blit(bg_border, ((a + 1) * 45, 0))
                # right part of upper border:
                self.screen.blit(bg_border, (self.size * 90 + 45 * a, 0))
                # left border:
                self.screen.blit(bg_border, (0, a * 45))
                # low border:
                self.screen.blit(bg_border, ((a * 45), self.size * 90 + 45))
                # right borders:
                self.screen.blit(bg_border, ((self.size * 90 + 45), (a + 1) * 45))
                self.screen.blit(bg_border, ((self.size * 90 + 90), (a + 1) * 45))
                self.screen.blit(bg_border, ((self.size * 90 + 135), (a + 1) * 45))
                self.screen.blit(bg_border, ((self.size * 90 + 180), (a + 1) * 45))

    def draw_labels_and_buttons(self):
            fail_label = FONT.render(f"You lost, remove trolls until they cant see each other to continue", True,
                                     (255, 255, 255))
            solution_label = FONT.render(f"Show solution", True, (255, 255, 255))

            # draw solver button:
            self.solver_button.draw(self.screen)
            self.screen.blit(solution_label, (60 + 90 * self.size, 56, 180, 45))
            # if button is pressed:
            if self.solver_button.troll_is_placed:
                # show solution:
                self.complete_matrix()
            if self.fail:
                self.screen.blit(fail_label, (0, 20))

    def draw_high_score(self):
        # high score:
        high_score01, high_score02, high_score03 = self.high_score.show_high_score()
        # create labels
        high_score_label = FONT.render("High score:", True, (255, 255, 255))
        high_score01_label = FONT.render(f"1:   {high_score01}", True, (255, 255, 255))
        high_score02_label = FONT.render(f"2:   {high_score02}", True, (255, 255, 255))
        high_score03_label = FONT.render(f"3:   {high_score03}", True, (255, 255, 255))
        # draw high score:
        self.screen.blit(high_score_label, (60 + 90 * self.size, 120))
        self.screen.blit(high_score01_label, (60 + 90 * self.size, 150))
        self.screen.blit(high_score02_label, (60 + 90 * self.size, 180))
        self.screen.blit(high_score03_label, (60 + 90 * self.size, 210))

    # method that controls whats being shown in the window:
    def change_window(self):
        # restart the frame per second counter:
        if self.frame + 1 >= 40:
            self.frame = 0
        # draw background:
        self.draw_background()
        self.draw_labels_and_buttons()
        # place the clickable boxes:
        for rad in range(len(self.troll_boxes_matrix)):
            for box in self.troll_boxes_matrix[rad]:
                box.draw(self.screen)
                if box.troll_is_placed:
                    # if the troll is placed and the user fails, show dying trolls:
                    if self.fail:
                        # toggling through the images using the fps and tick:
                        self.screen.blit(self.troll.troll_01[1][self.frame // 4],
                                         ((box.x - 32), box.y))
                    else:
                        # if the troll is placed:
                        self.screen.blit(self.troll.troll_idle[self.frame // 4],
                                         ((box.x - 32), box.y))
        if self.win:
            command = self.win_menu()
            # return to main_window
            if command == "restart":
                return "restart"
        # check for win, fail and keep score:
        self.fail = self.fail_control()
        self.win = self.win_control()
        self.score = self.score_keeper()
        # run and draw the timer:
        self.timer()

        self.draw_high_score()
        # update the screen each round:
        pg.display.update()
        self.frame += 1
        self.clock.tick(self.fps)

    # method that runs the window:
    def main_window(self):
        self.start_time = pg.time.get_ticks()
        # create the matrix
        self.matrix_maker()
        # create troll:
        self.troll = Troll(0)
        # high score:
        self.high_score = HighScore()
        # create algorithmic solver button:
        self.solver_button = TrollBox(45 + 90 * self.size, 45, 180, 45, "")
        run = True
        # while loop that keeps the window running:
        while run:
            # for loop that detects events by the user:
            for event in pg.event.get():
                # close the screen if you press the x
                if event.type == pg.QUIT:
                    pg.quit()
                    # exit the code:
                    sys.exit()
                # control events in every box in the matrix:
                for rad in range(len(self.troll_boxes_matrix)):
                    for box in self.troll_boxes_matrix[rad]:
                        box.handle_event(event)
                self.solver_button.handle_event(event)
            # draw the current status:
            command = self.change_window()
            # return to the main function
            if command == "restart":
                return "restart"

    # method that will show the best way to solve the game, currently not used
    def complete_matrix(self):
            blackbox = pg.transform.scale(pg.image.load("blackbox.jpeg"), (45, 45))
            self.cant_place_label = FONT.render("Cant show matrix, remove trolls", True, (255, 255, 255))
            algorithm = ShowASolution(self.size)
            matrix = algorithm.solving_mechanism()
            for y_pos in range(self.size):
                for x_pos in range(self.size):
                    if matrix[y_pos][x_pos] == "T":
                        self.screen.blit(blackbox, (((x_pos * 90) + 68), ((y_pos * 90) + 78)))

    # function that controls if the placement is allowed
    # toggles between False and True depending on if the user lost or not:
    def fail_control(self):
            for a in range(self.size):
                for y in range(self.size):
                    for x in range(self.size):
                        # controlling first the column, then the row, then diagonals returns fail if placement is not valid given the parameters bellow:
                        if a != 0 and y + a < self.size and y + a != y and self.troll_boxes_matrix[y][
                            x].troll_is_placed and self.troll_boxes_matrix[y + a][x].troll_is_placed or \
                                x + a < self.size and x + a != x and self.troll_boxes_matrix[y][x].troll_is_placed and \
                                self.troll_boxes_matrix[y][x + a].troll_is_placed or \
                                a != 0 and x + a < self.size and y + a < self.size and self.troll_boxes_matrix[y][
                            x].troll_is_placed and self.troll_boxes_matrix[y + a][x + a].troll_is_placed or \
                                a != 0 and self.size > x - a >= 0 and 0 <= y + a < self.size and \
                                self.troll_boxes_matrix[y][x].troll_is_placed and self.troll_boxes_matrix[y + a][
                            x - a].troll_is_placed:
                            fail = True
                            return fail
            # if all current placements are valid:
            fail = False
            return fail

    # method that controls if the user has won the game
    def win_control(self):
            win_control_list = []
            for y in range(self.size):
                for x in range(self.size):
                    # control each box of the matrix and append the win_control list
                    if self.troll_boxes_matrix[y][x].troll_is_placed:
                        win_control_list.append("1")
            # if the number of trolls placed == the height/width of the board, the user has won:
            if len(win_control_list) == self.size and not self.fail:
                win = True
            else:
                win = False
            return win

    # method to track the score:
    def score_keeper(self):
            score_list = []
            for y in range(self.size):
                for x in range(self.size):
                    # append "1" to the list for each troll that is placed
                    # Since the fail_control regulates the placement
                    if self.troll_boxes_matrix[y][x].troll_is_placed:
                        score_list.append("1")
            fail_list = []
            if self.fail:
                fail_list.append(0)
                self.fail_variable = len(fail_list) * 0.1
            # solves fail due to division by zero when the time is 0:
            if self.passed_time == 0:
                self.score = 0
            # score calculation, needs to be improved:
            else:
                if self.fail_variable is None:
                    self.score = round(((len(score_list) * 10) ** 4 / self.passed_time), 2)
                else:
                    self.score = round(((len(score_list) * 10) ** 4 / self.passed_time) - self.fail_variable, 2)
            return self.score

    # method to change window if the user wins:
    def win_menu(self):
        bg_border = pg.transform.scale(pg.image.load("dirt_picture.png"), (45, 45))
        restart_label = FONT.render("Press here to restart", True, (255, 255, 255))
        restart_box = TrollBox(135, 215, 270, 45)
        for a in range(1, 7):
            self.screen.blit(bg_border, (90 + a * 45, 135))
            self.screen.blit(bg_border, (90 + a * 45, 180))
            self.screen.blit(bg_border, (90 + a * 45, 225))
            self.screen.blit(bg_border, (90 + a * 45, 270))
        win_label01 = FONT.render(f"You won, your score was:", True, (255, 255, 255))
        win_label02 = FONT.render(f"{round(self.score, 1)} points", True, (255, 255, 255))
        self.screen.blit(win_label01, (135, 135))
        self.screen.blit(win_label02, (135, 175))
        restart_box.draw(self.screen)
        self.screen.blit(restart_label, (162, 227))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                # exit the code:
                sys.exit()
            restart_box.handle_event(event)
        # if restart is pressed, return to change_window
        if restart_box.troll_is_placed:
            self.high_score.change_high_score(self.score)
            return "restart"

# class for the different trolls:
# super initializer not here since i want to import everything
class Troll(MainScreen):
    # super-initializer not here since i want to import everything
    def __init__(self, number):
        # number will be used to show different trolls:
        self.number = number
        # size of the troll:
        troll_width = 144
        troll_height = 90
        # pictures for the first troll:
        troll_idle_01 = [(pg.transform.scale(pg.image.load("Troll_01_1_IDLE_000.png"),
                                                  (troll_width, troll_height))),
                              (pg.transform.scale(pg.image.load("Troll_01_1_IDLE_001.png"),
                                                  (troll_width, troll_height))),
                              (pg.transform.scale(pg.image.load("Troll_01_1_IDLE_002.png"),
                                                  (troll_width, troll_height))),
                              (pg.transform.scale(pg.image.load("Troll_01_1_IDLE_003.png"),
                                                  (troll_width, troll_height))),
                              (pg.transform.scale(pg.image.load("Troll_01_1_IDLE_004.png"),
                                                  (troll_width, troll_height))),
                              (pg.transform.scale(pg.image.load("Troll_01_1_IDLE_005.png"),
                                                  (troll_width, troll_height))),
                              (pg.transform.scale(pg.image.load("Troll_01_1_IDLE_006.png"),
                                                  (troll_width, troll_height))),
                              (pg.transform.scale(pg.image.load("Troll_01_1_IDLE_007.png"),
                                                  (troll_width, troll_height))),
                              (pg.transform.scale(pg.image.load("Troll_01_1_IDLE_008.png"),
                                                  (troll_width, troll_height))),
                              (pg.transform.scale(pg.image.load("Troll_01_1_IDLE_009.png"),
                                                  (troll_width, troll_height))), ]
        troll_die_01 = [
            (pg.transform.scale(pg.image.load("Troll_01_1_DIE_000.png"),
                                (troll_width, troll_height))),
            (pg.transform.scale(pg.image.load("Troll_01_1_DIE_001.png"),
                                (troll_width, troll_height))),
            (pg.transform.scale(pg.image.load("Troll_01_1_DIE_002.png"),
                                (troll_width, troll_height))),
            (pg.transform.scale(pg.image.load("Troll_01_1_DIE_003.png"),
                                (troll_width, troll_height))),
            (pg.transform.scale(pg.image.load("Troll_01_1_DIE_004.png"),
                                (troll_width, troll_height))),
            (pg.transform.scale(pg.image.load("Troll_01_1_DIE_005.png"),
                                (troll_width, troll_height))),
            (pg.transform.scale(pg.image.load("Troll_01_1_DIE_006.png"),
                                (troll_width, troll_height))),
            (pg.transform.scale(pg.image.load("Troll_01_1_DIE_007.png"),
                                (troll_width, troll_height))),
            (pg.transform.scale(pg.image.load("Troll_01_1_DIE_008.png"),
                                (troll_width, troll_height))),
            (pg.transform.scale(pg.image.load("Troll_01_1_DIE_009.png"),
                                (troll_width, troll_height))), ]
        # lists of the trolls and their different modes(currently only 1):
        self.troll_01 = [troll_idle_01, troll_die_01]
        # list of trolls(currently only 1):
        troll_list = [self.troll_01]
        # currently used list for showing troll_01:
        self.troll_idle = troll_list[number][0]


def run_game():
    # initialise pygame
    pg.init()
    # start the start menu and return the size when the user clicks on it:
    start = StartMenu()
    size = start.start_screen()
    # start the main screen with the size included from the previous screen
    game = MainScreen(size)
    command = game.main_window()
    # if the restart-button is pressed after winning, restart:
    if command == "restart":
        run_game()


# main code:
if __name__ == "__main__":
    run_game()
