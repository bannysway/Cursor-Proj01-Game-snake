"""
简单音频生成工具
快速生成短小的测试用背景音乐
"""

import os
import wave
import struct
import math
import random

def generate_simple_background_music(file_path, duration=5):
    """生成简单的背景音乐样本（仅5秒）"""
    print(f"正在生成简单背景音乐 ({duration}秒)...")
    
    # 设置参数
    sample_rate = 22050  # 降低采样率加快处理速度
    num_samples = sample_rate * duration
    samples = []
    
    # 简单的音符频率
    frequencies = [261.63, 329.63, 392.00, 440.00]
    
    # 生成简单的音乐样本
    for i in range(num_samples):
        t = i / sample_rate
        # 使用多个频率的简单混合
        val = 0
        for idx, freq in enumerate(frequencies):
            # 每个频率使用不同的振幅和相位
            amplitude = 0.2 / (idx + 1)
            phase = idx * math.pi / 4
            val += amplitude * math.sin(2 * math.pi * freq * t + phase)
        
        # 加入轻微噪声
        noise = random.random() * 0.05 - 0.025
        val += noise
        
        # 确保值在-1到1之间
        val = max(-1, min(1, val))
        
        # 转换为16位整数
        samples.append(int(val * 32767))
    
    # 确保目录存在
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # 将样本写入WAV文件
    with wave.open(file_path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        
        # 打包样本为二进制数据
        binary_data = b''
        for sample in samples:
            binary_data += struct.pack('<h', sample)
        
        wf.writeframes(binary_data)
    
    print(f"简单背景音乐已生成: {os.path.basename(file_path)}")

if __name__ == "__main__":
    # 获取当前脚本的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建输出文件路径
    output_path = os.path.join(os.path.dirname(current_dir), "assets", "sounds", "simple_background.wav")
    
    # 生成音乐
    generate_simple_background_music(output_path) 