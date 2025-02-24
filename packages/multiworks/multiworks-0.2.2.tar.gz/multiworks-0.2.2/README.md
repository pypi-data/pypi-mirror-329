multiworks Module

The multiworks module provides various utility functions, including text encryption/decryption and fun interactive games.
Below are the detailed descriptions of the available functions:

enc Function

The enc function encrypts a given plaintext message using a custom algorithm. This function is ideal for 
obfuscating sensitive information before storing or transmitting it.

How to Use

Import the module:


import multiworks


message = "Hello, World!"
encrypted_message = multiworks.enc(message)
print(f"Encrypted Message: {encrypted_message}")


dec Function

The dec function decrypts a previously encrypted message back into its original plaintext form.
 This function is essential for reading messages that were encrypted using the enc function.

How to Use

Import the module:


import multiworks

Decrypt a message:

encrypted_message = "EncryptedMessageHere"
decrypted_message = multiworks.dec(encrypted_message)
print(f"Decrypted Message: {decrypted_message}")

RPS Function

The RPS function is a classic game of Rock, Paper, Scissors. This timeless game is a great 
way to settle simple disputes or just have some fun. Each choice beats one of the other two options:

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

Example

import multiworks

result = multiworks.RPS() 
print(result) # Start the game

SWG Function

The SWG function is a simple, fun, and interactive game inspired by the classic rock-paper-scissors. 
In this game, you have three choices: Snake, Water, and Gun. Each choice beats one of the other two options:

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

Example

import multiworks

result = multiworks.SWG()
print(result)  # Start the game

Summary

The multiworks module's enc and dec functions provide a straightforward way to secure your messages through encryption and decryption. Additionally, the module includes the RPS and SWG functions for some lighthearted entertainment. These functions are easy to use and integrate into your projects, ensuring that your sensitive information remains protected and offering a fun diversion when needed.

