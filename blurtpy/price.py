# -*- coding: utf-8 -*-
from blurtgraphenebase.py23 import bytes_types, integer_types, string_types, text_type
from fractions import Fraction
from blurtpy.instance import shared_blockchain_instance
from .exceptions import InvalidAssetException
from .account import Account
from .amount import Amount, quantize
from .asset import Asset
from .utils import formatTimeString
from .utils import parse_time, assets_from_string
from decimal import Decimal


def check_asset(other, self, stm):
    if isinstance(other, dict) and "asset" in other and isinstance(self, dict) and "asset" in self:
        if not Asset(other["asset"], blockchain_instance=stm) == Asset(self["asset"], blockchain_instance=stm):
            raise AssertionError()
    else:
        if not other == self:
            raise AssertionError()


class Price(dict):
    """ This class deals with all sorts of prices of any pair of assets to
        simplify dealing with the tuple::

            (quote, base)

        each being an instance of :class:`blurtpy.amount.Amount`. The
        amount themselves define the price.

        .. note::

            The price (floating) is derived as ``base/quote``

        :param list args: Allows to deal with different representations of a price
        :param Asset base: Base asset
        :param Asset quote: Quote asset
        :param Blurt blockchain_instance: Blurt instance
        :returns: All data required to represent a price
        :rtype: dictionary

        Way to obtain a proper instance:

            * ``args`` is a str with a price and two assets
            * ``args`` can be a floating number and ``base`` and ``quote`` being instances of :class:`blurtpy.asset.Asset`
            * ``args`` can be a floating number and ``base`` and ``quote`` being instances of ``str``
            * ``args`` can be dict with keys ``price``, ``base``, and ``quote`` (*graphene balances*)
            * ``args`` can be dict with keys ``base`` and ``quote``
            * ``args`` can be dict with key ``receives`` (filled orders)
            * ``args`` being a list of ``[quote, base]`` both being instances of :class:`blurtpy.amount.Amount`
            * ``args`` being a list of ``[quote, base]`` both being instances of ``str`` (``amount symbol``)
            * ``base`` and ``quote`` being instances of :class:`blurtpy.asset.Amount`

        This allows instanciations like:

        * ``Price("0.315 TBD/BLURT")``
        * ``Price(0.315, base="TBD", quote="BLURT")``
        * ``Price(0.315, base=Asset("TBD"), quote=Asset("BLURT"))``
        * ``Price({"base": {"amount": 1, "asset_id": "TBD"}, "quote": {"amount": 10, "asset_id": "TBD"}})``
        * ``Price(quote="10 BLURT", base="1 TBD")``
        * ``Price("10 BLURT", "1 TBD")``
        * ``Price(Amount("10 BLURT"), Amount("1 TBD"))``
        * ``Price(1.0, "TBD/BLURT")``

        Instances of this class can be used in regular mathematical expressions
        (``+-*/%``) such as:

        .. code-block:: python

            >>> from blurtpy.price import Price
            >>> from blurtpy import Blurt
            >>> stm = Blurt("https://api.blurtit.com")
            >>> Price("0.3314 TBD/BLURT", blockchain_instance=stm) * 2
            0.662804 TBD/BLURT
            >>> Price(0.3314, "TBD", "BLURT", blockchain_instance=stm)
            0.331402 TBD/BLURT

    """
    def __init__(
        self,
        price=None,
        base=None,
        quote=None,
        base_asset=None,  # to identify sell/buy
        blockchain_instance=None,
        **kwargs
    ):
        if blockchain_instance is None:
            if kwargs.get("blurt_instance"):
                blockchain_instance = kwargs["blurt_instance"]
        self.blockchain = blockchain_instance or shared_blockchain_instance()
        if price == "":
            price = None
        if (price is not None and isinstance(price, string_types) and not base and not quote):
            import re
            price, assets = price.split(" ")
            base_symbol, quote_symbol = assets_from_string(assets)
            base = Asset(base_symbol, blockchain_instance=self.blockchain)
            quote = Asset(quote_symbol, blockchain_instance=self.blockchain)
            frac = Fraction(float(price)).limit_denominator(10 ** base["precision"])
            self["quote"] = Amount(amount=frac.denominator, asset=quote, blockchain_instance=self.blockchain)
            self["base"] = Amount(amount=frac.numerator, asset=base, blockchain_instance=self.blockchain)

        elif (price is not None and isinstance(price, dict) and
                "base" in price and
                "quote" in price):
            if "price" in price:
                raise AssertionError("You cannot provide a 'price' this way")
            # Regular 'price' objects according to blurt-core
            # base_id = price["base"]["asset_id"]
            # if price["base"]["asset_id"] == base_id:
            self["base"] = Amount(price["base"], blockchain_instance=self.blockchain)
            self["quote"] = Amount(price["quote"], blockchain_instance=self.blockchain)
            # else:
            #    self["quote"] = Amount(price["base"], blockchain_instance=self.blockchain)
            #    self["base"] = Amount(price["quote"], blockchain_instance=self.blockchain)

        elif (price is not None and isinstance(base, Asset) and isinstance(quote, Asset)):
            frac = Fraction(float(price)).limit_denominator(10 ** base["precision"])
            self["quote"] = Amount(amount=frac.denominator, asset=quote, blockchain_instance=self.blockchain)
            self["base"] = Amount(amount=frac.numerator, asset=base, blockchain_instance=self.blockchain)

        elif (price is not None and isinstance(base, string_types) and isinstance(quote, string_types)):
            base = Asset(base, blockchain_instance=self.blockchain)
            quote = Asset(quote, blockchain_instance=self.blockchain)
            frac = Fraction(float(price)).limit_denominator(10 ** base["precision"])
            self["quote"] = Amount(amount=frac.denominator, asset=quote, blockchain_instance=self.blockchain)
            self["base"] = Amount(amount=frac.numerator, asset=base, blockchain_instance=self.blockchain)

        elif (price is None and isinstance(base, string_types) and isinstance(quote, string_types)):
            self["quote"] = Amount(quote, blockchain_instance=self.blockchain)
            self["base"] = Amount(base, blockchain_instance=self.blockchain)
        elif (price is not None and isinstance(price, string_types) and isinstance(base, string_types)):
            self["quote"] = Amount(price, blockchain_instance=self.blockchain)
            self["base"] = Amount(base, blockchain_instance=self.blockchain)
        # len(args) > 1

        elif isinstance(price, Amount) and isinstance(base, Amount):
            self["quote"], self["base"] = price, base

        # len(args) == 0
        elif (price is None and isinstance(base, Amount) and isinstance(quote, Amount)):
            self["quote"] = quote
            self["base"] = base

        elif ((isinstance(price, float) or isinstance(price, integer_types) or isinstance(price, Decimal)) and
                isinstance(base, string_types)):
            import re
            base_symbol, quote_symbol = assets_from_string(base)
            base = Asset(base_symbol, blockchain_instance=self.blockchain)
            quote = Asset(quote_symbol, blockchain_instance=self.blockchain)
            frac = Fraction(float(price)).limit_denominator(10 ** base["precision"])
            self["quote"] = Amount(amount=frac.denominator, asset=quote, blockchain_instance=self.blockchain)
            self["base"] = Amount(amount=frac.numerator, asset=base, blockchain_instance=self.blockchain)

        else:
            raise ValueError("Couldn't parse 'Price'.")

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        if ("quote" in self and
                "base" in self and
                self["base"] and self["quote"]):  # don't derive price for deleted Orders
            dict.__setitem__(self, "price", self._safedivide(
                self["base"]["amount"],
                self["quote"]["amount"]))

    def copy(self):
        return Price(
            None,
            base=self["base"].copy(),
            quote=self["quote"].copy(),
            blockchain_instance=self.blockchain)

    def _safedivide(self, a, b):
        if b != 0.0:
            return a / b
        else:
            return float('Inf')

    def symbols(self):
        return self["base"]["symbol"], self["quote"]["symbol"]

    def as_base(self, base):
        """ Returns the price instance so that the base asset is ``base``.

            .. note:: This makes a copy of the object!

            .. code-block:: python

                >>> from blurtpy.price import Price
                >>> from blurtpy import Blurt
                >>> stm = Blurt("https://api.blurtit.com")
                >>> Price("0.3314 TBD/BLURT", blockchain_instance=stm).as_base("BLURT")
                3.017483 BLURT/TBD

        """
        if base == self["base"]["symbol"]:
            return self.copy()
        elif base == self["quote"]["symbol"]:
            return self.copy().invert()
        else:
            raise InvalidAssetException

    def as_quote(self, quote):
        """ Returns the price instance so that the quote asset is ``quote``.

            .. note:: This makes a copy of the object!

            .. code-block:: python

                >>> from blurtpy.price import Price
                >>> from blurtpy import Blurt
                >>> stm = Blurt("https://api.blurtit.com")
                >>> Price("0.3314 TBD/BLURT", blockchain_instance=stm).as_quote("TBD")
                3.017483 BLURT/TBD

        """
        if quote == self["quote"]["symbol"]:
            return self.copy()
        elif quote == self["base"]["symbol"]:
            return self.copy().invert()
        else:
            raise InvalidAssetException

    def invert(self):
        """ Invert the price (e.g. go from ``TBD/BLURT`` into ``BLURT/TBD``)

            .. code-block:: python

                >>> from blurtpy.price import Price
                >>> from blurtpy import Blurt
                >>> stm = Blurt("https://api.blurtit.com")
                >>> Price("0.3314 TBD/BLURT", blockchain_instance=stm).invert()
                3.017483 BLURT/TBD

        """
        tmp = self["quote"]
        self["quote"] = self["base"]
        self["base"] = tmp
        return self

    def json(self):
        return {
            "base": self["base"].json(),
            "quote": self["quote"].json()
        }

    def __repr__(self):
        return "{price:.{precision}f} {base}/{quote}".format(
            price=self["price"],
            base=self["base"]["symbol"],
            quote=self["quote"]["symbol"],
            precision=(
                self["base"]["asset"]["precision"] +
                self["quote"]["asset"]["precision"]
            )
        )

    def __float__(self):
        return float(self["price"])

    def _check_other(self, other):
        if not other["base"]["symbol"] == self["base"]["symbol"]:
            raise AssertionError()
        if not other["quote"]["symbol"] == self["quote"]["symbol"]:
            raise AssertionError()

    def __mul__(self, other):
        a = self.copy()
        if isinstance(other, Price):
            # Rotate/invert other
            if (
                self["quote"]["symbol"] not in other.symbols() and
                self["base"]["symbol"] not in other.symbols()
            ):
                raise InvalidAssetException

            # base/quote = a/b
            # a/b * b/c = a/c
            a = self.copy()
            if self["quote"]["symbol"] == other["base"]["symbol"]:
                a["base"] = Amount(
                    float(self["base"]) * float(other["base"]), self["base"]["symbol"],
                    blockchain_instance=self.blockchain
                )
                a["quote"] = Amount(
                    float(self["quote"]) * float(other["quote"]), other["quote"]["symbol"],
                    blockchain_instance=self.blockchain
                )
            # a/b * c/a =  c/b
            elif self["base"]["symbol"] == other["quote"]["symbol"]:
                a["base"] = Amount(
                    float(self["base"]) * float(other["base"]), other["base"]["symbol"],
                    blockchain_instance=self.blockchain
                )
                a["quote"] = Amount(
                    float(self["quote"]) * float(other["quote"]), self["quote"]["symbol"],
                    blockchain_instance=self.blockchain
                )
            else:
                raise ValueError("Wrong rotation of prices")
        elif isinstance(other, Amount):
            check_asset(other["asset"], self["quote"]["asset"], self.blockchain)
            a = other.copy() * self["price"]
            a["asset"] = self["base"]["asset"].copy()
            a["symbol"] = self["base"]["asset"]["symbol"]
        else:
            a["base"] *= other
        return a

    def __imul__(self, other):
        if isinstance(other, Price):
            tmp = self * other
            self["base"] = tmp["base"]
            self["quote"] = tmp["quote"]
        else:
            self["base"] *= other
        return self

    def __div__(self, other):
        a = self.copy()
        if isinstance(other, Price):
            # Rotate/invert other
            if sorted(self.symbols()) == sorted(other.symbols()):
                return float(self.as_base(self["base"]["symbol"])) / float(other.as_base(self["base"]["symbol"]))
            elif self["quote"]["symbol"] in other.symbols():
                other = other.as_base(self["quote"]["symbol"])
            elif self["base"]["symbol"] in other.symbols():
                other = other.as_base(self["base"]["symbol"])
            else:
                raise InvalidAssetException
            a["base"] = Amount(
                float(self["base"].amount / other["base"].amount), other["quote"]["symbol"],
                blockchain_instance=self.blockchain
            )
            a["quote"] = Amount(
                float(self["quote"].amount / other["quote"].amount), self["quote"]["symbol"],
                blockchain_instance=self.blockchain
            )
        elif isinstance(other, Amount):
            check_asset(other["asset"], self["quote"]["asset"], self.blockchain)
            a = other.copy() / self["price"]
            a["asset"] = self["base"]["asset"].copy()
            a["symbol"] = self["base"]["asset"]["symbol"]
        else:
            a["base"] /= other
        return a

    def __idiv__(self, other):
        if isinstance(other, Price):
            tmp = self / other
            self["base"] = tmp["base"]
            self["quote"] = tmp["quote"]
        else:
            self["base"] /= other
        return self

    def __floordiv__(self, other):
        raise NotImplementedError("This is not possible as the price is a ratio")

    def __ifloordiv__(self, other):
        raise NotImplementedError("This is not possible as the price is a ratio")

    def __lt__(self, other):
        if isinstance(other, Price):
            self._check_other(other)
            return self["price"] < other["price"]
        else:
            return self["price"] < float(other or 0)

    def __le__(self, other):
        if isinstance(other, Price):
            self._check_other(other)
            return self["price"] <= other["price"]
        else:
            return self["price"] <= float(other or 0)

    def __eq__(self, other):
        if isinstance(other, Price):
            self._check_other(other)
            return self["price"] == other["price"]
        else:
            return self["price"] == float(other or 0)

    def __ne__(self, other):
        if isinstance(other, Price):
            self._check_other(other)
            return self["price"] != other["price"]
        else:
            return self["price"] != float(other or 0)

    def __ge__(self, other):
        if isinstance(other, Price):
            self._check_other(other)
            return self["price"] >= other["price"]
        else:
            return self["price"] >= float(other or 0)

    def __gt__(self, other):
        if isinstance(other, Price):
            self._check_other(other)
            return self["price"] > other["price"]
        else:
            return self["price"] > float(other or 0)

    __truediv__ = __div__
    __truemul__ = __mul__
    __str__ = __repr__

    @property
    def market(self):
        """ Open the corresponding market

            :returns: Instance of :class:`blurtpy.market.Market` for the
                      corresponding pair of assets.
        """
        from .market import Market
        return Market(
            base=self["base"]["asset"],
            quote=self["quote"]["asset"],
            blockchain_instance=self.blockchain
        )


