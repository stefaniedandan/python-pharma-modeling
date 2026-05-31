#1000人的循环BE模拟
#会写for...in循环是关键！！
###自己乱写版，救命好难
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示为方块的问题

def run_be_simulation(cv_ka, cv_v, sample_size=100):
    """
    【函数功能】：模拟一次临床试验并判断是否等效
    【入口】：cv_ka (吸收变异), cv_v (分布容积变异), sample_size (受试者人数，默认100)
    """
    n_per_group = 100
    t = np.linspace(0, 24, 100)
    D = 100

    def get_lognormal_params(mean, cv):
        """辅助函数：将常规的均值和CV转化为对数正态分布的mu和sigma"""
        sigma = np.sqrt(np.log(cv ** 2 + 1))
        mu = np.log(mean) - 0.5 * sigma ** 2
        return mu, sigma

    # --- 第一步：内功逻辑 - 生成受试者参数 ---
    # 药学原理：使用对数正态分布模拟，保证参数永远为正，且符合人体生理的长尾效应 [cite: 18, 20, 22]
    # 这里我们会用到你之前掌握的 np.random.lognormal
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

    ka_list = np.random.lognormal(mean=np.log(0.5), sigma=cv_ka, size=sample_size)
    v_list = np.random.lognormal(mean=np.log(10), sigma=cv_v, size=sample_size)

    # --- 第二步：内功逻辑 - 核心计算 (AUC & Cmax) ---
    # 建立一个空篮子（局部变量），每次运行函数时都会自动清空，防止数据污染 [cite: 29]
    auc_R_list, auc_T_list = [], []
    cmax_R_list, cmax_T_list = [], []
    results_t = []  # 记录受试制剂数据
    results_r = []  # 记录参比制剂数据

    # 模拟给药并用“梯形法”计算每个人的 AUC [cite: 10, 27]
    for i in range(n_per_group):
        C_R = (D * ka_R) / (V_R_pop[i] * (ka_R - ke_R)) * (np.exp(-ke_R * t) - np.exp(-ka_R * t))
        C_T = (D * ka_T) / (V_T_pop[i] * (ka_T - ke_T)) * (np.exp(-ke_T * t) - np.exp(-ka_T * t))

    # 收集双指标
        auc_R_list.append(np.trapezoid(C_R, t))
        auc_T_list.append(np.trapezoid(C_T, t))

        cmax_R_list.append(np.max(C_R))
        cmax_T_list.append(np.max(C_T))

    # (这里会放入你之前写好的 for i in range(sample_size) 循环代码)
    # ... 计算逻辑 ...

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

    # --- 第三步：内功逻辑 - 统计判定 ---
    # 1. 对 AUC 和 Cmax 取自然对数 [cite: 17]
    # 2. 计算 T/R 的几何均值比 (GMR) 的 90% 置信区间 [cite: 15]
        log_R, log_T = np.log(auc_R), np.log(auc_T)
        diff = log_T - log_R

        mean_diff = np.mean(diff)
        se_diff = stats.sem(diff)
    # ...
        mean_diff = np.mean(diff)
        se_diff = stats.sem(diff)
        df = len(diff) - 1
        t_crit = stats.t.ppf(0.95, df)

        ci_low = np.exp(mean_diff - t_crit * se_diff)
        ci_high = np.exp(mean_diff + t_crit * se_diff)
        gmr = np.exp(mean_diff)


     # --- 第四步：出口 - 给出最终结论 ---
    # 判断 90% CI 是否完全落在 80.00% - 125.00% 之间 [cite: 15]
        if (ci_low >= 0.8) and (ci_high <= 1.25):
           return True  # 恭喜，试验通过！
        else:
           return False  # 遗憾，不通过。
    rint("=" * 40)
    print("       新药生物等效性 (BE) 评价报告")
    print("=" * 40)
    pass_auc = check_be(auc_R, auc_T, "AUC ")
    pass_cmax = check_be(cmax_R, cmax_T, "Cmax")
    print("-" * 40)

    if pass_auc and pass_cmax:
            print("🏆 最终结论：【合格】双指标均满足 80-125% 标准！可以上市！")
    else:
            print("💔 最终结论：【不合格】需重新调整制剂处方！")

