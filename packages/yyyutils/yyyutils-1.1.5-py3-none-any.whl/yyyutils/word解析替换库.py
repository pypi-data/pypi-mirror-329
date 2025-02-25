import win32com.client
import os


def extract_axmath_to_latex(doc_path):
    # 创建Word应用实例
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False

    try:
        # 打开Word文档
        doc = word.Documents.Open(doc_path)

        # 遍历文档中的所有对象
        for i in range(doc.InlineShapes.Count):
            shape = doc.InlineShapes[i]
            print(f"Shape {i + 1}: {shape.Type}")

            # 检查是否是AxMath对象
            if shape.Type == 12:  # 12表示OLE对象
                ole_obj = shape.OLEFormat
                if "AxMath" in ole_obj.ClassType:
                    # 获取AxMath对象
                    axmath = ole_obj.Object

                    # 获取LaTeX代码
                    latex = axmath.TeXCode
                    print(f"Found equation {i + 1}: {latex}")

        doc.Close()
    finally:
        word.Quit()


# 使用示例
doc_path = r'C:\Desktop\课程设计\混凝土\RC课程设计2022110080吴科昱.docx'
extract_axmath_to_latex(doc_path)
