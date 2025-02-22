import inspect

# EXAMPLE INPUT
# """
#     Hello
#     World
#         With Indent
#     Back
# """
#
# EXAMPLE OUTPUT
# Hello
# World
#     With Indent
# Back
#
def multiline(text: str) -> str:
    """
    Cleans up indentation from multiline \"\"\" strings.
    Any whitespace that can be uniformly removed from the second line onwards is removed.
    """
    return inspect.cleandoc(text)
