from __future__ import print_function

import argparse
import os
import time

import tensorflow as tf
from fabulous import image
from fabulous import text
from fabulous.color import bold, red, blue, green
from model import Model
from six.moves import cPickle


def openscreen():

    clear_screen = chr(27) + "[2J"
    biggie = image.Image('./img/Biggie.jpg', width=75)
    biggie_in_lines = str(biggie).splitlines()
    tabbed_biggie = ''
    for line in biggie_in_lines:
        line = '\t\t\t\t\t\t' + line
        tabbed_biggie = tabbed_biggie + line + '\n'
    message = bold('''\t\t\t\t\t\t\t\t\tRap Battler by James Daly.
        \t\t\t\t\t\tWhen  you type a line hit enter to move to the next line.
        \t\t\t\t\t\tYou and the AI will take turns writing two lines at a time.''')
    lay_bars = text.Text("Lay some bars...", color="#ff8800", shadow=True, skew=0)
    gap = '\n\n'


    print(clear_screen)
    print(tabbed_biggie)
    print(message)
    print(lay_bars)
    print(gap)

def usersTurn(split_lines):
    you = text.Text('You:', color='#0022ff', shadow=False, fsize=14)
    print(you)
    input = getInput()
    print(split_lines)
    return input

def getInput():
    text1 = raw_input('\t\t\t\t\t\t\t')
    text2 = raw_input('\t\t\t\t\t\t\t')
    text = text1 + text2
    return text

def generateLyrics(prime, sample, model):
    char_pool_size = 2000
    save_dir = 'save'
    with open(os.path.join(save_dir, 'chars_vocab.pkl'), 'rb') as f:
        chars, vocab = cPickle.load(f)
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        saver = tf.train.Saver(tf.global_variables())
        ckpt = tf.train.get_checkpoint_state(save_dir)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            generated_text = model.sample(sess, chars, vocab, char_pool_size, prime, sample).encode('utf-8')
            return generated_text

def formatText(text):
    lines = text.splitlines()
    valid_lines = []
    for line in lines:
        if line != '':
            valid_lines.append(line)
    valid_lines.pop(0)
    return valid_lines

def aisTurn(output, indent, split_lines):
    print(text.Text('AI:', color='#ff2200', shadow=False, fsize=14))
    for i in range(2):
        print((indent + output[i]))
        time.sleep(0.5)
    print(split_lines)
    time.sleep(0.5)

def playAgain():
    answered = False
    answer = raw_input(text.Text("Play again? yes or no", color="ffffff", shadow=False, skew=6))
    answer = answer.lower()
    having_fun = False
    if answer == 'yes' or answer == 'y':
        having_fun = True
        answered = True
    elif answer == 'no' or answer == 'n':
        having_fun = False
        answered = True
    else:
        while not answered:
            answer = raw_input('Please answer yes or no!\t')
            if answer == 'yes' or answer == 'y':
                having_fun = True
                answered = True
            elif answer == 'no' or answer == 'n':
                having_fun = False
                answered = True
    return having_fun


def main():

    #collecting command line arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--sample', type=int, default=1,
                        help='0 to use max at each timestep, 1 to sample at '
                             'each timestep, 2 to sample on spaces')
    parser.add_argument('--turns', type=int, default=10,
                        help='Number of turns the game will play out')
    args = parser.parse_args()

    #loading up the model
    save_dir='save'
    with open(os.path.join(save_dir, 'config.pkl'), 'rb') as f:
        saved_args = cPickle.load(f)
        model = Model(saved_args, training=False)

    #formatting of screen text
    indent = '\t' * 7
    split_lines = '\n\n' + bold(green(indent + ('_' * 140))) + '\n\n'

    having_fun = True
    while(having_fun):
        openscreen()
        for i in range(args.turns):
            input = usersTurn(split_lines)
            raw_text = generateLyrics(input, args.sample, model)
            output = formatText(raw_text)
            aisTurn(output, indent, split_lines)
        having_fun = playAgain()


if __name__ == '__main__':
    main()