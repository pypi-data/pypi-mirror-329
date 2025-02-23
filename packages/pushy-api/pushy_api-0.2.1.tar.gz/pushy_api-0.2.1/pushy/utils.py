from .const import TAG_REGEX

def _format_tags(tags: list[str] | None) -> str:
    if not tags:
        return ''
    if not all(map(TAG_REGEX.fullmatch, tags)):
        raise ValueError(f'tags: Found a tag not satisfying {TAG_REGEX.pattern!r} regex')
    return ','.join(tags)
