from passlib.context import CryptContext


context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def Hashing_Password(plain_password):
    return context.hash(plain_password)


def verify_password(plain_password, hashed_password):
    return context.verify(plain_password, hashed_password)
