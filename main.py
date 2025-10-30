from paddle_ocr import PaddleOCRProcessor
import chromadb
from chromadb.config import Settings
from myconfig import myconfig
import json
import os


PROCESSED_RECORD = "processed.json"  # 本地记录文件
def load_processed():
    """读取已处理列表"""
    if not os.path.exists(PROCESSED_RECORD):
        return set()
    with open(PROCESSED_RECORD, "r", encoding="utf-8") as f:
        return set(json.load(f))
processed = load_processed()
def save_processed(path_set):
    """把已处理列表写回磁盘"""
    with open(PROCESSED_RECORD, "w", encoding="utf-8") as f:
        json.dump(list(path_set), f, ensure_ascii=False, indent=2)

processor = PaddleOCRProcessor(
    use_doc_orientation_classify=True,
    use_doc_unwarping=True
)

if __name__ == '__main__':
    print("开始ocr")
    ROOT_DIR = "fetched_pdfs"

    client = chromadb.PersistentClient(
        path="chroma_db",  # 你的持久化目录
        settings=Settings(anonymized_telemetry=False)
    )

    # 2. 拿到目标 collection
    collection_name = "pubmed_abstract"
    collection = client.get_collection(name=collection_name)
    all_records = collection.get(include=["metadatas", "documents"])
    metadatas = all_records["metadatas"]

    from tqdm import tqdm
    for meta in tqdm(metadatas, desc="仅更新 filename"):
        # 浅拷贝一份，防止直接修改原列表
        meta = dict(meta)
        file_path = meta.get("path")
        theme_name = file_path.split('/')[-2]
        file_name = file_path.split('/')[-1]

        new_file_path = f"{myconfig['new_root_path']}/{theme_name}/{file_name}"
        if new_file_path.endswith(".pdf") is False:
            continue
        output_directory = f"{myconfig['output_root_path']}/{theme_name}/{file_name.replace('.pdf', '')}"
        print("正在处理:"+new_file_path)
        print("输出路径:"+output_directory)
        if file_name in processed:
            continue
        try:
            processor.process_image(new_file_path, output_directory)
        except (AssertionError, RuntimeError):
            print("跳过错误")
            continue
        processed.add(file_name)
        save_processed(processed)