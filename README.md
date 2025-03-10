# 植物大战僵尸风格贪吃蛇游戏

一个基于Python和Pygame的贪吃蛇游戏，采用植物大战僵尸的卡通风格设计。

## 游戏特点

- 植物大战僵尸风格的图形和音效
- 多种食物类型，提供不同的得分和特殊能力
- 障碍物系统，增加游戏难度
- 特殊能力系统，如护盾和速度提升
- 多种游戏场景，如白天、夜晚和泳池
- 高质量的图形和动画效果

## 安装

1. 确保已安装Python 3.6或更高版本
2. 安装所需的依赖项：

```bash
pip install pygame
```

3. 克隆或下载本仓库
4. 进入项目目录

## 运行游戏

在项目根目录下运行以下命令：

```bash
python main.py
```

或者双击`start_game.bat`文件（Windows系统）或运行`./start_game.sh`文件（Linux/Mac系统）。

## 游戏控制

- 方向键：控制蛇的移动
- 空格键：暂停/继续游戏
- ESC键：退出游戏
- 回车键：开始游戏/重新开始

## 游戏元素

### 食物类型

- **阳光**：基础食物，提供10点分数
- **向日葵**：提供20点分数
- **坚果墙**：提供5点分数，激活护盾能力
- **豌豆射手**：提供15点分数，激活速度提升能力

### 特殊能力

- **护盾**：暂时使蛇无敌，可以穿过自己的身体和障碍物
- **速度提升**：暂时提高蛇的移动速度

### 障碍物

- **僵尸**：移动的障碍物，碰到会导致游戏结束
- **墓碑**：静止的障碍物，碰到会导致游戏结束

### 场景

- **白天**：标准场景，视野良好
- **夜晚**：视野受限，增加难度
- **泳池**：包含水域区域，移动速度不同

## 图像资源

游戏支持两种渲染模式：

1. **基本图形渲染**：使用Pygame的基本绘图功能，无需额外图像资源
2. **图像渲染**：使用PNG图像资源，提供更精细的视觉效果

### 添加自定义图像

1. 将PNG图像放在对应的目录中：
   - `assets/images/snake/` - 蛇的图像
   - `assets/images/food/` - 食物图像
   - `assets/images/obstacles/` - 障碍物图像
   - `assets/images/backgrounds/` - 背景图像
   - `assets/images/ui/` - UI元素图像

2. 确保图像文件名与配置文件中的名称匹配

3. 在`config.py`中设置`use_images = True`启用图像渲染

### 创建自定义图像

1. 使用SVG编辑器（如Inkscape）创建SVG图像
2. 将SVG文件保存在对应的目录中
3. 使用提供的转换工具将SVG转换为PNG：

```bash
python tools/svg_to_png.py --game-assets
```

详细说明请参阅`assets/images/README.md`和`assets/images/README_SVG_TO_PNG.md`。

## 音频资源

游戏需要以下音频文件：

- `assets/sounds/simple_background.wav` - 背景音乐
- `assets/sounds/eat_food.wav` - 收集食物音效
- `assets/sounds/game_over.wav` - 游戏结束音效
- `assets/sounds/menu_click.wav` - 菜单点击音效
- `assets/sounds/ability_activated.wav` - 特殊能力激活音效
- `assets/sounds/zombie_groan.wav` - 僵尸呻吟音效

## 字体资源

游戏使用以下字体：

- `assets/fonts/simhei.ttf` - 黑体中文字体

## 项目结构

```
hungrysnake/
├── assets/
│   ├── fonts/         - 字体文件
│   ├── images/        - 图像资源
│   └── sounds/        - 音频资源
├── entities/          - 游戏实体（蛇、食物、障碍物）
├── scenes/            - 游戏场景（菜单、游戏、结束）
├── ui/                - 用户界面元素
├── utils/             - 工具函数和类
├── tools/             - 开发工具
├── config.py          - 游戏配置
├── game_engine.py     - 游戏引擎
├── main.py            - 主程序
├── start_game.bat     - Windows启动脚本
└── start_game.sh      - Linux/Mac启动脚本
```

## 自定义游戏

可以通过修改`config.py`文件来自定义游戏：

- 调整窗口大小和网格大小
- 修改游戏速度和难度
- 更改颜色和视觉风格
- 添加新的食物类型和特殊能力
- 创建新的场景和障碍物

## 贡献

欢迎贡献代码、报告问题或提出改进建议！

## 许可证

本项目采用MIT许可证。详见LICENSE文件。 