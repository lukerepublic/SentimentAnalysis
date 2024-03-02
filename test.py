import re

fhand = open("test.txt", "r")

money = 501.000
line = "shoes 1,146,700 men.; government awards $8,198,905 contracts various firms."


print(-0.34 + -9)


word = "bulgaria.america turkey"
wordss = word.split()
# words = re.split("[.]", word)
# word = re.sub('[^a-zA-Z0-9]+', '', word)

for str in wordss:
    if re.search("[a-z]\.[a-z]", str):
        listy = str.split(".")
        wordss.append(listy[0])
        wordss.append(listy[1])
        wordss.remove(str)

# for line in fhand:
#     if re.search("war\.[a-z]", line):
#         print(line)
#     if re.search("[a-z]\.war", line):
#         print(line)

#theatre--french 
# dict_count = {}
# for line in fhand:
#     words = line.split()
#     for word in words:
#         if re.search("[a-z]", word):
#             dict_count[word] = dict_count.get(word, 0) + 1

# tmp_list = []
# for (key, val) in dict_count.items():
#     tmp_list.append((val, key))
# sorted_list = sorted(tmp_list, reverse=True)
# print(sorted_list[:10])



