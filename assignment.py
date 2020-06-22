import json
import csv
from adapter import StreamAdapter
from typing import Dict, Hashable, Iterable


class CourseWareB(StreamAdapter):
    """
    在下面定义CourseWareB
    答案状态在commonComponentState下的4cb5f12f9e164c6c545a55202bc818f2下的answer字段
    正确答案是1，2，0，36V
    """
    # @staticmethod
    # def __extract_panel_status(panel_status: Dict[str, str]) -> tuple:
    #     panel_state = [0, 0, 0, 0]
    #     for idx, n in panel_status.items():
    #         panel_state[int(idx)] = int(n)
    #     return tuple(panel_state)

    @classmethod
    def load_raw_state(cls, raw_state: str) -> Hashable:
        state = json.loads(raw_state).get("commonComponentState")
        panel_status = [0, 0, 0, 0]
        if state is not None:

            if "4cb5f12f9e164c6c545a55202bc818f2" in state:
                panel_status = state["4cb5f12f9e164c6c545a55202bc818f2"]["answer"]

        return panel_status

    @classmethod
    def is_user_right(cls, stream: Iterable) -> bool:
        right_ans = [1, 2, 0, 3]  # 我这里没有理解‘36V’的含义，猜想了一下
        return list(stream) == right_ans


if __name__ == "__main__":
    """
    在这里处理日志输出，输出结果为result.csv，三个字段为：学生ID，状态，是否为正确状态
    """
# __extract_panel_status函数输入是字典格式，而load_raw_state函数中的"answer"字段中的数据是列表格式，故此函数在CourseWareB中应该是不必要的
# 在example.py中的"status"字段中的数据应该是字典格式，在data.csv文件中没有找到相应字段，不太确定。
csv_writer = csv.writer(open('result.csv', 'w', encoding='GB18030', newline=''))
csv_writer.writerow(['学生ID', '状态', '是否为正常状态'])
with open('data.csv', 'r') as f:
    data = list(csv.reader(f, delimiter='\t'))
    for i in range(1, len(data)):
        state3 = CourseWareB.load_raw_state(data[i][3])
        bool_state = CourseWareB.is_user_right(state3)
        csv_writer.writerow([data[i][0], state3, bool_state])
