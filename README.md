<img width="830" height="166" alt="image" src="https://github.com/user-attachments/assets/1f3f1fc3-d0cf-4617-b5c2-9a7b8ec22a76" /># paddleocr-vl
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

在步骤3的时候可能会报错,



