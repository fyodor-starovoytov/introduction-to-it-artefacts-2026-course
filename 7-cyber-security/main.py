import dictionary_attack
import hashlib

userInput = input("Give me a password: ")
print(dictionary_attack.crack_sha1(hashlib.sha1(userInput.encode()).hexdigest()))

