from blurtgraphenebase.py23 import bytes_types, integer_types, string_types, text_type
from blurtpy.instance import shared_blockchain_instance
from blurtpy.asset import Asset
from .exceptions import InvalidAssetException
from .utils import assets_from_string
from decimal import Decimal, ROUND_DOWN
from fractions import Fraction


def check_asset(other, self, stm):
    if isinstance(other, dict) and "asset" in other and isinstance(self, dict) and "asset" in self:
        if not Asset(other["asset"], blockchain_instance=stm) == Asset(self["asset"], blockchain_instance=stm):
            raise AssertionError()
    else:
        if not other == self:
            raise AssertionError()


def quantize(amount, precision):
    # make sure amount is decimal and has the asset precision
    amount = Decimal(amount)
    places = Decimal(10) ** (-precision)
    return amount.quantize(places, rounding=ROUND_DOWN)  


class Amount(dict):
    """ This class deals with Amounts of any asset to simplify dealing with the tuple::

            (amount, asset)

        :param list args: Allows to deal with different representations of an amount
        :param float amount: Let's create an instance with a specific amount
        :param str asset: Let's you create an instance with a specific asset (symbol)
        :param boolean fixed_point_arithmetic: when set to True, all operation are fixed
            point operations and the amount is always be rounded down to the precision
        :param Blurt blurt_instance: Blurt instance
        :returns: All data required to represent an Amount/Asset
        :rtype: dict
        :raises ValueError: if the data provided is not recognized

        Way to obtain a proper instance:

            * ``args`` can be a string, e.g.:  "1 BLURT"
            * ``args`` can be a dictionary containing ``amount`` and ``asset_id``
            * ``args`` can be a dictionary containing ``amount`` and ``asset``
            * ``args`` can be a list of a ``float`` and ``str`` (symbol)
            * ``args`` can be a list of a ``float`` and a :class:`blurtpy.asset.Asset`
            * ``amount`` and ``asset`` are defined manually

        An instance is a dictionary and comes with the following keys:

            * ``amount`` (float)
            * ``symbol`` (str)
            * ``asset`` (instance of :class:`blurtpy.asset.Asset`)

        Instances of this class can be used in regular mathematical expressions
        (``+-*/%``) such as:

        .. testcode::

            from blurtpy.amount import Amount
            from blurtpy.asset import Asset
            a = Amount("1 BLURT")
            b = Amount(1, "BLURT")
            c = Amount("20", Asset("BLURT"))
            a + b
            a * 2
            a += b
            a /= 2.0

        .. testoutput::

            2.000 BLURT
            2.000 BLURT

    """
    def __init__(self, amount, asset=None, fixed_point_arithmetic=False, new_appbase_format=True, blockchain_instance=None, **kwargs):
        self["asset"] = {}
        self.new_appbase_format = new_appbase_format
        self.fixed_point_arithmetic = fixed_point_arithmetic
        
        if blockchain_instance is None:
            if kwargs.get("blurt_instance"):
                blockchain_instance = kwargs["blurt_instance"]
        self.blockchain = blockchain_instance or shared_blockchain_instance()           

        if amount and asset is None and isinstance(amount, Amount):
            # Copy Asset object
            self["amount"] = amount["amount"]
            self["symbol"] = amount["symbol"]
            self["asset"] = amount["asset"]

        elif amount and asset is None and isinstance(amount, list) and len(amount) == 3:
            # Copy Asset object
            self["amount"] = Decimal(amount[0]) / Decimal(10 ** amount[1])
            self["asset"] = Asset(amount[2], blockchain_instance=self.blockchain)
            self["symbol"] = self["asset"]["symbol"]

        elif amount and asset is None and isinstance(amount, dict) and "amount" in amount and "nai" in amount and "precision" in amount:
            # Copy Asset object
            self.new_appbase_format = True
            self["amount"] = Decimal(amount["amount"]) / Decimal(10 ** amount["precision"])
            self["asset"] = Asset(amount["nai"], blockchain_instance=self.blockchain)
            self["symbol"] = self["asset"]["symbol"]

        elif amount is not None and asset is None and isinstance(amount, string_types):
            self["amount"], self["symbol"] = amount.split(" ")
            self["asset"] = Asset(self["symbol"], blockchain_instance=self.blockchain)

        elif (amount and asset is None and isinstance(amount, dict) and "amount" in amount and "asset_id" in amount):
            self["asset"] = Asset(amount["asset_id"], blockchain_instance=self.blockchain)
            self["symbol"] = self["asset"]["symbol"]
            self["amount"] = Decimal(amount["amount"]) / Decimal(10 ** self["asset"]["precision"])

        elif (amount and asset is None and isinstance(amount, dict) and "amount" in amount and "asset" in amount):
            self["asset"] = Asset(amount["asset"], blockchain_instance=self.blockchain)
            self["symbol"] = self["asset"]["symbol"]
            self["amount"] = Decimal(amount["amount"]) / Decimal(10 ** self["asset"]["precision"])

        elif isinstance(amount, (float)) and asset and isinstance(asset, Asset):
            self["amount"] = str(amount)
            self["asset"] = asset
            self["symbol"] = self["asset"]["symbol"]

        elif isinstance(amount, (integer_types,  Decimal)) and asset and isinstance(asset, Asset):
            self["amount"] = amount
            self["asset"] = asset
            self["symbol"] = self["asset"]["symbol"]
            
        elif isinstance(amount, (float)) and asset and isinstance(asset, dict):
            self["amount"] = str(amount)
            self["asset"] = asset
            self["symbol"] = self["asset"]["symbol"]

        elif isinstance(amount, (integer_types, Decimal)) and asset and isinstance(asset, dict):
            self["amount"] = amount
            self["asset"] = asset
            self["symbol"] = self["asset"]["symbol"]            

        elif isinstance(amount, (float)) and asset and isinstance(asset, string_types):
            self["amount"] = str(amount)
            self["asset"] = Asset(asset, blockchain_instance=self.blockchain)
            self["symbol"] = asset

        elif isinstance(amount, (integer_types, Decimal)) and asset and isinstance(asset, string_types):
            self["amount"] = amount
            self["asset"] = Asset(asset, blockchain_instance=self.blockchain)
            self["symbol"] = asset  
        elif amount and asset and isinstance(asset, Asset):
            self["amount"] = amount
            self["symbol"] = asset["symbol"]
            self["asset"] = asset
        elif amount and asset and isinstance(asset, string_types):
            self["amount"] = amount
            self["asset"] = Asset(asset, blockchain_instance=self.blockchain)
            self["symbol"] = self["asset"]["symbol"]            
        else:
            raise ValueError
        if self.fixed_point_arithmetic:
            self["amount"] = quantize(self["amount"], self["asset"]["precision"])
        else:
            self["amount"] = Decimal(self["amount"])

    def copy(self):
        """ Copy the instance and make sure not to use a reference
        """
        return Amount(
            amount=self["amount"],
            asset=self["asset"].copy(),
            new_appbase_format=self.new_appbase_format,
            fixed_point_arithmetic=self.fixed_point_arithmetic,
            blockchain_instance=self.blockchain)

    @property
    def amount(self):
        """ Returns the amount as float
        """
        return float(self["amount"])

    @property
    def amount_decimal(self):
        """ Returns the amount as decimal
        """
        return self["amount"]

    @property
    def symbol(self):
        """ Returns the symbol of the asset
        """
        return self["symbol"]

    def tuple(self):
        return float(self), self.symbol

    @property
    def asset(self):
        """ Returns the asset as instance of :class:`blurt.asset.Asset`
        """
        if not self["asset"]:
            self["asset"] = Asset(self["symbol"], blockchain_instance=self.blockchain)
        return self["asset"]

    def json(self):
        if self.blockchain.is_connected() and self.blockchain.rpc.get_use_appbase():
            if self.new_appbase_format:
                return {'amount': str(int(self)), 'nai': self["asset"]["asset"], 'precision': self["asset"]["precision"]}
            else:
                return [str(int(self)), self["asset"]["precision"], self["asset"]["asset"]]
        else:
            return str(self)

    def __str__(self):
        amount = quantize(self["amount"], self["asset"]["precision"])
        symbol = self["symbol"]
        return "{:.{prec}f} {}".format(
            amount,
            symbol,
            prec=self["asset"]["precision"]
        )

    def __float__(self):
        if self.fixed_point_arithmetic:
            return float(quantize(self["amount"], self["asset"]["precision"]))
        else:
            return float(self["amount"])

    def __int__(self):
        amount = quantize(self["amount"], self["asset"]["precision"])
        return int(amount * 10 ** self["asset"]["precision"])

    def __add__(self, other):
        a = self.copy()
        if isinstance(other, Amount):
            check_asset(other["asset"], self["asset"], self.blockchain)
            a["amount"] += other["amount"]
        else:
            a["amount"] += Decimal(other)
        if self.fixed_point_arithmetic:
            a["amount"] = quantize(a["amount"], self["asset"]["precision"])
        return a

    def __sub__(self, other):
        a = self.copy()
        if isinstance(other, Amount):
            check_asset(other["asset"], self["asset"], self.blockchain)
            a["amount"] -= other["amount"]
        else:
            a["amount"] -= Decimal(other)
        if self.fixed_point_arithmetic:
            a["amount"] = quantize(a["amount"], self["asset"]["precision"])
        return a

    def __mul__(self, other):
        a = self.copy()
        if isinstance(other, Amount):
            check_asset(other["asset"], self["asset"], self.blockchain)
            a["amount"] *= other["amount"]
        elif isinstance(other, ExchangeRate):
            if not self["asset"] == other["quote"]["asset"]:
                raise AssertionError()
            a = self.copy() * other["price"]
            a["asset"] = other["base"]["asset"].copy()
            a["symbol"] = other["base"]["asset"]["symbol"]
        else:
            a["amount"] *= Decimal(other)
        if self.fixed_point_arithmetic:
            a["amount"] = quantize(a["amount"], self["asset"]["precision"])
        return a

    def __floordiv__(self, other):
        a = self.copy()
        if isinstance(other, Amount):
            return ExchangeRate(base=self, quote=other, blockchain_instance=self.blockchain)
        else:
            a["amount"] //= Decimal(other)
        if self.fixed_point_arithmetic:
            a["amount"] = quantize(a["amount"], self["asset"]["precision"])
        return a

    def __div__(self, other):
        a = self.copy()
        if isinstance(other, Amount):
            return ExchangeRate(base=self, quote=other, blockchain_instance=self.blockchain)
        elif isinstance(other, ExchangeRate):
            if not self["asset"] == other["base"]["asset"]:
                raise AssertionError()
            a = self.copy()
            a["amount"] = a["amount"] / other["price"]
            a["asset"] = other["quote"]["asset"].copy()
            a["symbol"] = other["quote"]["asset"]["symbol"]
        else:
            a["amount"] /= Decimal(other)
        if self.fixed_point_arithmetic:
            a["amount"] = quantize(a["amount"], self["asset"]["precision"])
        return a

    def __truediv__(self, other):
        return self.__div__(other)

    def __mod__(self, other):
        a = self.copy()
        if isinstance(other, Amount):
            check_asset(other["asset"], self["asset"], self.blockchain)
            a["amount"] %= other["amount"]
        else:
            a["amount"] %= Decimal(other)
        if self.fixed_point_arithmetic:
            a["amount"] = quantize(a["amount"], self["asset"]["precision"])
        return a

    def __pow__(self, other):
        a = self.copy()
        if isinstance(other, Amount):
            check_asset(other["asset"], self["asset"], self.blockchain)
            a["amount"] **= other["amount"]
        else:
            a["amount"] **= Decimal(other)
        if self.fixed_point_arithmetic:
            a["amount"] = quantize(a["amount"], self["asset"]["precision"])
        return a

    def __iadd__(self, other):
        if isinstance(other, Amount):
            check_asset(other["asset"], self["asset"], self.blockchain)
            self["amount"] += other["amount"]
        else:
            self["amount"] += Decimal(other)
        if self.fixed_point_arithmetic:
            self["amount"] = quantize(self["amount"], self["asset"]["precision"])
        return self

    def __isub__(self, other):
        if isinstance(other, Amount):
            check_asset(other["asset"], self["asset"], self.blockchain)
            self["amount"] -= other["amount"]
        else:
            self["amount"] -= Decimal(other)
        if self.fixed_point_arithmetic:
            self["amount"] = quantize(self["amount"], self["asset"]["precision"])
        return self

    def __imul__(self, other):
        if isinstance(other, Amount):
            check_asset(other["asset"], self["asset"], self.blockchain)
            self["amount"] *= other["amount"]
        else:
            self["amount"] *= Decimal(other)
        
        self["amount"] = quantize(self["amount"], self["asset"]["precision"])
        return self

    def __idiv__(self, other):
        if isinstance(other, Amount):
            check_asset(other["asset"], self["asset"], self.blockchain)
            return self["amount"] / other["amount"]
        else:
            self["amount"] /= Decimal(other)
        if self.fixed_point_arithmetic:
            self["amount"] = quantize(self["amount"], self["asset"]["precision"])
        return self

    def __ifloordiv__(self, other):
        if isinstance(other, Amount):
            self["amount"] //= other["amount"]
        else:
            self["amount"] //= Decimal(other)
        self["amount"] = quantize(self["amount"], self["asset"]["precision"])
        return self

    def __imod__(self, other):
        if isinstance(other, Amount):
            check_asset(other["asset"], self["asset"], self.blockchain)
            self["amount"] %= other["amount"]
        else:
            self["amount"] %= Decimal(other)
        if self.fixed_point_arithmetic:
            self["amount"] = quantize(self["amount"], self["asset"]["precision"])
        return self

    def __ipow__(self, other):
        if isinstance(other, Amount):
            self["amount"] **= other
        else:
            self["amount"] **= Decimal(other)
        if self.fixed_point_arithmetic:
            self["amount"] = quantize(self["amount"], self["asset"]["precision"])
        return self

    def __lt__(self, other):
        quant_amount = quantize(self["amount"], self["asset"]["precision"])
        if isinstance(other, Amount):
            check_asset(other["asset"], self["asset"], self.blockchain)
            return quant_amount < quantize(other["amount"], self["asset"]["precision"])
        else:
            return quant_amount < quantize((other or 0), self["asset"]["precision"])

    def __le__(self, other):
        quant_amount = quantize(self["amount"], self["asset"]["precision"])
        if isinstance(other, Amount):
            check_asset(other["asset"], self["asset"], self.blockchain)
            return quant_amount <= quantize(other["amount"], self["asset"]["precision"])
        else:
            return quant_amount <= quantize((other or 0), self["asset"]["precision"])

    def __eq__(self, other):
        quant_amount = quantize(self["amount"], self["asset"]["precision"])
        if isinstance(other, Amount):
            check_asset(other["asset"], self["asset"], self.blockchain)
            return quant_amount == quantize(other["amount"], self["asset"]["precision"])
        else:
            return quant_amount == quantize((other or 0), self["asset"]["precision"])

    def __ne__(self, other):
        quant_amount = quantize(self["amount"], self["asset"]["precision"])
        if isinstance(other, Amount):
            check_asset(other["asset"], self["asset"], self.blockchain)
            return self["amount"] != quantize(other["amount"], self["asset"]["precision"])
        elif isinstance(other, ExchangeRate):
            return False        
        else:
            return quant_amount != quantize((other or 0), self["asset"]["precision"])

    def __ge__(self, other):
        quant_amount = quantize(self["amount"], self["asset"]["precision"])
        if isinstance(other, Amount):
            check_asset(other["asset"], self["asset"], self.blockchain)
            return self["amount"] >= quantize(other["amount"], self["asset"]["precision"])
        else:
            return quant_amount >= quantize((other or 0), self["asset"]["precision"])

    def __gt__(self, other):
        quant_amount = quantize(self["amount"], self["asset"]["precision"])
        if isinstance(other, Amount):
            check_asset(other["asset"], self["asset"], self.blockchain)
            return quant_amount > quantize(other["amount"], self["asset"]["precision"])
        else:
            return quant_amount > quantize((other or 0), self["asset"]["precision"])

    __repr__ = __str__
    __truediv__ = __div__
    __truemul__ = __mul__


