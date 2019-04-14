from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABcsgNm20qut_EdSVGME-ZqCn3Im_VO3BTWYGjRDaXY38XlMawznNovFHxpPF3fjLWe7iaUXvpxuR7usrE_u5yVkxAtuS9txlNOnGNmuKhSXSwywAbpN4Eu1Uu4VRhX5_5nGCpMoD0FoSlLlhjBrL03Qrb7b3O7exwoA6v5KXWye0mwvcZWcdqGVJKjcwoBh0chJ6ga'

def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__== "__main__":
    main()