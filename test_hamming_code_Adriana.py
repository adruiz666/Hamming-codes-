#!/usr/bin/env python3

import unittest
from hamming_code_Adriana import HCResult, HammingCode

decode = [(0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1),
          (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
          (1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0),
          (1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0)]

encode = [(0, 1, 1, 0, 1, 1),
          (0, 0, 0, 0, 0, 0),
          (1, 0, 1, 1, 0, 1),
          (1, 1, 1, 1, 1, 0)]


corrected_input = (0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0)
corrected_input_res = ((0, 0, 1, 1, 0, 1), 'CORRECTED')

uncorrectable_input = (1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1)
uncorrectable_input_res = (None, 'UNCORRECTABLE')

class TestHammingCode(unittest.TestCase):
    def test_instance(self):
        """ Essential: Test class instantiation """
        #self.fail('implement me!')

    def test_decode_valid(self):
        """ Essential: Test method decode() with VALID input """
        valid_decode_results = []
        for codes in decode:
            valid_decode_results.append(HammingCode().decode(encoded_word=codes))

        print('\n DECODE VALID:')
        for i in range(len(valid_decode_results)):
            if (valid_decode_results[i][0]==encode[i]):
             print('\n DECODED WORD= ',decode[i]) 
             print("\n RESULT= ", valid_decode_results[i])
             #self.fail('implement me!')

    def test_decode_corrected(self):
        """ Essential: Test method decode() with CORRECTED input """   

        decode_corrected_res = HammingCode().decode(encoded_word=corrected_input)
        if (decode_corrected_res == corrected_input_res):
             print('\n DECODE CORRECTED: ')
         #print(f"input_word = {corrected_input}, obtained = {decode_corrected_res}, real_answer = {corrected_input_res}")
         print('\n CORRECTED= ', corrected_input) 
         print("\n RESULT= ", decode_corrected_res)
         print("\n ORIGINAL= ", corrected_input_res)

        #self.fail('implement me!')

    def test_decode_uncorrectable(self):
        """ Essential: Test method decode() with UNCORRECTABLE input """
        decode_uncorrectable_res = HammingCode().decode(encoded_word=uncorrectable_input)
        if (decode_uncorrectable_res == uncorrectable_input_res):
            print('\n DECODE UNCORRECTABLE:')
            print('\n UNCORRECTABLE WORD= ', uncorrectable_input)
            print('\n RESULT=',uncorrectable_input_res)

        #self.fail('implement me!')

    def test_encode(self):
        """ Essential: Test method encode() """
        valid_encode_results = []
        for code in encode:
            valid_encode_results.append(HammingCode().encode(source_word=code))

        print('\n ENCODE')
        for i in range(len(valid_encode_results)):
              print('\n ENCODED WORD= ',encode[i]) 
              if (valid_encode_results[i]==decode[i]):
               print("\n RESULT= ", valid_encode_results[i])
             
        #self.fail('implement me!')
if __name__ == '__main__':
    unittest.main()
