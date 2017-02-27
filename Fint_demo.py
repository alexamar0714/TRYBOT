import piazza_api
from Fint import Fint
import sys

def main():

    temp = sys.argv
    cid = int(temp[1])
    answer = sys.argv[2]
    email = ""
    password = ""
    class_code = "iy9ue7czifo1kk"

    fint = Fint()
    fint.setup_connection(email, password, class_code)
    x = fint.update(cid = cid)
    print("\n")
    print(x[0][1])
    fint.answer(cid = cid, content=answer)


if __name__ == "__main__":
    main()