from cryptography.fernet import Fernet

Key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
# F12 and click element inspector
# Copy and paste from source
message = b'gAAAAABcl4kVUw8WLI-LJo1J2zs-DyLIIpL9_owX5E11LmOHPEgRDRJYRjFeqLgNXRCgfELU5IGtnlq0TPH44cV3z2_1Yp7EVwwsBnlcY1pM0SQ3ndhmFHLMGA9C_mmW_jdt-09slpxo_VRpkm0sSWDo4x9dtAjqthFwmx6gzcAQ_eaHA5F98MWi9lzKncPastpvqUGkiEhA'

def main():
    f = Fernet(Key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()