###修正版本

import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示为方块的问题

def run_be_simulation(cv_ka, cv_v, sample_size=100):
    """
    【函数功能】：模拟一次临床试验并判断是否等效
    【入口】：cv_ka (T组吸收变异), cv_v (T组分布容积变异)
    """
    t = np.linspace(0, 24, 100)
    D = 100
    ke = 0.2  # 假设消除常数大家都很稳定

    def get_lognormal_params(mean, cv):
        """辅助函数：将均值和CV转化为对数正态分布的mu和sigma"""
        sigma = np.sqrt(np.log(cv ** 2 + 1))
        mu = np.log(mean) - 0.5 * sigma ** 2
        return mu, sigma

    # --- 第一步：内功逻辑 - 生成受试者参数 ---
    # 参比制剂 (R组)：假设原研药质量很稳定，CV固定为极小的 5% (0.05)
    mu_V_R, sig_V_R = get_lognormal_params(10, 0.05)
    V_R_pop = np.random.lognormal(mu_V_R, sig_V_R, sample_size)

    mu_ka_R, sig_ka_R = get_lognormal_params(1.2, 0.05)
    ka_R_pop = np.random.lognormal(mu_ka_R, sig_ka_R, sample_size)

    # 受试制剂 (T组)：使用我们从外面输入的 cv_v 和 cv_ka 来模拟咱们自己做的、可能波动的工艺
    mu_V_T, sig_V_T = get_lognormal_params(10, cv_v)
    V_T_pop = np.random.lognormal(mu_V_T, sig_V_T, sample_size)

    mu_ka_T, sig_ka_T = get_lognormal_params(1.2, cv_ka)
    ka_T_pop = np.random.lognormal(mu_ka_T, sig_ka_T, sample_size)

    # --- 第二步：内功逻辑 - 核心计算 (AUC) ---
    auc_R_list, auc_T_list = [], []

    for i in range(sample_size):
        # 注意这里：每个人用属于自己的 ka 和 V
        C_R = (D * ka_R_pop[i]) / (V_R_pop[i] * (ka_R_pop[i] - ke)) * (np.exp(-ke * t) - np.exp(-ka_R_pop[i] * t))
        C_T = (D * ka_T_pop[i]) / (V_T_pop[i] * (ka_T_pop[i] - ke)) * (np.exp(-ke * t) - np.exp(-ka_T_pop[i] * t))

        auc_R_list.append(np.trapezoid(C_R, t))
        auc_T_list.append(np.trapezoid(C_T, t))

    # --- 第三步：统计判定 (注意：这里的缩进已经退出了 for 循环！) ---
    auc_R = np.array(auc_R_list)
    auc_T = np.array(auc_T_list)

    log_R, log_T = np.log(auc_R), np.log(auc_T)
    diff = log_T - log_R

    mean_diff = np.mean(diff)
    se_diff = stats.sem(diff)
    df = len(diff) - 1
    t_crit = stats.t.ppf(0.95, df)

    ci_low = np.exp(mean_diff - t_crit * se_diff)
    ci_high = np.exp(mean_diff + t_crit * se_diff)

    # --- 第四步：出口 - 安静地返回结论 ---
    if (ci_low >= 0.8) and (ci_high <= 1.25):
        return True  # 等效
    else:
        return False  # 不等效


# ==========================================
# 下面的代码必须顶格写，不能缩进到 def 里面！
# ==========================================

# 1. 设定我们想要测试的处方变异程度（比如工艺很差，变异很大）
test_cv_ka = 0.4  # 吸收变异高达 40%
test_cv_v = 0.3  # 分布容积变异高达 30%
total_trials = 1000  # 模拟 1000 次完整的临床试验
pass_count = 0  # 建立一个记分牌，记录成功的次数

