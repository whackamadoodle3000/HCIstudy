import pygame
import os
import random
import numpy as np
import time
import sys

# Configuration
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080  # Adjust as needed
DURATION = 120  # Total time in seconds
FLASH_DURATION = 5  # Time each image stays on screen
NUM_IMAGES = 8  # Number of images to show
NOISE_STD_DEV = 7  # Gaussian noise standard deviation

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

# Load images
def get_images(folder):
    return [f for f in os.listdir(folder) if f.lower().endswith(".jpg")]

def display_image(image_path):
    img = pygame.image.load(image_path)
    screen.fill((0, 0, 0))
    
    # Maintain aspect ratio
    img_rect = img.get_rect()
    scale_factor = min(SCREEN_WIDTH / img_rect.width, SCREEN_HEIGHT / img_rect.height)
    new_size = (int(img_rect.width * scale_factor), int(img_rect.height * scale_factor))
    img = pygame.transform.scale(img, new_size)
    img_rect = img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
    screen.blit(img, img_rect)
    pygame.display.flip()

def flash_images(folder):
    image_files = get_images(folder)
    if len(image_files) < NUM_IMAGES:
        print("Not enough images in folder.")
        return
    
    selected_images = random.sample(image_files, NUM_IMAGES)
    random.shuffle(selected_images)

    # Compute display times with Gaussian noise
    intervals = np.linspace(0, DURATION, NUM_IMAGES + 2)[1:-1]
    times = np.clip(intervals + np.random.normal(0, NOISE_STD_DEV, NUM_IMAGES), 5, DURATION - 5)
    times.sort()
    
    start_time = time.time()
    current_image = 0
    running = True

    while running:
        elapsed = time.time() - start_time

        if current_image < NUM_IMAGES and elapsed >= times[current_image]:
            display_image(os.path.join(folder, selected_images[current_image]))
            time.sleep(FLASH_DURATION)  # Keep image on screen for flash duration
            screen.fill((0, 0, 0))
            pygame.display.flip()
            current_image += 1

        if elapsed >= DURATION:
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        clock.tick(30)

    pygame.quit()

def display_static(folder):
    image_files = get_images(folder)
    if not image_files:
        print("No images found in folder.")
        return
    
    display_image(os.path.join(folder, random.choice(image_files)))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        clock.tick(30)
    pygame.quit()

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <mode> <folder>")
        print("Modes: flash, static")
        sys.exit(1)
    
    mode = sys.argv[1].strip().lower()
    folder = sys.argv[2]
    
    if not os.path.isdir(folder):
        print("Invalid folder path.")
        sys.exit(1)
    
    if mode == 'flash':
        flash_images(folder)
    elif mode == 'static':
        display_static(folder)
    else:
        print("Invalid mode. Use 'flash' or 'static'.")
        sys.exit(1)

if __name__ == "__main__":
    main()
