import pygame
import sys
import struct

class DrawingApp:
    def __init__(self, width=800, height=600, background_image_path=None):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("图形化绘图程序")
        self.width = width
        self.height = height
        self.background_image_path = background_image_path
        self.background_image = None
        self.current_color = (0, 0, 0)  # 默认黑色
        self.brush_size = 5
        self.save_button = pygame.Rect(10, 10, 100, 50)
        self.last_mouse_pos = None  # 用于记录上一次鼠标位置

        # 尝试加载背景图片
        if background_image_path:
            try:
                self.background_image = pygame.image.load(background_image_path)
                self.background_image = pygame.transform.scale(self.background_image, (width, height))
            except Exception as e:
                print(f"加载背景图片失败: {e}")
                self.background_image = None

        # 创建一个透明的绘图层
        self.drawing_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.drawing_surface.fill((0, 0, 0, 0))  # 填充透明色

    def save_wzx(self, filename):
        width, height = self.screen.get_size()
        with open(filename, "wb") as f:
            f.write(b"WZX")  # 写入文件头
            f.write(struct.pack("II", width, height))  # 写入图像宽度和高度
            for y in range(height):
                for x in range(width):
                    color = self.screen.get_at((x, y))
                    f.write(struct.pack("BBB", *color[:3]))  # 写入像素数据
        print(f"图片已保存为 {filename}")

    def run(self):
        running = True
        drawing = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.save_button.collidepoint(event.pos):
                        self.save_wzx("drawing.wzx")
                    else:
                        drawing = True
                        self.last_mouse_pos = event.pos  # 记录鼠标按下时的位置
                elif event.type == pygame.MOUSEBUTTONUP:
                    drawing = False
                    self.last_mouse_pos = None  # 清空鼠标位置记录
                elif event.type == pygame.MOUSEMOTION and drawing:
                    mouse_pos = event.pos
                    if self.last_mouse_pos:
                        # 在绘图层上绘制连续的线条
                        pygame.draw.line(self.drawing_surface, self.current_color, self.last_mouse_pos, mouse_pos, self.brush_size)
                    self.last_mouse_pos = mouse_pos  # 更新鼠标位置
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.current_color = (255, 0, 0)
                    elif event.key == pygame.K_g:
                        self.current_color = (0, 255, 0)
                    elif event.key == pygame.K_b:
                        self.current_color = (0, 0, 255)
                    elif event.key == pygame.K_w:
                        self.current_color = (255, 255, 255)
                    elif event.key == pygame.K_k:
                        self.current_color = (0, 0, 0)

            # 绘制背景图片或填充白色
            if self.background_image:
                self.screen.blit(self.background_image, (0, 0))
            else:
                self.screen.fill((255, 255, 255))

            # 将绘图层绘制到屏幕上
            self.screen.blit(self.drawing_surface, (0, 0))

            # 绘制保存按钮
            pygame.draw.rect(self.screen, (200, 200, 200), self.save_button)
            font = pygame.font.SysFont(None, 36)
            text = font.render("Save", True, (0, 0, 0))
            self.screen.blit(text, (self.save_button.x + 20, self.save_button.y + 10))

            pygame.display.flip()

        pygame.quit()
        sys.exit()