class Order(Price):
    """ This class inherits :class:`blurtpy.price.Price` but has the ``base``
        and ``quote`` Amounts not only be used to represent the price (as a
        ratio of base and quote) but instead has those amounts represent the
        amounts of an actual order!

        :param Blurt blockchain_instance: Blurt instance

        .. note::

                If an order is marked as deleted, it will carry the
                'deleted' key which is set to ``True`` and all other
                data be ``None``.
    """
    def __init__(self, base, quote=None, blockchain_instance=None, **kwargs):

        self.blockchain = blockchain_instance or shared_blockchain_instance()

        if (
            isinstance(base, dict) and
            "sell_price" in base
        ):
            super(Order, self).__init__(base["sell_price"],
                                        blockchain_instance=self.blockchain)
            self["id"] = base.get("id")
        elif (
            isinstance(base, dict) and
            "min_to_receive" in base and
            "amount_to_sell" in base
        ):
            super(Order, self).__init__(
                Amount(base["min_to_receive"], blockchain_instance=self.blockchain),
                Amount(base["amount_to_sell"], blockchain_instance=self.blockchain),
                blockchain_instance=self.blockchain
            )
            self["id"] = base.get("id")
        elif isinstance(base, Amount) and isinstance(quote, Amount):
            super(Order, self).__init__(None, base=base, quote=quote,
                                        blockchain_instance=self.blockchain)
        else:
            raise ValueError("Unknown format to load Order")

    def __repr__(self):
        if "deleted" in self and self["deleted"]:
            return "deleted order %s" % self["id"]
        else:
            t = ""
            if "time" in self and self["time"]:
                t += "(%s) " % self["time"]
            if "type" in self and self["type"]:
                t += "%s " % str(self["type"])
            if "quote" in self and self["quote"]:
                t += "%s " % str(self["quote"])
            if "base" in self and self["base"]:
                t += "%s " % str(self["base"])
            return t + "@ " + Price.__repr__(self)

    __str__ = __repr__


