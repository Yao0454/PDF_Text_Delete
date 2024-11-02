import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF

# 删除指定文字的函数
def remove_text_from_pdf(input_pdf, output_pdf, text):
    # 打开 PDF 文件
    doc = fitz.open(input_pdf)

    # 遍历 PDF 中的每一页
    for page_num in range(doc.page_count):
        page = doc[page_num]
        
        # 获取页面上的所有匹配的文字框
        text_instances = page.search_for(text)
        
        # 删除指定区域内的文字框
        for inst in text_instances:
            page.add_redact_annot(inst, fill=(1, 1, 1))  # 使用白色填充覆盖文字
        page.apply_redactions()

    # 保存结果
    doc.save(output_pdf)
    doc.close()

# 打开文件选择对话框
def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        input_path_var.set(file_path)

# 打开文件保存对话框
def select_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if file_path:
        output_path_var.set(file_path)

# 删除文字并保存的主函数
def process_pdf():
    input_pdf = input_path_var.get()
    output_pdf = output_path_var.get()
    text = text_var.get()

    if not input_pdf or not output_pdf or not text:
        messagebox.showerror("Error", "请填写所有字段！")
        return

    try:
        remove_text_from_pdf(input_pdf, output_pdf, text)
        messagebox.showinfo("Success", f"文件已成功保存到 {output_pdf}")
    except Exception as e:
        messagebox.showerror("Error", f"处理文件时出错：{e}")

# 创建主窗口
root = tk.Tk()
root.title("PDF文字删除工具")
root.geometry("400x350")

# 输入 PDF 文件路径
tk.Label(root, text="选择输入 PDF 文件:").pack(pady=5)
input_path_var = tk.StringVar()
tk.Entry(root, textvariable=input_path_var, width=40).pack(pady=5)
tk.Button(root, text="浏览", command=select_input_file).pack(pady=5)

# 输入要删除的文字
tk.Label(root, text="输入要删除的文字:").pack(pady=5)
text_var = tk.StringVar()
tk.Entry(root, textvariable=text_var, width=40).pack(pady=5)

# 输出 PDF 文件路径
tk.Label(root, text="选择输出 PDF 文件:").pack(pady=5)
output_path_var = tk.StringVar()
tk.Entry(root, textvariable=output_path_var, width=40).pack(pady=5)
tk.Button(root, text="保存为...", command=select_output_file).pack(pady=5)

# 执行按钮
tk.Button(root, text="开始删除文字", command=process_pdf, bg="lightblue").pack(pady=20)

# 启动主循环
root.mainloop()
