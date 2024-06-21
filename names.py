import os

# 设定文件夹路径
folder_path = r'C:\Users\10317\Desktop\cv\nerf\other\nerf-pytorch-master\data\nerf_llff_data\llfftest\images'

# 获取文件夹中的所有文件名
file_names = os.listdir(folder_path)

# 对文件名进行排序，并重新命名
for file_name in file_names:
    # 提取数字部分（假设文件名格式为'数字.jpg'）
    number = int(file_name.split('.')[0])
    
    # 格式化数字部分，补全前导零（假设最大数字为999）
    new_name = f'{number:03}.jpg'
    
    # 获取完整的文件路径
    old_file_path = os.path.join(folder_path, file_name)
    new_file_path = os.path.join(folder_path, new_name)
    
    # 重命名文件
    os.rename(old_file_path, new_file_path)

print("文件重命名完成")