class ExchangeRate(dict):
    """ This class deals with all sorts of exchange rates of any pair of assets.

        :param list args: Allows to deal with different representations of a price
        :param Asset base: Base asset
        :param Asset quote: Quote asset
        :param Blurt blockchain_instance: Blurt instance
        :returns: All data required to represent an exchange rate
        :rtype: dictionary

        .. note::

            The rate (floating) is derived as ``base/quote``

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
            self["base"] = Amount(price["base"], blockchain_instance=self.blockchain)
            self["quote"] = Amount(price["quote"], blockchain_instance=self.blockchain)

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

        elif isinstance(price, Amount) and isinstance(base, Amount):
            self["quote"], self["base"] = price, base

        elif (price is None and isinstance(base, Amount) and isinstance(quote, Amount)):
            self["quote"] = quote
            self["base"] = base

        elif ((isinstance(price, float) or isinstance(price, integer_types) or isinstance(price, Decimal)) and
                isinstance(base, string_types)):
            base_symbol, quote_symbol = assets_from_string(base)
            base = Asset(base_symbol, blockchain_instance=self.blockchain)
            quote = Asset(quote_symbol, blockchain_instance=self.blockchain)
            frac = Fraction(float(price)).limit_denominator(10 ** base["precision"])
            self["quote"] = Amount(amount=frac.denominator, asset=quote, blockchain_instance=self.blockchain)
            self["base"] = Amount(amount=frac.numerator, asset=base, blockchain_instance=self.blockchain)

        else:
            raise ValueError("Couldn't parse 'ExchangeRate'.")

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        if ("quote" in self and
                "base" in self and
                self["base"] and self["quote"]):
            dict.__setitem__(self, "price", self._safedivide(
                self["base"]["amount"],
                self["quote"]["amount"]))

    def copy(self):
        return ExchangeRate(
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
        if base == self["base"]["symbol"]:
            return self.copy()
        elif base == self["quote"]["symbol"]:
            return self.copy().invert()
        else:
            raise InvalidAssetException

    def as_quote(self, quote):
        if quote == self["quote"]["symbol"]:
            return self.copy()
        elif quote == self["base"]["symbol"]:
            return self.copy().invert()
        else:
            raise InvalidAssetException

    def invert(self):
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
        if isinstance(other, ExchangeRate):
            if (
                self["quote"]["symbol"] not in other.symbols() and
                self["base"]["symbol"] not in other.symbols()
            ):
                raise InvalidAssetException

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
                raise ValueError("Wrong rotation of rates")
        elif isinstance(other, Amount):
            check_asset(other["asset"], self["quote"]["asset"], self.blockchain)
            a = other.copy() * self["price"]
            a["asset"] = self["base"]["asset"].copy()
            a["symbol"] = self["base"]["asset"]["symbol"]
        else:
            a["base"] *= other
        return a

    def __imul__(self, other):
        if isinstance(other, ExchangeRate):
            tmp = self * other
            self["base"] = tmp["base"]
            self["quote"] = tmp["quote"]
        else:
            self["base"] *= other
        return self

    def __div__(self, other):
        a = self.copy()
        if isinstance(other, ExchangeRate):
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
        if isinstance(other, ExchangeRate):
            tmp = self / other
            self["base"] = tmp["base"]
            self["quote"] = tmp["quote"]
        else:
            self["base"] /= other
        return self

    def __floordiv__(self, other):
        raise NotImplementedError("This is not possible as the rate is a ratio")

    def __ifloordiv__(self, other):
        raise NotImplementedError("This is not possible as the rate is a ratio")

    def __lt__(self, other):
        if isinstance(other, ExchangeRate):
            self._check_other(other)
            return self["price"] < other["price"]
        else:
            return self["price"] < float(other or 0)

    def __le__(self, other):
        if isinstance(other, ExchangeRate):
            self._check_other(other)
            return self["price"] <= other["price"]
        else:
            return self["price"] <= float(other or 0)

    def __eq__(self, other):
        if isinstance(other, ExchangeRate):
            self._check_other(other)
            return self["price"] == other["price"]
        else:
            return self["price"] == float(other or 0)

    def __ne__(self, other):
        if isinstance(other, ExchangeRate):
            self._check_other(other)
            return self["price"] != other["price"]
        else:
            return self["price"] != float(other or 0)

    def __ge__(self, other):
        if isinstance(other, ExchangeRate):
            self._check_other(other)
            return self["price"] >= other["price"]
        else:
            return self["price"] >= float(other or 0)

    def __gt__(self, other):
        if isinstance(other, ExchangeRate):
            self._check_other(other)
            return self["price"] > other["price"]
        else:
            return self["price"] > float(other or 0)

    __truediv__ = __div__
    __truemul__ = __mul__
    __str__ = __repr__
