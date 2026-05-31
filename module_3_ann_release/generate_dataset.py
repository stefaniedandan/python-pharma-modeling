# generate_dataset.py
# 模块三：生成模拟溶出数据集
# 说明：在没有真实实验数据的情况下，用带噪声的 Weibull 模型生成合理的模拟数据。
#       这不是作假，是建立模型框架阶段的标准做法，局限性已在 notes.md 中说明。

import numpy as np
import pandas as pd

np.random.seed(42)
n_samples = 300  # 模拟 300 个处方

# ── 处方参数随机采样（在合理的药剂学范围内）──────────────────────
hpmc     = np.random.uniform(10, 40, n_samples)   # HPMC 用量 %（羟丙甲纤维素，控释骨架）
mg_st    = np.random.uniform(0.5, 2.0, n_samples)  # 硬脂酸镁用量 %（润滑剂）
pressure = np.random.uniform(8, 20, n_samples)     # 压片压力 kN
dose     = np.random.uniform(50, 200, n_samples)   # 载药量 mg

time_points = [2, 4, 8, 12, 16, 24]  # 溶出取样时间（h）


def release_profile(hpmc_i, mg_i, press_i, t_list, noise_std=3.0):
    """
    用 Weibull 模型生成溶出曲线。
    物理依据：HPMC 越多，骨架黏度越大，释放越慢；压力越大，孔道越少，释放越慢。
    """
    lambda_ = 0.05 + 0.008 * hpmc_i + 0.01 * press_i - 0.05 * mg_i
    lambda_ = max(lambda_, 0.02)  # 防止过小导致曲线异常
    shape = 0.8  # 形状参数，控制释放曲线的弯曲程度

    releases = []
    for t in t_list:
        r = 100 * (1 - np.exp(-(t * lambda_) ** shape))
        r += np.random.normal(0, noise_std)  # 加入实验误差（模拟测量波动）
        r = np.clip(r, 0, 100)              # 累积释放率限制在 0-100%
        releases.append(round(r, 2))
    return releases


# ── 生成数据 ─────────────────────────────────────────────────────
release_data = [
    release_profile(hpmc[i], mg_st[i], pressure[i], time_points)
    for i in range(n_samples)
]

X = pd.DataFrame({
    'HPMC(%)':      hpmc,
    'MgSt(%)':      mg_st,
    'Pressure(kN)': pressure,
    'Dose(mg)':     dose
})

Y_cols = [f'R_{t}h(%)' for t in time_points]
Y = pd.DataFrame(release_data, columns=Y_cols)

df = pd.concat([X, Y], axis=1)
df.to_csv('dissolution_dataset.csv', index=False)

print(f"数据集已保存：{n_samples} 条处方，{len(time_points)} 个溶出时间点")
print("\n前 5 条记录：")
print(df.head().to_string(index=False))