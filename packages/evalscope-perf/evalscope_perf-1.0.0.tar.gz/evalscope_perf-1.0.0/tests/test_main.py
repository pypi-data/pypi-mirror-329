import pytest
from evalscope_perf.main import parse_output, setup_chinese_font
import matplotlib.pyplot as plt
import os

def test_parse_output():
    # 测试样例输出
    sample_output = """
    Average QPS: 10.5
    Average latency: 0.095
    Throughput(average output tokens per second): 150.75
    """
    metrics = parse_output(sample_output)
    
    assert metrics['Average QPS'] == 10.5
    assert metrics['Average latency'] == 0.095
    assert metrics['Throughput'] == 150.75

def test_parse_output_empty():
    # 测试空输出
    empty_output = ""
    metrics = parse_output(empty_output)
    
    assert len(metrics) == 0

def test_setup_chinese_font():
    # 测试中文字体设置
    setup_chinese_font()
    
    # 验证字体设置是否成功
    assert 'Hiragino Sans GB' in plt.rcParams['font.family']
    assert plt.rcParams['axes.unicode_minus'] is False

def test_font_file_exists():
    # 测试字体文件是否存在
    font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fonts', 'Hiragino Sans GB.ttc')
    assert os.path.exists(font_path), "字体文件不存在"
