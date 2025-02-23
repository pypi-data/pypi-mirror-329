_A='utf-8'
import os,json,base64,hashlib,random
from cryptography.fernet import Fernet
def sparta_9a09bb96af():A='__API_AUTH__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_78ad4f2352(objectToCrypt):A=objectToCrypt;C=sparta_9a09bb96af();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_da597c9e27(apiAuth):A=apiAuth;B=sparta_9a09bb96af();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_a7c11cff31(kCrypt):A='__SQ_AUTH__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_ddfc32f5e7(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_a7c11cff31(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_baa708e2c4(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_a7c11cff31(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_26dbc3016e(kCrypt):A='__SQ_EMAIL__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_ce70f2d898(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_26dbc3016e(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_935bc2a39a(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_26dbc3016e(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_e08e278cb4(kCrypt):A='__SQ_KEY_SSO_CRYPT__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_2d3586ed4e(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_e08e278cb4(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_b72fa9e498(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_e08e278cb4(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_30ecc211fd():A='__SQ_IPYNB_SQ_METADATA__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_e4f91ce1fc(objectToCrypt):A=objectToCrypt;C=sparta_30ecc211fd();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_386ccf6842(objectToDecrypt):A=objectToDecrypt;B=sparta_30ecc211fd();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)