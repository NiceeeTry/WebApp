def vovels(word:str, vovels:str='aeiou')->str:
    return ''.join((set(word).intersection(vovels)))