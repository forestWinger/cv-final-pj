# 基于NeRF及其变体的物体重建和新视图合成

![fern](https://github.com/duolaCmengaa/5/assets/145974277/9ac8e55e-9a1d-493b-adc6-61481bd89280)

![bicycle1](https://github.com/duolaCmengaa/5/assets/145974277/d9cf1779-b3ea-408e-830a-79c922681c98)

## 文件结构说明

我们提供 3 个数据集，可在 [MineData](https://drive.google.com/drive/folders/1JcWnWqofrvRd6TWf9Ix0hpnNLA0eoJkg) 下载。每个数据集（fern、bicycle、testdata）均包含 **data** 与 **logs** 两个子文件夹：

- **data**：原始数据集  
- **logs**：训练得到的模型权重、日志以及渲染视频

以下以 fern 为例展示目录层级（其余数据集结构相同，仅文件名不同）。

### data

```text
data/
└── nerf_llff_data/
    └── fern/llfftest/
        ├── images/                 原始分辨率
        ├── images_4/               4× 下采样
        ├── images_8/               8× 下采样
        ├── sparse/0/               COLMAP 输出
        │   ├── cameras.bin
        │   ├── images.bin
        │   ├── points3D.bin
        │   └── project.ini
        ├── database.db
        ├── poses_bounds.npy
        └── view_imgs.txt           训练用图像清单
```

### logs

```text
logs/
└── fern_test/llfftest/
    ├── testset_200000/             测试集渲染
    ├── 050000.tar                  权重快照
    ├── 100000.tar
    ├── 150000.tar
    ├── 200000.tar                  迭代 200k 权重
    ├── args.txt
    ├── config.txt
    └── llfftest_spiral_200000_rgb.mp4   最终渲染视频
└── summaries/
    └── fern_test/llfftest/
        └── events.out.tfevents.*   TensorBoard 日志
```

### 项目根目录

```text
configs/                 训练参数
    ├── fern.txt
    └── llfftest.txt
data/                    三个数据集的 data 文件夹
logs/                    仅在继续训练或渲染时需要
images_8.py              8× 下采样脚本
load_*.py                各数据集读取脚本
names.py                 批量命名脚本
requirements.txt         依赖列表
run_nerf.py              训练入口
run_nerf_helpers.py      工具函数
```

---

## 训练与渲染

> **提示**：若从零开始训练，请不要在根目录放置 logs；只有在继续训练或渲染时才需要。

### 1. 从零开始训练 fern

```bash
python run_nerf.py --config configs/fern.txt
```

### 2. 继续训练（使用已有权重）

将对应 logs 复制到正确路径后，运行同一条命令即可自动从最新权重继续。如需修改总迭代步数，请在 run_nerf.py 中调整 `N_iters`。

### 3. 从零开始训练自有数据集 bicycle

```bash
python run_nerf.py --config configs/llfftest.txt --spherify --no_ndc
```
（360° 数据需加 `--spherify --no_ndc`）

### 4. 渲染环绕视频

- fern

  ```bash
  python run_nerf.py --config configs/fern.txt --render_only
  ```
  输出路径：`logs/fern_test/renderonly_path_199999/`

- 自有数据集

  ```bash
  python run_nerf.py --config configs/llfftest.txt --spherify --no_ndc --render_only
  ```
  输出路径：`logs/llfftest/renderonly_path_199999/`

### 5. 评估预留测试集

确保 testdata 的 data 与 logs 就位，并将 configs/llfftest.txt 中 `llffhold` 设为 1：

```bash
python run_nerf.py --config configs/llfftest.txt \
                   --spherify --no_ndc --render_only --render_test
```
平均 PSNR 会打印，并保存在 `logs/llfftest/renderonly_test_199999/`。

### 6. TensorBoard

```bash
tensorboard --logdir=<日志目录路径>
```

---

## 自定义数据集制作

- 安装并使用 COLMAP 与 LLFF code  
- 参考教程：<https://blog.csdn.net/qq_43575504/article/details/129357568>

生成的 data 文件夹放入项目后即可按上文流程训练。
