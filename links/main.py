# main.py
from models import some_function  # استيراد دالة من ملف models.py
from memes import another_function  # استيراد دالة من ملف memes.py

def main():
    print("This is the main program!")
    some_function()
    another_function()

if __name__ == "__main__":
    main()
