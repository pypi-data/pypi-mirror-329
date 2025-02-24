from sklearn.metrics import precision_score, recall_score
import pandas as pd
from prettytable import PrettyTable
from typing import Dict, Union, List
import numpy as np


def calc_classification_metrics(data: Dict[str, List[Union[int, str]]]) -> None:
    """
    计算并展示分类模型的评估指标

    Args:
        data: 包含'label'和'predict'键的字典，值为标签列表

    Raises:
        ValueError: 输入数据格式错误或标签不一致
        KeyError: 输入字典缺少必要的键
        TypeError: 输入数据类型错误
    """
    try:
        # 输入验证
        if not isinstance(data, dict):
            raise TypeError("输入必须是字典类型")

        # 检查必要的键是否存在
        required_keys = {"label", "predict"}
        if not all(key in data for key in required_keys):
            raise KeyError(f"输入字典必须包含以下键: {required_keys}")

        # 获取真实标签和预测标签
        true_labels = np.array(data["label"])
        pred_labels = np.array(data["predict"])

        # 检查标签长度是否一致
        if len(true_labels) != len(pred_labels):
            raise ValueError("真实标签和预测标签的长度不一致")

        # 检查是否有数据
        if len(true_labels) == 0:
            raise ValueError("输入数据为空")

        # 检查标签值是否有效
        if not (set(true_labels) and set(pred_labels)):
            raise ValueError("标签值无效")

        # 计算各项指标
        macro_precision = precision_score(
            true_labels, pred_labels, average="macro", zero_division=0
        )
        macro_recall = recall_score(
            true_labels, pred_labels, average="macro", zero_division=0
        )
        weighted_precision = precision_score(
            true_labels, pred_labels, average="weighted", zero_division=0
        )
        weighted_recall = recall_score(
            true_labels, pred_labels, average="weighted", zero_division=0
        )
        class_precision = precision_score(
            true_labels, pred_labels, average=None, zero_division=0
        )
        class_recall = recall_score(
            true_labels, pred_labels, average=None, zero_division=0
        )

        # 打印指标说明
        print("\n指标说明:")
        print("Precision(精确率): 在所有预测为该类的样本中，真实为该类的比例")
        print("Recall(召回率): 在所有真实为该类的样本中，被正确预测的比例")
        print("Macro Average: 所有类别的平均值，每个类别权重相同")
        print("Weighted Average: 考虑每个类别样本数量的加权平均值")

        # 创建整体指标表格
        try:
            overall_table = PrettyTable()
            overall_table.field_names = ["Metric", "Precision", "Recall"]
            overall_table.add_row(
                ["Macro Average", f"{macro_precision:.4f}", f"{macro_recall:.4f}"]
            )
            overall_table.add_row(
                [
                    "Weighted Average",
                    f"{weighted_precision:.4f}",
                    f"{weighted_recall:.4f}",
                ]
            )

            # 获取唯一的标签列表
            unique_labels = sorted(set(true_labels))

            # 创建每个类别指标的数据框
            class_metrics = pd.DataFrame(
                {
                    "Label": unique_labels,
                    "Precision": class_precision,
                    "Recall": class_recall,
                }
            )
            class_metrics_sorted = class_metrics.sort_values(
                "Precision", ascending=False
            )

            # 创建排序后的类别指标表格
            class_table = PrettyTable()
            class_table.field_names = ["Label", "Precision", "Recall"]
            for _, row in class_metrics_sorted.iterrows():
                class_table.add_row(
                    [row["Label"], f"{row['Precision']:.4f}", f"{row['Recall']:.4f}"]
                )

            print("\n整体评估指标:")
            print(overall_table)
            print("\n各类别评估指标 (按Precision降序排列):")
            print(class_table)

        except Exception as e:
            print(f"生成表格时发生错误: {str(e)}")

    except TypeError as e:
        print(f"类型错误: {str(e)}")
    except ValueError as e:
        print(f"值错误: {str(e)}")
    except KeyError as e:
        print(f"键错误: {str(e)}")
    except Exception as e:
        print(f"发生未预期的错误: {str(e)}")


# 使用示例
if __name__ == "__main__":
    # 正确的输入示例
    valid_data = {"label": [0, 1, 2, 1, 0], "predict": [0, 1, 1, 1, 0]}
    calc_classification_metrics(valid_data)

    # 错误输入示例
    invalid_data = {"label": [0, 1, 2], "predict": [0, 1]}  # 长度不匹配
    calc_classification_metrics(invalid_data)
