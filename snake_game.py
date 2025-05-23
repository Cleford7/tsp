import pygame
import random

# Initialize Pygame
pygame.init()

# Define screen dimensions
screen_width = 800
screen_height = 600

# Create the game display screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game by AI Agent") # Updated caption

# --- Constants ---
# Colors (R, G, B)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0) # Snake color, Score color, Restart instruction color
RED = (255, 0, 0)   # Food color, Game Over color
WHITE = (255, 255, 255) # Potentially for future text or elements

# Game properties
SNAKE_BLOCK_SIZE = 20 # Size of each snake segment
FOOD_BLOCK_SIZE = 20  # Size of the food item
GAME_SPEED = 15       # Frames per second

# --- Class Definitions ---

class Snake:
    """
    Represents the snake in the game.
    Manages its movement, growth, drawing, and collision detection.
    """
    def __init__(self, x, y):
        """
        Initializes the snake.
        Args:
            x (int): Initial x-coordinate of the snake's head.
            y (int): Initial y-coordinate of the snake's head.
        """
        self.length = 1 # Initial length of the snake
        self.positions = [(x, y)] # List of (x,y) tuples representing snake's body, head is at index 0
        self.direction = (1, 0)  # Initial direction: (dx, dy) -> right
        self.color = GREEN
        self.score = 0           # Player's score

    def get_head_position(self):
        """Returns the (x, y) position of the snake's head."""
        return self.positions[0]

    def move(self):
        """
        Moves the snake by one block in its current direction.
        The body segments follow the head.
        """
        cur_x, cur_y = self.get_head_position()
        dx, dy = self.direction
        # Calculate new head position
        new_head = (cur_x + (dx * SNAKE_BLOCK_SIZE),
                    cur_y + (dy * SNAKE_BLOCK_SIZE))
            
        self.positions.insert(0, new_head) # Add new head to the front
        # If snake has not grown, remove the last segment to maintain length
        if len(self.positions) > self.length:
            self.positions.pop()

    def grow(self):
        """Increases the snake's length and score when it eats food."""
        self.length += 1
        self.score += 1

    def check_collision_with_self(self):
        """Checks if the snake's head has collided with any part of its body."""
        head = self.get_head_position()
        # Check if head position exists in the rest of the body segments
        return head in self.positions[1:]

    def draw(self, surface):
        """
        Draws the snake on the given surface.
        Args:
            surface (pygame.Surface): The surface to draw the snake on.
        """
        for p in self.positions:
            # Create a rectangle for each snake segment
            rect = pygame.Rect((p[0], p[1]), (SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE))
            pygame.draw.rect(surface, self.color, rect)

    def change_direction(self, new_direction):
        """
        Changes the snake's direction of movement.
        Prevents the snake from immediately reversing its direction.
        Args:
            new_direction (tuple): The new direction (dx, dy).
        """
        # Check if new direction is opposite to current direction
        if (new_direction[0] * -1, new_direction[1] * -1) == self.direction:
            return # Do not change direction if it's a reversal
        self.direction = new_direction

