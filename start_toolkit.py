#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from toolkit_main import main

if __name__ == "__main__":
    main()
"""
开发者工具集启动脚本
"""

if __name__ == "__main__":
    try:
        from toolkit_main import main
        main()
    except Exception as e:
        print(f"启动失败: {e}")
        import traceback
        traceback.print_exc()
        input("按回车键退出...")