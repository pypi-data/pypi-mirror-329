from sklearn.metrics import precision_score, recall_score
import numpy as np
from typing import Dict, Union, List


def calculate_classification_metrics(
    data: Dict[str, List[Union[int, str]]]
) -> Dict[str, Union[Dict[str, float], List[Dict[str, Union[str, float]]]]]:
    """
    计算分类模型的评估指标并返回结构化数据

    Args:
        data: 包含'label'和'predict'键的字典，值为标签列表

    Returns:
        包含以下结构的字典:
        {
            "explanation": List[str],               # 指标说明
            "overall": Dict[str, float],           # 宏观指标
            "classes": List[Dict[str, Union[str, float]]]  # 分类指标（按precision降序）
        }

    Raises:
        TypeError: 输入数据类型错误
        KeyError: 输入字典缺少必要键
        ValueError: 数据验证失败
    """
    # 输入验证
    if not isinstance(data, dict):
        raise TypeError("输入必须是字典类型")

    required_keys = {"label", "predict"}
    if not required_keys.issubset(data.keys()):
        raise KeyError(f"输入字典必须包含以下键: {required_keys}")

    true_labels = np.array(data["label"])
    pred_labels = np.array(data["predict"])

    if len(true_labels) != len(pred_labels):
        raise ValueError("真实标签和预测标签长度不一致")

    if len(true_labels) == 0:
        raise ValueError("输入数据不能为空")

    if not (set(true_labels) and set(pred_labels)):
        raise ValueError("检测到无效的标签值")

    # 计算指标
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

    # 分类别指标
    class_precision = precision_score(
        true_labels, pred_labels, average=None, zero_division=0
    )
    class_recall = recall_score(true_labels, pred_labels, average=None, zero_division=0)

    # 组织分类结果
    unique_labels = sorted(set(true_labels))
    class_metrics = [
        {
            "label": str(label),
            "precision": float(prec),
            "recall": float(rec),
        }
        for label, prec, rec in zip(unique_labels, class_precision, class_recall)
    ]

    # 按precision降序排序
    sorted_class_metrics = sorted(
        class_metrics, key=lambda x: x["precision"], reverse=True
    )

    return {
        "explanation": [
            "Precision(精确率): 在所有预测为该类的样本中，真实为该类的比例",
            "Recall(召回率): 在所有真实为该类的样本中，被正确预测的比例",
            "Macro Average: 所有类别的平均值，每个类别权重相同",
            "Weighted Average: 考虑每个类别样本数量的加权平均值",
        ],
        "overall": {
            "macro_precision": float(macro_precision),
            "macro_recall": float(macro_recall),
            "weighted_precision": float(weighted_precision),
            "weighted_recall": float(weighted_recall),
        },
        "classes": sorted_class_metrics,
    }


# 使用示例
if __name__ == "__main__":
    # 示例数据
    data = {"label": [0, 1, 0, 1, 2], "predict": [0, 1, 0, 0, 2]}

    # 获取指标
    metrics = calculate_classification_metrics(data)

    # 读取结果
    print("整体指标:", metrics["overall"])
    print("各类别指标:")
    for cls in metrics["classes"]:
        print(
            f'类别 {cls["label"]}: Precision={cls["precision"]:.2f}, Recall={cls["recall"]:.2f}'
        )
