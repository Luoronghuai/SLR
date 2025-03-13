import os
import imageio
import cv2
from tqdm import tqdm
import torch
from PIL import Image
from torchvision import transforms

def Process_1(videoPath, saveDataPath):
    # 解析视频文件路径
    videoFileName = os.path.basename(videoPath)
    nameString = videoFileName.split(".")[0]  # 获取文件名，不包括扩展名
    #saveImagePath = os.path.join(saveDataPath, nameString)
    saveImagePath = saveDataPath

    # 创建保存目录
    if not os.path.exists(saveImagePath):
        os.makedirs(saveImagePath)

    vid = imageio.get_reader(videoPath)  # 读取视频
    nframes = vid.count_frames()  # 获取视频帧数
    fps = vid.get_meta_data()['fps']  # 获取帧率
    videoTime = vid.get_meta_data()['duration']  # 获取视频时长
    resolution = vid.get_meta_data()['size']  # 获取视频分辨率

    print(f"视频帧数: {nframes}")
    print(f"帧率: {fps}")
    print(f"视频时长: {videoTime}秒")
    print(f"视频分辨率: {resolution}")

    # 遍历所有帧并保存为图片
    for i in tqdm(range(nframes)):
        try:
            image = vid.get_data(i)  # 获取第 i 帧
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 转换颜色格式
            image = cv2.resize(image, (256, 256))  # 调整大小

            # 格式化帧编号，确保文件名长度为5位
            nameString = str(i).zfill(5)
            imagePath = os.path.join(saveImagePath, f"{nameString}.jpg")

            # 保存图像
            cv2.imencode('.jpg', image)[1].tofile(imagePath)
        except Exception as e:
            print(f"处理帧 {i} 时出错：", e)

    vid.close()

    print(f"所有帧已经保存到 {saveImagePath}")

def Process_2(folder_path):
    # 使用transform来预处理图片
    transform = transforms.Compose([
        transforms.Resize((224, 224)),  # 调整图片大小为224x224
        transforms.ToTensor()  # 转换为张量并归一化到[0, 1]
    ])

    # 获取文件夹中的所有图片文件
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('png', 'jpg', 'jpeg'))]
    num = len(image_files)
    # 初始化一个空的列表来存储处理后的图片
    images = []

    # 读取每张图片并进行预处理
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        img = Image.open(image_path).convert('RGB')  # 打开图片并转换为RGB模式
        img_tensor = transform(img)  # 对图片应用transform
        images.append(img_tensor)  # 添加到图片列表中

    # 将图片列表堆叠成一个张量，形状为(240, 3, 224, 224)
    image_tensor = torch.stack(images)

    image_tensor = image_tensor.unsqueeze(0)
    # 检查最终的张量形状
    return image_tensor,num





if __name__ == '__main__':
    videoPath = "/root/zsample/train-04973.mp4"  # 需要处理的视频路径
    saveDataPath = "/root/zsample/sample"  # 保存图像帧的目录

    main(videoPath, saveDataPath)
    Process(saveDataPath)
