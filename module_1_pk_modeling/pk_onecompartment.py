#静脉 & 口服一室模型的曲线对比
import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 静脉注射一室模型
time_iv = np.arange(0, 24, 0.1)
concentration_iv = 200 * np.exp(-0.3 * time_iv)

# 口服一室模型
dose = 100
ka = 0.8
ke = 0.3
time_po = np.arange(0, 24, 0.1)
concentration_po = dose * ka / (ka - ke) * (np.exp(-ke * time_po) - np.exp(-ka * time_po))

# 合并绘图
plt.figure(figsize=(10, 6))
plt.plot(time_iv, concentration_iv, label='静脉注射（一室模型）', color='steelblue', linewidth=2)
plt.plot(time_po, concentration_po, label='口服给药（一室模型）', color='tomato', linewidth=2)

plt.xlabel('时间 (小时)', fontsize=13)
plt.ylabel('药物浓度 (mg/L)', fontsize=13)
plt.title('静脉注射与口服给药药代动力学曲线对比（一室模型）', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()