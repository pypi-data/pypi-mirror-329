from ie_datasets import WikiEvents


def test_wikievents_summary():
    with open("tests/wikievents_summary.txt") as f:
        assert f.read().strip("\n") == WikiEvents.get_wikievents_summary()


test_wikievents_summary()
