import re

pattern = re.compile("foobar")
test1 = "foo bar"
test2 = "barfoo"
test3 = "foobar"
print(pattern.findall(test1))
print(pattern.findall(test2))
print(pattern.findall(test3))
