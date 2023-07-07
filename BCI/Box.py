import pygame

from config import *


class Box:
    def __init__(self, position, frequency, screen_width, screen_height):
        self._frequency = frequency
        self._position = position
        self._color = BLUE
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._left = 0
        self._top = 0
        self._rect = self.rect()
        self._box_width = int(BOX_RATIO*screen_width)
        if self._box_width % 2 != 0:
            self._box_width += 1
        print(self._box_width)

    def get_position(self, position):
        """
        get the left and top positions for a rectangle based on the desired position on the screen.

        :param position: The desired position of the rectangle, which can be one of the following constants: LEFT, RIGHT, TOP, DOWN, or CENTER.

        :return: A tuple containing the left and top positions of the rectangle
        """
        box_width, box_height = self.get_box_dimensions()
        if position == LEFT_POSITION:
            left = (self._screen_width / 2 - 2.5 * box_width)
            top = (self._screen_height / 2 - box_height / 2)
        elif position == RIGHT_POSITION:
            left = (self._screen_width / 2 + 1.5 * box_width)
            top = (self._screen_height / 2 - box_height / 2)
        elif position == TOP_POSITION:
            top = self._screen_height / 2 - 2.5 * box_height
            left = self._screen_width / 2 - box_width / 2
        elif position == DOWN_POSITION:
            top = self._screen_height / 2 + 1.5 * box_height
            left = self._screen_width / 2 - box_width / 2
        elif position == CENTER_POSITION:
            left = self._screen_width / 2 - box_width / 2
            top = self._screen_height / 2 - box_height / 2
        else:
            raise ValueError("location %s unknown" % position)

        return left, top

    def get_frequency(self):
        return self._frequency

    def get_color(self):
        return self._color

    def rect(self):
        box_width, box_height = self.get_box_dimensions()

        self._left, self._top = self.get_position(self._position)
        rect = pygame.Rect(self._left, self._top, box_width, box_height)
        return rect

    def get_left(self):
        return self._left

    def get_top(self):
        return self._top

    def get_direction(self):
        return self._position

    def reset_color(self):
        self._color = BLUE

    def hide_box(self):
        self._color = BLACK

    def toggle_color(self):
        """
        Toggle the color of the box between blue and purple.
        """
        self._color = BLUE if self._color == PURPLE else PURPLE

    # def is_inside(self, x, y):
    #     """
    #     Check if a point is inside the box.

    #     :param x: The x coordinate of the point.
    #     :param y: The y coordinate of the point.

    #     :return: True if the point is inside the box, False otherwise.
    #     """
    #     return self._rect.collidepoint(x, y)
    
    
    def is_inside(self, x, y):
        """
        Check if a point is inside the box.

        :param x: The x coordinate of the point.
        :param y: The y coordinate of the point.

        :return: True if the point is inside the box, False otherwise.
        """
        box_width, box_height = self.get_real_box_dimensions()
        left, top = self.get_real_position(self._position)
        return left <= x <= left + box_width and top <= y <= top + box_height
    
    def get_pointed_direction(self, x, y):
        """
        Get the direction of the box that the point is inside of.

        :param x: The x coordinate of the point.
        :param y: The y coordinate of the point.

        :return: The direction of the box that the point is inside of, or None if the point is not inside any box.
        """
        box_width, box_height = self.get_real_box_dimensions()

        if self.get_real_position(LEFT_POSITION)[0] <= x <= self.get_real_position(LEFT_POSITION)[0] + box_width and self.get_real_position(LEFT_POSITION)[1] <= y <= self.get_real_position(LEFT_POSITION)[1] + box_height:
            return 'left'
        elif self.get_real_position(RIGHT_POSITION)[0] <= x <= self.get_real_position(RIGHT_POSITION)[0] + box_width and self.get_real_position(RIGHT_POSITION)[1] <= y <= self.get_real_position(RIGHT_POSITION)[1] + box_height:
            return 'right'
        elif self.get_real_position(TOP_POSITION)[0] <= x <= self.get_real_position(TOP_POSITION)[0] + box_width and self.get_real_position(TOP_POSITION)[1] <= y <= self.get_real_position(TOP_POSITION)[1] + box_height:
            return 'top'
        elif self.get_real_position(DOWN_POSITION)[0] <= x <= self.get_real_position(DOWN_POSITION)[0] + box_width and self.get_real_position(DOWN_POSITION)[1] <= y <= self.get_real_position(DOWN_POSITION)[1] + box_height:
            return 'down' 
        else:
            return 'stop'

    def get_box_dimensions(self):
        """
        Get the dimension of the box.

        :return: The dimension of the box.
        """
        box_width = pygame.display.Info().current_w * BOX_RATIO
        box_height = pygame.display.Info().current_w * BOX_RATIO 
        return box_width, box_height
    
    def get_real_position(self, position):
        """
        get the left and top positions for a rectangle based on the desired position on the screen.

        :param position: The desired position of the rectangle, which can be one of the following constants: LEFT, RIGHT, TOP, DOWN, or CENTER.

        :return: A tuple containing the left and top positions of the rectangle
        """
        box_width, box_height = self.get_real_box_dimensions()
        if position == LEFT_POSITION:
            left = (self._screen_width / 2 - 1.5 * box_width)
            top = (self._screen_height / 2 - box_height / 2)
        elif position == RIGHT_POSITION:
            left = (self._screen_width / 2 + 0.5 * box_width)
            top = (self._screen_height / 2 - box_height / 2)
        elif position == TOP_POSITION:
            top = self._screen_height / 2 - 1.5 * box_height
            left = self._screen_width / 2 - box_width / 2
        elif position == DOWN_POSITION:
            top = self._screen_height / 2 + 0.5 * box_height
            left = self._screen_width / 2 - box_width / 2
        elif position == CENTER_POSITION:
            left = self._screen_width / 2 - box_width / 2
            top = self._screen_height / 2 - box_height / 2
        else:
            raise ValueError("location %s unknown" % position)

        return left, top
    
    def get_real_box_dimensions(self):
        """
        Get the dimension of the box.

        :return: The dimension of the box.
        """
        box_width = pygame.display.Info().current_w * REAL_BOX_RATIO
        box_height = pygame.display.Info().current_h * REAL_BOX_RATIO + ((pygame.display.Info().current_w/pygame.display.Info().current_h) * REAL_BOX_RATIO)
        return box_width, box_height


if __name__ == '__main__':
    pygame.init()
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    box = Box(TOP_POSITION, 10, SCREEN_WIDTH, SCREEN_HEIGHT)
    print(box.get_position(TOP_POSITION))
    print(box.get_position(RIGHT_POSITION))
    print(box.get_position(DOWN_POSITION))
    print(box.get_position(LEFT_POSITION))
    print(box.get_position(CENTER_POSITION))
    print(box.rect())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill(WHITE)
        # pygame.draw.rect(screen, box.get_color(), box.rect())
        rec = pygame.Rect(SCREEN_WIDTH//2 -25, SCREEN_HEIGHT//2 -25, 50, 50)
        # center the rectangle on the screen
        # rec = pygame.Rect(0, 0, 50, 50)
        # rec.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        # line in the middle of the screen to help center the rectangle
        pygame.draw.line(screen, BLACK, (SCREEN_WIDTH//2, 0), (SCREEN_WIDTH//2, SCREEN_HEIGHT))
        pygame.draw.line(screen, BLACK, (0, SCREEN_HEIGHT//2), (SCREEN_WIDTH, SCREEN_HEIGHT//2))


        pygame.draw.rect(screen, box.get_color(), rec)
        pygame.display.update()