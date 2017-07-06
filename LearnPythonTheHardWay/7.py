formatter = "%r %r %r %r"

print formatter % (1, 2, 3, 4)
print formatter % ("one", "two", "three", "four")
print formatter % (True, False, False, True)
# '%r %r %r %r' '%r %r %r %r' '%r %r %r %r' '%r %r %r %r'
print formatter % (formatter, formatter, formatter, formatter)
# no line change, blank space seperate the four setences.
# 'I had this thing.' 'That you could type up right.' "But it didn't sing." 'So I said goodnight.'
# but you must be attention to one of the outputs has ""  ?
print formatter % (
    "I had this thing.",
    "That you could type up right.",
    "But it didn't sing.",
    "So I said goodnight."
)