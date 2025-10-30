# paddleocr-vl
用paddleocr-VL模型对大量pdf文件进行OCR识别并转换成md格式

# paddleocr-vl 部署
本人的部署环境：
cuda:12.8
torch:2.8
python -V: 3.11
ubuntu 22.04
GPU:RTX 4090ti 单卡即可

# 安装流程:
1. 创建虚拟环境
conda create -n ppocr-vllm python=3.11 -y
conda activate ppocr-vllm
2. 安装 PaddleOCR
python -m pip install paddlepaddle-gpu==3.2.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu126/
python -m pip install -U "paddleocr[doc-parser]"
python -m pip install https://paddle-whl.bj.bcebos.com/nightly/cu126/safetensors/safetensors-0.6.2.dev0-cp38-abi3-linux_x86_64.whl
3. 安装推理加速服务依赖
paddleocr install_genai_server_deps vllm
4. 验证是否安装成功VLLM
python -c "import vllm; print(f'vLLM version: {vllm.__version__}')"

在步骤3的时候可能会有一下问题
报错1：
<img width="830" height="166" alt="image" src="https://github.com/user-attachments/assets/1f3f1fc3-d0cf-4617-b5c2-9a7b8ec22a76" />
一直在这里卡着直到报错，我们可以到这里直接crtl+c直接退出。
报错2：
<img width="1311" height="217" alt="image" src="https://github.com/user-attachments/assets/0b3215f0-2acf-445f-8b5a-4a9bc15ad515" />
我自己有一段乱操作之后右侧出现过上面这个图片的问题，看报错信息说明的是torch版本不对，因此我重新卸载了torch，重新执行步骤3的命令，他会重新帮我们下载好torch对应的版本。

对于报错1，是flash-atten没有安装好的话，我们可以自己去找对应的安装包，然后将下载好的安装包传到你的服务器上并安装。
安装包地址：https://github.com/Dao-AILab/flash-attention/releases?page=1

根据我的部署环境，我下载的是
<img width="898" height="693" alt="image" src="https://github.com/user-attachments/assets/3ce4fb4e-fda8-4505-8248-d3ae45e6a754" />
执行python -m pip install flash_attn-2.7.3+cu12torch2.8cxx11abiFALSE-cp311-cp311-linux_x86_64.whl​ (需要cd到flash-atten安装包的路径下，然后执行该指令)。

到这里应该算是安装好了，接下来需要启动vllm框架。
paddlex_genai_server --model_name PaddleOCR-VL-0.9B --backend vllm --port 8118
如果出现一下图片的情况说明执行成功
<img width="1594" height="827" alt="image" src="https://github.com/user-attachments/assets/80b8a471-6b51-4df4-b961-283e398b1e9f" />

接下来可以另外开一个session窗口，然后conda activate ppocr-vllm，调用上面的vllm接口执行ocr识别。









