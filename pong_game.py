import pygame
pygame.init() # always initialize pygame

WIDTH, HEIGHT = 700, 500 # Variables in all capitals indicate cosntants
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # playing window
pygame.display.set_caption('Pong') # window caption

FPS = 60 # frames per second

# COLOURS
WHITE = (255,255,255)
BLACK = (0,0,0)

# PADDLE
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100

# BALL
BALL_RADIUS = 7

# SCORING
SCORE_FONT = pygame.font.SysFont('comicsans', size=50)
WINNING_SCORE = 1

class Paddle:
    COLOR = WHITE # class constantS/ATTRIBUTES
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(surface = win, color = self.COLOR, 
                              rect = (self.x, self.y, self.width, self.height))
        
    def move(self, up=True):
        if up:
            self.y -= self.VEL # move paddle up by VEL amount
        else:
            self.y += self.VEL # move paddle down by VEL amount
    
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    MAX_VEL = 5
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.vel_x = self.MAX_VEL
        self.vel_y = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y 

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.vel_x *= -1 # reset x component towards opponent
        self.vel_y = 0


def draw(win, paddles, ball, left_score, right_score): # draws stuff on display
    win.fill(BLACK) # fill window with a colour RGB

    # Scoring
    left_score_text = SCORE_FONT.render(f'{left_score}', 1,  WHITE)
    right_score_text = SCORE_FONT.render(f'{right_score}',  1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (3*WIDTH//4 - right_score_text.get_width()//2, 20))

    # draw paddles
    for paddle in paddles:
        paddle.draw(win) # this is the draw in class Paddle

    # draw divider line (decorative)
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1: # if i is even
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 10/2, i, 10, HEIGHT//20))

    # draw ball
    ball.draw(win)

    pygame.display.update() # updates display, performs any drawing operations
                            # (computationally expensive)

def handle_collision(ball, left_paddle, right_paddle):

    # collisions from bottom and upper wall
    if ball.y + ball.radius >= HEIGHT: # bottom wall
        ball.vel_y *= -1 # reverse y-component
    elif ball.y - ball.radius <= 0: # upper wall
        ball.vel_y *= -1

    # collisions from left and right wall
    if ball.vel_x < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.vel_x *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height/2) / ball.MAX_VEL
                vel_y = difference_in_y / reduction_factor
                ball.vel_y = -1 * vel_y
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.vel_x *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height/2) / ball.MAX_VEL
                vel_y = difference_in_y / reduction_factor
                ball.vel_y = -1 * vel_y


def handle_paddle_movement(keys, left_paddle, right_paddle):
    # left_paddle movement
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    # right_paddle movement
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height<= HEIGHT:
        right_paddle.move(up=False)
    
def main():
    run = True
    clock = pygame.time.Clock() # implement a Clock to regulate the frame rate
    
    # Paddles
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT) # subtraction s.t. paddle is centred
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT) # subtraction s.t. paddle is centred

    # Ball
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)

    # Scoring
    left_score = 0
    right_score = 0

    while run: # main running loop
        clock.tick(FPS) # while loop will run at 60 FPS maximum 
                        # if computer is slow

        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score) # draws on window every single frame

        for event in pygame.event.get(): # events that occur in game
            if event.type == pygame.QUIT: # check if we exit game
                run = False 
                break
        
        keys = pygame.key.get_pressed() # get the state of all keyboard buttons (pressed or not)
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        # Scoring
        if ball.x < 0:
            right_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()

        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = 'Left Player Won!'
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = 'Right Player Won!'
        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            # draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)
            WIN.blit(text, (WIDTH/2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000) # milliseconds
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0


    pygame.quit() # close program
        
if __name__ == '__main__': # ensures main() is called only when we run this file,
                           # when the file is simply imported
    main()
