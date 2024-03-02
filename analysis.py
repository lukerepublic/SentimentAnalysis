import requests
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# global variables and file initialization 
word_freq1918 = {}
word_freq2020 = {}

fraction1918 = {"flu": 0, "virus": 0, "death": 0}
fraction2020 = {"flu": 0, "virus": 0, "death": 0}

dollars1918 = ""
dollars2020 = ""

sentiment1918 = 0.0
sentiment2020 = 0.0

data_stopwords = requests.get("https://gist.githubusercontent.com/larsyencken/1440509/raw/53273c6c202b35ef00194d06751d8ef630e53df2/stopwords.txt").text

titles1918 = open("titles_1918.txt", "r")
titles2020 = open("titles_2020.txt", "r")
test = open("test.txt", "w")

##==================================================================##

# function to remove stop words
def remove_stopwords(input_string):
  dict_stopwords = {}
  for val in data_stopwords.split("\n"):
    dict_stopwords[val.strip()] = 1
 
  output_string = ""
  for word in input_string.lower().split():
    if (word in dict_stopwords):
      continue
    output_string += word + " "
  output_string = output_string.strip()
  return output_string

# filter out words with special characters attached
def stripper(word):
   word = re.sub('[^a-zA-Z0-9]+', '', word)
   return word

# function to count word frequency
def count_words(current_line):
    word_freq = {}
    words = current_line.split()
    for word in words:
        if re.search("[a-z]", word):
            word = stripper(word)     
            word_freq[word] = word_freq.get(word, 0) + 1
    freq_list = list(word_freq.items())
    return freq_list
    
# function to sort the dictionary in reverse order (highest to lowest frequency)
def sort_by_frequency(word_freq):
    sorted_dict = {}
    tmp_list = []
    for (key, val) in word_freq.items():
       tmp_list.append((val, key))

    sorted_list = sorted(tmp_list, reverse=True)
    for (key, val) in sorted_list[:10]:
       sorted_dict[val] = key
    return sorted_dict

# function to calculate frequency of titles that contain the terms "flu", "virus", "death"
def term_frequency(current_line):
   flu_count = 0
   virus_count = 0
   death_count = 0
   term_counts = []

   current_line = current_line.lower()
   words = current_line.split()
   for word in words:
      word = stripper(word)
      if re.search("^flu$", word):
         flu_count = flu_count + 1
      if re.search("^virus$", word):
         virus_count = virus_count + 1
      if re.search("^death$", word):
         death_count = death_count + 1
   
   term_counts.append(flu_count)
   term_counts.append(virus_count)
   term_counts.append(death_count)
   return term_counts

# function to sum dollar amounts
def sum_dollars(current_line):
   total = 0.00
   dollars = re.findall("\$[0-9,]+", current_line)
  
   # strip dollar amounts of their symbols and add them up
   for amount in dollars:
      amount = amount[1:]
      if re.search("[^0-9]", amount[len(amount)-1]):
         amount = amount[:len(amount)-1]
      amount = float(re.sub(",", '', amount))
      total = total + amount
   return total

# function for sentiment analysis
def get_sentiment(sentence):
  try:
    analyzer = SentimentIntensityAnalyzer()
  
    vs = analyzer.polarity_scores(sentence)

    return(vs['compound'])
  except:
    return -1



##==================================================================##

# ╔════════•●•════════╗ #
#**#  Program Start  #**#
# ╚════════•●•════════╝ #

#----------------------------------# 
#  Word frequency for Spanish Flu  #
#----------------------------------#
for line in titles1918:
   line = remove_stopwords(line)
   test.write(line+"\n")
   letters = count_words(line)

   # update word_freq1918 with more letters from the returned list 
   for (key, val) in letters:
      word_freq1918[key] = word_freq1918.get(key, 0) + val

# sort word_freq1918
word_freq1918 = sort_by_frequency(word_freq1918)

#----------------------------#  
#  Word frequency for COVID  #
#----------------------------# 
for line in titles2020:
    line = remove_stopwords(line)
    letters = count_words(line)

    # update word_freq2020 with more letters from the returned list 
    for (key, val) in letters:
       word_freq2020[key] = word_freq2020.get(key, 0) + val

# sort word_freq2020
word_freq2020 = sort_by_frequency(word_freq2020)

