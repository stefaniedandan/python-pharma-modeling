#50人的一次虚拟BE模拟
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示为方块的问题

# --- 1. 基础设置 ---
n_per_group = 50
t = np.linspace(0, 24, 100)
D = 100


def get_lognormal_params(mean, cv):
    """辅助函数：将常规的均值和CV转化为对数正态分布的mu和sigma"""
    sigma = np.sqrt(np.log(cv ** 2 + 1))
    mu = np.log(mean) - 0.5 * sigma ** 2
    return mu, sigma


# --- 2. 药研级参数生成：全面使用对数正态分布防止负数 ---
ka_R = 1.2
ke_R = 0.2
# 假设R组均值为10，波动CV为20%
mu_V_R, sig_V_R = get_lognormal_params(10, 0.2)
V_R_pop = np.random.lognormal(mu_V_R, sig_V_R, n_per_group)

ka_T = 1.2
ke_T = 0.2
# 假设T组均值也是10，但质量稍差，波动CV增大到35%
mu_V_T, sig_V_T = get_lognormal_params(10, 0.35)
V_T_pop = np.random.lognormal(mu_V_T, sig_V_T, n_per_group)

# --- 3. 准备收集数据的篮子 ---
auc_R_list, auc_T_list = [], []
cmax_R_list, cmax_T_list = [], []

# --- 4. 模拟服药过程 ---
for i in range(n_per_group):
    C_R = (D * ka_R) / (V_R_pop[i] * (ka_R - ke_R)) * (np.exp(-ke_R * t) - np.exp(-ka_R * t))
    C_T = (D * ka_T) / (V_T_pop[i] * (ka_T - ke_T)) * (np.exp(-ke_T * t) - np.exp(-ka_T * t))

    # 收集双指标
    auc_R_list.append(np.trapezoid(C_R, t))
    auc_T_list.append(np.trapezoid(C_T, t))

    cmax_R_list.append(np.max(C_R))
    cmax_T_list.append(np.max(C_T))

# 转为数组
auc_R, auc_T = np.array(auc_R_list), np.array(auc_T_list)
cmax_R, cmax_T = np.array(cmax_R_list), np.array(cmax_T_list)


# --- 5. 编写“数字化药审官”函数 ---
def check_be(data_R, data_T, label):
    # --- 防弹衣 1：强制转换，确保没有 <= 0 的值 ---
    # 给数据加一个极小的“微尘” (1e-10)，防止出现 log(0)
    data_R = np.maximum(data_R, 1e-10)
    data_T = np.maximum(data_T, 1e-10)

    # --- 防弹衣 2：过滤 nan 值 ---
    # 如果数据里有 nan，说明之前的公式算崩了，我们要把它剔除
    mask = ~np.isnan(data_R) & ~np.isnan(data_T)
    clean_R = data_R[mask]
    clean_T = data_T[mask]

    # 现在可以放心地取对数了
    log_R, log_T = np.log(clean_R), np.log(clean_T)
    diff = log_T - log_R

    # ... 后面的统计逻辑保持不变 ...
    mean_diff = np.mean(diff)
    se_diff = stats.sem(diff)
    # ...
    mean_diff = np.mean(diff)
    se_diff = stats.sem(diff)
    df = len(diff) - 1
    t_crit = stats.t.ppf(0.95, df)

    ci_low = np.exp(mean_diff - t_crit * se_diff) * 100
    ci_high = np.exp(mean_diff + t_crit * se_diff) * 100
    gmr = np.exp(mean_diff) * 100

    is_pass = (ci_low >= 80) and (ci_high <= 125)

    print(f"[{label}] GMR: {gmr:.2f}% | 90% CI: [{ci_low:.2f}%, {ci_high:.2f}%] -> {'✅通过' if is_pass else '❌失败'}")
    return is_pass


# --- 6. 终极宣判 ---
print("=" * 40)
print("       新药生物等效性 (BE) 评价报告")
print("=" * 40)
pass_auc = check_be(auc_R, auc_T, "AUC ")
pass_cmax = check_be(cmax_R, cmax_T, "Cmax")
print("-" * 40)

if pass_auc and pass_cmax:
    print("🏆 最终结论：【合格】双指标均满足 80-125% 标准！可以上市！")
else:
    print("💔 最终结论：【不合格】需重新调整制剂处方！")


#探索把kaT改大，发现AUC和Cmax不再以相同幅度变化
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示为方块的问题

# --- 1. 基础设置 ---
n_per_group = 50
t = np.linspace(0, 24, 100)
D = 100


def get_lognormal_params(mean, cv):
    """辅助函数：将常规的均值和CV转化为对数正态分布的mu和sigma"""
    sigma = np.sqrt(np.log(cv ** 2 + 1))
    mu = np.log(mean) - 0.5 * sigma ** 2
    return mu, sigma


