def checkQuote(text):
    if text.isdigit() & (len(text) == 4):
        return True
    else:
        return False

def checkStar(text):
    if text[0] == "*":
        return True
    else:
        return False