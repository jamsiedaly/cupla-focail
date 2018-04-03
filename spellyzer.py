import enchant
import re

def get_spelling_error_rate(text):
  regex = re.compile('[^a-zA-Z0-9]')
  words = text.split()
  dictionary = enchant.Dict('en_US')
  total_words = len(words)
  print('Total words      : ' + str(total_words))
  incorrect_words = 0
  for word in words:
    word = regex.sub('', word)
    if(word):
      real_word = dictionary.check(word)
      if(real_word == False):
        incorrect_words += 1
  print('Incorrect words  : ' + str(incorrect_words))
  error_percentage = (float(incorrect_words)/float(total_words))*100
  print('Error percentage : ' + str(error_percentage) + '%')
  return error_percentage

def main():
  get_spelling_error_rate('What are you looking at Jabrony')

if __name__ == '__main__':
    main()
