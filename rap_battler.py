from __future__ import print_function
import tensorflow as tf

import phonetics
import spellyzer

import argparse
import os
from six.moves import cPickle

from model import Model

from six import text_type

import pyttsx

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--sample', type=int, default=1,
                        help='0 to use max at each timestep, 1 to sample at '
                             'each timestep, 2 to sample on spaces')
    parser.add_argument('--turns', type=int, default=5,
                        help='Number of turns the game will play out')

    args = parser.parse_args()
    engine = pyttsx.init()

    save_dir='save'
    with open(os.path.join(save_dir, 'config.pkl'), 'rb') as f:
        saved_args = cPickle.load(f)
        model = Model(saved_args, training=False)

    print('Lay some bars... \n')
    for i in range(args.turns):
        input = get_input()
        raw_text = battle(input, args.sample, model)
        output = format_text(raw_text)
        for i in range(2):
            print(output[i])
            engine.say(output[i])
            bug = engine.runAndWait()

model = None

def battle(prime, sample, model):
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

def get_input():
    text1 = raw_input("\n")
    text2 = raw_input("")
    text = text1 + text2
    return text

def format_text(text):
    lines = text.splitlines()
    valid_lines = []
    for line in lines:
        if line != '':
            valid_lines.append(line)
    valid_lines.pop(0)
    return valid_lines

if __name__ == '__main__':
    main()

