import brute_force_attack
import hashlib

userInput = input("Give me a password: ")
print(brute_force_attack.crack_sha1(hashlib.sha1(userInput.encode()).hexdigest()))

