from stock_catcher.catcher import get_default_cac_file_path


def test_getDefaultCacFilePath():
    expected_path = "/home/pliu/git/py-packaging/src/stock_catcher/data/CAC40_2024.csv"
    actual_path = get_default_cac_file_path().as_posix()
    assert actual_path == expected_path