##==================================================================##

#----------------------------------------#  
#  Fraction of articles for Spanish Flu  #
#----------------------------------------# 

titles1918.seek(0)
total_lines = 0
term_count = [0, 0, 0]
for line in titles1918:
   terms = term_frequency(line)
   total_lines = total_lines + 1

   # update term_count with more terms from the returned list 
   for index in range(0, 3):
      term_count[index] = term_count[index] + terms[index]

divisor = total_lines / 100
fraction1918["flu"] = round((term_count[0] / divisor), 3)
fraction1918["virus"] = round((term_count[1] / divisor), 3)
fraction1918["death"] = round((term_count[2] / divisor), 3)

#----------------------------------#  
#  Fraction of articles for COVID  #
#----------------------------------# 

titles2020.seek(0)
total_lines = 0
term_count = [0, 0, 0]
for line in titles2020:
   terms = term_frequency(line)
   total_lines = total_lines + 1

   # update term_count with more terms from the returned list 
   for index in range(0, 3):
      term_count[index] = term_count[index] + terms[index]

divisor = total_lines / 100
fraction2020["flu"] = round((term_count[0] / divisor), 3)
fraction2020["virus"] = round((term_count[1] / divisor), 3)
fraction2020["death"] = round((term_count[2] / divisor), 3)

##==================================================================##

#----------------------------------#  
#  Dollar Amounts for Spanish Flu  #
#----------------------------------# 

titles1918.seek(0)
sum = 0
for line in titles1918:
   line_total = sum_dollars(line)
   sum = sum + line_total

# reformat total as a string
if sum.is_integer():
   sum = int(sum)
   sum = '${:,}'.format(sum)
else:
   total = '${:,.2f}'.format(sum)
dollars1918 = sum

#----------------------------#  
#  Dollar Amounts for COVID  #
#----------------------------# 

titles2020.seek(0)
sum = 0
for line in titles2020:
   line_total = sum_dollars(line)
   sum = sum + line_total

# reformat total as a string
if sum.is_integer():
   sum = int(sum)
   sum = '${:,}'.format(sum)
else:
   total = '${:,.2f}'.format(sum)
dollars2020 = sum

##==================================================================##

#-------------------------------------#  
#  Average Sentiment for Spanish Flu  #
#-------------------------------------# 

titles1918.seek(0)
sentiment_sum = 0.0
total_lines = 0
for line in titles1918:
   sentiment = get_sentiment(line)
   sentiment_sum = sentiment_sum + sentiment
   total_lines = total_lines + 1

# calculate average
sentiment1918 = round((sentiment_sum / total_lines), 3)

#-------------------------------#  
#  Average Sentiment for COVID  #
#-------------------------------# 

titles2020.seek(0)
sentiment_sum = 0.0
total_lines = 0
for line in titles2020:
   sentiment = get_sentiment(line)
   sentiment_sum = sentiment_sum + sentiment
   total_lines = total_lines + 1

# calculate average
sentiment2020 = round((sentiment_sum / total_lines), 3)

##==================================================================##

#        ʰ͙ᵉ͙ˡ͙ˡ͙ᵒ͙        
#    Printing Zone    
# ╚════ ≪ °❈° ≫ ════╝ 

print("\nTop 10 most frequent words from articles in 1918:")
for (key,val) in word_freq1918.items():
   print(key+":",val)

print("\nTop 10 most frequent words from articles in 2020:")
for (key,val) in word_freq2020.items():
   print(key+":",val)

print("\n===================================================\n")

print("Fraction of article titles from 1918 that have the terms \"flu\", \"virus\", and \"death\":")
for (key,val) in fraction1918.items():
   print(key+":",val)

print("\nFraction of article titles from 2020 that have the terms \"flu\", \"virus\", and \"death\":")
for (key,val) in fraction2020.items():
   print(key+":",val)

print("\n===================================================\n")

print("Sum of dollar amounts present in article titles from 1918:")
print(dollars1918)

print("\nSum of dollar amounts present in article titles from 2020:")
print(dollars2020)

print("\n===================================================\n")

print("Average Sentiment of articles titles from 1918")
print(sentiment1918)

print("\nAverage Sentiment of articles titles from 2020")
print(sentiment2020,"\n")
