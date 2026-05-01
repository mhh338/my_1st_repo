import pyjokes

joke = pyjokes.get_joke()
print(joke)

# Chapter 3 practice set

# 1, Print a name taken as user input followed by good afternoon
a = input("Enter a name: ")
print(a + " Good Afternoon") # OR
print(f"{a} Good Aternoon")

#2, Detecting double spaces
print(a.find("  "))

#3, Replacing double spaces with single space
print(a.replace("  ", " "))

#4, Fill the name and date in the letter template
letter = ''' Dear <|Name|>, 
                 Your selected
                <|Date|>'''
print(letter.replace("<|Name|>", "Tony").replace("<|Date|>", "10th March 2026"))

#5, Format the letter using escape sequence
let = "Dear Sir,\n\t This is a good letter, \n\t Thank you!"
print(let)
