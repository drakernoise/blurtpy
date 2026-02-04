# -*- coding: utf-8 -*-
import logging
import json
import io
import collections
import hashlib
from binascii import hexlify, unhexlify
import requests
from .instance import shared_blockchain_instance
from blurtpy.account import Account
from blurtgraphenebase.py23 import integer_types, string_types, text_type, py23_bytes
from blurtgraphenebase.account import PrivateKey
from blurtgraphenebase.ecdsasig import sign_message, verify_message


class ImageUploader(object):
    def __init__(
        self,
        base_url="https://blurtitimages.com",
        challenge="ImageSigningChallenge",
        blockchain_instance=None,
        **kwargs
    ):
        self.challenge = challenge
        self.base_url = base_url
        if blockchain_instance is None:
            if kwargs.get("blurt_instance"):
                blockchain_instance = kwargs["blurt_instance"]        
        self.blurt = blockchain_instance or shared_blockchain_instance()
        if self.blurt.is_blurt and base_url == "https://blurtitimages.com":
            self.base_url = "https://images.blurt.blog"

    def upload(self, image, account, image_name=None):
        """ Uploads an image

            :param image: path to the image or image in bytes representation which should be uploaded
            :type image: str, bytes
            :param str account: Account which is used to upload. A posting key must be provided.
            :param str image_name: optional

            .. code-block:: python

                from blurtpy import Blurt
                from blurtpy.imageuploader import ImageUploader
                stm = Blurt(keys=["5xxx"]) # private posting key
                iu = ImageUploader(blockchain_instance=stm)
                iu.upload("path/to/image.png", "account_name") # "private posting key belongs to account_name

        """
        account = Account(account, blockchain_instance=self.blurt)
        if "posting" not in account:
            account.refresh()
        if "posting" not in account:
            raise AssertionError("Could not access posting permission")
        for authority in account["posting"]["key_auths"]:
            posting_wif = self.blurt.wallet.getPrivateKeyForPublicKey(authority[0])

        if isinstance(image, string_types):
            image_data = open(image, 'rb').read()
        elif isinstance(image, io.BytesIO):
            image_data = image.read()
        else:
            image_data = image

        message = py23_bytes(self.challenge, "ascii") + image_data
        signature = sign_message(message, posting_wif)
        signature_in_hex = hexlify(signature).decode("ascii")

        files = {image_name or 'image': image_data}
        url = "%s/%s/%s" % (
            self.base_url,
            account["name"],
            signature_in_hex
        )
        r = requests.post(url, files=files)
        return r.json()
