import uuid
import hashlib
import re
from models import checkUser

def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

def checkRegistrationForm(form):
    error = {}
    InputEmail = form['InputEmail']
    InputPassword = form['InputPassword']
    ConfirmPassword = form['ConfirmPassword']
    if not (re.match(r'^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z]).{8,}$', InputPassword)):
        error['InputPassword'] = 'Password must greater than 8 characters, have atleast one uppercase, one lowercase, one digit, one special character'
    if (ConfirmPassword != InputPassword):
        error['ConfirmPassword'] = 'Passwords must match'
    result = checkUser({"email": InputEmail})
    if result['success']:
        if result['exists']:
            error['InputEmail'] = 'User already exists'
    else:
        error['InternalError'] = 'Some internal error occured while validating email'
    return error

def checkDocumentForm(form):
    try:
        error = {}
        DocType = form['DocType']
        if(DocType == 'Driving Licence'):
            DLNumber = form['DLNumber']
            stateCode = DLNumber[:2]
            numberCode = DLNumber[2:]
            if((not stateCode.isalpha()) or (not numberCode.isnumeric()) or len(DLNumber)!=15):
                error['DLNumber'] = 'Invalid DL'
        elif(DocType == 'Aadhar Card'):
            AANumber = str(form['AANumber'])
            print('{0} {1} {2}'.format(AANumber, type(AANumber), len(AANumber)))
            if((not AANumber.isnumeric()) or (len(AANumber) != 12) ):
                error['AANumber'] = 'Invalid Aadhar Card Number'
        elif(DocType == 'Debit Card'):
            DCNumber = str(form['DCNumber'])
            print('{0} {1} {2}'.format(DCNumber, type(DCNumber), len(DCNumber)))
            if ((not DCNumber.isnumeric()) or (len(DCNumber) != 16)):
                error['DCNumber'] = 'Invalid Debit Card Number'
            DCCVV = str(form['DCCVV'])
            if ((not DCCVV.isnumeric()) or (len(DCCVV) != 3)):
                error['DCCVV'] = 'Invalid CVV'
        return error
    except Exception as  err:
        print(err)
