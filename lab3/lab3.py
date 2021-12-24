import numpy as npy
import matplotlib.pyplot as plt

# 时长为1秒
t = 1
# 采样率为60hz
fs = 60
t_split = npy.arange(0, t * fs)

# 1hz与25hz叠加的正弦信号
x_1hz = t_split * 1 * npy.pi * 2 / fs
x_25hz = t_split * 25 * npy.pi * 2 / fs
signal_sin_1hz = npy.sin(x_1hz)
signal_sin_25hz = npy.sin(x_25hz)
signal_sin = signal_sin_1hz + 0.25 * signal_sin_25hz

N = 17
f1 = int((10 + 22) / 2)
w1 = 2 * npy.pi * f1 / fs

# print(signal_sin)
# TODO: 补全这部分代码
# 通带边缘频率为10Hz，
# 阻带边缘频率为22Hz，
# 阻带衰减为44dB，窗内项数为17的汉宁窗函数
# 构建低通滤波器
# 函数需要返回滤波后的信号
def w():
    w_list = []
    for i in range(-8, 9):
        w_list.append(0.5 + 0.5 * npy.cos(2 * npy.pi * i / (N - 1)))
    return npy.array(w_list)

def h():
    h_list = []
    for i in range(-8, 9):
        if (i == 0):
            h_list.append(w1 / npy.pi)
        else:
            h_list.append(npy.sin(w1 * i) / (npy.pi * i))
    return npy.array(h_list)

def filter_fir(raw_input):
    return npy.convolve(raw_input, h() * w())[:60]

# TODO: 首先正向对信号滤波(此时输出信号有一定相移)
# 将输出信号反向，再次用该滤波器进行滤波
# 再将输出信号反向
# 函数需要返回零相位滤波后的信号
def filter_zero_phase(filter_fired_input):
    return npy.flip(filter_fir(npy.flip(filter_fir(filter_fired_input))))

if __name__ == "__main__":
    delay_filtered_signal = filter_fir(signal_sin)
    zero_phase_filtered_signal = filter_zero_phase(signal_sin)

    plt.plot(t_split, signal_sin, label='origin')
    plt.plot(t_split, delay_filtered_signal, label='fir')
    plt.plot(t_split, zero_phase_filtered_signal, label='zero phase')

    plt.show()
