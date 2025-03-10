"""
SVG转PNG工具
将SVG图像转换为PNG格式
"""

import os
import sys
import argparse
import subprocess
import platform

# 尝试导入cairosvg，如果失败则提供替代方案
HAS_CAIROSVG = False
try:
    # 先检查是否有Cairo库
    try:
        import ctypes
        ctypes.cdll.LoadLibrary("cairo")
        # 如果成功加载Cairo库，再尝试导入cairosvg
        import cairosvg
        HAS_CAIROSVG = True
    except:
        print("警告: 未找到Cairo库，无法使用cairosvg。")
except ImportError:
    print("警告: 未安装cairosvg库。将使用替代方法。")

if not HAS_CAIROSVG:
    print("将使用替代方法转换SVG文件。")
    print("如果要使用cairosvg，请安装以下依赖:")
    print("1. 安装Cairo库 (https://www.cairographics.org/download/)")
    print("2. 安装cairosvg: pip install cairosvg")

def convert_svg_to_png_with_cairosvg(svg_path, png_path, width=None, height=None):
    """
    使用cairosvg将SVG文件转换为PNG文件
    
    参数:
        svg_path: SVG文件路径
        png_path: PNG文件输出路径
        width: 输出PNG的宽度（像素）
        height: 输出PNG的高度（像素）
    """
    if not HAS_CAIROSVG:
        return False
        
    try:
        print(f"转换 {svg_path} 为 {png_path}")
        cairosvg.svg2png(
            url=svg_path,
            write_to=png_path,
            output_width=width,
            output_height=height
        )
        print(f"转换成功: {png_path}")
        return True
    except Exception as e:
        print(f"转换失败: {e}")
        return False

def convert_svg_to_png_with_inkscape(svg_path, png_path, width=None, height=None):
    """
    使用Inkscape将SVG文件转换为PNG文件
    
    参数:
        svg_path: SVG文件路径
        png_path: PNG文件输出路径
        width: 输出PNG的宽度（像素）
        height: 输出PNG的高度（像素）
    """
    try:
        print(f"使用Inkscape转换 {svg_path} 为 {png_path}")
        
        # 检查Inkscape是否安装
        inkscape_cmd = "inkscape"
        if platform.system() == "Windows":
            # 在Windows上，尝试查找Inkscape安装路径
            program_files = os.environ.get("ProgramFiles", "C:\\Program Files")
            inkscape_path = os.path.join(program_files, "Inkscape", "bin", "inkscape.exe")
            if os.path.exists(inkscape_path):
                inkscape_cmd = f'"{inkscape_path}"'
        
        # 构建命令
        cmd = [inkscape_cmd]
        
        # 检查Inkscape版本
        try:
            version_output = subprocess.check_output([inkscape_cmd, "--version"], 
                                                   stderr=subprocess.STDOUT, 
                                                   universal_newlines=True)
            is_new_version = "Inkscape 1." in version_output
        except:
            is_new_version = False
        
        # 根据Inkscape版本构建命令
        if is_new_version:
            cmd.extend(["--export-filename", png_path])
        else:
            cmd.extend(["--export-png", png_path])
        
        if width:
            cmd.extend(["--export-width", str(width)])
        if height:
            cmd.extend(["--export-height", str(height)])
        
        cmd.append(svg_path)
        
        # 执行命令
        subprocess.run(cmd, check=True)
        print(f"转换成功: {png_path}")
        return True
    except Exception as e:
        print(f"Inkscape转换失败: {e}")
        return False

def convert_svg_to_png_with_imagemagick(svg_path, png_path, width=None, height=None):
    """
    使用ImageMagick将SVG文件转换为PNG文件
    
    参数:
        svg_path: SVG文件路径
        png_path: PNG文件输出路径
        width: 输出PNG的宽度（像素）
        height: 输出PNG的高度（像素）
    """
    try:
        print(f"使用ImageMagick转换 {svg_path} 为 {png_path}")
        
        # 构建命令
        cmd = ["convert"]
        
        if width and height:
            cmd.extend(["-size", f"{width}x{height}"])
        
        cmd.append(svg_path)
        
        if width and height:
            cmd.extend(["-resize", f"{width}x{height}"])
        
        cmd.append(png_path)
        
        # 执行命令
        subprocess.run(cmd, check=True)
        print(f"转换成功: {png_path}")
        return True
    except Exception as e:
        print(f"ImageMagick转换失败: {e}")
        return False

