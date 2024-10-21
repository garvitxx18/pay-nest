def getOTP():
    return f"SELECT otp FROM pay_nest_user WHERE id = %s"

def getPhoneNumber(id):
    return f"SELECT phone_number FROM pay_nest_user WHERE id = {id};"
