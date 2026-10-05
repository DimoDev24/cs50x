from cs50 import get_string

text = get_string("Text: ")

letters = 0
sentences = 0
words = 1

for c in text:
    if c.isalpha():
        letters += 1
    elif c == '.' or c == '!' or c == '?':
        sentences += 1
    elif c == ' ':
        words += 1

L = letters / words * 100
S = sentences / words * 100

grade = round(0.0588 * L - 0.296 * S - 15.8)

if grade < 1:
    print("Before Grade 1")
elif grade >= 16:
    print("Grade 16+")
elif grade >= 1 and grade < 16:
    print(f"Grade {grade}")