def convert_svg_to_png_with_pillow(svg_path, png_path, width=None, height=None):
    """
    使用Pillow和svglib将SVG文件转换为PNG文件
    
    参数:
        svg_path: SVG文件路径
        png_path: PNG文件输出路径
        width: 输出PNG的宽度（像素）
        height: 输出PNG的高度（像素）
    """
    try:
        print(f"使用Pillow和svglib转换 {svg_path} 为 {png_path}")
        
        # 尝试导入所需库
        try:
            from svglib.svglib import svg2rlg
            from reportlab.graphics import renderPM
            from PIL import Image
        except ImportError:
            print("错误: 未安装svglib或Pillow库。请使用以下命令安装:")
            print("pip install svglib pillow")
            return False
        
        # 转换SVG为ReportLab图形对象
        drawing = svg2rlg(svg_path)
        
        # 计算缩放比例
        if width and height:
            # 获取原始尺寸
            orig_width, orig_height = drawing.width, drawing.height
            # 计算缩放比例
            scale_x = width / orig_width
            scale_y = height / orig_height
            # 使用较小的缩放比例，保持宽高比
            scale = min(scale_x, scale_y)
            # 应用缩放
            drawing.width, drawing.height = orig_width * scale, orig_height * scale
            drawing.scale(scale, scale)
        
        # 渲染为PNG
        renderPM.drawToFile(drawing, png_path, fmt="PNG")
        
        # 如果需要精确的宽高，使用Pillow调整大小
        if width and height:
            img = Image.open(png_path)
            img = img.resize((width, height), Image.LANCZOS)
            img.save(png_path)
        
        print(f"转换成功: {png_path}")
        return True
    except Exception as e:
        print(f"Pillow转换失败: {e}")
        return False

def convert_svg_to_png(svg_path, png_path, width=None, height=None):
    """
    将单个SVG文件转换为PNG文件，尝试多种方法
    
    参数:
        svg_path: SVG文件路径
        png_path: PNG文件输出路径
        width: 输出PNG的宽度（像素）
        height: 输出PNG的高度（像素）
    """
    # 尝试使用cairosvg
    if HAS_CAIROSVG:
        if convert_svg_to_png_with_cairosvg(svg_path, png_path, width, height):
            return True
    
    # 尝试使用Pillow和svglib
    if convert_svg_to_png_with_pillow(svg_path, png_path, width, height):
        return True
    
    # 尝试使用Inkscape
    if convert_svg_to_png_with_inkscape(svg_path, png_path, width, height):
        return True
    
    # 尝试使用ImageMagick
    if convert_svg_to_png_with_imagemagick(svg_path, png_path, width, height):
        return True
    
    print(f"错误: 无法转换 {svg_path}，请安装以下工具之一:")
    print("1. svglib和Pillow (pip install svglib pillow)")
    print("2. Inkscape (https://inkscape.org/)")
    print("3. ImageMagick (https://imagemagick.org/)")
    print("4. cairosvg (pip install cairosvg)")
    return False

def batch_convert_svg_to_png(svg_dir, png_dir=None, width=None, height=None, recursive=False):
    """
    批量将SVG文件转换为PNG文件
    
    参数:
        svg_dir: SVG文件目录
        png_dir: PNG文件输出目录，如果为None则输出到相同目录
        width: 输出PNG的宽度（像素）
        height: 输出PNG的高度（像素）
        recursive: 是否递归处理子目录
    """
    # 确保SVG目录存在
    if not os.path.exists(svg_dir):
        print(f"错误: SVG目录不存在: {svg_dir}")
        return False
    
    # 如果未指定PNG目录，则使用SVG目录
    if png_dir is None:
        png_dir = svg_dir
    
    # 确保输出目录存在
    os.makedirs(png_dir, exist_ok=True)
    
    success_count = 0
    failure_count = 0
    
    # 处理当前目录中的SVG文件
    for filename in os.listdir(svg_dir):
        file_path = os.path.join(svg_dir, filename)
        
        # 如果是目录且需要递归处理
        if os.path.isdir(file_path) and recursive:
            # 创建对应的输出子目录
            sub_png_dir = os.path.join(png_dir, filename) if png_dir != svg_dir else file_path
            # 递归处理子目录
            sub_success, sub_failure = batch_convert_svg_to_png(
                file_path, sub_png_dir, width, height, recursive
            )
            success_count += sub_success
            failure_count += sub_failure
        
        # 处理SVG文件
        elif filename.lower().endswith('.svg'):
            svg_path = file_path
            png_path = os.path.join(png_dir, filename.replace('.svg', '.png'))
            
            if convert_svg_to_png(svg_path, png_path, width, height):
                success_count += 1
            else:
                failure_count += 1
    
    print(f"\n转换完成: {success_count} 成功, {failure_count} 失败")
    return success_count, failure_count

