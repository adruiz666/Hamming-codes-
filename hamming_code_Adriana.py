#!/usr/bin/env python3

from enum import Enum
from typing import List, Tuple, Union


# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE

class HCResult(Enum):
    """
    Return codes for the Hamming Code interface
    """
    VALID = 'OK'
    CORRECTED = 'FIXED'
    UNCORRECTABLE = 'ERROR'


class HammingCode:
    """
    Provides decoding capabilities for the specified Hamming Code
    """

    def __init__(self):
        """
        Initializes the class HammingCode with all values necessary.
        """
        self.total_bits = 10  # n
        self.data_bits = 6  # k
        self.parity_bits = 5  # r

        # Predefined non-systematic generator matrix G'
        g_p = [[1, 1, 1, 0, 0, 0, 0, 1, 0, 0],
               [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
               [1, 0, 0, 1, 0, 1, 0, 0, 0, 0],
               [0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
               [1, 1, 0, 1, 0, 0, 0, 1, 1, 0],
               [1, 0, 0, 1, 0, 0, 0, 1, 0, 1]]

        # Convert non-systematic G' into systematic matrices G, H
        self.g = self.__convert_to_g(g_p)
        self.h = self.__derive_h(self.g)

    def __convert_to_g(self, g_p: List):
        """
        Converts a non-systematic generator matrix into a systematic

        Args:
            gns (List): Non-systematic generator matrix
        Returns:
            list: Converted systematic generator matrix
        """
        #Subtract row 1 from: row 3, row 5, row 6
        g_p[2]= [a ^ b for a, b in zip(g_p[0], g_p[2])]
        g_p[4]= [a ^ b for a, b in zip(g_p[0], g_p[4])]
        g_p[5]= [a ^ b for a, b in zip(g_p[0], g_p[5])]
        
        #Subtract row 2 from: row 1, row 3, row 6
        g_p[0]= [a ^ b for a, b in zip(g_p[1], g_p[0])]
        g_p[2]= [a ^ b for a, b in zip(g_p[1], g_p[2])]
        g_p[5]= [a ^ b for a, b in zip(g_p[1], g_p[5])]
        
        #Subtract row 3 from: row 1, row 5, row 6
        g_p[0]= [a ^ b for a, b in zip(g_p[2], g_p[0])]
        g_p[4]= [a ^ b for a, b in zip(g_p[2], g_p[4])]
        g_p[5]= [a ^ b for a, b in zip(g_p[2], g_p[5])]
        
        #Subtract row 4 from: row 1, row 3
        g_p[0]= [a ^ b for a, b in zip(g_p[3], g_p[0])]
        g_p[2]= [a ^ b for a, b in zip(g_p[3], g_p[2])]
        
        #Subtract row 5 from: row 2, row 3
        g_p[1]= [a ^ b for a, b in zip(g_p[4], g_p[1])]
        g_p[2]= [a ^ b for a, b in zip(g_p[4], g_p[2])]
        
        #Subtract row 6 from: row 1, row 2, row 5
        g_p[0]= [a ^ b for a, b in zip(g_p[5], g_p[0])]
        g_p[1]= [a ^ b for a, b in zip(g_p[5], g_p[1])]
        g_p[4]= [a ^ b for a, b in zip(g_p[5], g_p[4])]

        # REPLACE "pass" WITH YOUR IMPLEMENTATION
        #print("G=")        
        
        return g_p


    def __derive_h(self, g: List):
        """
        This method executes all steps necessary to derive H from G.

        Args:
            g (List):
        Returns:
            list:        """
        h = []
        for i in range(len(self.g[0])):
            row = []
            for item in self.g:
                row.append(item[i])
            h.append(row)

        H = h[6:]
        H[0].extend([1, 0, 0, 0])
        H[1].extend([0, 1, 0, 0])
        H[2].extend([0, 0, 1, 0])
        H[3].extend([0, 0, 0, 1])

        return H

    def encode(self, source_word: Tuple[int, ...]) -> Tuple[int, ...]:
        """
        Encodes the given word and returns the new codeword as tuple.

        Args:
            source_word (tuple): m-tuple (length depends on number of data bits)
        Returns:
            tuple: n-tuple (length depends on number of total bits)
        """
        if len(source_word) == len(self.g):
            encoded_word = []
            for i in range(len(self.g[0])):
                mult = 0
                for j in range(len(source_word)):
                    mult += source_word[j] * self.g[j][i]
                if mult %2 == 0:
                    encoded_word.append(0)
                else:
                    encoded_word.append(1)
            if sum(encoded_word) %2 == 0:
                encoded_word.append(1)
            else:
                encoded_word.append(0)
            encoded_word = tuple(encoded_word)
        else:
            print("Incorrect length of source word \n"
                  f"Given word's length = {len(source_word)}, it should be = {len(self.g)}")
            encoded_word = ()

        return encoded_word

    def decode(self, encoded_word: Tuple[int, ...]) -> Tuple[Union[None, Tuple[int, ...]], HCResult]:
        """
        Checks the channel alphabet word for errors and attempts to decode it.
        Args:
            encoded_word (tuple): n-tuple (length depends on number of total bits)
        Returns:
            Union: (m-tuple, HCResult) or (None, HCResult)(length depends on number of data bits)
        """

        lis = list(encoded_word[0:self.total_bits])
        decodedlist = []
        decoded_word = ()
        for i in range(len(self.h)):
            product_res = 0
            for j in range(len(self.h[0])):
                product_res += lis[j] * self.h[i][j]

            if product_res %2 != 0:
                decodedlist.append(1)

            else:
                decodedlist.append(0)

            if sum(decodedlist) == 0:
                decoded_word = encoded_word[0:self.data_bits]
                mess = HCResult.VALID
                
            else:
                transposed_h = list(map(list, zip(*self.h)))
                matching_index_list = []
                for r in range(len(transposed_h)):
                    if decodedlist == transposed_h[r]:
                        matching_index_list.append(r)
                        if lis[r] == 0:
                            lis[r] = 1
                        else:
                            lis[r] = 0
                        
                    else:
                       pass
                   
                if matching_index_list != []:
                    decoded_word = lis
                    decoded_word[matching_index_list[0]] = ~ decoded_word[matching_index_list[0]]
                    decoded_word = tuple(decoded_word[:self.data_bits])
                    mess = HCResult.CORRECTED
                else:
                    decoded_word = None
                    mess = HCResult.UNCORRECTABLE

        return (decoded_word, mess)
