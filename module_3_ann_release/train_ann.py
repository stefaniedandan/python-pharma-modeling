#读取上一步的csv数据，，生成pkl文件和散点图
# train_ann.py
# 模块三：训练人工神经网络，预测缓释片溶出行为

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
import joblib
import os

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

os.makedirs('results/figures', exist_ok=True)

# ── 1. 加载数据 ───────────────────────────────────────────────────
df = pd.read_csv('dissolution_dataset.csv')

feature_cols = ['HPMC(%)', 'MgSt(%)', 'Pressure(kN)', 'Dose(mg)']
target_cols  = [c for c in df.columns if c.startswith('R_')]
time_labels  = ['2h', '4h', '8h', '12h', '16h', '24h']

X = df[feature_cols].values
Y = df[target_cols].values

# ── 2. 划分训练集 / 测试集（8:2）─────────────────────────────────
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42
)
print(f"训练集：{X_train.shape[0]} 条，测试集：{X_test.shape[0]} 条")

# ── 3. 标准化 ────────────────────────────────────────────────────
# 神经网络对输入量纲敏感：HPMC 单位是 %，Pressure 单位是 kN，
# 不标准化的话梯度下降会偏向量纲大的方向，导致训练不稳定。
scaler_X = StandardScaler()
scaler_Y = StandardScaler()

X_train_sc = scaler_X.fit_transform(X_train)
X_test_sc  = scaler_X.transform(X_test)       # 注意：用训练集的参数变换测试集
Y_train_sc = scaler_Y.fit_transform(Y_train)
Y_test_sc  = scaler_Y.transform(Y_test)

# ── 4. 定义并训练 ANN ────────────────────────────────────────────
# 网络结构：4 输入 → [64, 64, 32] 三个隐藏层 → 6 输出
# relu 激活函数：计算快，避免梯度消失
# adam 优化器：自适应学习率，适合中小型数据集
model = MLPRegressor(
    hidden_layer_sizes=(64, 64, 32),
    activation='relu',
    solver='adam',
    max_iter=1000,
    learning_rate_init=0.001,
    random_state=42,
    verbose=False
)

model.fit(X_train_sc, Y_train_sc)
print("训练完成")

# ── 5. 评估性能 ──────────────────────────────────────────────────
Y_pred_sc = model.predict(X_test_sc)
Y_pred    = scaler_Y.inverse_transform(Y_pred_sc)

r2_overall  = r2_score(Y_test, Y_pred, multioutput='uniform_average')
mae_overall = mean_absolute_error(Y_test, Y_pred)

print(f"\n整体测试集性能：")
print(f"  R²  = {r2_overall:.4f}")
print(f"  MAE = {mae_overall:.2f}%")

print(f"\n各时间点 R²：")
for i, label in enumerate(time_labels):
    r2_i = r2_score(Y_test[:, i], Y_pred[:, i])
    print(f"  {label:>4s} : {r2_i:.4f}")

# ── 6. 保存模型 ──────────────────────────────────────────────────
joblib.dump(model,    'ann_model.pkl')
joblib.dump(scaler_X, 'scaler_X.pkl')
joblib.dump(scaler_Y, 'scaler_Y.pkl')
print("\n模型已保存（ann_model.pkl）")

# ── 7. 可视化：预测值 vs 真实值散点图 ────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(13, 8))
axes = axes.flatten()

for i, ax in enumerate(axes):
    ax.scatter(Y_test[:, i], Y_pred[:, i],
               alpha=0.5, s=20, color='steelblue', edgecolors='none')
    mn = min(Y_test[:, i].min(), Y_pred[:, i].min())
    mx = max(Y_test[:, i].max(), Y_pred[:, i].max())
    ax.plot([mn, mx], [mn, mx], 'r--', lw=1.5, label='理想预测线')
    r2_i = r2_score(Y_test[:, i], Y_pred[:, i])
    ax.set_title(f'{time_labels[i]}   R² = {r2_i:.3f}', fontsize=11)
    ax.set_xlabel('真实释放率 (%)', fontsize=9)
    ax.set_ylabel('预测释放率 (%)', fontsize=9)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

plt.suptitle('ANN 预测值 vs 真实值（各溶出时间点）', fontsize=13)
plt.tight_layout()
plt.savefig('results/figures/ann_prediction_scatter.png', dpi=150, bbox_inches='tight')
plt.show()
print("散点图已保存")