print(f"🚀 正在启动蒙特卡洛 BE 模拟 ({total_trials}次)...请稍候...")

# 2. 核心的千次外部循环
for i in range(total_trials):
    # 调用我们的“黑盒”函数，输入极端的变异参数
    is_passed = run_be_simulation(cv_ka=test_cv_ka, cv_v=test_cv_v)

    # 如果函数返回 True (等效)，记分牌就加 1
    if is_passed == True:
        pass_count += 1

# 3. 计算预测的通过率 (Power)
power = (pass_count / total_trials) * 100

# 4. 打印最终的高级汇报结果
print("\n" + "=" * 45)
print("      🧬 虚拟临床试验 (Virtual BE) 报告")
print("=" * 45)
print(f"📊 设定的处方波动: CV_ka={test_cv_ka}, CV_V={test_cv_v}")
print(f"✅ 模拟总试验次数: {total_trials} 次")
print(f"🎉 成功通过 BE 次数: {pass_count} 次")
print(f"🎯 预测新药研发成功率 (Power): {power:.1f}%")
print("=" * 45)


###样本真实化 上一次100人在实际中是难以达到的

import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示为方块的问题

def run_be_simulation(cv_ka, cv_v, sample_size=24):
    """
    【函数功能】：模拟一次临床试验并判断是否等效
    【入口】：cv_ka (T组吸收变异), cv_v (T组分布容积变异)
    """
    t = np.linspace(0, 24, 100)
    D = 24
    ke = 0.2  # 假设消除常数大家都很稳定

    def get_lognormal_params(mean, cv):
        """辅助函数：将均值和CV转化为对数正态分布的mu和sigma"""
        sigma = np.sqrt(np.log(cv ** 2 + 1))
        mu = np.log(mean) - 0.5 * sigma ** 2
        return mu, sigma

    # --- 第一步：内功逻辑 - 生成受试者参数 ---
    # 参比制剂 (R组)：假设原研药质量很稳定，CV固定为极小的 5% (0.05)
    mu_V_R, sig_V_R = get_lognormal_params(10, 0.05)
    V_R_pop = np.random.lognormal(mu_V_R, sig_V_R, sample_size)

    mu_ka_R, sig_ka_R = get_lognormal_params(1.2, 0.05)
    ka_R_pop = np.random.lognormal(mu_ka_R, sig_ka_R, sample_size)

    # 受试制剂 (T组)：使用我们从外面输入的 cv_v 和 cv_ka 来模拟咱们自己做的、可能波动的工艺
    mu_V_T, sig_V_T = get_lognormal_params(10, cv_v)
    V_T_pop = np.random.lognormal(mu_V_T, sig_V_T, sample_size)

    mu_ka_T, sig_ka_T = get_lognormal_params(1.0, cv_ka)
    ka_T_pop = np.random.lognormal(mu_ka_T, sig_ka_T, sample_size)

    # --- 第二步：内功逻辑 - 核心计算 (AUC) ---
    auc_R_list, auc_T_list = [], []

    for i in range(sample_size):
        # 注意这里：每个人用属于自己的 ka 和 V
        C_R = (D * ka_R_pop[i]) / (V_R_pop[i] * (ka_R_pop[i] - ke)) * (np.exp(-ke * t) - np.exp(-ka_R_pop[i] * t))
        C_T = (D * ka_T_pop[i]) / (V_T_pop[i] * (ka_T_pop[i] - ke)) * (np.exp(-ke * t) - np.exp(-ka_T_pop[i] * t))

        auc_R_list.append(np.trapezoid(C_R, t))
        auc_T_list.append(np.trapezoid(C_T, t))

    # --- 第三步：统计判定 (注意：这里的缩进已经退出了 for 循环！) ---
    auc_R = np.array(auc_R_list)
    auc_T = np.array(auc_T_list)

    log_R, log_T = np.log(auc_R), np.log(auc_T)
    diff = log_T - log_R

    mean_diff = np.mean(diff)
    se_diff = stats.sem(diff)
    df = len(diff) - 1
    t_crit = stats.t.ppf(0.95, df)

    ci_low = np.exp(mean_diff - t_crit * se_diff)
    ci_high = np.exp(mean_diff + t_crit * se_diff)

    # --- 第四步：出口 - 安静地返回结论 ---
    if (ci_low >= 0.8) and (ci_high <= 1.25):
        return True  # 等效
    else:
        return False  # 不等效