# --- 2. 药研级参数生成：全面使用对数正态分布防止负数 ---
ka_R = 0.5
ke_R = 0.2
# 假设R组均值为10，波动CV为20%
mu_V_R, sig_V_R = get_lognormal_params(10, 0.2)
V_R_pop = np.random.lognormal(mu_V_R, sig_V_R, n_per_group)

ka_T = 1.2
ke_T = 0.2
# 假设T组均值也是10，但质量稍差，波动CV增大到35%
mu_V_T, sig_V_T = get_lognormal_params(10, 0.35)
V_T_pop = np.random.lognormal(mu_V_T, sig_V_T, n_per_group)

# --- 3. 准备收集数据的篮子 ---
auc_R_list, auc_T_list = [], []
cmax_R_list, cmax_T_list = [], []

# --- 4. 模拟服药过程 ---
for i in range(n_per_group):
    C_R = (D * ka_R) / (V_R_pop[i] * (ka_R - ke_R)) * (np.exp(-ke_R * t) - np.exp(-ka_R * t))
    C_T = (D * ka_T) / (V_T_pop[i] * (ka_T - ke_T)) * (np.exp(-ke_T * t) - np.exp(-ka_T * t))

    # 收集双指标
    auc_R_list.append(np.trapezoid(C_R, t))
    auc_T_list.append(np.trapezoid(C_T, t))

    cmax_R_list.append(np.max(C_R))
    cmax_T_list.append(np.max(C_T))

# 转为数组
auc_R, auc_T = np.array(auc_R_list), np.array(auc_T_list)
cmax_R, cmax_T = np.array(cmax_R_list), np.array(cmax_T_list)


# --- 5. 编写“数字化药审官”函数 ---
def check_be(data_R, data_T, label):
    # --- 防弹衣 1：强制转换，确保没有 <= 0 的值 ---
    # 给数据加一个极小的“微尘” (1e-10)，防止出现 log(0)
    data_R = np.maximum(data_R, 1e-10)
    data_T = np.maximum(data_T, 1e-10)

    # --- 防弹衣 2：过滤 nan 值 ---
    # 如果数据里有 nan，说明之前的公式算崩了，我们要把它剔除
    mask = ~np.isnan(data_R) & ~np.isnan(data_T)
    clean_R = data_R[mask]
    clean_T = data_T[mask]

    # 现在可以放心地取对数了
    log_R, log_T = np.log(clean_R), np.log(clean_T)
    diff = log_T - log_R

    # ... 后面的统计逻辑保持不变 ...
    mean_diff = np.mean(diff)
    se_diff = stats.sem(diff)
    # ...
    mean_diff = np.mean(diff)
    se_diff = stats.sem(diff)
    df = len(diff) - 1
    t_crit = stats.t.ppf(0.95, df)

    ci_low = np.exp(mean_diff - t_crit * se_diff) * 100
    ci_high = np.exp(mean_diff + t_crit * se_diff) * 100
    gmr = np.exp(mean_diff) * 100

    is_pass = (ci_low >= 80) and (ci_high <= 125)

    print(f"[{label}] GMR: {gmr:.2f}% | 90% CI: [{ci_low:.2f}%, {ci_high:.2f}%] -> {'✅通过' if is_pass else '❌失败'}")
    return is_pass


# --- 6. 终极宣判 ---
print("=" * 40)
print("       新药生物等效性 (BE) 评价报告")
print("=" * 40)
pass_auc = check_be(auc_R, auc_T, "AUC ")
pass_cmax = check_be(cmax_R, cmax_T, "Cmax")
print("-" * 40)

if pass_auc and pass_cmax:
    print("🏆 最终结论：【合格】双指标均满足 80-125% 标准！可以上市！")
else:
    print("💔 最终结论：【不合格】需重新调整制剂处方！")


#绘图！！
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ── 参数设置 ──────────────────────────────────────────────
np.random.seed(42)
n_per_group = 50
t = np.linspace(0, 24, 100)
D = 100

def get_lognormal_params(mean, cv):
    sigma = np.sqrt(np.log(cv ** 2 + 1))
    mu = np.log(mean) - 0.5 * sigma ** 2
    return mu, sigma

