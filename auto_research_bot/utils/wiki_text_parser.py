import mwparserfromhell


class MediaWikiUtils:
    @staticmethod
    def parse_wikitext_to_plain_text(wikitext: str) -> str:
        wiki_code = mwparserfromhell.parse(wikitext)
        text = wiki_code.strip_code()
        return text
