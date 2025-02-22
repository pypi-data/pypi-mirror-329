# __init__.py

# __init__.py
# 不导入 main，避免循环依赖
from .drawing import DrawingApp
from .viewer import ImageViewer
# 执行一些初始化操作（如果需要）
print("Welcome to drawing_app")