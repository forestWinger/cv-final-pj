import os
import cv2

# 输入文件夹路径和输出文件夹路径
input_folder = "C:\\Users\\10317\\Desktop\\cv\\1\\bicycle1\\nerf-pytorch-master\\data\\nerf_llff_data\\llfftest\\images"
output_folder = "C:\\Users\\10317\\Desktop\\cv\\1\\bicycle1\\nerf-pytorch-master\\data\\nerf_llff_data\\llfftest\\images_8"

# 创建输出文件夹
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 获取输入文件夹中所有图片文件的列表
image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

# 循环处理每个图片文件
for i, image_file in enumerate(image_files, start=1):
    # 构建文件路径
    image_path = os.path.join(input_folder, image_file)
    if i < 10:

        output_path = os.path.join(output_folder, f"img0{i}.jpg")
    else:
        output_path = os.path.join(output_folder, f"img{i}.jpg")
    
    # 读取图像
    original_image = cv2.imread(image_path)
    
    # 检查图像是否成功读取
    if original_image is None:
        print(f"无法读取图像文件: {image_path}")
        continue
    
    # 下采样
    img_1 = original_image
    for _ in range(3):  # 下采样三次，相当于1/8
        img_1 = cv2.pyrDown(img_1)
    
    # 保存下采样后的图像
    cv2.imwrite(output_path, img_1)
    
    print(f"下采样完成: {image_file} -> {output_path}")
