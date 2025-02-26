from ie_datasets import ChemProt


def test_summary():
    with open("summaries/chemprot.txt") as f:
        assert f.read().strip("\n") == ChemProt.get_summary()


test_summary()
