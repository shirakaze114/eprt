import cups
import pypandoc
import datetime
from re import sub

from flask import Flask

conn = cups.Connection()
printers = conn.getPrinters()
printer_name = "MP_2501L"

def makedoc(title,author,text):
    doc = ""
    time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
    with open("template.md",mode="r",encoding="utf-8") as f:
        doc = f.read().replace("{{title}}",title).replace("{{date}}",time).replace("{{author}}",author)
        doc = doc.replace("{{body}}",text)

    filename = 'markdowns/'+f"{sub(r'[\/:*?"<>| ]','-',title)}-{author}-{time}.md"
    with open(filename,mode="w",encoding="utf-8") as f:
        f.write(doc)

    return filename

title = "how can u makejob"
author = "Me"
text = "Hello World!"

# pypandoc.convert_file('ohshit.md', to='docx',extra_args=['--reference-doc=god.docx'], outputfile='ohshit.docx'),
# pypandoc.convert_file('ohshit.docx', to='pdf',extra_args=['--pdf-engine=xelatex','-V', outputfile='ohshit.pdf')
pypandoc.convert_file(makedoc(title,author,text),  to='pdf',extra_args=['--pdf-engine=xelatex', '-V titlepage=true'], outputfile='ohshit.pdf')

# conn.printFile(printer_name,'ohshit.pdf',"Auto Print Job",{}) 
exit()
app = Flask(__name__)

@app.route("/")
def index_page():
    pass

@app.route("/act/print", methods=["POST"])
def blowjob():
    pass

def main():
    app.run(host="0.0.0.0", port=80, debug=False, threaded=True)

if __name__ == "__main__":
    main()

exit()
conn.printFile(printer_name,'filepath',"AutoPrint",{}) 
# for printer in printers:
#     print(printer, printers[printer]["device-uri"])
