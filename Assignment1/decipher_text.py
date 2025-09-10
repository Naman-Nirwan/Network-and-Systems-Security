# Write your script here
from collections import Counter
import random



from math import log10

class ngram_score(object):
    def __init__(self,ngramfile):
        self.ngrams = {}
        with open(ngramfile, 'r') as file:

            for line in file:
                key,count = line.split(" ") 
                self.ngrams[key] = int(count)
            self.L = len(key)
            self.N = 0
            for key in self.ngrams.keys():
                self.N += self.ngrams[key]
            #calculate log probabilities
        for key in self.ngrams.keys():
            self.ngrams[key] = log10(float(self.ngrams[key])/self.N)
        self.floor = log10(0.01/self.N)

    def score(self,text):
        ''' compute the score of text '''
        score = 0
        ngrams = self.ngrams.__getitem__
        text=text.replace(" ","")
        for i in range(len(text)-self.L+1):
            if text[i:i+self.L] in self.ngrams: score += ngrams(text[i:i+self.L])
            else: 
                score += self.floor
        return abs(score)/len(text)
    

class DecipherText(object): # Do not change this
    def __init__(self):
        self.UPPERLETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def word_pattern(self,word):
        curr=0
        letterNum={}
        word=word.upper()
        wordPattern=""
        for letter in word:
            if letter in letterNum:
                wordPattern+=str(letterNum[letter])+"."
            else:
                letterNum[letter]=curr
                curr+=1
                wordPattern+=str(letterNum[letter])+"."
        return wordPattern

    def loadEnglish(self):
        dictionaryFile = open('./source/submissions/dictionary.txt')
        Words = {}
        for word in dictionaryFile.read().split('\n'):
            Words[word.upper()]=self.word_pattern(word)
        dictionaryFile.close()
        return Words

    def Blank_letter_maping(self):
        return {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [],
            'H': [], 'I': [], 'J': [], 'K': [], 'L': [], 'M': [], 'N': [],
            'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [],
            'V': [], 'W': [], 'X': [], 'Y': [], 'Z': []}

    def analyze_frequency(self,text):
        text = text.replace(" ", "")
        text = text.replace(",", "")
        text = text.replace(";", "")
        text = text.replace("!", "")
        text = text.replace(".", "")
        text=text.replace("\n","")
        return Counter(text)

    def frequency_substitution(self,ciphertext):
        # English letter frequency (ETAOINSHRDLC...)
        english_freq_order = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

        # Analyze cipher frequencies
        cipher_freq_order = [char for char, _ in self.analyze_frequency(ciphertext).most_common()]

        # Generate initial cipher-to-plain mapping
        cipher_to_plain = {cipher: plain for cipher, plain in zip(cipher_freq_order, english_freq_order)}

        # Decode using initial mapping
        def decode(text, mapping):
            decoded = []
            for char in text:
                if char in mapping:
                    decoded.append(mapping[char])
                else:
                    decoded.append(char)  # Keep spaces or symbols
            return ''.join(decoded)

        # Brute force possible mappings (with small cipher text)
        perm =english_freq_order[:len(cipher_freq_order)]
        trial_map = {cipher: plain for cipher, plain in zip(cipher_freq_order, perm)}
        decoded = decode(ciphertext, trial_map)
            
        return decoded,trial_map

    def add_letters_to_mapping(self,letterMapping, word, candidate):
        for i in range(len(word)):
            if candidate[i] not in letterMapping[word[i]]:
                letterMapping[word[i]].append(candidate[i])
        return letterMapping

    def intersect_mappings(self,mapA, mapB):
        intersectedMapping = self.Blank_letter_maping()
        for letter in self.UPPERLETTERS:
            if mapA[letter]==[]:
                intersectedMapping[letter]=mapB[letter]
            elif mapB[letter]==[]:
                intersectedMapping[letter]=mapA[letter]
            else:
                for i in mapA[letter]:
                    if i in mapB[letter]:
                        intersectedMapping[letter].append(i)
        return intersectedMapping

    def removeSolved(self,mapping):
        mask=True
        while mask:
            mask=False
            solvedLetter=[]
            for letter in self.UPPERLETTERS:
                if len(mapping[letter])==1:
                    solvedLetter.append(mapping[letter][0])
            for letter in self.UPPERLETTERS:
                for s in solvedLetter:
                    if len(mapping[letter])!=1 and s in mapping[letter]:
                        mapping[letter].remove(s)
                        if len(mapping[letter])==1:
                            mask=True
        return mapping

    def filter_mapping(self,mapping):
        filtered_mapping=self.Blank_letter_maping()
        assigned_list=list(self.UPPERLETTERS)
        alphabet_list=list(self.UPPERLETTERS)
        for letter in self.UPPERLETTERS:
            if len(mapping[letter])==1 and mapping[letter][0] in alphabet_list:
                filtered_mapping[letter]=mapping[letter]
                alphabet_list.remove(mapping[letter][0])
                assigned_list.remove(letter)
            elif len(mapping[letter])>1:
                for s in mapping[letter]:
                    if s in alphabet_list:
                        alphabet_list.remove(s)
                        filtered_mapping[letter].append(s)
                        assigned_list.remove(letter)
                        break
        for letter in assigned_list:
            filtered_mapping[letter].append(alphabet_list[len(alphabet_list)-1])
            alphabet_list.pop()
        return filtered_mapping

    def decrypt(self,ciphertext):
        ciphertext,trial_map=self.frequency_substitution(ciphertext)
        ciphertext=ciphertext.upper()
        newtext=ciphertext.replace(',','')
        newtext=newtext.replace('.','')
        newtext=newtext.replace('!','')
        newtext=newtext.replace(';','')
        newtext=newtext.replace('\n','')
        word_list=newtext.split(' ')
        Global_mapping=self.Blank_letter_maping()
        dictionary=self.loadEnglish()
        for word in word_list:
            local_mapping=self.Blank_letter_maping()
            wordPattern=self.word_pattern(word)
            for key in dictionary:
                if dictionary[key]==wordPattern:
                    local_mapping=self.add_letters_to_mapping(local_mapping,word,key)
            Global_mapping=self.intersect_mappings(Global_mapping,local_mapping)

        new_mapping=self.removeSolved(Global_mapping)
        decoded_text=""
        filtered_mapping=self.filter_mapping(new_mapping)
        for letter in ciphertext:
            if letter in self.UPPERLETTERS:
                decoded_text+=filtered_mapping[letter][0]
            else:
                decoded_text+=letter
        return filtered_mapping,decoded_text,trial_map

    def decipher(self, ciphertext): # Do not change this
        """Decipher the given ciphertext"""

        # Write your script here
        key,decoded_text,trial_map = self.decrypt(ciphertext)
    # Score decoded text
        fitness = ngram_score('./source/submissions/english_quadgrams.txt')
        best_score=fitness.score(decoded_text)
        i=0
        while i<=1500:
            ij=random.sample(list(self.UPPERLETTERS),2)
            new_key=key.copy()
            new_key[ij[0]],new_key[ij[1]]=new_key[ij[1]],new_key[ij[0]]
            ik=[new_key[ij[0]][0],new_key[ij[1]][0]]
            new_text=decoded_text
            new_text=new_text.replace(ik[0],"#")
            new_text=new_text.replace(ik[1],ik[0])
            new_text=new_text.replace("#",ik[1])
            new_score=fitness.score(new_text)
            if new_score<best_score:
                best_score=new_score
                key=new_key
                decoded_text=new_text
                i=0
            else:
                i+=1
        for letter in trial_map:
            trial_map[letter]=key[trial_map[letter]][0]
        deciphered_key = ""
        for letter in trial_map:
            key[trial_map[letter]][0]=letter
        for letter in self.UPPERLETTERS:
            deciphered_key+=key[letter][0]
        deciphered_text = ''.join(decoded_text)

        print("Ciphertext: " + ciphertext) # Do not change this
        print("Deciphered Plaintext: " + deciphered_text) # Do not change this
        print("Deciphered Key: " + deciphered_key) # Do not change this

        return deciphered_text, deciphered_key # Do not change this

if __name__ == '__main__': # Do not change this
    decipher=DecipherText() # Do not change this
