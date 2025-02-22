
from inter_lowrank import Lowrank_calculator

# 加载模型
Lowrank_C = Lowrank_calculator(model_name="rpcanetma9",model_path="/Users/yourname/My_mission/API/RPCANet_Code/result/20240519T07-24-39_rpcanetma9_nudt/best.pkl", use_cuda=True)

# 计算低秩，保存为.mat
lowrank = Lowrank_C.calculate(
    img_path="/Users/yourname/My_mission/API/RPCANet_Code/datasets/test",
    model_name="rpcanetma9",
    data_name="test_packet",
    save_dir= './mats/lowranks'
)

# 绘制低秩数据图 保存为.png
draw_lowrank = Lowrank_C.draw_lowrank(
    model_name="rpcanetma9",
    data_name="test_packet",
    mat_dir= './mats/lowranks',
    save_dir = './mats/lowranks/figure'
)