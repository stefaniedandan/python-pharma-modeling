#分别固定ka、改变ke；固定ke、改变ka
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示为方块的问题
import numpy as np

#口服一室模型公式
dose = 100
ka = 0.8
ke = 0.3
time = np.arange(start= 0, stop=24, step=0.1)
concentration = dose * ka / (ka - ke ) * (np.exp(-ke * time) - np.exp(-ka * time))

# 分别计算不同 ka 下的浓度
ka1 = 0.5
conc1 = dose * ka1 / (ka1 - ke) * (np.exp(-ke * time) - np.exp(-ka1 * time))

ka2 = 0.8
conc2 = dose * ka2 / (ka2 - ke) * (np.exp(-ke * time) - np.exp(-ka2 * time))

ka3 = 1.2
conc3 = dose * ka3 / (ka3 - ke) * (np.exp(-ke * time) - np.exp(-ka3 * time))
#绘图
plt.plot(time, concentration)
plt.plot(time, conc1, label='ka=0.5')
plt.plot(time, conc2, label='ka=0.8')
plt.plot(time, conc3, label='ka=1.2')
plt.xlabel('时间（小时）')
plt.ylabel('浓度（mg/L）')
plt.title('口服给药 固定ke=0.3')
plt.legend()
plt.grid(True)
plt.show()

# 分别计算不同 ke 下的浓度
ke1 = 0.1
conc4 = dose * ka / (ka - ke1) * (np.exp(-ke1 * time) - np.exp(-ka * time))

ke2 = 0.2
conc5 = dose * ka / (ka - ke2) * (np.exp(-ke2 * time) - np.exp(-ka * time))

ke3 = 0.3
conc6 = dose * ka / (ka - ke3) * (np.exp(-ke3 * time) - np.exp(-ka * time))

ke4 = 0.4
conc7 = dose * ka / (ka - ke4) * (np.exp(-ke4 * time) - np.exp(-ka * time))

ke5 = 0.5
conc8 = dose * ka / (ka - ke5) * (np.exp(-ke5 * time) - np.exp(-ka * time))

ke6 = 0.6
conc9 = dose * ka / (ka - ke6) * (np.exp(-ke6 * time) - np.exp(-ka * time))

ke7 = 0.7
conc10 = dose * ka / (ka - ke7) * (np.exp(-ke7 * time) - np.exp(-ka * time))

#绘图
plt.plot(time, concentration)
plt.plot(time, conc4, label='ke=0.1')
plt.plot(time, conc5, label='ke=0.2')
plt.plot(time, conc6, label='ke=0.3')
plt.plot(time, conc7, label='ke=0.4')
plt.plot(time, conc8, label='ke=0.5')
plt.plot(time, conc9, label='ke=0.6')
plt.plot(time, conc10, label='ke=0.7')
plt.xlabel('时间（小时）')
plt.ylabel('浓度（mg/L）')
plt.title('口服给药 固定ka=0.8')
plt.xticks(np.arange(0, 25, 2))   # 显示 0,2,4,...,24
plt.legend()
plt.grid(True)
plt.show()

# 4.21发现问题重新推 分别计算不同 ke 下的浓度（当ka为1.2）
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示为方块的问题
import numpy as np

#口服一室模型公式
dose = 100
ka = 1.2
ke = 0.3
time = np.arange(start= 0, stop=24, step=0.1)
concentration = dose * ka / (ka - ke ) * (np.exp(-ke * time) - np.exp(-ka * time))

ke1 = 0.1
conc4 = dose * ka / (ka - ke1) * (np.exp(-ke1 * time) - np.exp(-ka * time))

ke2 = 0.2
conc5 = dose * ka / (ka - ke2) * (np.exp(-ke2 * time) - np.exp(-ka * time))

ke3 = 0.3
conc6 = dose * ka / (ka - ke3) * (np.exp(-ke3 * time) - np.exp(-ka * time))

ke4 = 0.4
conc7 = dose * ka / (ka - ke4) * (np.exp(-ke4 * time) - np.exp(-ka * time))

ke5 = 0.5
conc8 = dose * ka / (ka - ke5) * (np.exp(-ke5 * time) - np.exp(-ka * time))

ke6 = 0.6
conc9 = dose * ka / (ka - ke6) * (np.exp(-ke6 * time) - np.exp(-ka * time))

ke7 = 0.7
conc10 = dose * ka / (ka - ke7) * (np.exp(-ke7 * time) - np.exp(-ka * time))

#绘图
plt.plot(time, concentration)
plt.plot(time, conc4, label='ke=0.1')
plt.plot(time, conc5, label='ke=0.2')
plt.plot(time, conc6, label='ke=0.3')
plt.plot(time, conc7, label='ke=0.4')
plt.plot(time, conc8, label='ke=0.5')
plt.plot(time, conc9, label='ke=0.6')
plt.plot(time, conc10, label='ke=0.7')
plt.xlabel('时间（小时）')
plt.ylabel('浓度（mg/L）')
plt.title('口服给药 固定ka=1.2')
plt.xticks(np.arange(0, 25, 2))   # 显示 0,2,4,...,24
plt.legend()
plt.grid(True)
plt.show()

# 4.21发现问题重新推 分别计算不同 ke 下的浓度（当ka为1.5）
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示为方块的问题
import numpy as np

#口服一室模型公式
dose = 100
ka = 1.5
ke = 0.3
time = np.arange(start= 0, stop=24, step=0.1)
concentration = dose * ka / (ka - ke ) * (np.exp(-ke * time) - np.exp(-ka * time))
print(f"当前 ka = {ka}")

ke1 = 0.1
conc4 = dose * ka / (ka - ke1) * (np.exp(-ke1 * time) - np.exp(-ka * time))

ke2 = 0.2
conc5 = dose * ka / (ka - ke2) * (np.exp(-ke2 * time) - np.exp(-ka * time))

ke3 = 0.3
conc6 = dose * ka / (ka - ke3) * (np.exp(-ke3 * time) - np.exp(-ka * time))

ke4 = 0.4
conc7 = dose * ka / (ka - ke4) * (np.exp(-ke4 * time) - np.exp(-ka * time))

ke5 = 0.5
conc8 = dose * ka / (ka - ke5) * (np.exp(-ke5 * time) - np.exp(-ka * time))

ke6 = 0.6
conc9 = dose * ka / (ka - ke6) * (np.exp(-ke6 * time) - np.exp(-ka * time))

ke7 = 0.7
conc10 = dose * ka / (ka - ke7) * (np.exp(-ke7 * time) - np.exp(-ka * time))

#绘图
plt.plot(time, concentration)
plt.plot(time, conc4, label='ke=0.1')
plt.plot(time, conc5, label='ke=0.2')
plt.plot(time, conc6, label='ke=0.3')
plt.plot(time, conc7, label='ke=0.4')
plt.plot(time, conc8, label='ke=0.5')
plt.plot(time, conc9, label='ke=0.6')
plt.plot(time, conc10, label='ke=0.7')
plt.xlabel('时间（小时）')
plt.ylabel('浓度（mg/L）')
plt.title('口服给药 固定ka=1.5')
plt.xticks(np.arange(0, 25, 2))   # 显示 0,2,4,...,24
plt.legend()
plt.grid(True)
plt.show()