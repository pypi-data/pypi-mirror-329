def enc_dce_help():
    print('''
        This Python program allows you to:

1. Encode a given text using a custom character mapping.

2. Decode the encoded text back to its original form using a reverse mapping dictionary.

The encoding function replaces each character in the input string with its corresponding mapped value,
while the decoding function reverses this process, ensuring accurate retrieval of the original text.\n''')

def enc(afx2):
    char_Small = {
        'a': "ums", 'b': "sye", 'c': "oisun", 'd': "omai", 'e': "use", 
        'f': "ntv", 'g': "bne", 'h': "9nr", 'i': "net", 'j': "i7re", 
        'k': "usr", 'l': "n76", 'm': "uyia", 'n': "opm", 'o': "ae", 
        'p': "uia", 'q': "un27", 'r': "ioa7", 's': "br4", 't': "bba", 
        'u': "4v4t", 'v': "br4t", 'w': "5b5", 'x': "rdve4", 'y': "bt5", 
        'z': "dg5",
        'A': 'ef', 'B': 'hjh', 'C': 'efg', 'D': 'hrg', 'E': 'fse6', 
        'F': 'ms8', 'G': 'jh4', 'H': '8shf', 'I': 'wir', 'J': 'jd8', 
        'K': 'js7', 'L': 'ns23', 'M': 'wiu0', 'N': 'nc4r', 'O': '7h3', 
        'P': 'dfg', 'Q': 'j8k', 'R': 'sfkl', 'S': 'jk3', 'T': 'kla', 
        'U': 'vdj', 'V': 'd9d', 'W': 'nd4', 'X': 'k3m', 
        'Y': 'lwj', 'Z': 'klne',
        ' ': 'jhis'
    }

    def custom_replace_characters(input_string, char_mapping):
        result = []
        for char in input_string:
            if char in char_mapping:
                result.append(char_mapping[char])
            else:
                result.append(char)
        return ''.join(result)

    # Perform replacement once and store the result
    replaced_ax = custom_replace_characters(afx2, char_Small)
    
      # Print output
    return replaced_ax  # Return the value


def dec(afx):
    char_Small = {
        'a': "ums", 'b': "sye", 'c': "oisun", 'd': "omai", 'e': "use", 
        'f': "ntv", 'g': "bne", 'h': "9nr", 'i': "net", 'j': "i7re", 
        'k': "usr", 'l': "n76", 'm': "uyia", 'n': "opm", 'o': "ae", 
        'p': "uia", 'q': "un27", 'r': "ioa7", 's': "br4", 't': "bba", 
        'u': "4v4t", 'v': "br4t", 'w': "5b5", 'x': "rdve4", 'y': "bt5", 
        'z': "dg5",
        'A': 'ef', 'B': 'hjh', 'C': 'efg', 'D': 'hrg', 'E': 'fse6', 
        'F': 'ms8', 'G': 'jh4', 'H': '8shf', 'I': 'wir', 'J': 'jd8', 
        'K': 'js7', 'L': 'ns23', 'M': 'wiu0', 'N': 'nc4r', 'O': '7h3', 
        'P': 'dfg', 'Q': 'j8k', 'R': 'sfkl', 'S': 'jk3', 'T': 'kla', 
        'U': 'vdj', 'V': 'd9d', 'W': 'nd4', 'X': 'k3m', 
        'Y': 'lwj', 'Z': 'klne',
        ' ': 'jhis'
    }

    reverse_char_Small = {v: k for k, v in char_Small.items()}

    def decode_string(encoded_string, reverse_mapping):
        result = []
        i = 0
        while i < len(encoded_string):
            for length in range(1, 8):  
                substr = encoded_string[i:i+length]
                if substr in reverse_mapping:
                    result.append(reverse_mapping[substr])
                    i += length
                    break
            else:
                result.append(encoded_string[i])
                i += 1
        return ''.join(result)

    decoded_string = decode_string(afx, reverse_char_Small)
      # Keep this if you want to see output
    return decoded_string  # Add return statement


