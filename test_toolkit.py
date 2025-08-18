#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开发者工具集测试脚本
"""

import sys
import os

def test_imports():
    """测试必要的模块导入"""
    print("🔍 测试模块导入...")
    
    # 测试标准库导入
    try:
        import json
        import time
        import datetime
        print("✅ 标准库导入成功")
    except Exception as e:
        print(f"❌ 标准库导入失败: {e}")
        return False
    
    # 测试PyQt5导入
    try:
        from PyQt5.QtWidgets import QApplication, QWidget
        from PyQt5.QtCore import Qt
        print("✅ PyQt5导入成功")
    except Exception as e:
        print(f"❌ PyQt5导入失败: {e}")
        return False
    
    # 测试本地模块导入
    try:
        # 添加当前目录到路径
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from tools.base_tool import BaseTool
        from tools.json_formatter_tool import JSONFormatterTool
        from tools.timestamp_converter_tool import TimestampConverterTool
        print("✅ 本地模块导入成功")
    except Exception as e:
        print(f"❌ 本地模块导入失败: {e}")
        return False
    
    return True


def test_json_parsing():
    """测试JSON解析功能"""
    print("\n🔍 测试JSON解析功能...")
    
    try:
        # 测试标准JSON
        import json
        test_json = '{"name": "test", "value": 123}'
        result = json.loads(test_json)
        assert result["name"] == "test"
        assert result["value"] == 123
        print("✅ 标准JSON解析成功")
        
        # 测试Python字典格式
        import ast
        test_dict = "{'name': 'test', 'value': 123}"
        result = ast.literal_eval(test_dict)
        assert result["name"] == "test"
        assert result["value"] == 123
        print("✅ Python字典解析成功")
        
    except Exception as e:
        print(f"❌ JSON解析测试失败: {e}")
        return False
    
    return True


def test_timestamp_conversion():
    """测试时间戳转换功能"""
    print("\n🔍 测试时间戳转换功能...")
    
    try:
        import time
        import datetime
        
        # 测试当前时间戳
        current_timestamp = int(time.time())
        assert isinstance(current_timestamp, int)
        assert current_timestamp > 0
        print("✅ 时间戳生成成功")
        
        # 测试时间戳转时间
        dt = datetime.datetime.fromtimestamp(current_timestamp)
        assert isinstance(dt, datetime.datetime)
        print("✅ 时间戳转时间成功")
        
        # 测试时间转时间戳
        timestamp = int(dt.timestamp())
        assert isinstance(timestamp, int)
        print("✅ 时间转时间戳成功")
        
    except Exception as e:
        print(f"❌ 时间戳转换测试失败: {e}")
        return False
    
    return True


def main():
    """主测试函数"""
    print("=" * 50)
    print("开发者工具集测试")
    print("=" * 50)
    
    # 运行各项测试
    tests = [
        test_imports,
        test_json_parsing,
        test_timestamp_conversion
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ 测试 {test.__name__} 发生异常: {e}")
            failed += 1
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print("测试结果:")
    print(f"  通过: {passed}")
    print(f"  失败: {failed}")
    print(f"  总计: {passed + failed}")
    
    if failed == 0:
        print("\n🎉 所有测试通过!")
        return True
    else:
        print("\n💥 部分测试失败!")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)