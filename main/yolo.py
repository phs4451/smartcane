import objectRecognition as objrec
imgname
encoded_img = objrec.encode_img(imgname)
objrec.send_img(encoded_img,server_ip)

