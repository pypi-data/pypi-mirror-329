from ie_datasets import SciERC


def test_summary():
    with open("summaries/scierc.txt") as f:
        assert f.read().strip("\n") == SciERC.get_summary()


test_summary()
