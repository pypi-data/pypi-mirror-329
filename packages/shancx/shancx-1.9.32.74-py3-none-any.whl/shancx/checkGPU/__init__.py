#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2024/10/17 上午午10:40
# @Author : shancx
# @File : __init__.py
# @email : shanhe12@163.com
import torch
def CheckGpuPlus(num=1):
    if torch.cuda.is_available():
        print(f"CUDA is available. Number of GPUs available: {torch.cuda.device_count()}")
        
        for i in range(torch.cuda.device_count()):
            print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
        device = torch.device(f'cuda:{num}' if torch.cuda.is_available() else 'cpu')   
        return device
    else:
        print("CUDA is not available. Using CPU.")
        return None

#pd.concat(filter(None, results))
#valid_results = [df for df in results if isinstance(df, pd.DataFrame) and not df.empty]
