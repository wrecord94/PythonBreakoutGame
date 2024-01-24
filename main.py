import pygame
import os  # For images
import random

# TO DO:
# - Get the lives working correctly ✅
# - Ball needs to disappear when going below the paddle. (Remove from list) ✅
# - Ball needs to respawn when player presses a key and launches downwards. ✅
# - BUG when balls empty we need to only be able to spawn a new ball ✅
# - Blocks need to be on a list so that we can handle collisions ✅
# - Need to handle the blocks being hit ✅
# - 🐞 Initial ball release is causing issues ✅
# - 🐞 Movement of paddle off-screen in line with new screen size ✅
# - Handle when lives are gone game over message to be shown ✅
# - Handle destroying blocks ✅
# - Create border at top similar to edges ✅
# - Handles Level Complete ✅
# - Display the current level on the screen  ✅
# - Scoring as blocks destroyed ✅
# - Multiple lines of blocks ✅
# - Speed increases each level ✅
# - 🐞 Fix the collisions with blocks to be more accurate ✅
# - 🐞 Place the ball's respawn point at a good random location ✅
# - 🐞 Make the blocks bigger to help collisions ✅
# - End of game
# - Future enhancements:
# - Make OOP
# - Make Different block colours on each level
# - Additional features like guns, boosts, and additional balls.

# << ------------------------ Main Surface or window ------------------------
WIDTH, HEIGHT = 784, 720  # Tuple to supply to below method
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Method to set up window
pygame.display.set_caption("First Game!")  # Title

# << ------------------------   CONSTANTS  ------------------------
PURPLE = (75, 0, 130)
FPS = 60  # Need to set this to stop our while loop running thousands of time per second
BACKGROUND_IMAGE = pygame.image.load(os.path.join('Assets', 'background.png'))  # Dims 1280, 720
GREEN = (30, 207, 192)

VEL = 10  # Game Velocity

# ------- >> PADDLE
PADDLE_IMAGE = pygame.image.load(os.path.join('Assets', 'paddle.png'))  # Dims 112, 18
PADDLE_IMAGE_WIDTH = 112
PADDLE_IMAGE_HEIGHT = 18

# ------- > BALLS
BALL_IMAGE = pygame.image.load(os.path.join('Assets', 'ball.png'))  # Dims 12, 12
BALL_IMAGE_WIDTH = 12
BALL_IMAGE_HEIGHT = 12
BALL_VEL_X, BALL_VEL_Y = 5, 5

# ------- > BLOCKS
BLOCK_IMAGE = pygame.image.load(os.path.join('Assets', 'blue_block.png'))  # Dims 246, 116
BLOCK_IMAGE_WIDTH = 246 // 2.5
BLOCK_IMAGE_HEIGHT = 58 // 2.5
BLOCK_IMAGE = pygame.transform.scale(surface=BLOCK_IMAGE, size=(BLOCK_IMAGE_WIDTH, BLOCK_IMAGE_HEIGHT))

# ------- > TOP BORDER
BORDER_TOP = pygame.Rect(0, 0, WIDTH, 5)

# --------------------------- EVENTS --------------------------- >>
LIFE_LOST = pygame.USEREVENT + 1
LEVEL_COMPLETE = pygame.USEREVENT + 2

# --------------------- SCOREBOARD ---------------------
pygame.font.init()
font_health = pygame.font.Font(None, 36)  # You can adjust the font size as needed
font_game_over = pygame.font.Font(None, 36)  # You can adjust the font size as needed


def draw_window(paddle_box, blocks, balls, lives, level, score):  # Pass in the rectangles as parameters
    """Takes the paddle and blocks as parameters and draws the window using the x and y coordinates attached to these
    parameters"""
    WIN.fill(color=PURPLE)  # Sets background colour
    WIN.blit(BACKGROUND_IMAGE, (0, 0))  # Blit used to get images onto the screen
    WIN.blit(PADDLE_IMAGE, (paddle_box.x, paddle_box.y))  # Place using dims
    for block in blocks:
        WIN.blit(BLOCK_IMAGE, (block.x, block.y))
    for ball in balls:
        WIN.blit(BALL_IMAGE, (ball.x, ball.y))
    pygame.draw.rect(surface=WIN, color=GREEN, rect=BORDER_TOP)  # Draw top border

    # Render lives text
    lives_text = font_health.render(f'Lives: {lives}', True, (255, 255, 255))
    WIN.blit(lives_text, (10, 10))

    # Render Level text
    level_text = font_health.render(f'Level: {level}', True, (255, 255, 255))
    WIN.blit(level_text, (WIDTH - 100, 10))

    # Render Level text
    score_text = font_health.render(f'Score: {score}', True, (255, 255, 255))
    WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

    pygame.display.update()  # Updates screen to show what we drew as our background colour


def handles_paddle_movement(paddle_box, keys):
    if keys[pygame.K_LEFT] and paddle_box.x >= 2:  # Second part of this define our boundary for movement
        paddle_box.x -= VEL  # Move paddle left
    if keys[pygame.K_RIGHT] and paddle_box.x <= WIDTH - PADDLE_IMAGE_WIDTH:  # Boundary for movement
        paddle_box.x += VEL  # Move paddle right


