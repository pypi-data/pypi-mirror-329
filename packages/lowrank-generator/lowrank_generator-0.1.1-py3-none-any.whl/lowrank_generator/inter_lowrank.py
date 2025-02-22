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


class Lowrank_calculator:
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
    
    def calculate(self, img_path,model_name, data_name):
        y = range(7)
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
                back = self.extract_layer_features(input, self.model.decos[i].lowrank)
                back[back < 0] = 0
                u,s,v = np.linalg.svd(back)
                matrix[i].append(s)
            u, s, v = np.linalg.svd(org)
            matrix[6].append(s) #最后一位用来储存原始图片的奇艺值
        
        save_dir = './mats/lowrank'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        m1 = np.mean(matrix[0], axis=0)
        scio.savemat('./mats/lowrank/{}_{}_svd_m1.mat'.format(model_name,data_name), {'s': m1})
        m2 = np.mean(matrix[1], axis=0)
        scio.savemat('./mats/lowrank/{}_{}_svd_m2.mat'.format(model_name,data_name), {'s': m2})
        m3 = np.mean(matrix[2], axis=0)
        scio.savemat('./mats/lowrank/{}_{}_svd_m3.mat'.format(model_name,data_name), {'s': m3})
        m4 = np.mean(matrix[3], axis=0)
        scio.savemat('./mats/lowrank/{}_{}_svd_m4.mat'.format(model_name,data_name), {'s': m4})
        m5 = np.mean(matrix[4], axis=0)
        scio.savemat('./mats/lowrank/{}_{}_svd_m5.mat'.format(model_name,data_name), {'s': m5})
        m6 = np.mean(matrix[5], axis=0)
        scio.savemat('./mats/lowrank/{}_{}_svd_m6.mat'.format(model_name,data_name), {'s': m6})
        m7 = np.mean(matrix[6], axis=0)
        scio.savemat('./mats/lowrank/{}_{}_svd_m7.mat'.format(model_name,data_name), {'s': m7})

        std1 = np.std(matrix[0], axis=0)
        scio.savemat('./mats/lowrank/{}_{}_svd_std1.mat'.format(model_name,data_name), {'s': std1})
        std2 = np.std(matrix[1], axis=0)
        scio.savemat('./mats/lowrank/{}_{}_svd_std2.mat'.format(model_name,data_name), {'s': std2})
        std3 = np.std(matrix[2], axis=0)
        scio.savemat('./mats/lowrank/{}_{}_svd_std3.mat'.format(model_name,data_name), {'s': std3})
        std4 = np.std(matrix[3], axis=0)
        scio.savemat('./mats/lowrank/{}_{}_svd_std4.mat'.format(model_name,data_name), {'s': std4})
        std5 = np.std(matrix[4], axis=0)
        scio.savemat('./mats/lowrank/{}_{}_svd_std5.mat'.format(model_name,data_name), {'s': std5})
        std6 = np.std(matrix[5], axis=0)
        scio.savemat('./mats/lowrank/{}_{}_svd_std6.mat'.format(model_name,data_name), {'s': std6})
        std7 = np.std(matrix[6], axis=0)
        scio.savemat('./mats/lowrank/{}_{}_svd_std7.mat'.format(model_name,data_name), {'s': std7})

    def load_data(file_path, variable_name):
        mat_data = sio.loadmat(file_path)
        return mat_data[variable_name].squeeze()

    def draw_lowrank(self,model_name, data_name):
        # Load data from .mat files
        mat_data = sio.loadmat('./mats/lowrank/{}_{}_svd_m1.mat'.format(model_name,data_name))
        s0 = mat_data['s'].squeeze()
        mat_data = sio.loadmat('./mats/lowrank/{}_{}_svd_m2.mat'.format(model_name,data_name))
        s1 = mat_data['s'].squeeze()
        mat_data = sio.loadmat('./mats/lowrank/{}_{}_svd_m3.mat'.format(model_name,data_name))
        s2 = mat_data['s'].squeeze()
        mat_data = sio.loadmat('./mats/lowrank/{}_{}_svd_m4.mat'.format(model_name,data_name))
        s3 = mat_data['s'].squeeze()
        mat_data = sio.loadmat('./mats/lowrank/{}_{}_svd_m5.mat'.format(model_name,data_name))
        s4 = mat_data['s'].squeeze()
        mat_data = sio.loadmat('./mats/lowrank/{}_{}_svd_m6.mat'.format(model_name,data_name))
        s5 = mat_data['s'].squeeze()
        mat_data = sio.loadmat('./mats/lowrank/{}_{}_svd_m7.mat'.format(model_name,data_name))
        org1 = mat_data['s'].squeeze()
        #s0 = self.load_data('./mats/{}_{}_svd_m1.mat'.format(model_name,data_name), 's')
        #s1 = self.load_data('./mats/{}_{}_svd_m2.mat'.format(model_name,data_name), 's')
        #s2 = self.load_data('./mats/{}_{}_svd_m3.mat'.format(model_name,data_name), 's')
        #s3 = self.load_data('./mats/{}_{}_svd_m4.mat'.format(model_name,data_name), 's')
        #s4 = self.load_data('./mats/{}_{}_svd_m5.mat'.format(model_name,data_name), 's')
        #s5 = self.load_data('./mats/{}_{}_svd_m6.mat'.format(model_name,data_name), 's')
        #org1 = self.load_data('./mats/{}_{}_svd_m7.mat'.format(model_name,data_name), 's')

        # Create data frame for main plot
        data_main = pd.DataFrame({
            'Rank': list(range(1, len(s0) + 1)) + list(range(1, len(s1) + 1)) + list(range(1, len(s2) + 1)) +
                    list(range(1, len(s3) + 1)) + list(range(1, len(s4) + 1)) + list(range(1, len(s5) + 1)) + list(range(1, len(org1) + 1)),
            'Singular Value': list(s0) + list(s1) + list(s2) + list(s3) + list(s4) + list(s5) + list(org1),
            'Stage': ['Stage 1'] * len(s0) + ['Stage 2'] * len(s1) + ['Stage 3'] * len(s2) +
                     ['Stage 4'] * len(s3) + ['Stage 5'] * len(s4) + ['Stage 6'] * len(s5) + ['Org'] * len(org1)
        })

        # Create data frame for inset plot
        data_inset = pd.DataFrame({
            'Rank': list(range(1, len(s0) + 1)) + list(range(1, len(s1) + 1)) + list(range(1, len(s2) + 1)) + list(range(1, len(s3) + 1)),
            'Singular Value': list(s0) + list(s1) + list(s2) + list(s3),
            'Stage': ['Stage 1'] * len(s0) + ['Stage 2'] * len(s1) + ['Stage 3'] * len(s2) + ['Stage 4'] * len(s3)
        })

        # Define the colors and the correct order of the legend
        colors = ['#4daf4a', '#e41a1c', '#377eb8', '#cd79ff', '#ffd927', '#999999', '#ff7400']
        stage_order = ['Stage 1', 'Stage 2', 'Stage 3', 'Stage 4', 'Stage 5', 'Stage 6', 'Org']

        # Create the main plot using plotnine
        main_plot = (ggplot(data_main, aes(x='Rank', y='Singular Value', color='Stage')) +
                     geom_point(size=3) +
                     geom_line(size=1.5) +
                     labs(title='Low-rankness Measurement Across Stages', x='Rank', y='Singular Value') +
                     scale_x_continuous(limits=(0.5, 10.5), breaks=list(range(1, 11))) +
                     scale_y_continuous(limits=(0, 4*10**4)) +
                     scale_color_manual(values=colors, breaks=stage_order) +
                     theme(
                         figure_size=(8, 6),
                         text=element_text(size=16,family='Times New Roman'),
                         plot_title=element_text(size=20, family='Times New Roman', ha='center'),
                         panel_grid_major=element_line(color='white', size=1, linetype='--'),
                         panel_grid_minor=element_line(color='white', size=0.5, linetype=':'),
                         axis_text=element_text(size=18),
                         axis_title=element_text(size=18),
                         legend_title=element_blank(),
                         legend_text=element_text(size=16),
                         legend_position=(0.85, 0.35),
                         legend_background=element_rect(fill='white', color='grey', alpha=0.4, size=0.7),
                         legend_direction='vertical',
                         legend_box_margin=5,
                     ))

        # Create the inset plot using plotnine without legend and setting xlim
        inset_plot = (ggplot(data_inset, aes(x='Rank', y='Singular Value', color='Stage')) +
                      geom_point(size=5) +
                      geom_line(size=3) +
                      scale_x_continuous(limits=(0.5, 10.5), breaks=list(range(1, 11))) +
                      labs(title='Zoom In For Initial Four Stages') +
                      scale_color_manual(values=colors, breaks=stage_order) +
                      theme_void() +
                      theme(
                          plot_title=element_text(size=20, family='Times New Roman', ha='center'),
                          panel_grid_major=element_line(color='grey', linetype='--', size=0.5),
                          panel_grid_minor=element_line(color='grey', linetype=':', size=0.25),
                          axis_text=element_text(size=18),
                          legend_position='none'
                      ))

        # Save the plots as images
        main_plot.save("main_plot.png", dpi=400)
        inset_plot.save("inset_plot.png", dpi=400)

        # Combine the images using PIL and matplotlib
        main_img = Image.open("main_plot.png")
        inset_img = Image.open("inset_plot.png")

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.imshow(main_img, aspect='auto')
        ax.axis('off')

        # Create and position the inset plot
        left, bottom, width, height = [0.55, 0.5, 0.3, 0.3]
        ax_inset = fig.add_axes([left, bottom, width, height])
        ax_inset.imshow(inset_img, aspect='auto')
        ax_inset.axis('off')

        # Adjust y-axis to use scientific notation
        formatter = ScalarFormatter()
        formatter.set_powerlimits((0, 0))
        ax.yaxis.set_major_formatter(formatter)
        ax_inset.yaxis.set_major_formatter(formatter)

        plt.savefig("combined_plot_rpcanet_packet_test.png", dpi=400, bbox_inches='tight')
        plt.show()

