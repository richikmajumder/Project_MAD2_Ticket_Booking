from email.message import EmailMessage
import ssl,smtplib
import pdfkit,imgkit,cv2,qrcode

def report_pdf(content):
  pdfkit.from_string(content, 'files/Report.pdf')
  print('PDF generated successfully')

def send_ticket_png(content):
  options={'enable-local-file-access': None}
  imgkit.from_string(content,'files/ticket.png',options)
  print("Image generated successfully")

def compress_image(input_path, output_path, quality=85):
  img = cv2.imread(input_path)
  cv2.imwrite(output_path, img, [cv2.IMWRITE_JPEG_QUALITY, quality])
  print("Image compressed successfully")

def generate_qr(data):
  qr = qrcode.QRCode(version=1, box_size=10, border=5)
  qr.add_data(data)
  qr.make(fit=True)
  img = qr.make_image(fill_color="black", back_color="white")
  img.save("files/qrcode.png")
  print("QR code generated successfully")

def send_email_with_attachment(sender_email,receiver_email,subject,body,password,file,filetype):
  em = EmailMessage()
  em["From"]=sender_email
  em["To"]=receiver_email
  em["Subject"]=subject
  em.set_content(body)
  with open(file, 'rb') as f:
    file_data = f.read()
    if filetype in ['jpg','png']:
      maintype='image'
    maintype='application'
    em.add_attachment(file_data, maintype=maintype, subtype=filetype, filename=file.split('/')[-1])
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context) as smtp:
    smtp.login(sender_email,password)
    smtp.send_message(em)
  print("Email sent successfully")


def send_email_reminder(sender_email,receiver_email,subject,body,password):
  em = EmailMessage()
  em["From"]=sender_email
  em["To"]=receiver_email
  em["Subject"]=subject
  em.set_content(body)
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context) as smtp:
    smtp.login(sender_email,password)
    smtp.send_message(em)
  print("Email sent successfully")


def send_monthly_report(sender_email,receiver_email,subject,body,password):
  em = EmailMessage()
  em["From"]=sender_email
  em["To"]=receiver_email
  em["Subject"]=subject
  em.set_content("Please enable HTML to view this email.")
  em.add_alternative(body, subtype="html")
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context) as smtp:
    smtp.login(sender_email,password)
    smtp.send_message(em)
  print("Monthly report sent successfully")

def send_monthly_report_pdf(sender_email,receiver_email,file,password):
  em = EmailMessage()
  em["From"]=sender_email
  em["To"]=receiver_email
  em["Subject"]="Your monthly entertainment report"
  body="""Hello,

We are pleased to share with you your Monthly Entertainment Report from The Ticketing App Team. Please find the attached report for your reference.

Attached: Report.pdf

If you have any questions or require further assistance, feel free to contact us. We are here to help!

Thank you for using The Ticketing App.

Best regards,
The Ticketing App Team"""
  em.set_content(body)
  with open(file, 'rb') as f:
    file_data = f.read()
    em.add_attachment(file_data, maintype="application", subtype="pdf", filename=file.split('/')[-1])
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context) as smtp:
    smtp.login(sender_email,password)
    smtp.send_message(em)
  print("Monthly pdf report sent successfully")