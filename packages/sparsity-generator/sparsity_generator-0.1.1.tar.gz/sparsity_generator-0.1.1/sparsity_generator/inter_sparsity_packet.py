import torch
import torch.nn as nn
import numpy as np
import scipy.io as scio
import cv2
import matplotlib.pyplot as plt
from torch.autograd import Variable
from export import get_model  # 确保 models.py 存在
import os.path as osp
import os
import glob

import pandas as pd
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from plotnine import *
from PIL import Image
import statistics

class LayerActivations:
    """ 用于提取特定层的特征图 """
    def __init__(self, model, layer_num=None):
        if layer_num is not None:
            self.hook = model[layer_num].register_forward_hook(self.hook_fn)
        else:
            self.hook = model.register_forward_hook(self.hook_fn)
        self.features = None

    def hook_fn(self, module, input, output):
        self.features = output[0].cpu()

    def remove(self):
        self.hook.remove()


class Sparsity_calculator:
    def __init__(self, model_name,model_path, use_cuda=True):
        """
        初始化热力图生成器

        :param model_path: 预训练模型路径 (.pth)
        :param use_cuda: 是否使用 GPU 计算
        """
        self.device = torch.device("cuda" if use_cuda and torch.cuda.is_available() else "cpu")
        self.model = self.load_model(model_name,model_path)

    def load_model(self, model_name ,model_path):
        """
        加载模型

        :param model_path: 预训练模型路径
        :return: 加载的 PyTorch 模型
        """
        print(f"Loading model from {model_path}...")
        net = get_model(model_name)  # 你可以更改模型架构
        checkpoint = torch.load(model_path, map_location=self.device)
        net.load_state_dict(checkpoint)
        net.to(self.device)
        net.eval()
        print("Model loaded successfully!")
        return net

    def preprocess_image(self, img_path):
        """
        预处理输入图像

        :param img_path: 输入图像路径
        :return: 预处理后的 PyTorch Tensor
        """
        img = cv2.resize(cv2.imread(osp.join(img_path), 0), (256, 256)).astype(int)
        org = img.reshape((1, 1, 256, 256))

        img = np.float32(cv2.resize(img, (256, 256))) / 255.
        tmp = img.reshape((1, 1, 256, 256))
        input = torch.from_numpy(tmp)
        return input, org

    def extract_layer_features(self, input_tensor, layer):
        """
        通过 LayerActivations 提取指定层的特征图

        :param input_tensor: 预处理后的图像 Tensor
        :param layer: 需要提取的模型层
        :return: 该层的输出特征图
        """
        activation_extractor = LayerActivations(layer)
        with torch.no_grad():
            _ = self.model(input_tensor)  # 进行前向传播
        activation_extractor.remove()
        return activation_extractor.features.numpy().squeeze()  # 转换为 numpy 格式
    
    def calculate(self, img_path,model_name, data_name, save_dir):
        y = range(6)
        matrix = [[] for _ in y]
        path = osp.join(img_path,f"*.png")
        f = glob.iglob(path)
        print(f)
        
        for png in f:
            print(png)
            input, org = self.preprocess_image(png)
            # backs, bh, bc, sparses, merges = [], [], [], [], []
            backs, sparses, merges = [], [], []
            for i in range(6):
                # back, bh, bc, = mid_rst(net, net.decos[i].lowrank, input)
                sparsity = self.extract_layer_features(input, self.model.decos[i].sparse)
                sparsity[sparsity < 0] = 0
                l0_norms = np.sum(sparsity != 0)/ (256*256)
                matrix[i].append(l0_norms)
            

        m1 = statistics.mean(matrix[0])
        m2 = statistics.mean(matrix[1])
        m3 = statistics.mean(matrix[2])
        m4 = statistics.mean(matrix[3])
        m5 = statistics.mean(matrix[4])
        m6 = statistics.mean(matrix[5])

        std_1 = statistics.stdev(matrix[0])
        std_2 = statistics.stdev(matrix[1])
        std_3 = statistics.stdev(matrix[2])
        std_4 = statistics.stdev(matrix[3])
        std_5 = statistics.stdev(matrix[4])
        std_6 = statistics.stdev(matrix[5])
        
        print(m1)
        print(m2)
        print(m3)
        print(m4)
        print(m5)
        print(m6)
        print('----------')

        print(std_1)
        print(std_2)
        print(std_3)
        print(std_4)
        print(std_5)
        print(std_6)

        save_dir = save_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        scio.savemat('{}/{}_{}_svd_m1.mat'.format(save_dir,model_name,data_name), {'sparsity': m1})
        scio.savemat('{}/{}_{}_svd_m2.mat'.format(save_dir,model_name,data_name), {'sparsity': m2})
        scio.savemat('{}/{}_{}_svd_m3.mat'.format(save_dir,model_name,data_name), {'sparsity': m3})
        scio.savemat('{}/{}_{}_svd_m4.mat'.format(save_dir,model_name,data_name), {'sparsity': m4})
        scio.savemat('{}/{}_{}_svd_m5.mat'.format(save_dir,model_name,data_name), {'sparsity': m5})
        scio.savemat('{}/{}_{}_svd_m6.mat'.format(save_dir,model_name,data_name), {'sparsity': m6})
#
        scio.savemat('{}/{}_{}_svd_std1.mat'.format(save_dir,model_name,data_name), {'sparsity': std_1})
        scio.savemat('{}/{}_{}_svd_std2.mat'.format(save_dir,model_name,data_name), {'sparsity': std_2})
        scio.savemat('{}/{}_{}_svd_std3.mat'.format(save_dir,model_name,data_name), {'sparsity': std_3})
        scio.savemat('{}/{}_{}_svd_std4.mat'.format(save_dir,model_name,data_name), {'sparsity': std_4})
        scio.savemat('{}/{}_{}_svd_std5.mat'.format(save_dir,model_name,data_name), {'sparsity': std_5})
        scio.savemat('{}/{}_{}_svd_std6.mat'.format(save_dir,model_name,data_name), {'sparsity': std_6})
   

    