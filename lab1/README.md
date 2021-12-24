## 《信号处理原理》第一次实验报告

>   新雅92 & 计92 丁浩宸



### 一、实验需求：

-   在`square_wave`里正确实现原函数$f(t)$
-   解出$f(t)$的傅里叶级数的$a_n$和$b_n$，并在`fourier_coefficient`中加以实现
-   改变`N_fourier`的值，运行程序，输出视频



### 二、实验过程：

#### (1) 实现原函数$f(t)$

```python
def square_wave(t):
    n = int(t / math.pi)
    n0 = float(t / math.pi)

    if (n == n0):				# n和n0相等时，说明n0实际上是整数，即t能整除pi。此处需要进行特判。
        if (n == 0):
            return 1
        else:
            return 0
    else:
        if (n % 2 == 0):
            return 1
        else:
            return 0
```



#### (2) 计算原函数的傅里叶级数的$a_n$和$b_n$。

1.   $a_0=\frac 12$
2.   $a_n=\frac T2 \int_0^{\frac T2} \frac 12 \cos n\omega_0t dt=0$
3.   $b_n=\frac T2 \int_0^{\frac T2} \frac 12 \sin n\omega_0t dt=\frac{1-\cos (n\pi)}{n\pi}$，因此当$n$为奇数时$b_n=\frac{2}{n\pi}$，否则$b_n=0$。



#### (3) 将上述$a_n$和$b_n$写在代码中实现

```python
def fourier_coefficient(n):
    # 每读取一个n，计算它对应的a（或b）下标，并存入相应的index中。另一个则保持为初始值-1。
    a_index = -1
    b_index = -1

    if (n % 2 == 0):
        a_index = n / 2;
    else:
        b_index = (n + 1) / 2 
	
    # 对a、b下标的情况进行分类讨论。有了之前的下标存储方式，此处就不容易出错了。
    if (a_index == 0):
        return 0.5
    elif (a_index > 0):
        return 0
    elif (b_index % 2 == 0):
        return 0
    else:
        return float(2 / (b_index * math.pi))
```



### 三、实验结果

详见各视频。各视频录制时使用的`N_coefficient`已在视频名称中标注。