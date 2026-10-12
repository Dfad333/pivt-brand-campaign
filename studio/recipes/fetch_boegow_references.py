import os
import urllib.request

OUT = r"C:\Users\tarek\AppData\Local\Temp\claude\E--PivtMedia\e834e237-b716-4dcd-84af-e9644bb7821d\scratchpad\boegow"
os.makedirs(OUT, exist_ok=True)

urls = {
    "a-jul06-the-feeling": "https://scontent-ord5-3.cdninstagram.com/v/t51.82787-15/732215426_18041765963802719_4536644235645552443_n.jpg?stp=dst-jpg_e35_s640x640_tt6&_nc_cat=109&ccb=7-5&_nc_sid=18de74&efg=eyJlZmdfdGFnIjoiRkVFRC5iZXN0X2ltYWdlX3VybGdlbi5DMyJ9&_nc_ohc=rwTPfA6uPRIQ7kNvwHqoprO&_nc_oc=AdoDTLWVYakQ-kVRm4k5ERLdUbZtnK_72x5vbGYKcql4n50SNaUrITiYJbjcix5g83F_lI378cXaQaDhTVVsgZVa&_nc_zt=23&_nc_ht=scontent-ord5-3.cdninstagram.com&_nc_gid=9wOj7npqpexKbkR9YJiONw&_nc_ss=79689&oh=00_AQEN_W-dwj3D_vfjUBZPjjkwsQIsfKIWzAQrAuuifUe_sA&oe=6A75490C",
    "b-jun18-crossword": "https://scontent-ord5-3.cdninstagram.com/v/t51.82787-15/725578769_18039026999802719_3959168005893237626_n.jpg?stp=dst-jpg_e35_s640x640_tt6&_nc_cat=100&ccb=7-5&_nc_sid=18de74&efg=eyJlZmdfdGFnIjoiRkVFRC5iZXN0X2ltYWdlX3VybGdlbi5DMyJ9&_nc_ohc=zhnJFBP7WYMQ7kNvwEiL1Sd&_nc_oc=AdqJmD5NgR__jobqd5hW_6V3GuRM9jUWUclPOGMJl5sexxdwdca13RWrwO_uCApwIfQ35wehwG_yn3mqVxfZ_haN&_nc_zt=23&_nc_ht=scontent-ord5-3.cdninstagram.com&_nc_gid=9wOj7npqpexKbkR9YJiONw&_nc_ss=79689&oh=00_AQFrOETSmaDyzDuipgMv1Dq2A3brLACjo3e8CgN1tMe2IA&oe=6A754489",
    "c-jun13-poster": "https://scontent-ord5-2.cdninstagram.com/v/t51.82787-15/730244765_18040852400802719_5584363406252331518_n.jpg?stp=dst-jpg_e35_s640x640_tt6&_nc_cat=102&ccb=7-5&_nc_sid=18de74&efg=eyJlZmdfdGFnIjoiQ0xJUFMuYmVzdF9pbWFnZV91cmxnZW4uQzMifQ%3D%3D&_nc_ohc=BZGwiP3ikPgQ7kNvwFp-eic&_nc_oc=AdovJnwQEc5Ajj8bVo53OXLLjQ-P5ZMD15a2nVQcxLTOD306aHQKP1Ku3TV7dtNpAFC8_mgrL68MTRXd7nZyEONy&_nc_zt=23&_nc_ht=scontent-ord5-2.cdninstagram.com&_nc_gid=9wOj7npqpexKbkR9YJiONw&_nc_ss=79689&oh=00_AQGZTnNuiDndC2hLdby1DD-C163J9vFCkxF_gtJ8I1-G9g&oe=6A756BBC",
    "d-jun09-poster": "https://scontent-ord5-1.cdninstagram.com/v/t51.82787-15/719351768_18037738253802719_8140185344758825547_n.jpg?stp=dst-jpg_e35_s640x640_tt6&_nc_cat=111&ccb=7-5&_nc_sid=18de74&efg=eyJlZmdfdGFnIjoiRkVFRC5iZXN0X2ltYWdlX3VybGdlbi5DMyJ9&_nc_ohc=UDHeBdOrxqIQ7kNvwGz53vp&_nc_oc=Adod3068D_zKRgpkQCxKW6IF5imBsdcb23O9qzAKaTzcR5uID3FMPDyXjDUJVkgTx7nPgXygKagBB9uARGPRNoNl&_nc_zt=23&_nc_ht=scontent-ord5-1.cdninstagram.com&_nc_gid=9wOj7npqpexKbkR9YJiONw&_nc_ss=79689&oh=00_AQGUbfv4rHz8Y8M63ahSQ-DRPk7W5X7fm-cyIAn-i--0Yw&oe=6A756BBB",
    "e-mar18": "https://scontent-ord5-3.cdninstagram.com/v/t51.82787-15/654024055_18026798354802719_9173193257181734668_n.jpg?stp=dst-jpg_e35_s640x640_tt6&_nc_cat=100&ccb=7-5&_nc_sid=18de74&efg=eyJlZmdfdGFnIjoiQ0FST1VTRUxfSVRFTS5iZXN0X2ltYWdlX3VybGdlbi5DMyJ9&_nc_ohc=i4ukL1CV4roQ7kNvwEr1NLz&_nc_oc=Adpz2NOqswDZdYE0qaPB_Hv5sQu8AoBez2uSYaum__obRg9IRIhSrIOF6subJM_Y275K9KpmxdPIIxCyjx4qoKAB&_nc_zt=23&_nc_ht=scontent-ord5-3.cdninstagram.com&_nc_gid=9wOj7npqpexKbkR9YJiONw&_nc_ss=79689&oh=00_AQHWQluWTRwB1T25pEGiFUl0AEA6hMHRYXTMG5_AhdnyOA&oe=6A75418C",
    "f-nov04": "https://scontent-ord5-1.cdninstagram.com/v/t51.82787-15/573059831_18011488883802719_8738553216653426771_n.jpg?stp=dst-jpg_e35_s640x640_tt6&_nc_cat=105&ccb=7-5&_nc_sid=18de74&efg=eyJlZmdfdGFnIjoiQ0FST1VTRUxfSVRFTS5iZXN0X2ltYWdlX3VybGdlbi5DMyJ9&_nc_ohc=SL_QpGRvzhgQ7kNvwGeES8k&_nc_oc=AdqteKaJ8jq-1QwEVfwLtUMnpP2XoqajwnzqeTIKfqm51oMkdKaECBoWXSrag6Cn5y_bRM3pkD8oO6HwzLpFb0Qb&_nc_zt=23&_nc_ht=scontent-ord5-1.cdninstagram.com&_nc_gid=9wOj7npqpexKbkR9YJiONw&_nc_ss=79689&oh=00_AQFrJhGfXbHzBm7H1I-X_y1mLXt2Dk0PlopraoFsT9v5DQ&oe=6A755F53",
    "g-aug16": "https://scontent-ord5-1.cdninstagram.com/v/t51.82787-15/532817193_18002274335802719_7542844054058197910_n.jpg?stp=dst-jpg_e35_s640x640_tt6&_nc_cat=101&ccb=7-5&_nc_sid=18de74&efg=eyJlZmdfdGFnIjoiQ0FST1VTRUxfSVRFTS5iZXN0X2ltYWdlX3VybGdlbi5DMyJ9&_nc_ohc=DW7kQ8uYt24Q7kNvwHm0yMT&_nc_oc=AdpR1_FV2S1VFsgeJzfRoRmXypkeBLppJJTEJicku76d3gadtI7yub59AwRCHz21ELCVL9abCWQiEQtCEdSvFkTx&_nc_zt=23&_nc_ht=scontent-ord5-1.cdninstagram.com&_nc_gid=9wOj7npqpexKbkR9YJiONw&_nc_ss=79689&oh=00_AQFYBAXeYJynQvojTm-gEfKrv6pV1ukF4tLK03DNRfWJyA&oe=6A755095",
    "h-aug10": "https://scontent-ord5-1.cdninstagram.com/v/t51.82787-15/529745785_18001589858802719_646178450231181562_n.jpg?stp=dst-jpg_e35_s640x640_tt6&_nc_cat=101&ccb=7-5&_nc_sid=18de74&efg=eyJlZmdfdGFnIjoiQ0FST1VTRUxfSVRFTS5iZXN0X2ltYWdlX3VybGdlbi5DMyJ9&_nc_ohc=69KIp9yPrJkQ7kNvwERDR_b&_nc_oc=Adr5eXEJF_Y9M8RkPQnW49xpIQtSKmKY9tF2JPpUXqMquehJqmQRV8rdrQD4Kb6aY1InKVbE2fjbD9Rcm8DCdfdq&_nc_zt=23&_nc_ht=scontent-ord5-1.cdninstagram.com&_nc_gid=9wOj7npqpexKbkR9YJiONw&_nc_ss=79689&oh=00_AQEvw0mZtnOnTXK4kKnqztNiptjQtuTPxQpwFp-a6PDVqw&oe=6A75624F",
}

for name, url in urls.items():
    dest = os.path.join(OUT, name + ".jpg")
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Referer": "https://www.instagram.com/",
        })
        with urllib.request.urlopen(req, timeout=30) as r, open(dest, "wb") as f:
            f.write(r.read())
        print("ok  ", name, os.path.getsize(dest))
    except Exception as e:
        print("FAIL", name, e)
