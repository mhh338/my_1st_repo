import pymupdf
import webbrowser
import os

# Paste the path of your file in " "
doc = pymupdf.open(r"C:\Users\Windows\Desktop\sample-local-pdf.pdf")

for i, page in enumerate(doc):
    text = page.get_text("text", sort = True)
    print(f"Page {i+1}:\n{text}\n")


# Logic for opening the text in the web-browser tab. 
# with open("text.html", "w") as f:
#     for i, page in enumerate(doc):
#         text = page.get_text("text", sort = True)
#         f.write(f"<html><body><p>\n{text}\n</p?</body></html>")
# webbrowser.open("file://" + os.path.realpath("text.html"))