#绘制自动化测试效益折线图
import matplotlib.pyplot as plt

# 定义参数
T1 = 30  # 手动执行的耗时（小时）
T2 = 74   # 自动化测试脚本编写的耗时（小时）
T3 = 6   # 脚本维护的耗时（小时）

# 计算测试效益
N_values = range(1, 101)
benefits = [(T2 + T3) / T1 * N for N in N_values]

# 绘制曲线图
plt.figure()
plt.plot(N_values, benefits)
plt.xlabel('N')
plt.ylabel('Test Benefits')
plt.title('Change of Test Benefits with N')
plt.grid(True)
plt.show()
