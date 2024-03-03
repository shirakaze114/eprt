import cups
import pypandoc

conn = cups.Connection()
printers = conn.getPrinters()
printer_name = "MP_2501L"

pypandoc.convert_file('ohshit.md', to='docx',extra_args=['--reference-docx=god.docx'], outputfile='ohshit.docx'),
exit()
conn.printFile(printer_name,'filepath',"AutoPrint",{}) 
# for printer in printers:
#     print(printer, printers[printer]["device-uri"])
