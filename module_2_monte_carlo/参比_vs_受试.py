#分组参比试剂和受试试剂模拟BE，并且改变V和T对模拟效果的影响
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示为方块的问题

# 1. 基础设置
n_per_group = 50
t = np.linspace(0, 24, 100)
V = 10
D = 100

# 2. 生成两组不同的参数
# 参比制剂 (Reference, R): 吸收较快
ka_R = np.random.normal(1.2, 0.1, n_per_group)
ke_R = np.random.normal(0.2, 0.03, n_per_group)

# 受试制剂 (Test, T): 假设吸收稍微慢一点
ka_T = np.random.normal(0.8, 0.1, n_per_group)
ke_T = np.random.normal(0.2, 0.03, n_per_group)

# 确保没有负数（用昨天学到的暴力修正法）
ka_R, ka_T = np.maximum(ka_R, 0.1), np.maximum(ka_T, 0.1)
ke_R, ke_T = np.maximum(ke_R, 0.01), np.maximum(ke_T, 0.01)

plt.figure(figsize=(10, 6))

# 3. 循环画两组人的线（用颜色区分）
for i in range(n_per_group):
    # 画 R 组：浅红色
    C_R = (D * ka_R[i]) / (V * (ka_R[i] - ke_R[i])) * (np.exp(-ke_R[i] * t) - np.exp(-ka_R[i] * t))
    plt.plot(t, C_R, color='red', alpha=0.1)

    # 画 T 组：浅蓝色
    C_T = (D * ka_T[i]) / (V * (ka_T[i] - ke_T[i])) * (np.exp(-ke_T[i] * t) - np.exp(-ka_T[i] * t))
    plt.plot(t, C_T, color='blue', alpha=0.1)

# 4. 计算并画出两组的平均线
C_R_mean = (D * np.mean(ka_R)) / (V * (np.mean(ka_R) - np.mean(ke_R))) * (
            np.exp(-np.mean(ke_R) * t) - np.exp(-np.mean(ka_R) * t))
C_T_mean = (D * np.mean(ka_T)) / (V * (np.mean(ka_T) - np.mean(ke_T))) * (
            np.exp(-np.mean(ke_T) * t) - np.exp(-np.mean(ka_T) * t))

plt.plot(t, C_R_mean, color='darkred', linewidth=3, label='参比制剂 (R) 平均曲线')
plt.plot(t, C_T_mean, color='darkblue', linewidth=3, label='受试制剂 (T) 平均曲线')

# 5. 美化
plt.title("生物等效性 (BE) 模拟对比图", fontsize=14)
plt.xlabel("时间 (h)", fontsize=12)
plt.ylabel("浓度 (mg/L)", fontsize=12)
plt.legend()
plt.grid(True, alpha=0.2)
plt.show()

#【2】改变T药，与R药的区别为V变大
# 1. 基础设置
n_per_group = 50
t = np.linspace(0, 24, 100)
V_R = 10  # 参比制剂的分布容积
V_T = 15  # 受试制剂的分布容积（单独修改这里）
D = 100

# 2. 生成两组不同的参数
# 参比制剂 (Reference, R): 吸收较快
ka_R = np.random.normal(1.2, 0.1, n_per_group)
ke_R = np.random.normal(0.2, 0.03, n_per_group)

# 受试制剂 (Test, T): 假设吸收稍微慢一点
ka_T = np.random.normal(1.2, 0.1, n_per_group)
ke_T = np.random.normal(0.2, 0.03, n_per_group)

# 确保没有负数（用昨天学到的暴力修正法）
ka_R, ka_T = np.maximum(ka_R, 0.1), np.maximum(ka_T, 0.1)
ke_R, ke_T = np.maximum(ke_R, 0.01), np.maximum(ke_T, 0.01)

plt.figure(figsize=(10, 6))

# 3. 循环画两组人的线（用颜色区分）
for i in range(n_per_group):
    # 画 R 组：浅红色
    C_R = (D * ka_R[i]) / (V_R * (ka_R[i] - ke_R[i])) * (np.exp(-ke_R[i] * t) - np.exp(-ka_R[i] * t))
    plt.plot(t, C_R, color='red', alpha=0.1)

    # 画 T 组：浅蓝色
    C_T = (D * ka_T[i]) / (V_T * (ka_T[i] - ke_T[i])) * (np.exp(-ke_T[i] * t) - np.exp(-ka_T[i] * t))
    plt.plot(t, C_T, color='blue', alpha=0.1)

# 4. 计算并画出两组的平均线
C_R_mean = (D * np.mean(ka_R)) / (V_R * (np.mean(ka_R) - np.mean(ke_R))) * (
            np.exp(-np.mean(ke_R) * t) - np.exp(-np.mean(ka_R) * t))