def RAN(upper_limit):
    if upper_limit < 0 or upper_limit > 9:
        return None

    seed = id(object()) + (upper_limit * 123456789)
    seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF

    digit = seed % (upper_limit + 1)
    return digit

def SWG_help():
    print('''
        SWG() Function

The SWG() function is a simple, fun, and interactive game inspired by the classic rock-paper-scissors. In this game,
you have three choices: Snake, Water, and Gun. Each choice beats one of the other two options:

Snake (0): Snake drinks Water but is shot by Gun.
Water (1): Water douses Gun but is drunk by Snake.
Gun (2): Gun shoots Snake but is doused by Water.
        
How to Play
        
Call the SWG() function to start the game.
The function will prompt you to choose between Snake, Water, and Gun.
        
Enter your choice as follows:
0 for Snake
1 for Water
2 for Gun
        
The function will then randomly select its own choice.
The function will compare the two choices and determine the winner based on the rules above.
The result of the game will be displayed, showing whether you won, lost, or if it was a tie.

Enjoy playing Snake, Water, Gun and may the best choice win!\n''')

def SWG():
    SWG_choice = int(input("\n0 for Snake, 1 for Water, 2 for Gun: "))
    RAN_digit = RAN(2)

    def check(RAN, SWG):
        if RAN == SWG:
            return 0  
        if (RAN == 0 and SWG == 1) or (RAN == 1 and SWG == 2) or (RAN == 2 and SWG == 0):
            return -1
        return 1

    score = check(RAN_digit, SWG_choice)

    print("\nYou:", SWG_choice)
    print("Computer:", RAN_digit)

    if score == 0:
        print("It's a Draw\n")
    elif score == -1:
        print("You Lose\n")
    else:
        print("You Won\n")

def RPS_help():
    print('''
        RPS() Function

The RPS() function is a classic game of Rock, Paper, Scissors. This timeless game is a great way to settle simple disputes or just have some fun.

Each choice beats one of the other two options:

Rock (0): Rock crushes Scissors but is covered by Paper.
Paper (1): Paper covers Rock but is cut by Scissors.
Scissors (2): Scissors cut Paper but are crushed by Rock.
        
How to Play
        
Call the RPS() function to start the game.
The function will prompt you to choose between Rock, Paper, and Scissors.
        
Enter your choice as follows:
0 for Rock
1 for Paper
2 for Scissors
        
The function will then randomly select its own choice.
The function will compare the two choices and determine the winner based on the rules above.
The result of the game will be displayed, showing whether you won, lost, or if it was a tie.

Enjoy playing Rock, Paper, Scissors and may the best choice win!\n''')

def RPS():
    RPS_choice = int(input("\n0 for Rock, 1 for Paper, 2 for Scissor: "))
    RAN_digit = RAN(2)

    def check(RAN, RPS):
        if RAN == RPS:
            return 0  
        if (RAN == 0 and RPS == 1) or (RAN == 2 and RPS == 1) or (RAN == 0 and RPS == 2) or (RAN == 1 and RPS == 0):
            return -1
        return 1

    score = check(RAN_digit, RPS_choice)

    print("\nYou:", RPS_choice)
    print("Computer:", RAN_digit)

    if score == 0:
        print("It's a Draw\n")
    elif score == -1:
        print("You Lose\n")
    else:
        print("You Won\n")





































# f = open('multiworks/file.txt','r')
# text = f.read()
# b = enc(text)
# print(b)
# f2 = open('multiworks/file.txt','w')
# f2.write(str(b))
# f2.close()



# f = open('multiworks/file.txt','r')
# text = f.read()
# b = dec(text)
# print(b)
# f2 = open('multiworks/file.txt','w')
# f2.write(str(b))
# f2.close()



# h = enc("Whats Up?")
# print(h)
# print(dec(h))