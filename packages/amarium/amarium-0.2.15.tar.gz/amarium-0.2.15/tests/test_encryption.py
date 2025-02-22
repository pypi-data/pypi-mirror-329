import sys
import os

import pytest

from amarium.encryption import generate_asymmetric_keys, encrypt_file, decrypt_file


def test_asymmetric_key_generation():
    # case 1
    key_size = 2048
    public_key_name = "tests/public_test.pem"
    private_key_name = "tests/private_test.pem"
    if os.path.isfile(public_key_name):
        os.remove(public_key_name)

    if os.path.isfile(private_key_name):
        os.remove(private_key_name)

    generate_asymmetric_keys(
        key_size=key_size,
        private_key_name=private_key_name,
        public_key_name=public_key_name,
        write_secret=False,
    )
    assert "public_test.pem" in os.listdir("tests")
    assert "private_test.pem" not in os.listdir("tests")
    # case 2
    generate_asymmetric_keys(
        key_size=key_size,
        private_key_name=private_key_name,
        public_key_name=public_key_name,
        write_secret=True,
    )
    assert "public_test.pem" in os.listdir("tests")
    assert "private_test.pem" in os.listdir("tests")


def test_file_encryption():
    message = "Amarium is a decent library to write and read files"

    file_name = "test_encryption_files/test_encrypt.txt"
    if os.path.isfile(file_name):
        os.remove(file_name)
    with open(file_name, "w") as test_file:
        test_file.write(message)

    save_file = "test_encryption_files/test_encrypted_test_file.txt"
    public_key_file = "tests/public_test.pem"

    in_place = False

    encrypt_file(
        file_name=file_name,
        public_key_file=public_key_file,
        save_file=save_file,
        in_place=in_place,
    )
    assert os.path.isfile(save_file)

    in_place = True
    encrypt_file(
        file_name=file_name, public_key_file=public_key_file, in_place=in_place
    )


def test_decryption():
    encrypted_file = "test_encryption_files/test_encrypted_test_file.txt"
    private_key_path = "tests/private_test.pem"

    message = decrypt_file(
        encrypted_file=encrypted_file, private_key_path=private_key_path
    )
    assert message == b"Amarium is a decent library to write and read files"