# ==========================================
# 下面的代码必须顶格写，不能缩进到 def 里面！
# ==========================================

# 1. 设定我们想要测试的处方变异程度（比如工艺很差，变异很大）
test_cv_ka = 0.4  # 吸收变异高达 40%
test_cv_v = 0.3  # 分布容积变异高达 30%
total_trials = 1000  # 模拟 1000 次完整的临床试验
pass_count = 0  # 建立一个记分牌，记录成功的次数

print(f"🚀 正在启动蒙特卡洛 BE 模拟 ({total_trials}次)...请稍候...")

# 2. 核心的千次外部循环
for i in range(total_trials):
    # 调用我们的“黑盒”函数，输入极端的变异参数
    is_passed = run_be_simulation(cv_ka=test_cv_ka, cv_v=test_cv_v)

    # 如果函数返回 True (等效)，记分牌就加 1
    if is_passed == True:
        pass_count += 1

# 3. 计算预测的通过率 (Power)
power = (pass_count / total_trials) * 100

# 4. 打印最终的高级汇报结果
print("\n" + "=" * 45)
print("      🧬 虚拟临床试验 (Virtual BE) 报告")
print("=" * 45)
print(f"📊 设定的处方波动: CV_ka={test_cv_ka}, CV_V={test_cv_v}")
print(f"✅ 模拟总试验次数: {total_trials} 次")
print(f"🎉 成功通过 BE 次数: {pass_count} 次")
print(f"🎯 预测新药研发成功率 (Power): {power:.1f}%")
print("=" * 45)

# Power 随样本量变化曲线
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ── 核心函数：单次BE模拟（升级版：返回详细数据）─────────────
def run_be_simulation(cv_ka, cv_v, sample_size):
    t = np.linspace(0, 24, 100)
    D = 100
    ke = 0.2

    def get_lognormal_params(mean, cv):
        sigma = np.sqrt(np.log(cv ** 2 + 1))
        mu = np.log(mean) - 0.5 * sigma ** 2
        return mu, sigma

    V_R_pop  = np.random.lognormal(*get_lognormal_params(10,  0.05), sample_size)
    ka_R_pop = np.random.lognormal(*get_lognormal_params(1.2, 0.05), sample_size)
    V_T_pop  = np.random.lognormal(*get_lognormal_params(10,  cv_v),  sample_size)
    ka_T_pop = np.random.lognormal(*get_lognormal_params(1.2, cv_ka), sample_size)

    auc_R_list, auc_T_list = [], []
    for i in range(sample_size):
        C_R = (D * ka_R_pop[i]) / (V_R_pop[i]  * (ka_R_pop[i] - ke)) * (np.exp(-ke * t) - np.exp(-ka_R_pop[i] * t))
        C_T = (D * ka_T_pop[i]) / (V_T_pop[i]  * (ka_T_pop[i] - ke)) * (np.exp(-ke * t) - np.exp(-ka_T_pop[i] * t))
        auc_R_list.append(np.trapezoid(C_R, t))
        auc_T_list.append(np.trapezoid(C_T, t))

    auc_R, auc_T = np.array(auc_R_list), np.array(auc_T_list)
    diff      = np.log(auc_T) - np.log(auc_R)
    mean_diff = np.mean(diff)
    se_diff   = stats.sem(diff)
    t_crit    = stats.t.ppf(0.95, len(diff) - 1)
    ci_low    = np.exp(mean_diff - t_crit * se_diff)
    ci_high   = np.exp(mean_diff + t_crit * se_diff)
    gmr       = np.exp(mean_diff)
    is_pass   = (ci_low >= 0.8) and (ci_high <= 1.25)

    # 返回判定结论 + 本次试验的统计细节
    return is_pass, {
        "GMR":     round(gmr * 100, 2),
        "CI_低":   round(ci_low * 100, 2),
        "CI_高":   round(ci_high * 100, 2),
        "均值差":  round(mean_diff, 4),
        "SE":      round(se_diff, 4),
    }