def simulate_and_calc(ka_R, ke_R, ka_T, ke_T, cv_R=0.2, cv_T=0.35):
    """模拟50人数据，返回 AUC 和 Cmax 的 GMR、CI"""
    mu_V_R, sig_V_R = get_lognormal_params(10, cv_R)
    mu_V_T, sig_V_T = get_lognormal_params(10, cv_T)
    V_R_pop = np.random.lognormal(mu_V_R, sig_V_R, n_per_group)
    V_T_pop = np.random.lognormal(mu_V_T, sig_V_T, n_per_group)

    auc_R, auc_T, cmax_R, cmax_T = [], [], [], []
    for i in range(n_per_group):
        C_R = (D * ka_R) / (V_R_pop[i] * (ka_R - ke_R)) * (np.exp(-ke_R * t) - np.exp(-ka_R * t))
        C_T = (D * ka_T) / (V_T_pop[i] * (ka_T - ke_T)) * (np.exp(-ke_T * t) - np.exp(-ka_T * t))
        auc_R.append(np.trapezoid(C_R, t))
        auc_T.append(np.trapezoid(C_T, t))
        cmax_R.append(np.max(C_R))
        cmax_T.append(np.max(C_T))

    def calc_ci(r, t_):
        r, t_ = np.maximum(r, 1e-10), np.maximum(t_, 1e-10)
        diff = np.log(t_) - np.log(r)
        mean_diff = np.mean(diff)
        se = stats.sem(diff)
        t_crit = stats.t.ppf(0.95, len(diff) - 1)
        gmr = np.exp(mean_diff) * 100
        ci_lo = np.exp(mean_diff - t_crit * se) * 100
        ci_hi = np.exp(mean_diff + t_crit * se) * 100
        return gmr, ci_lo, ci_hi

    auc_res  = calc_ci(np.array(auc_R),  np.array(auc_T))
    cmax_res = calc_ci(np.array(cmax_R), np.array(cmax_T))
    return auc_res, cmax_res

# ── 两种场景 ──────────────────────────────────────────────
scenarios = [
    {"label": "场景一\nka_R=1.2, ka_T=1.2", "ka_R": 1.2, "ke_R": 0.2, "ka_T": 1.2, "ke_T": 0.2},
    {"label": "场景二\nka_R=0.5, ka_T=1.2", "ka_R": 0.5, "ke_R": 0.2, "ka_T": 1.2, "ke_T": 0.2},
]

results = []
for s in scenarios:
    auc_res, cmax_res = simulate_and_calc(s["ka_R"], s["ke_R"], s["ka_T"], s["ke_T"])
    results.append({"label": s["label"], "AUC": auc_res, "Cmax": cmax_res})

# ── 绘制森林图 ────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))

metrics   = ["AUC", "Cmax"]
colors    = {"AUC": "#2E86AB", "Cmax": "#E84855"}
y_ticks, y_labels = [], []

row = 0
for i, res in enumerate(results):
    for j, metric in enumerate(metrics):
        gmr, lo, hi = res[metric]
        y = -(row)                          # 从上往下排列
        is_pass = (lo >= 80) and (hi <= 125)
        color = colors[metric]
        marker = "D" if is_pass else "X"

        # 水平 CI 线
        ax.plot([lo, hi], [y, y], color=color, linewidth=2, solid_capstyle='round')
        # GMR 点
        ax.scatter(gmr, y, color=color, s=80, zorder=5, marker=marker)
        # 数值标注
        ax.text(hi + 0.8, y, f"{gmr:.1f}% [{lo:.1f}%, {hi:.1f}%]",
                va='center', fontsize=9, color='#333333')

        label = f"{res['label']}  —  {metric}"
        y_ticks.append(y)
        y_labels.append(label)
        row += 1

    # 场景间加空行
    row += 0.6

# ── 参考线和边界线 ────────────────────────────────────────
y_min, y_max = -(row - 1) - 0.8, 0.8
ax.axvline(100, color='black',   linewidth=1.2, linestyle='-',  label='GMR = 100%')
ax.axvline(80,  color='#E05C00', linewidth=1.2, linestyle='--', label='80% 下限')
ax.axvline(125, color='#E05C00', linewidth=1.2, linestyle='--', label='125% 上限')
ax.axvspan(80, 125, alpha=0.07, color='green', label='等效区间')

# ── 图例图标说明 ──────────────────────────────────────────
ax.scatter([], [], marker='D', color='gray', label='通过 ✅', s=60)
ax.scatter([], [], marker='X', color='gray', label='未通过 ❌', s=60)

ax.set_yticks(y_ticks)
ax.set_yticklabels(y_labels, fontsize=10)
ax.set_xlabel('GMR 及 90% 置信区间 (%)', fontsize=12)
ax.set_title('生物等效性森林图：AUC 与 Cmax 的 GMR 及 90% CI', fontsize=13, fontweight='bold')
ax.set_xlim(60, 175)
ax.set_ylim(y_min, y_max)
ax.legend(loc='lower right', fontsize=9, framealpha=0.8)
ax.grid(axis='x', linestyle='--', alpha=0.4)
ax.spines[['top', 'right']].set_visible(False)

plt.tight_layout()
plt.show()