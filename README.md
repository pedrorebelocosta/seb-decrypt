# Warning for rncryptor

As **rncryptor** is going to interpret the content as UTF-8 modify **line 124** in **rncryptor.py** with the following:

    return decrypted_data
Instead of:

    return self.post_decrypt_data(decrypted_data)

# Disclaimer
This is something I've worked on out of curiosity for password-based encryption on **.seb** files generated by Safe Exam Browser
