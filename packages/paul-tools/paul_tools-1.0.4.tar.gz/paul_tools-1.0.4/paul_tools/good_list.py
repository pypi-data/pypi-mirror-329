# 定義模組的所有導出成員
__all__ = ["list"]


# 自定義列表類，繼承自內建的 list 類
class _list(list):
    # 添加 join 方法，用於將列表中的元素連接成字符串
    def join(self, sep: str) -> str:
        # 使用指定的分隔符將列表中的元素連接成字符串
        return sep.join(str(item) for item in self)


# 將自定義的 _list 類賦值給 list
list = _list
