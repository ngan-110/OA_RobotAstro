from ctypes import pointer
from typing import Pattern, Union, Tuple, List, Dict, Any

import numpy as np
import numpy.typing as npt

"""
Some type annotations
"""
Numeric = Union[float, int, np.number, None]


"""
Global list of parts of speech
"""
POS = ['ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM',
       'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'X']

"""
Utility functions for reading files and sentences
"""
def read_sentence(f):
    sentence = []
    while True:
        line = f.readline()
        if not line or line == '\n':
            return sentence
        line = line.strip()
        word, tag = line.split("\t", 1)
        sentence.append((word, tag))

def read_corpus(file):
    f = open(file, 'r', encoding='utf-8')
    sentences = []
    while True:
        sentence = read_sentence(f)
        if sentence == []:
            return sentences
        sentences.append(sentence)

""" Courtesy of Ed post HW4: Pretty Print Onew Output#1310 """
def pretty_print(Onew):
    maxLen = 0
    for key in Onew.keys():
        maxLen = max(len(key), maxLen)

    form = "{:"+str(maxLen)+"}" + ("\t{}" * len(POS))
    print(form.format(*(["WORD"] + POS)))

    for key in Onew.keys():
        print_statement = [key] + list(np.round(Onew[key], 2).astype(str))
        print(form.format(*(print_statement)))

"""
3.1: Supervised learning
Param: data is a list of sentences, each of which is a list of (word, POS) tuples
Return: P(X0), 1D array; Tprob, 2D array; Oprob, dictionary {word:probabilities} 
"""
def learn_model(data:List[List[Tuple[str]]]
                ) -> Tuple[npt.NDArray, npt.NDArray, Dict[str,npt.NDArray]]:
    PX_0 = np.zeros(len(POS))
    Tprob = np.zeros((len(POS), len(POS)))
    Oprob = {}
    sum_Oprob = np.zeros(len(POS))
    
    for f in data:  
        word_count = 0   
        for word in f:
            if (word_count == 0):
                prev = POS.index(word[1])
                PX_0[POS.index(word[1])] += 1
            else:
                Tprob[POS.index(word[1]),prev ] += 1
            prev = POS.index(word[1])
            if word[0] not in Oprob:
                Oprob[word[0]] = np.zeros(len(POS))
            Oprob[word[0]][POS.index(word[1])] += 1
            sum_Oprob[POS.index(word[1])] += 1
            word_count += 1
    # Normalize
    PX_0 = PX_0 / np.sum(PX_0)  
    Tprob = Tprob / np.sum(Tprob)
    for key_word in Oprob:
        for j in range(len(POS)):
            if (Oprob[key_word][j] != 0):
                Oprob[key_word][j] = Oprob[key_word][j] / sum_Oprob[j]
    return PX_0, Tprob, Oprob


"""
3.2: Viterbi forward algorithm
Param: P(X0), 1D array; Tprob, 2D array; Oprob, dictionary {word:probabilities}; obs, list of words (strings)
Return: m, 1D array; pointers, 2D array
"""
def viterbi_forward(X0:npt.NDArray, Tprob:npt.NDArray, Oprob:Dict[str,npt.NDArray], obs:List[str]
                    ) -> Tuple[npt.NDArray, npt.NDArray]:
    pointers = np.zeros((len(obs), len(POS)))
    m_ = np.zeros(len(POS))
    m = X0
    for i in range (len(obs)):
        for k in range (len(POS)):
            m_[k] = max(np.multiply(m, Tprob[k]))
        if obs[i] not in Oprob:
            m = m_
        else:
            m = np.multiply(Oprob[obs[i]], m_)
        for k in range (len(m_)):
            pointers[i][k] = np.argmax(np.multiply(m, Tprob[k]))
    return m, pointers

"""
3.2: Viterbi backward algorithm
Param: m, 1D array; pointers, 2D array
Return: List of most likely POS (strings)
"""
def viterbi_backward(m:npt.NDArray,
                     pointers:npt.NDArray
                     ) -> List[str]:
    valuemax = POS[np.argmax(m)]
    sequence = [valuemax]
    max_index = np.argmax(m)
    for i in range (len(pointers) - 2, -1, -1):
        valuemax = POS[int(pointers[i][max_index])]
        sequence.append(valuemax)
        max_index = int(pointers[i][max_index])
    sequence = sequence[::-1]
    return sequence


"""
3.3: Evaluate Viterbi by predicting on data set and returning accuracy rate
Param: P(X0), 1D array; Tprob, 2D array; Oprob, dictionary {word:probabilities}; data, list of lists of (word,POS) pairs
Return: Prediction accuracy rate
"""
def evaluate_viterbi(X0:npt.NDArray, Tprob:npt.NDArray, Oprob:Dict[str,npt.NDArray], data:List[List[Tuple[str]]]
                     ) -> float:
    total = 0
    correct = 0
    for f in data:
        total += len(f)
        obs = []
        real_POS = []
        for word in f:
            obs.append(word[0])
            real_POS.append(word[1])  
        m, pointers = viterbi_forward(X0, Tprob, Oprob, obs)
        sequence = viterbi_backward(m, pointers)
        for i in range (len(sequence)):
            if (sequence[i] == real_POS[i]):
                correct += 1
    accuracy = correct / total     
    return accuracy


"""
3.4: Forward algorithm
Param: P(X0), 1D array; Tprob, 2D array; Oprob, dictionary {word:probabilities}; obs, list of words (strings)
Return: P(XT, e_1:T)
"""
def forward(X0:npt.NDArray,
            Tprob:npt.NDArray,
            Oprob:Dict[str,npt.NDArray],
            obs:List[str]
            ) -> npt.NDArray:

    alpha_k = X0
    for i in range (len(obs)):
        if obs[i] not in Oprob:
            alpha_k =  Tprob @ alpha_k
        else:
            alpha_k = np.multiply(Oprob[obs[i]] , ( Tprob @ alpha_k ))
    return alpha_k

"""
3.4: Backward algorithm
Param: Tprob, 2D array; Oprob, dictionary {word:probabilities}; obs, list of words (strings); k, timestep
Return: P(e_k+1:T | Xk)
"""
def backward(Tprob:npt.NDArray,
             Oprob:Dict[str,npt.NDArray],
             obs:List[str],
             k:int
             ) -> npt.NDArray:

    beta_k = np.ones(len(POS))
    for i in range (len(obs) - 1, k, -1):
        if obs[i] in Oprob:
            beta_k = Tprob.T @ ( np.multiply( Oprob[obs[i]] , beta_k ))
        else:
            beta_k = Tprob.T @ beta_k
    return beta_k

"""
3.4: Forward-backward algorithm
Param: P(X0), 1D array; Tprob, 2D array; Oprob, dictionary {word:probabilities}; obs, list of words (strings); k, timestep
Return: P(Xk | e_1:T)
"""
def forward_backward(X0:npt.NDArray,
                     Tprob:npt.NDArray,
                     Oprob:Dict[str,npt.NDArray],
                     obs:List[str],
                     k:int
                     ) -> npt.NDArray:
    alpha_k = forward(X0, Tprob, Oprob, obs[:k+1])
    beta_k = backward(Tprob, Oprob, obs, k)
    gamma_k = np.multiply(alpha_k,beta_k)
    gamma_k = gamma_k / np.sum(gamma_k)
    return gamma_k


"""
3.5: Expected observation probabilities given data sequence
Param: P(X0), 1D array; Tprob, 2D array; Oprob, dictionary {word:probabilities}; data, list of lists of words
Return: New Oprob, dictionary {word:probabilities}
"""
def expected_emissions(X0:npt.NDArray,
                       Tprob:npt.NDArray,
                       Oprob:Dict[str,npt.NDArray],
                       data:List[List[str]]
                       ) -> Dict[str,npt.NDArray]:
    new_Oprob = {}
    denominator_gamma = np.zeros(len(POS))
    for f in data:
        for k  in range(len(f)):
            gamma_k = forward_backward(X0, Tprob, Oprob, f, k)
            if (f[k] not in new_Oprob):
                new_Oprob[f[k]] = gamma_k
            else:
                new_Oprob[f[k]] = new_Oprob[f[k]] + gamma_k
            denominator_gamma += gamma_k
    for key_word in new_Oprob:
        for k in range (len(POS)):
            if (new_Oprob[key_word][k] != 0):
                new_Oprob[key_word][k] = new_Oprob[key_word][k] / denominator_gamma[k]
    return new_Oprob


if __name__ == "__main__":
    # Run below for 3.3
    train = read_corpus('train.upos.tsv')
    test = read_corpus('test.upos.tsv')
    X0, T, O = learn_model(train)
    print("Train accuracy:", evaluate_viterbi(X0, T, O, train))
    print("Test accuracy:", evaluate_viterbi(X0, T, O, test))

    # Run below for 3.5
    obs = [[pair[0] for pair in sentence] for sentence in [test[0]]]
    Onew = expected_emissions(X0, T, O, obs)
    pretty_print(Onew)
    print(Onew)