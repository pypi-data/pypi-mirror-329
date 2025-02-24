from graphrag_tagger.chat.llm import LLM


# Create a DummyLLM that overrides __call__.
class DummyLLM(LLM):
    def __init__(self, model="test-model"):
        # Skip actual initialization.
        self.model_name = model

    def __call__(self, messages: list):
        prompt = messages[0]["content"]
        if "transform a list of messy topics" in prompt:
            return '{"topics": ["TopicA", "TopicB"]}'
        elif "analyze a given text excerpt" in prompt:
            return '["TopicA", "TopicC"]'
        return "{}"


def test_clean_topics():
    llm = DummyLLM()
    result = llm.clean_topics(["messy topic one", "messy topic two"])
    assert result == {"topics": ["TopicA", "TopicB"]}


def test_classify():
    llm = DummyLLM()
    result = llm.classify("Some document text", ["TopicA", "TopicB", "TopicC"])
    assert result == ["TopicA", "TopicC"]
