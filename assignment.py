import json
import pandas as pd
from adapter import StreamAdapter
from typing import Dict, Hashable, Iterable


class CourseWareB(StreamAdapter):
    """
    在下面定义CourseWareB
    答案状态在commonComponentState下的4cb5f12f9e164c6c545a55202bc818f2下的answer字段
    正确答案是1，2，0，36V
    """
    @staticmethod
    def __extract_panel_status(panel_status: Dict[str, str]) -> tuple:
        panel_state = [0, 0, 0, 0]
        for idx, n in panel_status.items():
            panel_state[int(idx)] = int(n)
        return tuple(panel_state)

    @classmethod
    def load_raw_state(cls, raw_state: str) -> Hashable:
        state = json.loads(raw_state).get("commonComponentState")
        panel_status = (0, 0, 0, 0)
        if state is not None:

            if "4cb5f12f9e164c6c545a55202bc818f2" in state:
                panel_status = cls.__extract_panel_status(
                    state["4cb5f12f9e164c6c545a55202bc818f2"]["answer"]
                )

        return panel_status

    @classmethod
    def is_user_right(cls, stream: Iterable) -> bool:
        right_ans = (1, 2, 0, 3)  # 我这里没有理解‘36V’的含义，猜想了一下
        return list(stream)[-1] == right_ans


if __name__ == "__main__":
    """
    在这里处理日志输出，输出结果为result.csv，三个字段为：学生ID，状态，是否为正确状态
    """
    # 使用CourseWareB处理data.csv时，中间出现了小问题，不知道是不是我的csv读取方式不匹配
    # 于是我换了一种方式处理
    total_data = pd.read_csv('data.csv', header=None, converters={8: str}, delimiter="\t")
    cstate = total_data[3]
    # 清除第一行格式错误的数据并重新编号，如不这样做在下面循环从1开始
    cstate.drop([0], inplace=True)
    cstate.reset_index(drop=True, inplace=True)
    # 变量初始化
    right_answer = [1, 2, 0, 3]
    answer = []
    bool_state = [0]*len(cstate)
    # 提取所需数据
    for i in range(0, len(cstate)):
        state = json.loads(cstate[i]).get("commonComponentState")
        answer.append(state["4cb5f12f9e164c6c545a55202bc818f2"]["answer"])
        bool_state[i] = answer[i] == right_answer
    # 制作result.csv，把上述得到的数据存入，删除第一行是使存入数据与原始数据行数相同
    total_data.drop(total_data.columns[1:5], axis=1, inplace=True)
    total_data.drop([0], inplace=True)
    total_data.insert(1, 'state', answer)
    total_data.insert(2, 'bool_state', bool_state)
    total_data.columns = ['学生ID', '状态', '是否为正确状态']
    total_data.to_csv('result.csv', encoding='GB18030', header=True, index=False)  # 保存并防止汉字出现乱码
