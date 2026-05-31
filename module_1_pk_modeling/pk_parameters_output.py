#这部分是计算对应浓度的
import numpy as np

# 假设你已经计算好了 time 和浓度
time = np.arange(0, 24, 0.1)
dose = 100
ka = 0.8

# 计算不同 ke 的浓度
ke_list = [0.2, 0.3, 0.5]
conc_dict = {}
for ke in ke_list:
    conc = dose * ka / (ka - ke) * (np.exp(-ke * time) - np.exp(-ka * time))
    conc_dict[ke] = conc
import csv

# 准备数据：第一列是时间，后面每列是不同 ke 的浓度
rows = []
rows.append(["时间(小时)"] + [f"ke_{ke}" for ke in ke_list])
for i, t in enumerate(time):
    row = [t] + [conc_dict[ke][i] for ke in ke_list]
    rows.append(row)

# 写入 CSV 文件
with open('浓度对比表.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("表格已保存为 浓度对比表.csv，可以用 Excel 打开。")

#这部分是计算半衰期和AUC的
import numpy as np
import pandas as pd #pandas用于生成专业的表格

time = np.arange(0, 24, 0.1)
dose = 100
ka = 0.8

results = []
for ke in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
    # 计算浓度
    conc = dose * ka / (ka - ke) * (np.exp(-ke * time) - np.exp(-ka * time))
    # 峰值浓度和达峰时间
    cmax = np.max(conc)
    tmax = time[np.argmax(conc)]
    # 半衰期
    t_half = np.log(2) / ke
    # AUC
    auc = np.trapezoid (conc, time)
    results.append([ke, cmax, tmax, t_half, auc])

print(f"ka={ka}")
df = pd.DataFrame(results, columns=['ke', 'Cmax (mg/L)', 'tmax (h)', 't1/2 (h)', 'AUC (mg·h/L)'])
print(df.round(2))  # 保留两位小数
df.to_csv('半衰期和AUC计算结果.csv', index=False)
print("CSV文件已保存")

#数据及变化情况和昨天的不一致 再次验证
import matplotlib.pyplot as plt
# ... 你的参数
for ke in [0.2, 0.3]:
    conc = dose * ka / (ka - ke) * (np.exp(-ke * time) - np.exp(-ka * time))
    plt.plot(time, conc, label=f'ke={ke}')
plt.legend()
plt.show()

#发现昨天代码有误，并非先大后小趋势，重新跑
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

time = np.arange(0, 24, 0.1)
dose = 100

# 尝试不同的 ka 值
ka_list = [0.8, 1.2, 1.6, 2.0]
ke_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

for ka in ka_list:
    print(f"\n====== ka = {ka} ======")
    peaks = []
    for ke in ke_list:
        if ke >= ka:  # 避免分母为零或负数
            continue
        conc = dose * ka / (ka - ke) * (np.exp(-ke * time) - np.exp(-ka * time))
        cmax = np.max(conc)
        peaks.append((ke, cmax))
        print(f"ke={ke:.1f}, Cmax={cmax:.1f}")

    # 画出该 ka 下的所有曲线（可选）
    plt.figure()
    for ke in ke_list:
        if ke >= ka:
            continue
        conc = dose * ka / (ka - ke) * (np.exp(-ke * time) - np.exp(-ka * time))
        plt.plot(time, conc, label=f'ke={ke}')
    plt.xlabel('时间 (小时)')
    plt.ylabel('浓度 (mg/L)')
    plt.title(f'口服给药 固定 ka={ka}')
    plt.legend()
    plt.grid(True)
    plt.show()

#我服了 deepseek你笨笨的 昨天验证的趋势是错的 固定ka cmax应该是随ke增大逐渐减小
#用散点图验证
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

time = np.arange(0, 24, 0.1)
dose = 100
ka_list = [0.8, 1.2, 1.6, 2.0]
ke_list = np.arange(0.1, 1.0, 0.05)

plt.figure(figsize=(9, 6))

for ka in ka_list:
    ke_valid = []
    cmax_list = []
    for ke in ke_list:
        if ke >= ka:
            continue
        conc = dose * ka / (ka - ke) * (np.exp(-ke * time) - np.exp(-ka * time))
        ke_valid.append(ke)
        cmax_list.append(np.max(conc))
    plt.scatter(ke_valid, cmax_list, label=f'ka = {ka}', s=40)

plt.xlabel('消除速率常数 ke (每h)', fontsize=13)
plt.ylabel('峰值浓度 Cmax (mg/L)', fontsize=13)
plt.title('Cmax 随 ke 的变化（不同 ka，口服一室模型）', fontsize=14)
plt.legend(title='吸收速率常数', fontsize=11)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()