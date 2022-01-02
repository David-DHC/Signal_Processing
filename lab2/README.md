# Frequency-division-multiplexing
《信号处理原理》频分复用编程作业
## 代码说明
0. 运行方法：`python3 lab2.py`。依赖：numpy、librosa、soundfile。
1. 请不要删除任何文件夹，这会导致代码目录被破坏，代码无法运行。
2. 原始音频请参见raw文件夹，其中lyrics.md中记录了原始音频的文字内容。
3. 运行前可以删除任何encoded、output、pre_process文件夹内的音频文件。

## 实现思路

### 预处理
0. 计算C值：C = f * T，T为每帧时长，f为截断频率。原题要求f=3400Hz，但这是纯人声的f值；由于我所选的音频夹杂有音乐声，经过对比试验后，我决定提高f值以追求更好的输出结果。而根据Nyquist定理，f值不能超过采样率8000Hz的一半，所以我把f提高到了3999Hz。
1. 使用`librosa.load(filename, sr)`函数读取原始音频，注意该函数返回两个值，一个是ndarray类型的音频数据，一个是所用的采样率sr。
2. 逐帧截断：取每帧对应的切片即可。
3. 使用`librosa.resample(y, orig_sr, target_sr)`函数进行重采样，其中目标采样率是要求的8000Hz。该函数的返回值即是对y进行重采样之后得到的新的音频数据（记为data）。
4. 使用`soundfile.write(filename, data, sample_rate)`把音频导出

### Encoding
在每一帧中，都需要对四个音频做以下处理：
1. 对data进行FFT变换，得到频谱：`spectrum = np.fft.fft(data)`
2. 截断，保留频谱的前C项即可。
3. 把四段音频的频谱首尾相接（`np.append`），组成一个4C长的ndarray。注意，在使用`np.append(ndarray1, ndarray2)`进行拼接时，函数只是在返回值处返回了两个数列的拼接结果，参数里的两个ndarray都不会发生变化。

此后对该帧的处理为：

1. 将得到的长4C的ndarray复制一份，除掉这份的第一项之后再倒置（`np.flip`）、取共轭(`np.conjugate`）并append在后面，得到长度为8C-1的复数序列。
2. 对其进行逆变换（`np.fft.ifft`）
3. 实验要求我们检验虚部（`.imag`）是否为0，我们就在这里进行一下检查。
4. 构建一个新的ndarray保存其实部（`.real`）。特别需要注意，构建空的ndarray的方法，不是`array = np.ndarray()`，而是`array = np.ndarray([])`。
5. 导出音频。


### Decoding
在每一帧中，都需要对Encoding输出的音频做以下处理:
1. 读取音频，并进行FFT变换，得到8C-1项的ndarray。
2. 这些项中，前4C项分别对应到4个原始音频，每个音频C项。我们对每C项进行复制、除掉第一项、倒置、取共轭、append，得到长度为2C-1的复数序列。
3. 得到四个长度为2C-1的复数序列，它们分别对应到四个音频的同一帧。这样，把所有音频、所有帧对应的复数序列都算出来，把相同音频的按顺序拼在一起，就可以导出音频了。

## 实验思考
对比观察可以得到，帧数的改变并不会导致频分复用输出质量的改变，只有截断频率（f值）和采样率会造成影响。人声的f值对应到3400Hz左右，但是音乐声可能会高于这个值。