def handles_ball_movement(balls, paddle_box, blocks, lives):
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
        elif ball.top <= 5:  # Handles hitting top of the screen
            ball.top = 6
            BALL_VEL_Y *= -1
        # ----------- PART 2: Collision with paddle
        if ball.colliderect(paddle_box):
            BALL_VEL_Y *= -1
            ball.bottom = paddle_box.top - BALL_IMAGE_HEIGHT
        # ----------- PART 3: Missed paddle and life lost
        if ball.top >= HEIGHT:
            # print("LIFE NEEDS TO BE LOST NOW")
            balls.remove(ball)
            pygame.event.post(pygame.event.Event(LIFE_LOST))
        # ----------- PART 4: Handles ball and block collision
        block_collision(ball=ball, blocks=blocks)


def block_collision(ball, blocks):
    global BALL_VEL_Y, score, BALL_VEL_X
    for block in blocks:  # Loop through each block and check if the ball has collided with it
        if ball.colliderect(block):  # If there is a collision
            score += 5
            print(f"Ball pos before adjustment: ({ball.x}, {ball.y})")
            print(f"Block pos before adjustment: ({block.x}, {block.y}")

            # Determine side of collision
            if ball.top <= block.bottom and ball.bottom >= block.bottom:
                print("Collision from the top")
                BALL_VEL_Y *= -1
                ball.top = block.bottom + 1
            elif ball.bottom >= block.top and ball.top <= block.top:
                print("Collision from the bottom")
                BALL_VEL_Y *= -1
                ball.bottom = block.top - 1
            elif ball.left <= block.right and ball.right >= block.right:
                print("Collision from the left")
                BALL_VEL_X *= -1
                ball.left = block.right + 1
            elif ball.right >= block.left and ball.left <= block.left:
                print("Collision from the right")
                BALL_VEL_X *= -1
                ball.right = block.left - 1


            print(f"Ball pos after adjustment: ({ball.x}, {ball.y})")
            print(f"Block pos after adjustment: ({block.x}, {block.y}")

            blocks.remove(block)  # Remove block from block list

            print(f"Ball hit a block!")
            if not blocks:
                print("No blocks left therefore level completed")
                pygame.event.post(pygame.event.Event(LEVEL_COMPLETE))


def new_balls_please():
    new_ball = pygame.Rect((random.randint(0, WIDTH)), 300, BALL_IMAGE_WIDTH, BALL_IMAGE_HEIGHT)
    return new_ball


def create_our_lines_of_blocks(level):
    blocks = []
    for line_of_blocks in range(1, level + 5):
        for i in range(1, 7):
            block = pygame.Rect(i * BLOCK_IMAGE_WIDTH, 50 + (line_of_blocks - 1) * BLOCK_IMAGE_HEIGHT,
                                BLOCK_IMAGE_WIDTH, BLOCK_IMAGE_HEIGHT)
            blocks.append(block)

    return blocks


def draw_game_over_text(level_reached):
    game_over_text = font_health.render(f'GAME OVER you reached level: {level_reached}', True, GREEN)
    WIN.blit(game_over_text,
             (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3 - game_over_text.get_height() // 2))
    next_game_starts = font_health.render(f'Next game starts in 5 seconds!', True, GREEN)
    WIN.blit(next_game_starts,
             (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)


def level_completed(level):
    pygame.time.delay(3000)  # When level complete pause for 3 seconds
    blocks = create_our_lines_of_blocks(level)  # Then create new lines of blocks

    return blocks


# # << ------------------------   MAIN GAME LOOP  ------------------------
def main():
    global score, BALL_VEL_X, BALL_VEL_Y
    paddle_box = pygame.Rect(584, 700, PADDLE_IMAGE_WIDTH, PADDLE_IMAGE_HEIGHT)
    level = 1
    blocks = create_our_lines_of_blocks(level)  # Create one nice long line of blocks!

    lives = 3
    game_over = False
    score = 0

    balls = []
    new_ball = new_balls_please()
    balls.append(new_ball)

    clock = pygame.time.Clock()  # Need to set this to stop our while loop running thousands of time per second
    run = True  # To keep while loop running
    game_over = False
    while run and not game_over:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # User closes game
                run = False  # Ends while loop and ends game
                pygame.quit()
            if event.type == LIFE_LOST:
                lives -= 1
                print(f"Lives = {lives}")
            if lives == 0:
                print(f"GAME_OVER = {game_over}")
                draw_game_over_text(level_reached=level)  # Prints the game over text and paused for 10 seconds
                game_over = True
                break  # Then breaks out of checking for events, and we restart the while run loop
            if event.type == LEVEL_COMPLETE:
                level += 1
                BALL_VEL_X = abs(BALL_VEL_X) + 0.5
                BALL_VEL_Y = abs(BALL_VEL_Y) + 0.5
                print(f"Ball Velocity is now: {BALL_VEL_X, BALL_VEL_Y}")
                print(f"Now on Level: {level}")
                blocks = level_completed(level)
            if event.type == pygame.KEYDOWN:  # This handles the space bar being pressed
                # Had to add the below to stop being able to generate new balls at any point in time
                if event.key == pygame.K_SPACE and not balls:
                    print("Respawn Ball")
                    new_ball = new_balls_please()
                    balls.append(new_ball)
        # << ------------------------   MOVEMENT  ------------------------
        keys = pygame.key.get_pressed()  # Gets key press
        # Function for paddle movement
        handles_paddle_movement(paddle_box=paddle_box, keys=keys)
        # Function for ball movement
        handles_ball_movement(balls=balls, paddle_box=paddle_box, blocks=blocks, lives=lives)

        # Updates the window with the movement above and any event related changes
        draw_window(paddle_box=paddle_box, blocks=blocks, balls=balls, lives=lives, level=level, score=score)

    main()  # This is a recursive call to trigger the main to run again when lives are all gone


if __name__ == "__main__":
    main()