class FilledOrder(Price):
    """ This class inherits :class:`blurtpy.price.Price` but has the ``base``
        and ``quote`` Amounts not only be used to represent the price (as a
        ratio of base and quote) but instead has those amounts represent the
        amounts of an actually filled order!

        :param Blurt blockchain_instance: Blurt instance

        .. note:: Instances of this class come with an additional ``date`` key
                  that shows when the order has been filled!
    """

    def __init__(self, order, blockchain_instance=None, **kwargs):

        self.blockchain = blockchain_instance or shared_blockchain_instance()
        if isinstance(order, dict) and "current_pays" in order and "open_pays" in order:
            # filled orders from account history
            if "op" in order:
                order = order["op"]

            super(FilledOrder, self).__init__(
                Amount(order["open_pays"], blockchain_instance=self.blockchain),
                Amount(order["current_pays"], blockchain_instance=self.blockchain),
                blockchain_instance=self.blockchain
            )
            if "date" in order:
                self["date"] = formatTimeString(order["date"])

        else:
            raise ValueError("Couldn't parse 'Price'.")

    def json(self):
        return {
            "date": formatTimeString(self["date"]),
            "current_pays": self["base"].json(),
            "open_pays": self["quote"].json(),
        }

    def __repr__(self):
        t = ""
        if "date" in self and self["date"]:
            t += "(%s) " % self["date"]
        if "type" in self and self["type"]:
            t += "%s " % str(self["type"])
        if "quote" in self and self["quote"]:
            t += "%s " % str(self["quote"])
        if "base" in self and self["base"]:
            t += "%s " % str(self["base"])
        return t + "@ " + Price.__repr__(self)

    __str__ = __repr__
