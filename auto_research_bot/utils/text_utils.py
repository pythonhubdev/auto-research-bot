import mwparserfromhell


class TextUtils:
    @staticmethod
    def parse_wikitext_to_plain_text(wikitext: str) -> str:
        wiki_code = mwparserfromhell.parse(wikitext)
        text = wiki_code.strip_code()
        return text

    @staticmethod
    def truncate_text(text: str, max_tokens: int, model_name: str = "gpt-3.5-turbo-1106") -> str:
        import tiktoken

        encoding = tiktoken.encoding_for_model(model_name)
        tokens = encoding.encode(text)
        if len(tokens) > max_tokens:
            truncated_tokens = tokens[:max_tokens]
            return encoding.decode(truncated_tokens)
        return text
