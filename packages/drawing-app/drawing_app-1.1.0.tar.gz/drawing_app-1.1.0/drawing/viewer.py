import pygame
import sys
import struct

class ImageViewer:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("显示图片")
        self.width = width
        self.height = height

    def load_wzx(self, filename):
        with open(filename, "rb") as f:
            header = f.read(3)
            if header != b"WZX":
                raise ValueError("Invalid .wzx file format")
            width, height = struct.unpack("II", f.read(8))
            surface = pygame.Surface((width, height))
            for y in range(height):
                for x in range(width):
                    pixel_data = f.read(3)
                    if len(pixel_data) != 3:
                        raise ValueError("文件内容不完整")
                    color = struct.unpack("BBB", pixel_data)
                    surface.set_at((x, y), color)
            return surface

    def run(self, filename):
        try:
            image = self.load_wzx(filename)
        except Exception as e:
            print(f"加载失败: {e}")
            pygame.quit()
            sys.exit()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.blit(image, (0, 0))
            pygame.display.flip()

        pygame.quit()
        sys.exit()