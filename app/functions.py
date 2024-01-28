import re
def isValidEmail(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)


def isValidPassword(password):
    if (len(password)>6 
        and any(c.islower() for c in password)
        and any(c.isupper() for c in password)
        and any(c.isdigit() for c in password)
        and any(c.isalnum() for c in password)
        and re.search('[^a-zA-Z0-9]', password)   # checks for special character
        ):
        return True
    else:
        return False