_A='utf-8'
import os,json,base64,hashlib,random
from cryptography.fernet import Fernet
def sparta_ff813b4d84():A='__API_AUTH__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_84b049083d(objectToCrypt):A=objectToCrypt;C=sparta_ff813b4d84();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_91096cb4a6(apiAuth):A=apiAuth;B=sparta_ff813b4d84();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_f5d3aea57b(kCrypt):A='__SQ_AUTH__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_d1d4136bad(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_f5d3aea57b(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_51ade40ae8(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_f5d3aea57b(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_0de9e88115(kCrypt):A='__SQ_EMAIL__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_ec019ce1fa(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_0de9e88115(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_40fdcf8414(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_0de9e88115(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_7fd9831e62(kCrypt):A='__SQ_KEY_SSO_CRYPT__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_84e52607bb(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_7fd9831e62(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_83872dce22(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_7fd9831e62(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_24bea1b7b5():A='__SQ_IPYNB_SQ_METADATA__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_07321817dd(objectToCrypt):A=objectToCrypt;C=sparta_24bea1b7b5();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_40b24fee2b(objectToDecrypt):A=objectToDecrypt;B=sparta_24bea1b7b5();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)