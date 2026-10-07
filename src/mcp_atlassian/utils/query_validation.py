"""Validation helpers shared by JQL and CQL query construction.

Both the Jira and Confluence search mixins enforce a project/space allowlist
by textually wrapping a caller-supplied query, e.g. ``f"({jql}) AND ({filter})"``.
That wrapping is only safe if the caller's query is itself a syntactically
complete boolean expression: an unbalanced closing parenthesis lets the
caller's clause close the wrapping group early and start a new, unconstrained
``OR`` branch (JQL/CQL bind ``AND`` tighter than ``OR``), escaping the
allowlist entirely. Reject such input before any wrapping happens.
"""


def has_balanced_quotes_and_parens(query: str) -> bool:
    """Check that ``query`` has balanced quotes and parentheses.

    Parentheses inside a quoted string literal are not counted, matching how
    JQL/CQL themselves treat quoted content (e.g. ``summary ~ "weird (case)"``
    is one balanced literal, not an unmatched paren).

    Args:
        query: Raw JQL or CQL query string.

    Returns:
        False if the query has any unmatched parenthesis or an unterminated
        quote — meaning it is not safe to wrap in an additional ``(...)``
        group — True otherwise.
    """
    depth = 0
    quote_char: str | None = None
    i = 0
    n = len(query)
    while i < n:
        ch = query[i]
        if quote_char:
            if ch == "\\" and i + 1 < n:
                i += 2
                continue
            if ch == quote_char:
                quote_char = None
        elif ch in ("'", '"'):
            quote_char = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth < 0:
                return False
        i += 1
    return depth == 0 and quote_char is None
