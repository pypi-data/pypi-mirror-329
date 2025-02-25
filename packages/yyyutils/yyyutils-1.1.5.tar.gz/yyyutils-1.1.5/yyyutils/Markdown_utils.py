import os
from loguru import logger
from magic_pdf.pipe.UNIPipe import UNIPipe
from magic_pdf.pipe.OCRPipe import OCRPipe
from magic_pdf.pipe.TXTPipe import TXTPipe
from magic_pdf.rw.DiskReaderWriter import DiskReaderWriter
import magic_pdf.model as model_config

def prepare_output_path(pdf_path, output_dir):
    pdf_name = os.path.basename(pdf_path).split(".")[0]
    if output_dir:
        output_path = os.path.join(output_dir, pdf_name)
    else:
        pdf_path_parent = os.path.dirname(pdf_path)
        output_path = os.path.join(pdf_path_parent, pdf_name)
    output_image_path = os.path.join(output_path, 'images')
    return output_path, output_image_path

class Markdown_工具箱:
    @staticmethod
    def pdf_parse_main(
            pdf_path: str,
            parse_method: str = 'auto',
            model_json_path: str = None,
            is_json_md_dump: bool = True,
            output_dir: str = None
    ):
        if not os.path.isfile(pdf_path):
            logger.error(f"pdf_path {pdf_path} is not a valid file")
            return
        if parse_method not in ['auto', 'ocr', 'txt']:
            logger.error(f"invalid parse_method {parse_method}")
            return

        try:
            output_path, output_image_path = prepare_output_path(pdf_path, output_dir)
            image_path_parent = os.path.basename(output_image_path)
            pdf_bytes = open(pdf_path, "rb").read()
            image_writer = DiskReaderWriter(output_image_path)
            md_writer = DiskReaderWriter(output_path)

            model_config.__use_inside_model__ = True  # 确保使用内置模型

            if parse_method == "auto":
                jso_useful_key = {"_pdf_type": "", "model_list": []}
                pipe = UNIPipe(pdf_bytes, jso_useful_key, image_writer)
            elif parse_method == "txt":
                pipe = TXTPipe(pdf_bytes, [], image_writer)
            elif parse_method == "ocr":
                pipe = OCRPipe(pdf_bytes, [], image_writer)

            pipe.pipe_classify()
            pipe.pipe_analyze()
            pipe.pipe_parse()
            content_list = pipe.pipe_mk_uni_format(image_path_parent)
            md_content = pipe.pipe_mk_markdown(image_path_parent)
            print(md_content)
        except Exception as e:
            logger.error(f"pdf_parse_main error: {e}")

if __name__ == '__main__':
    pdf_path = r'D:\Python\Python38\Lib\site-packages\mytools\yyyutils\部分真题.pdf'
    Markdown_工具箱.pdf_parse_main(pdf_path, parse_method='auto', is_json_md_dump=True)