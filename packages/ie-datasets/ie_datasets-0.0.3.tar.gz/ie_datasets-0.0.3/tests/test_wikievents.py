from ie_datasets import WikiEvents


def test_summary():
    with open("summaries/wikievents.txt") as f:
        assert f.read().strip("\n") == WikiEvents.get_summary()


test_summary()
