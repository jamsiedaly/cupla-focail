from __future__ import print_function
import tensorflow as tf

import phonetics
import spellyzer

import argparse
import os
from six.moves import cPickle

from model import Model

from six import text_type


def main():
    parser = argparse.ArgumentParser(
                       formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--save_dir', type=str, default='save',
                        help='model directory to store checkpointed models')
    parser.add_argument('-n', type=int, default=500,
                        help='number of characters to sample')
    parser.add_argument('--prime', type=text_type, default=' ',
                        help='prime text')
    parser.add_argument('--sample', type=int, default=1,
                        help='0 to use max at each timestep, 1 to sample at '
                             'each timestep, 2 to sample on spaces')
    parser.add_argument('--artist_name', type=str, default='Artist_Name',
                        help='A file to save the outputed text in')
    parser.add_argument('--details', type=str, default='_not_supplied_',
                        help='A file to save the outputed text in')
	

    args = parser.parse_args()
    sample(args.save_dir, args.n, args.prime, args.sample, args.artist_name, args.details)


def sample(save_dir, n, prime, sample, artist_name, details):
    with open(os.path.join(save_dir, 'config.pkl'), 'rb') as f:
        saved_args = cPickle.load(f)
    with open(os.path.join(save_dir, 'chars_vocab.pkl'), 'rb') as f:
        chars, vocab = cPickle.load(f)
    model = Model(saved_args, training=False)
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        saver = tf.train.Saver(tf.global_variables())
        ckpt = tf.train.get_checkpoint_state(save_dir)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            generated_text = model.sample(sess, chars, vocab, n, prime, sample).encode('utf-8')
            print(generated_text)
            output_text_directory = 'Experiment Outcomes/'+ artist_name + '/' + str(n);
            if not os.path.exists(output_text_directory):
                os.makedirs(output_text_directory)
            file_name = output_text_directory + '/' + details + '.txt'
            output_file = open(file_name, 'w+')
            output_file.write(generated_text)
            ipa_file_name = file_name + '.ipa'
            ipa_file = open(ipa_file_name, 'w+')
            ipa_text = phonetics.get_phonetic_transcription(generated_text.decode('utf-8'))
            ipa_file.write(ipa_text)
            spellyzer.get_spelling_error_rate(generated_text)

if __name__ == '__main__':
    main()
