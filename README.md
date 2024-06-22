# 基于NeRF的物体重建和新视图合成

基本要求：

（1） 选取身边的物体拍摄多角度图片/视频，并使用COLMAP估计相机参数，随后使用现成的框架进行训练；

（2） 基于训练好的NeRF渲染环绕物体的视频，并在预留的测试图片上评价定量结果。

本项目是基于NeRF官方[NeRF](http://www.matthewtancik.com/nerf)和开源代码:[NeRF-pytorch](https://github.com/yenchenlin/nerf-pytorch)来实现的

我们渲染了两个数据集，一个是NeRF官方提供的数据集，另外一个是我们自己拍摄的共享单车的照片。以下是我们基于训练好的NeRF渲染环绕物体的视频，示例如下

![fern](https://github.com/duolaCmengaa/5/assets/145974277/9ac8e55e-9a1d-493b-adc6-61481bd89280)

![bicycle1](https://github.com/duolaCmengaa/5/assets/145974277/d9cf1779-b3ea-408e-830a-79c922681c98)



## 准备
首先下载好本仓库的所有文件

```
git clone https://github.com/duolaCmengaa/5.git
cd 5
pip install -r requirements.txt
```

<details>
  <summary> Dependencies (click to expand) </summary>
  
  ## Dependencies
  - PyTorch 1.4
  - matplotlib
  - numpy
  - imageio
  - imageio-ffmpeg
  - configargparse
  
The LLFF data loader requires ImageMagick.




</details>



### 文件存放路径
我们提供了三个数据集，数据集可以前往[MineData](https://drive.google.com/drive/folders/1JcWnWqofrvRd6TWf9Ix0hpnNLA0eoJkg)下载，其中还保存了训练好的模型权重和渲染的视频，fern和bicycle文件夹里存放了logs和data文件夹，testdata文件夹里只有data文件，各个文件夹里所要用到的文件如下所示

#### data

```
                                                                                      
├── data                                                                                                                                                                                               
│   ├── nerf_llff_data                                                                                                  
│   │   └── fern/llfftest                                                                                                                             
│   │   │   └──images   
│   │   │   │   └──img01.jpg
│   │   │   │   └──img02.jpg
│   │   │   │   └── ...
│   │   │   └──images_4 "四倍下采样"
│   │   │   │   └──img01.jpg
│   │   │   │   └──img02.jpg
│   │   │   │   └── ...
│   │   │   └──images_8 "八倍下采样"
│   │   │   │   └──img01.jpg
│   │   │   │   └──img02.jpg
│   │   │   │   └── ...
│   │   │   └──sparse
│   │   │   │   └──0
│   │   │   │   │   └──cameras.bin
│   │   │   │   │   └──images.bin
│   │   │   │   │   └──points3D.bin
│   │   │   │   │   └──project.ini
│   │   │   └──database.db 
│   │   │   └──poses_bounds.npy
│   │   │   └──view_imgs.txt "所使用的图片"  
```

#### logs

```
                                                                                      
├── logs                                                                                                                                                                                               
│   ├── fern_test/llfftest 
│   │   └── testset_200000 "测试用的图片"
│   │   │   └──img01.jpg
│   │   │   └──img02.jpg
│   │   └── 050000.tar
│   │   └── 100000.tar
│   │   └── 150000.tar
│   │   └── 200000.tar "迭代200000步的模型权重
│   │   └── args.txt
│   │   └── config.txt
│   │   └── llfftest_spiral_200000_rgb.mp4 "最终渲染出的视频"
│   ├── summaries                                                                                                
│   │   └── fern_test/llfftest
│   │   │   │   └── events.out.tfevents.1718818883.c32264eda658.369162.0 "Tensorboard日志文件"                                                                                                                        

```

#### 全局文件存放路径

```
                                                                                      
├── configs                                                                                                                                                                                    │   └── fern.txt
│   └── llfftest.txt       
│   ├── data
│   │   └── ...
│   ├── logs
│   │   └── ...

│   │   └── testset_200000 "测试用的图片"
│   │   │   └──img01.jpg
│   │   │   └──img02.jpg
logs
│   │   └── 050000.tar
│   │   └── 100000.tar
│   │   └── 150000.tar
│   │   └── 200000.tar "迭代200000步的模型权重
│   │   └── args.txt
│   │   └── config.txt
│   │   └── llfftest_spiral_200000_rgb.mp4 "最终渲染出的视频"
│   ├── summaries                                                                                                
│   │   └── fern_test/llfftest
│   │   │   │   └── events.out.tfevents.1718818883.c32264eda658.369162.0 "Tensorboard日志文件"                                                                                                                        

```





Download data for two example datasets: `lego` and `fern`
```
bash download_example_data.sh
```

To train a low-res `lego` NeRF:
```
python run_nerf.py --config configs/lego.txt
```
After training for 100k iterations (~4 hours on a single 2080 Ti), you can find the following video at `logs/lego_test/lego_test_spiral_100000_rgb.mp4`.

![](https://user-images.githubusercontent.com/7057863/78473103-9353b300-7770-11ea-98ed-6ba2d877b62c.gif)

---

To train a low-res `fern` NeRF:
```
python run_nerf.py --config configs/fern.txt
```
After training for 200k iterations (~8 hours on a single 2080 Ti), you can find the following video at `logs/fern_test/fern_test_spiral_200000_rgb.mp4` and `logs/fern_test/fern_test_spiral_200000_disp.mp4`

![](https://user-images.githubusercontent.com/7057863/78473081-58ea1600-7770-11ea-92ce-2bbf6a3f9add.gif)

---

### More Datasets
To play with other scenes presented in the paper, download the data [here](https://drive.google.com/drive/folders/128yBriW1IG_3NJ5Rp7APSTZsJqdJdfc1). Place the downloaded dataset according to the following directory structure:
```
├── configs                                                                                                       
│   ├── ...                                                                                     
│                                                                                               
├── data                                                                                                                                                                                                       
│   ├── nerf_llff_data                                                                                                  
│   │   └── fern                                                                                                                             
│   │   └── flower  # downloaded llff dataset                                                                                  
│   │   └── horns   # downloaded llff dataset
|   |   └── ...
|   ├── nerf_synthetic
|   |   └── lego
|   |   └── ship    # downloaded synthetic dataset
|   |   └── ...
```

---

To train NeRF on different datasets: 

```
python run_nerf.py --config configs/{DATASET}.txt
```

replace `{DATASET}` with `trex` | `horns` | `flower` | `fortress` | `lego` | etc.

---

To test NeRF trained on different datasets: 

```
python run_nerf.py --config configs/{DATASET}.txt --render_only
```

replace `{DATASET}` with `trex` | `horns` | `flower` | `fortress` | `lego` | etc.


### Pre-trained Models

You can download the pre-trained models [here](https://drive.google.com/drive/folders/1jIr8dkvefrQmv737fFm2isiT6tqpbTbv). Place the downloaded directory in `./logs` in order to test it later. See the following directory structure for an example:

```
├── logs 
│   ├── fern_test
│   ├── flower_test  # downloaded logs
│   ├── trex_test    # downloaded logs
```

You will also need the [LLFF code](http://github.com/fyusion/llff) (and COLMAP) set up to compute poses if you want to run on your own real data.

