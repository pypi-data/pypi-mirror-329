def search4vowels(phrase:str)->set:
    """ Returns a set of the 'vowels' found in 'word'."""
    vowels=set('aeiou')
    return vowels.intersection(set(phrase))


def search4letters(phrase:str,letters:str='aeiou')->set:
    """ Returns a set of the 'letters' found in 'phrase'."""
    return set(letters).intersection(set(phrase))

