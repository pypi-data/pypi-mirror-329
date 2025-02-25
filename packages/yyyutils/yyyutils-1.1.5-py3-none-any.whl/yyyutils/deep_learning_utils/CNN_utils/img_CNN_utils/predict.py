import torch
import torchvision.transforms as transforms
from PIL import Image
import os
import re


def predict_single_image(model, best_model_path, img_path, resize):
    """
    单张图片预测，img_path为图片路径，resize为图片缩放尺寸
    """
    transforms_list = [transforms.Resize((resize, resize)), transforms.ToTensor()]
    if os.path.exists('./mean_std.txt'):
        with open('./mean_std.txt', 'r') as file:
            data = file.read()

        # 使用正则表达式找到均值和标准差列表的部分
        mean_match = re.search(r'mean: \[(.*?)\]', data)
        std_match = re.search(r'std: \[(.*?)\]', data)

        if mean_match and std_match:
            # 从正则表达式匹配中提取均值和标准差列表的部分
            mean_str = mean_match.group(1)
            std_str = std_match.group(1)

            # 将字符串转换为浮点数列表
            mean = [float(num) for num in mean_str.split(',')]
            std = [float(num) for num in std_str.split(',')]
            print('读取mean_std.txt文件成功！')
            print('mean:', mean)
            print('std:', std)
            transforms_list.append(transforms.Normalize(mean, std))
        else:
            raise ValueError('mean_std.txt文件格式错误！')
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.load_state_dict(torch.load(best_model_path))
    model.to(device)
    img = Image.open(img_path)
    img = transforms.Compose(transforms_list)(img)
    img = img.unsqueeze(0)
    img = img.to(device)
    with torch.no_grad():
        output = model(img)
        pre_label = torch.argmax(output, dim=1).item()
        result = pre_label.item()
    print("预测值：", result)


def predict_single(model, best_model_path, x):
    """
    单个样本预测, x为输入样本(处理过的)
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.load_state_dict(torch.load(best_model_path))
    model.to(device)
    with torch.no_grad():
        x = x.unsqueeze(0)
        output = model(x)
        pre_label = torch.argmax(output, dim=1).item()
        result = pre_label.item()
    print("预测值：", result)