# ── 场景配置 ──────────────────────────────────────────────
scenarios = [
    {"label": "优质处方", "cv_ka": 0.2, "cv_v": 0.15, "color": "#2E86AB"},
    {"label": "普通处方", "cv_ka": 0.4, "cv_v": 0.30, "color": "#F4A261"},
    {"label": "劣质处方", "cv_ka": 0.6, "cv_v": 0.45, "color": "#E84855"},
]
sample_sizes = [12, 18, 24, 36, 48, 60, 80, 100, 120, 150]
total_trials = 500

# ── 蒙特卡洛主循环（同时收集CSV数据）────────────────────
print("🚀 开始模拟，请稍候...\n")

all_records = []   # ← 所有试验的逐条记录，用于导出CSV

fig, ax = plt.subplots(figsize=(10, 6))

for scenario in scenarios:
    power_list = []

    for n in sample_sizes:
        pass_count = 0

        for trial_id in range(total_trials):
            is_pass, detail = run_be_simulation(scenario["cv_ka"], scenario["cv_v"], n)
            if is_pass:
                pass_count += 1

            # 记录每一条试验数据
            all_records.append({
                "处方类型":    scenario["label"],
                "CV_ka":       scenario["cv_ka"],
                "CV_V":        scenario["cv_v"],
                "样本量":      n,
                "试验编号":    trial_id + 1,
                "GMR (%)":     detail["GMR"],
                "90% CI 低 (%)": detail["CI_低"],
                "90% CI 高 (%)": detail["CI_高"],
                "均值差 (log)": detail["均值差"],
                "SE":          detail["SE"],
                "是否通过BE":  "通过" if is_pass else "失败",
            })

        power = pass_count / total_trials * 100
        power_list.append(power)
        print(f"  {scenario['label']} | n={n:>3} → Power={power:.1f}%")

    ax.plot(sample_sizes, power_list,
            marker='o', linewidth=2.2, markersize=7,
            color=scenario["color"], label=scenario["label"])

# ── 导出 CSV ──────────────────────────────────────────────
df = pd.DataFrame(all_records)
df.to_csv("be_trial_results.csv", index=False, encoding="utf-8-sig")

# 同时打印每个场景×样本量的汇总统计
print("\n📋 汇总统计（各组平均GMR和通过率）：")
summary = (
    df.groupby(["处方类型", "样本量"])
    .agg(
        平均GMR=("GMR (%)", "mean"),
        GMR标准差=("GMR (%)", "std"),
        通过次数=("是否通过BE", lambda x: (x == "通过").sum()),
        Power预测=("是否通过BE", lambda x: f"{(x=='通过').mean()*100:.1f}%")
    )
    .round(2)
    .reset_index()
)
print(summary.to_string(index=False))
print(f"\n✅ 已保存 {len(df):,} 条记录 → be_trial_results.csv")

# ── 装饰图表 ──────────────────────────────────────────────
ax.axhline(80, color='gray', linewidth=1.2, linestyle='--', label='80% 效能目标线')
ax.axhspan(80, 100, alpha=0.05, color='green')
ax.set_xlabel('样本量（每组受试者人数）', fontsize=12)
ax.set_ylabel('BE 通过率 / Power (%)', fontsize=12)
ax.set_title('蒙特卡洛模拟：Power 随样本量的变化曲线\n（不同处方质量场景，每点模拟500次）',
             fontsize=13, fontweight='bold')
ax.set_xticks(sample_sizes)
ax.set_ylim(0, 105)
ax.legend(fontsize=10, loc='lower right', framealpha=0.85)
ax.grid(True, linestyle='--', alpha=0.4)
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.show()
