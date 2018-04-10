import argparse

import enchant
import re


def get_spelling_error_rate(text):
  alpha_numeric = re.compile('[^a-zA-Z0-9]')
  words = text.split()
  dictionary = enchant.Dict('en_US')
  total_words = len(words)
  print('Total words      : ' + str(total_words))
  incorrect_words = 0
  for word in words:
    word = alpha_numeric.sub('', word)
    if(word):
      real_word = dictionary.check(word)
      if(real_word == False):
        incorrect_words += 1
  print('Incorrect words  : ' + str(incorrect_words))
  error_percentage = (float(incorrect_words)/float(total_words))*100
  print('Error percentage : ' + str(error_percentage) + '%')
  return error_percentage


def main():

  # collecting command line arguments
  parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('--file', type=str, default='./data/tinyshakespeare/input.txt',
                      help='file to spell check')
  args = parser.parse_args()

  file = open(args.file, 'r')
  text = file.read()
  get_spelling_error_rate(text)

if __name__ == '__main__':
    main()
