"""Module for encryption of files. Useful for all kinds of situtations.

:author: Julian M. Kleber
"""

from typing import Tuple, Optional

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

from .utils import prepare_file_name_saving


def decrypt_file(encrypted_file: str, private_key_path: str):
    """The decrypt_file function takes in an encrypted file and a private key,
    then decrypts the file using the private key.

    :param encrypted_file: str: Used to Pass the file name of the
        encrypted file to be decrypted.
    :param private_key: str: Used to Read the private key file and
        decrypt the encrypted message.
    :return: The original message.  :doc-author: Julian M. Kleber
    """

    with open(encrypted_file, "rb") as ecf:
        encrypted = (
            ecf.read()
        )  # From before (could have been stored then read back here)

    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)

    original_message = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA512()),
            algorithm=hashes.SHA512(),
            label=None,
        ),
    )
    return original_message


def encrypt_file(
    file_name: str,
    public_key_file: str,
    in_place: bool = False,
    save_file: Optional[str] = None,
) -> None:
    """The encrypt_file function takes a file name, public key, and optional
    in-place flag. It then encrypts the contents of the file using the provided
    public key. If in_place is True, it will overwrite the original file with
    its encrypted version. Otherwise it will create a new encrypted version of
    that file.

    :param file_name:str: Used to Specify the name of the file to be
    encrypted. :param public_key:str: Used to Specify the name of the
    public key file. :param in_place:bool=False: Used to Determine
    whether the file should be overwritten or not. :param save_
    file:Optional[str]=None:
     :param file_name: str: Used to Specify the name of the file to be
    encrypted. :param public_key: str: Used to Specify the name of the
    public key     file. :param in_place: bool=False: Used to Determine
    whether the file     should be overwritten or not. :param save_
    file:Optional[str]=None:
    :param file_name: str: Used to Specify the name of the file to be
        encrypted.
    :param public_key: str: Used to Specify the name of the public key
        file.
    :param in_place: bool=False: Used to Determine whether the file
        should be overwritten or not. :param save_
        file:Optional[str]=None:
    :param file_name: str: Used to Specify the name of the file to be
        encrypted.
    :param public_key: str: Used to Specify the name of the public key
        file.
    :param in_place: bool=False: Used to Determine whether the file
        should be overwritten or not. :param save_
        file:Optional[str]=None:
    :param file_name: str: Used to Specify the name of the file to be
        encrypted.
    :param public_key: str: Used to Specify the name of the public key
        file.
    :param in_place: bool=False: Used to Determine whether the file
        should be overwritten or not.
    :param save_file: Optional[str]=None: Used to Allow the user to
        specify a file name for saving the encrypted file.
    :return: None.  :doc-author: Julian M. Kleber
    """

    with open(public_key_file, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(), backend=default_backend()
        )

    if in_place:
        save_file = file_name

    with open(file_name, "r", encoding="utf-8") as to_encrypt:
        file_content = str.encode(to_encrypt.read())

    encrypted = public_key.encrypt(
        file_content,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA512()),
            algorithm=hashes.SHA512(),
            label=None,
        ),
    )

    with open(save_file, "wb") as encrypted_file:
        encrypted_file.write(encrypted)


def generate_asymmetric_keys(
    key_size: int, private_key_name: str, public_key_name: str, write_secret: bool
) -> Tuple[bytes, bytes]:
    """The generate_asymmetric_keys function generates a private key and public
    key pair. The keys are generated using the RSA algorithm with a specified
    bit size. The keys are then written to files in PEM format.

    :param key_size: int: Used to specify the size of the key that will
        be generated.
    :param private_key_name: str: Used to Name the private key file.
    :param public_key_name: str: Used to specify the name of the public
        key file.
    :return: The private and public keys.  :doc-author: Julian M. Kleber
    """

    private_key_name = prepare_file_name_saving(private_key_name)
    public_key_name = prepare_file_name_saving(public_key_name)
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=key_size, backend=default_backend()
    )

    secret_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    if write_secret:
        with open(
            private_key_name, "wb"
        ) as key_file:  # writes in binary mode if there a special file errors
            key_file.write(secret_pem)

    public_key = private_key.public_key()

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    with open(public_key_name, "wb") as key_file:
        key_file.write(public_pem)

    return public_key, private_key