C_T_mean = (D * np.mean(ka_T)) / (V_T * (np.mean(ka_T) - np.mean(ke_T))) * (
            np.exp(-np.mean(ke_T) * t) - np.exp(-np.mean(ka_T) * t))

plt.plot(t, C_R_mean, color='darkred', linewidth=3, label='参比制剂 (R) 平均曲线')
plt.plot(t, C_T_mean, color='darkblue', linewidth=3, label='受试制剂 (T) 平均曲线')

# 5. 美化
plt.title("生物等效性 (BE) 模拟对比图（改T）", fontsize=14)
plt.xlabel("时间 (h)", fontsize=12)
plt.ylabel("浓度 (mg/L)", fontsize=12)
plt.legend()
plt.grid(True, alpha=0.2)
plt.show()


#【3】改变T药的V，并添加了随机性
# 1. 基础设置
n_per_group = 50
t = np.linspace(0, 24, 100)
V_R = 10  # 参比制剂的分布容积
V_T = 15  # 受试制剂的分布容积（单独修改这里）
D = 100

# 2. 生成两组不同的参数
# 参比制剂 (Reference, R): 吸收较快
ka_R = np.random.normal(1.2, 0.1, n_per_group)
ke_R = np.random.normal(0.2, 0.03, n_per_group)
V_R_pop = np.random.normal(10, 2, n_per_group)

# 受试制剂 (Test, T): 假设吸收稍微慢一点
ka_T = np.random.normal(1.2, 0.1, n_per_group)
ke_T = np.random.normal(0.2, 0.03, n_per_group)
V_T_pop = np.random.normal(15, 2, n_per_group)

# 确保没有负数（用昨天学到的暴力修正法）
ka_R, ka_T = np.maximum(ka_R, 0.1), np.maximum(ka_T, 0.1)
ke_R, ke_T = np.maximum(ke_R, 0.01), np.maximum(ke_T, 0.01)

plt.figure(figsize=(10, 6))

# 3. 循环画两组人的线（用颜色区分）
for i in range(n_per_group):
    # 画 R 组：浅红色
    C_R = (D * ka_R[i]) / (V_R * (ka_R[i] - ke_R[i])) * (np.exp(-ke_R[i] * t) - np.exp(-ka_R[i] * t))
    plt.plot(t, C_R, color='red', alpha=0.1)

    # 画 T 组：浅蓝色
    C_T = (D * ka_T[i]) / (V_T * (ka_T[i] - ke_T[i])) * (np.exp(-ke_T[i] * t) - np.exp(-ka_T[i] * t))
    plt.plot(t, C_T, color='blue', alpha=0.1)

# 4. 计算并画出两组的平均线
C_R_mean = (D * np.mean(ka_R)) / (V_R * (np.mean(ka_R) - np.mean(ke_R))) * (
            np.exp(-np.mean(ke_R) * t) - np.exp(-np.mean(ka_R) * t))
C_T_mean = (D * np.mean(ka_T)) / (V_T * (np.mean(ka_T) - np.mean(ke_T))) * (
            np.exp(-np.mean(ke_T) * t) - np.exp(-np.mean(ka_T) * t))

plt.plot(t, C_R_mean, color='darkred', linewidth=3, label='参比制剂 (R) 平均曲线')
plt.plot(t, C_T_mean, color='darkblue', linewidth=3, label='受试制剂 (T) 平均曲线')

# 5. 美化
plt.title("生物等效性 (BE) 模拟对比图（T的V变大，V具有随机性）", fontsize=14)
plt.xlabel("时间 (h)", fontsize=12)
plt.ylabel("浓度 (mg/L)", fontsize=12)
plt.legend()
plt.grid(True, alpha=0.2)
plt.show()


#【3】扩大V的影响
# 1. 基础设置
n_per_group = 50
t = np.linspace(0, 24, 100)
V_R = 10  # 参比制剂的分布容积
V_T = 15  # 受试制剂的分布容积（单独修改这里）
D = 100

# 2. 生成两组不同的参数
# 参比制剂 (Reference, R): 吸收较快
ka_R = 1.2
ke_R = 0.2
V_R_pop = np.random.normal(10, 2, n_per_group)

# 受试制剂 (Test, T): 假设吸收稍微慢一点
ka_T = 1.2
ke_T = 0.2
V_T_wild = np.random.normal(15, 8, n_per_group)
V_T_wild = np.maximum(V_T_wild, 5) # 别让容积变成负数或太小

plt.figure(figsize=(10, 6))

