class MyDict:

    def __init__(self, arg):
        self.arg = arg


    def make_dictionary(self):
        arg = self.arg
        word_dic = {1: {"א": 1,
                        "ב": 2,
                        "ג": 3,
                        "ד": 4,
                        "ה": 5,
                        "ו": 6,
                        "ז": 7,
                        "ח": 8,
                        "ט": 9,
                        "י": 10,
                        "כ": 20,
                        "ך": 20,
                        "ל": 30,
                        "מ": 40,
                        "ם": 40,
                        "נ": 50,
                        "ן": 50,
                        "ס": 60,
                        "ע": 70,
                        "פ": 80,
                        "ף": 80,
                        "צ": 90,
                        "ץ": 90,
                        "ק": 100,
                        "ר": 200,
                        "ש": 300,
                        "ת": 400},
                    2: {"א": 1,
                        "ב": 2,
                        "ג": 3,
                        "ד": 4,
                        "ה": 5,
                        "ו": 6,
                        "ז": 7,
                        "ח": 8,
                        "ט": 9,
                        "י": 10,
                        "כ": 20,
                        "ל": 30,
                        "מ": 40,
                        "נ": 50,
                        "ס": 60,
                        "ע": 70,
                        "פ": 80,
                        "צ": 90,
                        "ק": 100,
                        "ר": 200,
                        "ש": 300,
                        "ת": 400,
                        "ך": 500,
                        "ם": 600,
                        "ן": 700,
                        "ף": 800,
                        "ץ": 900}
                    }
        try:
            word_dic = word_dic[arg]
            return word_dic
        except KeyError:
            print("errore di lettura chiave dizionario. Uscita")
            quit()


def main(choice):
    new = MyDict(choice)

if __name__ == "__main__":
        main()