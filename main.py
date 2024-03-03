import cups
import pypandoc
import datetime
from re import sub

from flask import Flask,request 

conn = cups.Connection()
printers = conn.getPrinters()
# printer_name = "MP_2501L"
printer_name = "Brother_MFC-7860DN"

def makedoc(title,author,text, ip):
    doc = ""
    time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
    with open("template.md",mode="r",encoding="utf-8") as f:
        doc = f.read().replace("{{title}}",title).replace("{{date}}",time).replace("{{author}}",author).replace("{{ip}}",ip)
        doc = doc.replace("{{body}}",text)

    filename = f"{sub(r'[\/:*?"<>| ]','-',title)}-{author}-{time}.md"
    with open('markdowns/'+filename,mode="w",encoding="utf-8") as f:
        f.write(doc)

    return filename

def convert(filename):
    outputname = filename+".pdf"
    pypandoc.convert_file('markdowns/'+filename,  to='pdf',extra_args=['--pdf-engine=xelatex', '-V titlepage=true'], outputfile="pdfs/"+outputname)
    return outputname

# title = "how can u makejob"
# author = "Me"
# text = "Hello World!"

# pypandoc.convert_file('ohshit.md', to='docx',extra_args=['--reference-doc=god.docx'], outputfile='ohshit.docx'),
# pypandoc.convert_file('ohshit.docx', to='pdf',extra_args=['--pdf-engine=xelatex','-V', outputfile='ohshit.pdf')
# pypandoc.convert_file(makedoc(title,author,text),  to='pdf',extra_args=['--pdf-engine=xelatex', '-V titlepage=true'], outputfile='ohshit.pdf')

# conn.printFile(printer_name,'ohshit.pdf',"Auto Print Job",{}) 

app = Flask(__name__)

@app.route("/")
def index_page():
    with open("templates/index.html",mode="r",encoding="utf-8") as f:
        return f.read()

@app.route("/act/print", methods=["POST"])
def blowjob():
    if request.form.get('passwd')!="kzkhasbigcock":
        return '{"code":200, "error": "cnm"}'

    print(request.data)
    author = request.form.get('author')
    title = 'ePRT-'+request.form.get('title')
    text = request.form.get('text').replace("\n","  \n")
    ip = request.remote_addr

    filename = convert(makedoc(title,author,text,ip))
    
    conn.printFile(printer_name, "pdfs/"+filename,f"{datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")}" ,{}) 
    return '{"code":200, "file": "'+filename+'"}'

def main():
    app.run(host="0.0.0.0", port=8080, debug=False, threaded=True)

if __name__ == "__main__":
    main()

exit()
conn.printFile(printer_name,'filepath',"AutoPrint",{}) 
# for printer in printers:
#     print(printer, printers[printer]["device-uri"])
