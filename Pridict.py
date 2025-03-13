import configparser
import torch
import torch.nn as nn
import pickle
import Net
import decode
import Pridict_video_data


def load_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path, encoding="utf-8")
    # 读取 [Path] 和 [Params] 两个节中的参数
    path_params = config["Path"]
    param_params = config["Params"]
    configParams = {
        "bestModuleSavePath": path_params.get("bestModuleSavePath"),
        "device": torch.device("cuda:" + param_params.get("device") if torch.cuda.is_available() else "cpu"),
        "hiddenSize": param_params.getint("hiddenSize"),
        "lr": param_params.getfloat("lr"),
        "batchSize": param_params.getint("batchSize"),
        "numWorkers": param_params.getint("numWorkers"),
        "pinmMemory": bool(param_params.getint("pinmMemory")),
        "moduleChoice": param_params.get("moduleChoice"),
        "dataSetName": param_params.get("dataSetName")
    }
    return configParams


def deploy_predict(configParams):
    device = configParams["device"]
    moduleChoice = configParams["moduleChoice"]
    dataSetName = configParams["dataSetName"]
    hiddenSize = configParams["hiddenSize"]
    # 部署时采用每次单个样本预测
    max_num_states = 1
    currentModuleSavePath = configParams["bestModuleSavePath"]

    # 加载词汇表（从 vocab_data.pkl 中读取）
    with open("/root/word_idx/vocab_data.pkl", "rb") as f:
        vocab_data = pickle.load(f)
    word2idx = vocab_data['word2idx']
    idx2word = vocab_data['idx2word']
    # 假设 idx2word 为一个列表，且 idx2word[0] 为 PAD
    wordSetNum = len(idx2word) - 1

    videoPath = "/root/zsample/train-04973.mp4"
    saveDataPath = "/root/zsample/sample"
    Pridict_video_data.Process_1(videoPath, saveDataPath)

    input, num = Pridict_video_data.Process_2(saveDataPath)

    input_num = torch.tensor([num])

    # 将该张量放入一个列表中
    input_num = [input_num]

    # 定义模型并加载预训练权重
    moduleNet = Net.moduleNet(hiddenSize, wordSetNum * max_num_states + 1, moduleChoice, device, dataSetName, True)
    moduleNet = moduleNet.to(device)
    checkpoint = torch.load(currentModuleSavePath, map_location=device)
    moduleNet.load_state_dict(checkpoint['moduleNet_state_dict'])
    moduleNet.eval()

    # 初始化解码器，使用 beam search 模式
    decoder = decode.Decode(word2idx, wordSetNum + 1, 'beam')

    # 定义 LogSoftmax 层（与训练时一致）
    logSoftMax = nn.LogSoftmax(dim=-1)

    print("开始预测，输出预测文本结果：")
    input = input.to(device)
    with torch.no_grad():
        outputs = moduleNet(input, input_num, False)
        # 假设模型输出的第一个元素 logProbs1 为主要预测输出，outputs[5] 为每个样本的时间步长度
        logProbs1 = outputs[0]
        lgt = outputs[5]
        logProbs1 = logSoftMax(logProbs1)
        # 调用解码器，返回预测文本（此处 decode 方法直接返回文本列表）
        pred_text = decoder.decode(logProbs1, lgt, batch_first=False, probs=False)

        for sample in pred_text:
            if isinstance(sample, torch.Tensor):
                flat_sample = [str(item.item()) for item in sample]  # 将每个张量元素转换为字符串
                continue
            else:
                # 否则，处理 sample 作为包含元组的列表
                flat_sample = [word for sublist in sample for word, _ in sublist]  # 只提取元组中的词语部分
            print("---------------------------------")
            prediction_text = ' '.join(flat_sample)
            print("预测文本：", prediction_text)  # 用空格连接词语
            print("---------------------------------")


if __name__ == '__main__':
    # config.ini 文件路径，根据实际情况调整
    config_path = "/root/TFNet-main/params/config.ini"
    configParams = load_config(config_path)
    deploy_predict(configParams)
