from wujing.utils.load_data import load_csv, load_excel


def test_load_csv():
    assert "王麻子" == load_csv("./testdata/person_info_utf8.csv")[0]["name"]
    assert 66 == load_csv("./testdata/person_info_gbk.csv")[0]["age"]

def test_load_excel():
    assert 3 == len(load_excel("./testdata/person_info.xlsx"))
