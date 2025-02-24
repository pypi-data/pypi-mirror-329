import io
import sys
from typing import Optional

import chardet
import pandas as pd
from datasets import Dataset, DatasetDict


def convert_to_utf8_in_memory(file_path: str) -> str:
    with open(file_path, "rb") as f:
        raw_data = f.read()
        detected_encoding = chardet.detect(raw_data)["encoding"]

    if detected_encoding is None:
        detected_encoding = "utf-8"  # 默认编码

    if detected_encoding.lower() != "utf-8":
        data = raw_data.decode(detected_encoding)
    else:
        data = raw_data.decode("utf-8")

    return data


def load_csv(file_path: str) -> Optional[Dataset]:
    try:
        utf8_data = convert_to_utf8_in_memory(file_path)
        utf8_buffer = io.StringIO(utf8_data)
        df = pd.read_csv(utf8_buffer)
        dataset = Dataset.from_pandas(df)
        return dataset
    except Exception as e:
        print(f"Error loading CSV dataset from {file_path}: {e}", file=sys.stderr)
        return None


def load_excel(file_path: str) -> Optional[DatasetDict]:
    try:
        all_sheets = pd.read_excel(file_path, sheet_name=None)
        datasets = {}

        for sheet_name, df in all_sheets.items():
            df = df.ffill().astype(str)
            datasets[sheet_name] = Dataset.from_pandas(df)

        return DatasetDict(datasets)
    except Exception as e:
        print(f"Error loading Excel dataset from {file_path}: {e}", file=sys.stderr)
        return None


if __name__ == "__main__":
    print(load_excel("./testdata/person_info.xlsx"))
    print(load_csv("./testdata/person_info_gbk.csv"))
    print(load_csv("./testdata/person_info_utf8.csv"))