def convert_game_assets():
    """转换游戏资源中的所有SVG文件"""
    # 获取项目根目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    assets_dir = os.path.join(project_root, "assets", "images")
    
    # 确保assets/images目录存在
    if not os.path.exists(assets_dir):
        print(f"错误: 图像资源目录不存在: {assets_dir}")
        return False
    
    print("开始转换游戏资源中的SVG文件...")
    
    # 转换蛇图像
    snake_dir = os.path.join(assets_dir, "snake")
    if os.path.exists(snake_dir):
        print("\n转换蛇图像...")
        batch_convert_svg_to_png(snake_dir, width=30, height=30)
    
    # 转换食物图像
    food_dir = os.path.join(assets_dir, "food")
    if os.path.exists(food_dir):
        print("\n转换食物图像...")
        batch_convert_svg_to_png(food_dir, width=30, height=30)
    
    # 转换障碍物图像
    obstacles_dir = os.path.join(assets_dir, "obstacles")
    if os.path.exists(obstacles_dir):
        print("\n转换障碍物图像...")
        batch_convert_svg_to_png(obstacles_dir, width=30, height=30)
    
    # 转换背景图像
    backgrounds_dir = os.path.join(assets_dir, "backgrounds")
    if os.path.exists(backgrounds_dir):
        print("\n转换背景图像...")
        batch_convert_svg_to_png(backgrounds_dir, width=800, height=600)
    
    # 转换UI图像
    ui_dir = os.path.join(assets_dir, "ui")
    if os.path.exists(ui_dir):
        print("\n转换UI图像...")
        # 按钮图像
        for filename in os.listdir(ui_dir):
            if filename.startswith("button_") and filename.endswith(".svg"):
                svg_path = os.path.join(ui_dir, filename)
                png_path = os.path.join(ui_dir, filename.replace('.svg', '.png'))
                convert_svg_to_png(svg_path, png_path, width=200, height=50)
            elif filename.endswith(".svg"):
                svg_path = os.path.join(ui_dir, filename)
                png_path = os.path.join(ui_dir, filename.replace('.svg', '.png'))
                convert_svg_to_png(svg_path, png_path)
    
    print("\n所有游戏资源转换完成!")
    return True

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="将SVG图像转换为PNG格式")
    
    # 添加命令行参数
    parser.add_argument("--svg", help="SVG文件或目录路径")
    parser.add_argument("--png", help="PNG输出文件或目录路径")
    parser.add_argument("--width", type=int, help="输出PNG的宽度（像素）")
    parser.add_argument("--height", type=int, help="输出PNG的高度（像素）")
    parser.add_argument("--recursive", action="store_true", help="递归处理子目录")
    parser.add_argument("--game-assets", action="store_true", help="转换游戏资源中的所有SVG文件")
    
    args = parser.parse_args()
    
    # 转换游戏资源
    if args.game_assets:
        convert_game_assets()
        return
    
    # 检查必要参数
    if not args.svg:
        parser.print_help()
        print("\n错误: 必须指定SVG文件或目录路径")
        return
    
    # 单个文件转换
    if os.path.isfile(args.svg):
        if not args.svg.lower().endswith('.svg'):
            print(f"错误: 不是SVG文件: {args.svg}")
            return
        
        # 确定输出路径
        png_path = args.png if args.png else args.svg.replace('.svg', '.png')
        
        # 转换文件
        convert_svg_to_png(args.svg, png_path, args.width, args.height)
    
    # 批量转换
    elif os.path.isdir(args.svg):
        batch_convert_svg_to_png(args.svg, args.png, args.width, args.height, args.recursive)
    
    else:
        print(f"错误: 文件或目录不存在: {args.svg}")

if __name__ == "__main__":
    main() 