class Food:
    """
    Represents the food item in the game.
    Manages its position and drawing.
    """
    def __init__(self, snake_positions):
        """
        Initializes the food item.
        Args:
            snake_positions (list): A list of (x,y) tuples representing the snake's current body.
                                   Used to ensure food doesn't spawn on the snake.
        """
        self.color = RED
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions):
        """
        Places the food at a random position on the grid.
        Ensures the food does not spawn on top of the snake.
        Args:
            snake_positions (list): Current positions of the snake's body.
        """
        while True:
            # Generate random x, y coordinates aligned to the grid
            x = random.randrange(0, screen_width // FOOD_BLOCK_SIZE) * FOOD_BLOCK_SIZE
            y = random.randrange(0, screen_height // FOOD_BLOCK_SIZE) * FOOD_BLOCK_SIZE
            self.position = (x, y)
            # Ensure the food's new position is not on the snake
            if self.position not in snake_positions:
                break
    
    def draw(self, surface):
        """
        Draws the food item on the given surface.
        Args:
            surface (pygame.Surface): The surface to draw the food on.
        """
        rect = pygame.Rect((self.position[0], self.position[1]), (FOOD_BLOCK_SIZE, FOOD_BLOCK_SIZE))
        pygame.draw.rect(surface, self.color, rect)

# --- Font Definitions ---
# Using SysFont for simplicity, consider using .ttf files for more control
score_font = pygame.font.SysFont("arial", 35)        # Font for displaying the score
game_over_font = pygame.font.SysFont("arial", 70)    # Font for "Game Over" message
instruction_font = pygame.font.SysFont("arial", 30)  # Font for restart/quit instructions

# --- Helper Functions ---

def display_message(message, font, color, surface, position_center):
    """
    Renders and displays a message centered at a given position on a surface.
    Args:
        message (str): The text message to display.
        font (pygame.font.Font): The font to use for the message.
        color (tuple): The color of the text (R, G, B).
        surface (pygame.Surface): The surface to draw the message on.
        position_center (tuple): The (x, y) coordinates for the center of the message.
    """
    text_surface = font.render(message, True, color)
    text_rect = text_surface.get_rect(center=position_center)
    surface.blit(text_surface, text_rect)

def reset_game():
    """
    Resets the game to its initial state.
    Re-initializes snake, food, and game state variables.
    """
    global snake, food, game_active, game_over_state # Declare globals to modify them
    
    # Re-initialize snake at the center
    snake = Snake(screen_width // 2 - SNAKE_BLOCK_SIZE // 2, 
                  screen_height // 2 - SNAKE_BLOCK_SIZE // 2) # Centered properly
    # Re-initialize food, ensuring it's not on the new snake
    food = Food(snake.positions)
    
    game_active = True      # Set game to active play state
    game_over_state = False # Reset game over flag

# --- Game Initialization ---
# These variables will be managed by reset_game() initially and on restarts
snake: Snake 
food: Food
game_active: bool
game_over_state: bool

reset_game() # Call reset_game once to initialize all game components and states

# --- Main Game Loop ---
running = True
clock = pygame.time.Clock() # Create a Clock object to manage game speed

while running:
    # --- Event Handling ---
    if game_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # User clicked the close button
                running = False
            elif event.type == pygame.KEYDOWN: # User pressed a key
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1)) # Up
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))  # Down
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0)) # Left
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))  # Right
        
        # --- Game Logic ---
        snake.move()

        # Check for game over conditions:
        # 1. Snake hits screen boundary
        head_x, head_y = snake.get_head_position()
        if not (0 <= head_x < screen_width and 0 <= head_y < screen_height):
            game_active = False  # End current game session
            game_over_state = True # Set to true to show "Game Over" screen
        
        # 2. Snake hits itself (self-collision)
        # Only check if still active (e.g., didn't hit boundary in the same frame)
        if game_active and snake.check_collision_with_self():
            game_active = False
            game_over_state = True
        
        # Check for snake eating food:
        # Only check if still active
        if game_active and snake.get_head_position() == food.position:
            snake.grow() # Snake grows longer and score increases
            food.randomize_position(snake.positions) # New food appears

        # --- Drawing ---
        screen.fill(BLACK)      # Clear screen with black background
        snake.draw(screen)      # Draw the snake
        food.draw(screen)       # Draw the food
        
        # Display Score
        score_text_surface = score_font.render(f"Score: {snake.score}", True, GREEN)
        screen.blit(score_text_surface, (10, 10)) # Position score at top-left (with a small margin)

    else: # game_active is False (Game Over screen)
        if game_over_state: # Only display if a game has actually ended
            # Display "Game Over" and instructions
            display_message("Game Over!", game_over_font, RED, screen, 
                            (screen_width // 2, screen_height // 2 - 60))
            display_message(f"Final Score: {snake.score}", score_font, GREEN, screen,
                            (screen_width // 2, screen_height // 2))
            display_message("Press R to Restart or Q to Quit", instruction_font, GREEN, screen,
                            (screen_width // 2, screen_height // 2 + 60))
        
        # Event handling for Game Over screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: # User presses 'Q' to quit
                    running = False
                if event.key == pygame.K_r: # User presses 'R' to restart
                    reset_game()

    # --- Update Display and Control Speed ---
    pygame.display.flip() # Update the full display Surface to the screen
    clock.tick(GAME_SPEED) # Control the game speed (FPS)

# --- Quit Pygame ---
pygame.quit() # Uninitialize all Pygame modules
# sys.exit() # It's good practice to include sys.exit() if not running in an interactive shell
