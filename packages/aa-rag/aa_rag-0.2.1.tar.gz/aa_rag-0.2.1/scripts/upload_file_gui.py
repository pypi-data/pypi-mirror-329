import os
import base64
import streamlit as st

# 指定服务器上的根目录（请修改为你的实际目录）
BASE_DIR = "./resources"

# 初始化当前目录（存储在 session_state 中）
if "current_dir" not in st.session_state:
    st.session_state.current_dir = BASE_DIR


def list_dir(directory):
    """列出目录下的子目录和文件"""
    try:
        items = os.listdir(directory)
    except Exception as e:
        st.error(f"无法读取目录: {e}")
        return [], []
    dirs = [item for item in items if os.path.isdir(os.path.join(directory, item))]
    files = [item for item in items if os.path.isfile(os.path.join(directory, item))]
    return dirs, files


def navigate_to(directory):
    """切换当前目录"""
    st.session_state.current_dir = directory


def go_up(directory):
    """返回上一级目录，确保不越过 BASE_DIR"""
    if os.path.abspath(directory) != os.path.abspath(BASE_DIR):
        return os.path.dirname(directory)
    return directory


def preview_file(file_path):
    """预览文件，根据扩展名不同展示不同效果"""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        try:
            with open(file_path, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode("utf-8")
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"预览 PDF 文件失败: {e}")
    elif ext in [".md", ".markdown"]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            st.markdown(content)
        except Exception as e:
            st.error(f"预览 Markdown 文件失败: {e}")
    elif ext in [".txt"]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            st.text(content)
        except Exception as e:
            st.error(f"预览文本文件失败: {e}")
    else:
        st.info("该文件类型不支持预览。")


# 主页面标题和当前目录显示
st.title("服务器文件管理器")
current_dir = st.session_state.current_dir
st.write("**当前目录：**", current_dir)

# 如果不在根目录，显示返回上一级目录按钮
if os.path.abspath(current_dir) != os.path.abspath(BASE_DIR):
    if st.button("返回上一级目录"):
        navigate_to(go_up(current_dir))
        st.experimental_rerun()

# 显示当前目录下的子目录和文件
dirs, files = list_dir(current_dir)

st.header("文件夹")
if dirs:
    for d in dirs:
        # 每个目录显示为一个按钮，点击后进入该目录
        if st.button(d, key=f"dir_{d}"):
            new_path = os.path.join(current_dir, d)
            navigate_to(new_path)
            st.experimental_rerun()
else:
    st.info("当前目录下没有子文件夹。")

st.header("文件")
if files:
    for f in files:
        # 每个文件显示为一个按钮，点击后预览文件
        if st.button(f, key=f"file_{f}"):
            file_path = os.path.join(current_dir, f)
            st.subheader(f"预览文件：{f}")
            preview_file(file_path)
else:
    st.info("当前目录下没有文件。")

# 侧边栏操作区
st.sidebar.header("操作面板")

# 新建目录
st.sidebar.subheader("新建目录")
new_dir_name = st.sidebar.text_input("目录名")
if st.sidebar.button("创建目录"):
    if new_dir_name:
        new_dir_path = os.path.join(current_dir, new_dir_name)
        try:
            os.makedirs(new_dir_path, exist_ok=True)
            st.sidebar.success("目录创建成功！")
            st.experimental_rerun()
        except Exception as e:
            st.sidebar.error(f"创建目录失败：{e}")
    else:
        st.sidebar.error("请输入目录名。")

# 新建文本文件
st.sidebar.subheader("新建文本文件")
new_file_name = st.sidebar.text_input(
    "文件名（包含扩展名，如 file.txt）", key="new_file_name"
)
new_file_content = st.sidebar.text_area("文件内容", key="new_file_content")
if st.sidebar.button("创建文本文件"):
    if new_file_name:
        new_file_path = os.path.join(current_dir, new_file_name)
        try:
            with open(new_file_path, "w", encoding="utf-8") as f:
                f.write(new_file_content)
            st.sidebar.success("文本文件创建成功！")
            st.experimental_rerun()
        except Exception as e:
            st.sidebar.error(f"创建文本文件失败：{e}")
    else:
        st.sidebar.error("请输入文件名。")

# 上传文件
st.sidebar.subheader("上传文件")
uploaded_file = st.sidebar.file_uploader("选择文件上传", key="uploaded_file")
if uploaded_file is not None:
    file_path = os.path.join(current_dir, uploaded_file.name)
    try:
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.sidebar.success("文件上传成功！")
        st.experimental_rerun()
    except Exception as e:
        st.sidebar.error(f"上传文件失败：{e}")
