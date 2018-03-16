import argparse
import os
import sample
import phonetics

def main():
  parser = argparse.ArgumentParser(
                       formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('--save_dir', type=str, default='save',
                        help='model directory to store checkpointed models')
  parser.add_argument('-n', type=int, default=500,
                        help='number of characters to sample')
  parser.add_argument('--prime', type=str, default=' ',
                        help='prime text')
  parser.add_argument('--sample', type=int, default=1,
                        help='0 to use max at each timestep, 1 to sample at '
                             'each timestep, 2 to sample on spaces')
  parser.add_argument('--artist_name', type=str, default='Artist_Name',
                        help='A file to save the outputed text in')
  parser.add_argument('--details', type=str, default='_not_supplied_',
                        help='A file to save the outputed text in')

  args = parser.parse_args()
  generated_text = sample.sample(args.save_dir, args.n, args.prime, args.sample, args.artist_name, args.details)
  process_text(generated_text, args.artist_name, args.details, args.n)


def process_text(generated_text, artist_name, details, sample_size):
    output_text_directory = create_directory(artist_name, sample_size)
    output_file_name = output_text_directory + '/' + details + '.txt'
    ipa_file_name = output_file_name + '.ipa'
    output_file = open(output_file_name, 'w+')
    ipa_file = open(ipa_file_name, 'w+')
    output_file.write(generated_text)
    ipa_text = phonetics.get_phonetic_transcription(generated_text.decode('utf-8'))
    ipa_file.write(ipa_text)


def create_directory(artist_name, sample_size):
    #Experiment results are stored by artist and then by the size of the output
    directory_name = 'Experiment Outcomes/'+ artist_name + '/' + str(sample_size);
    if not os.path.exists(directory_name):
      os.makedirs(directory_name)
    return directory_name

if __name__ == '__main__':
    main()