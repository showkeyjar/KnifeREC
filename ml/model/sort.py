
"""
排序模型
"""


def sort(data, column, limit=20, asc=False):
    """
    todo 按指定字段排序
    """
    try:
        data.sort_values(column, ascending=asc, inplace=True)
        ret_df = data[:limit]
    except:
        ret_df = None
    return ret_df


