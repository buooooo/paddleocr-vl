import os
import time
from paddleocr import PaddleOCRVL
 
class PaddleOCRProcessor:
    def __init__(self, 
                 use_doc_orientation_classify=False,
                 use_doc_unwarping=False,
                 use_layout_detection=True):
        """
        初始化OCR处理管道
        :param use_doc_orientation_classify: 是否使用文档方向分类
        :param use_doc_unwarping: 是否使用文本图像矫正
        :param use_layout_detection: 是否使用版面区域检测
        """
        self.pipeline = PaddleOCRVL(
            vl_rec_backend="vllm-server",
            vl_rec_server_url="http://127.0.0.1:8118/v1",
            use_doc_orientation_classify=use_doc_orientation_classify,
            use_doc_unwarping=use_doc_unwarping,
            use_layout_detection=use_layout_detection
        )
    
    def process_image(self, input_path, output_dir):
        """
        处理单张图像并保存结果
        :param input_path: 输入图像路径
        :param output_dir: 输出目录路径
        """
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        # 开始计时
        start_time = time.time()
        print(f"开始处理图像: {os.path.basename(input_path)}")

 
        # 执行OCR识别
        output = self.pipeline.predict(
            input=input_path,
            save_path=output_dir
        )
        # 计算总处理时间
        end_time = time.time()
        total_time = end_time - start_time
        
        # 处理并保存结果
        for i, res in enumerate(output):
            # print(f"\n===== 页面 {i+1} 结果 =====")
            # res.print()  # 打印结构化输出
            
            # 生成唯一文件名（基于输入文件名）
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            if len(output) > 1:
                base_name += f"_page{i+1}"
            
            # 保存结果
            # res.save_to_json(save_path=output_dir)
            res.save_to_markdown(save_path=output_dir)
            # print("已经保存成md格式")
            # res.save_to_img(save_path=output_dir)  # 保存可视化图片
            # print("已经保存成图片格式")
        
        print(f"\n处理完成！结果已保存至: {output_dir}")
        print(f"总耗时: {total_time:.2f} 秒")
        print("=" * 50)
 
# 使用示例
if __name__ == "__main__":
    # 初始化处理器（可根据需要调整参数）
    processor = PaddleOCRProcessor(
        use_doc_orientation_classify=True,
        use_doc_unwarping=True
    )
    
    # 指定输入和输出路径
    input_image = r"/home/wlb/Desktop/pubmed/1.pdf"  # 替换为实际图像路径
    output_directory = "/home/wlb/Desktop/pubmed/output"  # 替换为输出目录
    
    # 处理图像
    processor.process_image(input_image, output_directory)