# 3. 循环画两组人的线（用颜色区分）
# 关键点：一定要加 [i]，把“50人的数组”变成“第 i 个人的单数”
    # 这样：单数 * (100个时间点) = 100个浓度点，这就对齐了！
for i in range(n_per_group):
    # 画 R 组：浅红色
    C_R = (D * ka_R) / (V_R_pop[i] * (ka_R - ke_R)) * (np.exp(-ke_R * t) - np.exp(-ka_R * t))
    plt.plot(t, C_R, color='red', alpha=0.1)

    # 画 T 组：浅蓝色
    C_T = (D * ka_T) / (V_T_wild[i] * (ka_T - ke_T)) * (np.exp(-ke_T * t) - np.exp(-ka_T * t))
    plt.plot(t, C_T, color='blue', alpha=0.1)

# 4. 计算并画出两组的平均线
C_R_mean = (D * np.mean(ka_R)) / (V_R_pop[i]* (np.mean(ka_R) - np.mean(ke_R))) * (
            np.exp(-np.mean(ke_R) * t) - np.exp(-np.mean(ka_R) * t))
C_T_mean = (D * np.mean(ka_T)) / (V_T_wild[i] * (np.mean(ka_T) - np.mean(ke_T))) * (
            np.exp(-np.mean(ke_T) * t) - np.exp(-np.mean(ka_T) * t))

plt.plot(t, C_R_mean, color='darkred', linewidth=3, label='参比制剂 (R) 平均曲线')
plt.plot(t, C_T_mean, color='darkblue', linewidth=3, label='受试制剂 (T) 平均曲线')

# 5. 美化
plt.title("生物等效性 (BE) 模拟对比图（增大V的影响）", fontsize=14)
plt.xlabel("时间 (h)", fontsize=12)
plt.ylabel("浓度 (mg/L)", fontsize=12)
plt.legend()
plt.grid(True, alpha=0.2)
plt.show()


#【4】扩大V的标准差
# 1. 基础设置
n_per_group = 50
t = np.linspace(0, 24, 100)
V_R = 10  # 参比制剂的分布容积
V_T = 10  # 受试制剂的分布容积（单独修改这里）
D = 100

# 2. 生成两组不同的参数
# 参比制剂 (Reference, R): 吸收较快
ka_R = 1.2
ke_R = 0.2
V_R_pop = np.random.normal(10, 1, n_per_group)

# 受试制剂 (Test, T): 假设吸收稍微慢一点
ka_T = 1.2
ke_T = 0.2
V_T_wild = np.random.normal(10, 4, n_per_group)
V_T_wild = np.maximum(V_T_wild, 6) # 别让容积变成负数或太小

plt.figure(figsize=(10, 6))

# 3. 循环画两组人的线（用颜色区分）
# 关键点：一定要加 [i]，把“50人的数组”变成“第 i 个人的单数”
    # 这样：单数 * (100个时间点) = 100个浓度点，这就对齐了！
for i in range(n_per_group):
    # 画 R 组：浅红色
    C_R = (D * ka_R) / (V_R_pop[i] * (ka_R - ke_R)) * (np.exp(-ke_R * t) - np.exp(-ka_R * t))
    plt.plot(t, C_R, color='red', alpha=0.1)

    # 画 T 组：浅蓝色
    C_T = (D * ka_T) / (V_T_wild[i] * (ka_T - ke_T)) * (np.exp(-ke_T * t) - np.exp(-ka_T * t))
    plt.plot(t, C_T, color='blue', alpha=0.1)

# 4. 计算并画出两组的平均线
C_R_mean = (D * np.mean(ka_R)) / (V_R_pop[i]* (np.mean(ka_R) - np.mean(ke_R))) * (
            np.exp(-np.mean(ke_R) * t) - np.exp(-np.mean(ka_R) * t))
C_T_mean = (D * np.mean(ka_T)) / (V_T_wild[i] * (np.mean(ka_T) - np.mean(ke_T))) * (
            np.exp(-np.mean(ke_T) * t) - np.exp(-np.mean(ka_T) * t))

plt.plot(t, C_R_mean, color='darkred', linewidth=3, label='参比制剂 (R) 平均曲线')
plt.plot(t, C_T_mean, color='darkblue', linewidth=3, label='受试制剂 (T) 平均曲线')

# 5. 美化
plt.title("生物等效性 (BE) 模拟对比图（增大V的标准差）", fontsize=14)
plt.xlabel("时间 (h)", fontsize=12)
plt.ylabel("浓度 (mg/L)", fontsize=12)
plt.legend()
plt.grid(True, alpha=0.2)
plt.show()