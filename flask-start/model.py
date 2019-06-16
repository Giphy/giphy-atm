import pickle
import tensorflow as tf
import numpy as np
import random


class RNNModel(object):
    @staticmethod
    def pick_word(probabilities, int_to_vocab):
        """
        Pick the next word with some randomness
        :param probabilities: Probabilites of the next word
        :param int_to_vocab: Dictionary of word ids as the keys and words as the values
        :return: String of the predicted word
        """
        return np.random.choice(list(int_to_vocab.values()), 1, p=probabilities)[0]


    def generate(self, prime_words, gen_length):
        print('call_model prime_words: {}'.format(prime_words))
        print('call_model gen_length: {}'.format(gen_length))

        loaded_graph = tf.Graph()
        with tf.Session(graph=loaded_graph) as sess:
            final_chapter_text = ''

            # Load the saved model
            loader = tf.train.import_meta_graph(self.save_dir + '.meta')
            loader.restore(sess, self.save_dir)

            # Get tensors from loaded graph
            input_text = loaded_graph.get_tensor_by_name('input:0')
            initial_state = loaded_graph.get_tensor_by_name('initial_state:0')
            final_state = loaded_graph.get_tensor_by_name('final_state:0')
            probs = loaded_graph.get_tensor_by_name('probs:0')

            for prime_word in prime_words.split(','):
                if not prime_word in self.vocab_to_int:
                    prime_word = random.choice(['why', 'and', 'so', 'again'])

                print('PRIME WORD: {}'.format(prime_word))

                # Sentences generation setup
                gen_sentences = prime_word.split()
                prev_state = sess.run(
                    initial_state, {input_text: np.array([[1 for word in gen_sentences]])})

                # Generate sentences
                for n in range(gen_length):
                    # Dynamic Input
                    dyn_input = [[self.vocab_to_int[word]
                                  for word in gen_sentences[-self.seq_length:]
                                  if word in self.vocab_to_int]]

                    dyn_seq_length = len(dyn_input[0])

                    # Get Prediction
                    probabilities, prev_state = sess.run(
                        [probs, final_state],
                        {input_text: dyn_input, initial_state: prev_state})

                    pred_word = self.pick_word(
                        probabilities[0][dyn_seq_length-1], self.int_to_vocab)

                    gen_sentences.append(pred_word)

                # Remove tokens
                chapter_text = ' '.join(gen_sentences)
                for key, token in self.token_dict.items():
                    chapter_text = chapter_text.replace(' ' + token.lower(), key)

                final_chapter_text += '\n{}'.format(chapter_text)

            return final_chapter_text


class Model560Epocs(RNNModel):
    save_dir = '/code/flask-start/models/whitman/epochs_560/save'
    corpus_int, vocab_to_int, int_to_vocab, token_dict = pickle.load(
        open('/code/flask-start/models/whitman/epochs_560/preprocess.p', mode='rb'))
    seq_length, _ = pickle.load(
        open('/code/flask-start/models/whitman/epochs_560/params.p', mode='rb'))


class Model10kEpocs(RNNModel):
    save_dir = '/code/flask-start/models/whitman/epochs_10k/save'
    corpus_int, vocab_to_int, int_to_vocab, token_dict = pickle.load(
        open('/code/flask-start/models/whitman/epochs_10k/preprocess.p', mode='rb'))
    seq_length, _ = pickle.load(
        open('/code/flask-start/models/whitman/epochs_10k/params.p', mode='rb'))
