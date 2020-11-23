from MakeSynonomousString import getSynonomousTextBot

def main():
    varcontinue = True
    while(varcontinue):
        phraseToConvert = str(input("Enter text to convert: "))
        smartBot = getSynonomousTextBot()
        smartBot.makeSynonomousText(phraseToConvert)
        varcontinue = bool(input("Continue?"))


main()
