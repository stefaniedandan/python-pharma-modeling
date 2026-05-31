#100人的随机口服血药浓度模拟
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示为方块的问题

# 1. 基础参数设定
n_subjects = 100  # 100位受试者
t = np.linspace(0, 24, 100)  # 0 到 24 小时，取 100 个采样点
D = 100  # 剂量 100mg
V = 10  # 假设表观分布容积 10L

# 2. 生成群体参数 (使用符合逻辑的标准差，避免负数)
# ka 均值 1.2, 标准差 0.2
ka_pop = np.random.normal(1.2, 0.2, n_subjects)
# ke 均值 0.2, 标准差 0.05
ke_pop = np.random.normal(0.2, 0.05, n_subjects)
ke_pop = np.maximum(ke_pop, 0.01) # 强制让所有小于0.01的数都变成0.01(超级关键！！！！！！)
plt.figure(figsize=(10, 6))

# 3. 【核心步骤】用循环为每一个人画线
for i in range(n_subjects):
    ka = ka_pop[i]
    ke = ke_pop[i]

    # 口服一室模型公式
    # 注意：如果 ka 和 ke 极度接近，分母会趋近于0，产生报错。这里忽略极端情况。
    C = (D * ka) / (V * (ka - ke)) * (np.exp(-ke * t) - np.exp(-ka * t))

    # 绘图技巧：alpha=0.2 让线条变透明，产生“烟雾”效果
    plt.plot(t, C, color='gray', alpha=0.2)

# 4. 计算并绘制“群体平均曲线”（红色粗线,即平均值的线）
mean_ka = np.mean(ka_pop)
mean_ke = np.mean(ke_pop)
C_mean = (D * mean_ka) / (V * (mean_ka - mean_ke)) * (np.exp(-mean_ke * t) - np.exp(-mean_ka * t))
plt.plot(t, C_mean, color='red', linewidth=3, label='群体平均趋势')

# 5. 专业美化
plt.title("100位受试者的口服血药浓度模拟 (群体趋势图、ke=0.05)", fontsize=14)
plt.xlabel("时间 (h)", fontsize=12)
plt.ylabel("血药浓度 (mg/L)", fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()


#改变ke从0.05到0.1
# 1. 基础参数设定
n_subjects = 100  # 100位受试者
t = np.linspace(0, 24, 100)  # 0 到 24 小时，取 100 个采样点
D = 100  # 剂量 100mg
V = 10  # 假设表观分布容积 10L

# 2. 生成群体参数 (使用符合逻辑的标准差，避免负数)
# ka 均值 1.2, 标准差 0.2
ka_pop = np.random.normal(1.2, 0.2, n_subjects)
# ke 均值 0.2, 标准差 0.1
ke_pop = np.random.normal(0.2, 0.1, n_subjects)
ke_pop = np.maximum(ke_pop, 0.01) # 强制让所有小于0.01的数都变成0.01(超级关键！！！！！！)
plt.figure(figsize=(10, 6))

# 3. 【核心步骤】用循环为每一个人画线
for i in range(n_subjects):
    ka = ka_pop[i]
    ke = ke_pop[i]

    # 口服一室模型公式
    # 注意：如果 ka 和 ke 极度接近，分母会趋近于0，产生报错。这里忽略极端情况。
    C = (D * ka) / (V * (ka - ke)) * (np.exp(-ke * t) - np.exp(-ka * t))

    # 绘图技巧：alpha=0.2 让线条变透明，产生“烟雾”效果
    plt.plot(t, C, color='gray', alpha=0.2)

# 4. 计算并绘制“群体平均曲线”（红色粗线）
mean_ka = np.mean(ka_pop)
mean_ke = np.mean(ke_pop)
C_mean = (D * mean_ka) / (V * (mean_ka - mean_ke)) * (np.exp(-mean_ke * t) - np.exp(-mean_ka * t))
plt.plot(t, C_mean, color='green', linewidth=3, label='群体平均趋势')

# 5. 专业美化
plt.title("100位受试者的口服血药浓度模拟 (群体趋势图、ke=0.1)", fontsize=14)
plt.xlabel("时间 (h)", fontsize=12)
plt.ylabel("血药浓度 (mg/L)", fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()