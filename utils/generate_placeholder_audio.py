"""
占位音频生成工具
用于生成测试用的占位音频文件
"""

import os
import struct
import wave
import math
import random

def generate_sine_wave(frequency, duration, sample_rate=44100):
    """生成正弦波音频数据"""
    n_samples = int(sample_rate * duration)
    s = []
    for i in range(n_samples):
        value = math.sin(2 * math.pi * frequency * i / sample_rate)
        # 将值缩放到 16 位有符号整数范围 (-32768 到 32767)
        s.append(int(value * 32767))
    return s

def clamp(value, min_value=-32768, max_value=32767):
    """确保值在指定范围内"""
    return max(min_value, min(max_value, value))

def save_wave_file(file_path, samples, sample_rate=44100, channels=1):
    """保存WAV文件"""
    # 确保目录存在
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with wave.open(file_path, 'w') as wave_file:
        wave_file.setnchannels(channels)
        wave_file.setsampwidth(2)  # 2 bytes per sample (16 bits)
        wave_file.setframerate(sample_rate)
        
        # 将样本打包为二进制数据
        binary_data = b''
        for sample in samples:
            # 确保样本值在范围内
            clamped_sample = clamp(sample)
            binary_data += struct.pack('<h', clamped_sample)  # 小端序 16 位有符号整数
        
        wave_file.writeframes(binary_data)

def generate_background_music(file_path, duration=30, sample_rate=44100):
    """生成简单的背景音乐"""
    print(f"正在生成背景音乐 ({duration}秒)...")
    
    # 基础音符频率 (C大调音阶)
    notes = {
        'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
        'G4': 392.00, 'A4': 440.00, 'B4': 493.88, 'C5': 523.25
    }
    
    # 简单的旋律模式 (PvZ风格的轻松旋律)
    melody = [
        ('E4', 0.5), ('G4', 0.5), ('C5', 1.0),
        ('B4', 0.5), ('G4', 0.5), ('E4', 1.0),
        ('A4', 0.5), ('B4', 0.5), ('C5', 1.0),
        ('A4', 0.5), ('G4', 0.5), ('E4', 1.0)
    ]
    
    # 生成完整音乐数据
    all_samples = []
    melody_duration = sum(note[1] for note in melody)
    repetitions = int(duration / melody_duration) + 1
    
    for _ in range(repetitions):
        for note, note_duration in melody:
            # 生成主旋律音符
            freq = notes[note]
            note_samples = []
            samples_count = int(sample_rate * note_duration)
            
            for i in range(samples_count):
                # 添加主音
                value = math.sin(2 * math.pi * freq * i / sample_rate) * 0.5
                # 添加和声 (5度和3度)
                harmony1 = math.sin(2 * math.pi * (freq * 1.5) * i / sample_rate) * 0.2
                harmony2 = math.sin(2 * math.pi * (freq * 1.25) * i / sample_rate) * 0.15
                # 添加轻微的环境噪声
                noise = (random.random() * 2 - 1) * 0.05
                
                # 组合所有声音
                combined = value + harmony1 + harmony2 + noise
                # 应用淡入淡出效果
                envelope = 1.0
                if i < sample_rate * 0.1:  # 淡入
                    envelope = i / (sample_rate * 0.1)
                elif i > samples_count - sample_rate * 0.1:  # 淡出
                    envelope = (samples_count - i) / (sample_rate * 0.1)
                
                # 最终样本值
                sample_value = int(combined * envelope * 32767 * 0.7)  # 稍微降低音量
                note_samples.append(clamp(sample_value))
            
            all_samples.extend(note_samples)
    
    # 裁剪到指定长度
    final_samples = all_samples[:int(sample_rate * duration)]
    
    # 保存为WAV文件
    save_wave_file(file_path, final_samples, sample_rate)
    print(f"背景音乐已生成: {os.path.basename(file_path)}")

def generate_placeholder_sounds(sounds_dir):
    """生成所有需要的占位音频文件"""
    print("正在生成占位音频文件...")
    
    # 确保音频目录存在
    os.makedirs(sounds_dir, exist_ok=True)
    
    # 生成简单的"吃食物"音效 - 高音短促音调
    eat_food_samples = generate_sine_wave(800, 0.15)
    save_wave_file(os.path.join(sounds_dir, "eat_food.wav"), eat_food_samples)
    print("已生成: eat_food.wav")
    
    # 生成"游戏结束"音效 - 低沉下降音调
    game_over_samples = []
    for i in range(44100):
        freq = 400 - i * 0.5
        if freq < 200:
            freq = 200
        value = math.sin(2 * math.pi * freq * i / 44100)
        game_over_samples.append(int(value * 32767 * (1 - i / 44100)))
    save_wave_file(os.path.join(sounds_dir, "game_over.wav"), game_over_samples[:22050])
    print("已生成: game_over.wav")
    
    # 生成"菜单点击"音效 - 短促点击声
    menu_click_samples = generate_sine_wave(600, 0.07)
    save_wave_file(os.path.join(sounds_dir, "menu_click.wav"), menu_click_samples)
    print("已生成: menu_click.wav")
    
    # 生成"能力激活"音效 - 上升音调
    ability_samples = []
    for i in range(11025):  # 0.25秒
        freq = 400 + i * 0.8  # 增加频率
        value = math.sin(2 * math.pi * freq * i / 44100)
        ability_samples.append(int(value * 32767))
    save_wave_file(os.path.join(sounds_dir, "ability_activated.wav"), ability_samples)
    print("已生成: ability_activated.wav")
    
    # 生成"僵尸呻吟"音效 - 低沉噪声
    zombie_samples = []
    for i in range(22050):  # 0.5秒
        # 添加一些噪声使其听起来更"僵尸"
        value = (
            math.sin(2 * math.pi * 150 * i / 44100) * 0.7 + 
            math.sin(2 * math.pi * 153 * i / 44100) * 0.3 + 
            (2 * random.random() - 1) * 0.1  # 添加随机噪声
        )
        # 确保值在范围内
        amplitude = 32767 * (1 - i / 44100 * 0.3)  # 轻微淡出
        zombie_samples.append(int(clamp(value * amplitude)))
    save_wave_file(os.path.join(sounds_dir, "zombie_groan.wav"), zombie_samples)
    print("已生成: zombie_groan.wav")
    
    # 生成背景音乐 (30秒循环)
    generate_background_music(os.path.join(sounds_dir, "pvz_background.wav"), duration=30)
    
    print("占位音频文件生成完成！")

if __name__ == "__main__":
    # 获取当前脚本的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建音频目录路径 (相对于项目根目录)
    sounds_dir = os.path.join(os.path.dirname(current_dir), "assets", "sounds")
    
    generate_placeholder_sounds(sounds_dir) 