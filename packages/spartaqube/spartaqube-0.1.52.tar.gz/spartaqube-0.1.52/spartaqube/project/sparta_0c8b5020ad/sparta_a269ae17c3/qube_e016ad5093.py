_A='utf-8'
import os,json,base64,hashlib,random
from cryptography.fernet import Fernet
def sparta_5f95983631():A='__API_AUTH__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_e5af43c207(objectToCrypt):A=objectToCrypt;C=sparta_5f95983631();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_28312411a0(apiAuth):A=apiAuth;B=sparta_5f95983631();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_5fea4ab77d(kCrypt):A='__SQ_AUTH__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_04c3b0ad98(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_5fea4ab77d(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_b362e070e4(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_5fea4ab77d(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_51651e8eb9(kCrypt):A='__SQ_EMAIL__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_cae0bc367b(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_51651e8eb9(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_1287396087(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_51651e8eb9(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_638e862079(kCrypt):A='__SQ_KEY_SSO_CRYPT__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_f2d97af113(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_638e862079(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_048693a3fd(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_638e862079(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_5926bb40c8():A='__SQ_IPYNB_SQ_METADATA__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_93d4face8f(objectToCrypt):A=objectToCrypt;C=sparta_5926bb40c8();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_648fc34e67(objectToDecrypt):A=objectToDecrypt;B=sparta_5926bb40c8();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)