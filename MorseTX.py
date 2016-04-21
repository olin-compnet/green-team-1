# Module MorseTX
from MorseCode import MorseCode


def MorseTX(M):
    for W in M.split(" "):
        for L in W:
            for Dd in MorseCode[L]:
                yield (1,1) if Dd == "." else (1, 3)
                yield (0,1)
            yield(0,2)
        yield (0,4)
    yield (0,8)
    

if __name__ == "__main__":
    print("AN ACE")
    for OOKtuple in MorseTX("AN ACE"):
        print(OOKtuple)
    print("OOK AT ME")
    for OOKtuple in MorseTX("OOK AT ME"):
        print(OOKtuple)