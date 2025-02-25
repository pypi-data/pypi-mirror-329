import copier
import os

def copy_template(src_path, dst_path, data=None):
    """
    使用copier复制模板。

    Args:
        src_path: 模板的源路径。
        dst_path: 目标路径。
        data: 传递给模板的上下文数据（字典）。
    """
    try:
        copier.run_copy(src_path, dst_path, data=data)  # vcs=False 禁用版本控制
    except Exception as e:
        raise e
        # print(f"{e}")


def copy_module(dst_path, data=None):
    copy_template(r"D:\git\xilong\copier\module", dst_path, data)

def copy_resources(dst_path, data=None):
    copy_template(r"D:\git\xilong\copier\resources", dst_path, data)


if __name__ == "__main__":
    # 示例用法
    template_source = r"D:\git\xilong\copier\module"  # 替换为你的模板源路径
    destination_path = r"haha"  # 替换为你的目标路径
    context_data = {
        "english": "My Project",
        "chinese": "Your Name",
        "table": "Your Name"
        # 其他模板变量
    }

    copy_template(template_source, destination_path, context_data)