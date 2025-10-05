import pygame
import random
import sys
import time
import os


class Dice:
    def __init__(self, dice_type="Q", count=1):
        pygame.init()

        if count < 1:
            count = 1
        elif count > 5:
            count = 5

        self.count = count
        self.dice_type = dice_type.upper() if dice_type.upper() in ["Q", "W"] else "Q"

        self.res = (1000, 600)
        self.screen = pygame.display.set_mode(self.res)
        pygame.display.set_caption("Dice Simulator")

        base_path = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.join(base_path, "../assets")

        icon_path = os.path.join(assets_path, "DIE.png")
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)

        self.BG_COLOR = (25, 25, 30)
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = True

        self.dice_images = [
            pygame.image.load(os.path.join(assets_path, f"{self.dice_type}{i}.png")).convert_alpha()
            for i in range(1, 7)
        ]
        self.dice_images = [pygame.transform.scale(img, (150, 150)) for img in self.dice_images]

        self.positions = [
            (150, 250),
            (350, 250),
            (550, 250),
            (750, 250),
            (950, 250),
        ]

        self.last_results = []

    def roll_animation(self):
        """Rolling animation before result"""
        start_time = time.time()
        while time.time() - start_time < 1.2:
            self.screen.fill(self.BG_COLOR)
            for i in range(self.count):
                img = random.choice(self.dice_images)
                pos = self.positions[i]
                self.screen.blit(img, (pos[0] - img.get_width() // 2, pos[1] - img.get_height() // 2))
            pygame.display.flip()
            self.clock.tick(20)

    def roll_result(self):
        """Final dice roll result"""
        results = [random.randint(1, 6) for _ in range(self.count)]
        self.last_results = results
        print(f"Rolled Results ({self.dice_type}): {results}")

    def draw_results(self):
        """Draw the last rolled dice and text"""
        self.screen.fill(self.BG_COLOR)

        for i, result in enumerate(self.last_results):
            img = self.dice_images[result - 1]
            pos = self.positions[i]
            self.screen.blit(img, (pos[0] - img.get_width() // 2, pos[1] - img.get_height() // 2))

        if self.last_results:
            total = sum(self.last_results)
            big_font = pygame.font.SysFont(None, 72)
            total_text = big_font.render(f"Total: {total}", True, (255, 255, 255))
            self.screen.blit(total_text, (40, 30))

        font = pygame.font.SysFont(None, 32)
        text = font.render("Press SPACE to roll | Press ESC to quit", True, (200, 200, 200))
        text_rect = text.get_rect(center=(self.res[0] // 2, self.res[1] - 40))
        self.screen.blit(text, text_rect)

        pygame.display.flip()

    def run(self):
        """Main loop"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
                        self.roll_animation()
                        self.roll_result()

            self.draw_results()
            self.clock.tick(self.fps)

        pygame.quit()
        sys.exit()


def exec():
    dice_type = input("Enter dice type (Q or W): ").strip().upper()
    count = input("Enter number of dice (1–5): ").strip()

    try:
        count = int(count)
    except ValueError:
        count = 1

    dice = Dice(dice_type=dice_type, count=count)
    dice.run()


if __name__ == "__main__":
    exec()
