import pygame
import os  # For images

# TO DO:
# - Get the lives working correctly ✅
# - Ball needs to disappear when going below the paddle. (Remove from list) ✅
# - Ball needs to respawn when player presses a key and launches downwards. ✅
# - BUG when balls empty we need to only be able to spawn a new ball
# - Need to handle the blocks being hit and

# << ------------------------ Main Surface or window ------------------------
WIDTH, HEIGHT = 1280, 720  # Tuple to supply to below method
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Method to set up window
pygame.display.set_caption("First Game!")  # Title

# << ------------------------   CONSTANTS  ------------------------
PURPLE = (75, 0, 130)
FPS = 60  # Need to set this to stop our while loop running thousands of time per second
BACKGROUND_IMAGE = pygame.image.load(os.path.join('Assets', 'background.png'))  # Dims 1280, 720

VEL = 7  # Game Velocity

# ------- > BLOCKS
BLOCKS_IMAGE = pygame.image.load(os.path.join('Assets', 'blocks.png'))  # Dims 488, 28
BLOCKS_IMAGE_WIDTH = 488
BLOCKS_IMAGE_HEIGHT = 28
# ------- >> PADDLE
PADDLE_IMAGE = pygame.image.load(os.path.join('Assets', 'paddle.png'))  # Dims 112, 18
PADDLE_IMAGE_WIDTH = 112
PADDLE_IMAGE_HEIGHT = 18
# ------- > BALLS
BALL_IMAGE = pygame.image.load(os.path.join('Assets', 'ball.png'))  # Dims 12, 12
BALL_IMAGE_WIDTH = 12
BALL_IMAGE_HEIGHT = 12
BALL_VEL_X, BALL_VEL_Y = 3, 3

# --------------------------- EVENTS --------------------------- >>
LIFE_LOST = pygame.USEREVENT + 1

# --------------------- SCOREBOARD ---------------------
pygame.font.init()
font = pygame.font.Font(None, 36)  # You can adjust the font size as needed


def draw_window(paddle_box, blocks_box, balls, lives):  # Pass in the rectangles as parameters
    """Takes the paddle and blocks as parameters and draws the window using the x and y coordinates attached to these
    parameters"""
    WIN.fill(color=PURPLE)  # Sets background colour
    WIN.blit(BACKGROUND_IMAGE, (0, 0))  # Blit used to get images onto the screen
    WIN.blit(PADDLE_IMAGE, (paddle_box.x, paddle_box.y))  # Place using dims
    WIN.blit(BLOCKS_IMAGE, (blocks_box.x, blocks_box.y))
    for ball in balls:
        WIN.blit(BALL_IMAGE, (ball.x, ball.y))
    # Render lives text
    lives_text = font.render(f'Lives: {lives}', True, (255, 255, 255))
    WIN.blit(lives_text, (10, 10))  # Adjust the position as needed
    pygame.display.update()  # Updates screen to show what we drew as our background colour


def handles_paddle_movement(paddle_box, keys):
    if keys[pygame.K_LEFT] and paddle_box.x >= 2:  # Second part of this define our boundary for movement
        paddle_box.x -= VEL  # Move paddle left
    if keys[pygame.K_RIGHT] and paddle_box.x <= 1280 - PADDLE_IMAGE_WIDTH:  # Boundary for movement
        paddle_box.x += VEL  # Move paddle right


def handles_ball_movement(balls, paddle_box):
    global BALL_VEL_X, BALL_VEL_Y  # Declare BALL_VEL as a global variable
    for ball in balls:
        ball.x += BALL_VEL_X  # Move ball right
        ball.y += BALL_VEL_Y  # Move ball down
        # ----------- PART 1: Collision with screen borders
        if ball.right >= WIDTH:
            ball.right = WIDTH - 1
            BALL_VEL_X *= -1
        elif ball.left <= 0:
            ball.left = 1
            BALL_VEL_X *= -1
        # ----------- PART 2: Collision with paddle
        if ball.colliderect(paddle_box):
            BALL_VEL_Y *= -1
            if ball.bottom < paddle_box.top:
                paddle_box.top = paddle_box.top + 1
        # ----------- PART 3: Missed paddle and life lost
        if ball.top >= HEIGHT:
            # print("LIFE NEEDS TO BE LOST NOW")
            balls.remove(ball)
            pygame.event.post(pygame.event.Event(LIFE_LOST))


def new_balls_please():
    new_ball = pygame.Rect(396, 50, BALL_IMAGE_WIDTH, BALL_IMAGE_HEIGHT)
    return new_ball


# # << ------------------------   MAIN GAME LOOP  ------------------------
def main():
    paddle_box = pygame.Rect(584, 700, PADDLE_IMAGE_WIDTH, PADDLE_IMAGE_HEIGHT)
    blocks_box = pygame.Rect(396, 50, BLOCKS_IMAGE_WIDTH, BLOCKS_IMAGE_HEIGHT)
    lives = 3
    balls = []
    ball_box = pygame.Rect(396, 50, BALL_IMAGE_WIDTH, BALL_IMAGE_HEIGHT)
    balls.append(ball_box)

    clock = pygame.time.Clock()  # Need to set this to stop our while loop running thousands of time per second
    run = True  # To keep while loop running
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # User closes game
                run = False  # Ends while loop and ends game
            if event.type == LIFE_LOST:
                lives -= 1
                print(f"Lives = {lives}")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not balls:
                    print("Respawn Ball")
                    new_ball = new_balls_please()
                    balls.append(new_ball)
        # << ------------------------   MOVEMENT  ------------------------
        keys = pygame.key.get_pressed()  # Gets key press
        # Function for paddle movement
        handles_paddle_movement(paddle_box=paddle_box, keys=keys)
        # Function for ball movement
        handles_ball_movement(balls=balls, paddle_box=paddle_box)

        # Updates the window with the movement above and any event related changes
        draw_window(paddle_box=paddle_box, blocks_box=blocks_box, balls=balls, lives=lives)


if __name__ == "__main__":
    main()
