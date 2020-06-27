from string_matching import load_text

if __name__ == "__main__":
    
    with open("../large_100.txt", "w+") as vl:

        with open("../kafka.txt", "r") as kafka:
            klines = kafka.readlines()
        
        for i in range(100):
            vl.writelines(klines)


    