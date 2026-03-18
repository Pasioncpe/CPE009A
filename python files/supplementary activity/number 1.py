def listwords(wordlist, string):
    
    #serves as a back to print for later
    ogsentence = string
    
    #essentially splits the words in the sentence (treats spaces as seperation, so group of characters
    #that has a space in-between is split and given their own index value)
    sentence = string.split()
    
    #continuously checks per index value if the word is in the list, and if so, it would censor it with asterisks that is to the amount of letters in that word.
    for i in range(len(sentence)):
        if sentence[i] in wordlist:
            sentence[i] = "*"*len(sentence[i])
    
    #this joins back all the words with a space in between them back into a string
    sentence = " ".join(sentence)
    
    #prints the original sentence and newly censored sentence
    print("original sentence: ", ogsentence)
    print("censored sentence: ", sentence)


#create a list for the words
wordlist = []

#a loop to continuously add words to the list until stopped (controlled sentinelt loop)
while True:
    word = input("Enter word to put to list (to cancel type -1):")
    if word == "-1":
        break
    else:
        wordlist.append(word)

#to get the user input
string = input ("Enter a sentence in lower case: ")

listwords(wordlist, string)
    
