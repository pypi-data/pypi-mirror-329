import re
import time
from enum import Enum
from pathlib import Path
from random import Random
from typing import TypedDict, TypeVar

from .__init__ import logger
from .I18n import I18n
from .Tools import color

__all__ = [
    "Roll",
    "RollType",
    "returnType",
    "RollNumReturnType",
    "RollNumReturnValueType",
]


T = TypeVar("T")


class RollType(Enum):
    """the type of the roll."""

    NONE = 0

    DND = 1
    COC = 2


class returnType(Enum):
    """
    An enumeration representing different return types for a function or process.

    Attributes:
        BigNotSuccess (int): Represents a significant failure with a value of -2.
        notSuccess (int): Represents a failure with a value of -1.
        NONE (int): Represents a neutral or no result with a value of 0.
        success (int): Represents a success with a value of 1.
        BigSuccess (int): Represents a significant success with a value of 2.
    """

    BigNotSuccess = -2
    notSuccess = -1
    NONE = 0
    success = 1
    BigSuccess = 2


class RollNumReturnValueType(TypedDict):
    Value: int
    msg: str | None
    RollValueClass: returnType


class RollNumReturnType(TypedDict):
    rollValueList: list[int]
    Type: RollType
    returnValueList: list[RollNumReturnValueType]


class Roll:
    rollNumTextStructureSet: set[re.Pattern[str]] = {
        re.compile(r"(\d*)(d|D)(\d+)(( +)?((\+|\-)(\d+)))?")
    }

    @staticmethod
    def rollTextReplace(text: str) -> str:
        """
        Replaces specific keywords in the input text with their corresponding translations.

        Args:
            text (str): The input text to be processed.

        Returns:
            str: The processed text with replacements if applicable.

        Replacements:
            - "int" or "intelligence" -> "智力"
            - "san" or "sanity" -> "理智"

        If a replacement is made, a space is appended to the result.

        Logs:
            Logs the input text and the resulting text after processing.
        """
        isReplace: bool = True
        rText = text
        match text.lower():
            case "int" | "intelligence":
                rText = "智力"
            case "san" | "sanity":
                rText = "理智"
            case _:
                isReplace = False
        rText += " " if isReplace else ""
        logger.debug(f"rollTextReplace({repr(text)}) -> {repr(rText)}")
        return rText

    def __init__(
        self,
        debug: bool = False,
        rollType: RollType = RollType.NONE,
        logSum: bool = True,
        isLog: bool = True,
        seed: int | float | str | bytes | bytearray = time.time(),
    ) -> None:
        self.debug = debug
        self.rollType = rollType
        self.logSum = logSum
        self.isLog = isLog
        self.__seed = seed

        self.__i18n_obj = I18n(
            dirRoot=str(Path(__file__).parent),
            langJson={
                "en_us": {
                    "updata": "2024/5/24 12:56 UTC+8",
                    "any": "{}",
                    "file_lang": "en_us",
                    "paul_tools__Roll__Roll__Exception__rollText_Not_Match_The_Structure": "rollText will not ben {},will ben {}.",
                },
                "zh_hk": {
                    "updata": "2024/5/24 12:56 UTC+8",
                    "any": "{}",
                    "file_lang": "zh_hk",
                    "paul_tools__Roll__Roll__Exception__rollText_Not_Match_The_Structure": "rollText 不是{}，而是{}。",
                },
            },
        )
        self.__random_obj = Random()
        self.__random_obj.seed(self.__seed)
        logger.debug(f"random.seed: {self.seed}")

    @property
    def seed(self) -> int | float | str | bytes | bytearray:
        return self.__seed

    @seed.setter
    def seed(self, seed: int | float | str | bytes | bytearray) -> None:
        self.__seed = seed
        self.__random_obj.seed(self.__seed)
        logger.debug(f"set seed={self.__seed}")

    def RollNumRegTools(self, rollText: str):
        rollTextNotMatchTheStructure = Exception(
            self.__i18n_obj.locale(
                "paul_tools__Roll__Roll__Exception__rollText_Not_Match_The_Structure",
                repr(rollText),
                repr(self.rollNumTextStructureSet),
            )
        )
        rollData: list[str] | None = None
        userReg = None
        for rollTextStructure in self.rollNumTextStructureSet:
            if (tmp1 := re.search(rollTextStructure, rollText)) is None:
                continue
            userReg = rollTextStructure
            rollData = [tmp1.group(1), tmp1.group(3), tmp1.group(6)]
            break
        if rollData is None or len(rollData) != 3:
            raise rollTextNotMatchTheStructure
        else:
            logger.debug(f"RollNumRegTools({repr(rollText)})--{userReg=}")

        if rollData[0] == "":
            rollData[0] = "1"
        intRollData: list[int] = []
        if rollData[2] is None:
            rollData[2] = "0"
        for tmp1 in rollData:
            intRollData.append(int(tmp1))
        logger.debug(f"RollNumRegTools({repr(rollText)})--{userReg=}-{intRollData=}")
        return intRollData

    def RollNum(
        self,
        rollText: str | None = None,
        *,
        xD: int | None = None,
        Dy: int | None = None,
        sumBonus: int = 0,
        bonus: int = 0,
        success: int | None = None,
        whyJudged: str = "",
    ) -> RollNumReturnType:
        if Dy is None:
            if rollText is not None:
                intRollData = self.RollNumRegTools(rollText)

                xD, Dy = [intRollData[0], intRollData[1]]
                if sumBonus == 0:
                    sumBonus = intRollData[2]
            else:
                logger.warning("Dy is None and rollText is None")
                raise ValueError("Dy is None and rollText is None")

        if xD is None:
            xD = 1
        rollValueList: list[int] = []
        returnValueList: list[RollNumReturnValueType] = []
        whyJudged = self.rollTextReplace(whyJudged)

        logger.debug(f"rollIntData: {xD}d{Dy}")

        if self.isLog:
            print("=" * 20)
            _ = f" {success=}" if success is not None else ""
            print(f"Roll:> {whyJudged}({xD}d{Dy} {sumBonus:+}){_}")
            del _

        # 擲骰
        for i in range(xD):
            _i = i + 1
            rollValue = self.__random_obj.randint(1, Dy)
            trueRollValue = rollValue + bonus

            ####
            # #tag DEBUG for debug
            # rollValue = 19
            # trueRollValue = rollValue+bonus
            ####

            addMsg: str = ""
            printColor: str = ""
            RollValueClass = returnType.NONE
            if self.rollType != RollType.NONE:
                if success is not None:
                    if self.rollType == RollType.DND:
                        if trueRollValue >= success:
                            addMsg = f" [{whyJudged}成功]"
                            printColor = "GREEN"
                            RollValueClass = returnType.success
                        elif trueRollValue < success:
                            addMsg = f" [{whyJudged}失敗]"
                            printColor = "RED"
                            RollValueClass = returnType.notSuccess
                    elif self.rollType == RollType.COC:
                        if trueRollValue < success:
                            addMsg = f" [{whyJudged}成功]"
                            printColor = "GREEN"
                            RollValueClass = returnType.success
                        else:
                            addMsg = f" [{whyJudged}失敗]"
                            printColor = "RED"
                            RollValueClass = returnType.notSuccess
                if self.rollType == RollType.DND and Dy == 20:
                    if rollValue == 20:
                        addMsg = f" [{whyJudged}大成功!]"
                        printColor = "LIGHTGREEN_EX"
                        RollValueClass = returnType.BigSuccess
                    elif rollValue == 1:
                        addMsg = f" [{whyJudged}大失敗!]"
                        printColor = "LIGHTRED_EX"
                        RollValueClass = returnType.BigNotSuccess
                if self.rollType == RollType.COC and Dy == 100:
                    if rollValue == 0:
                        addMsg = f" [{whyJudged}大成功!]"
                        printColor = "LIGHTGREEN_EX"
                        RollValueClass = returnType.BigSuccess
                    elif rollValue == 100:
                        addMsg = f" [{whyJudged}大失敗!]"
                        printColor = "LIGHTRED_EX"
                        RollValueClass = returnType.BigNotSuccess
            msg: str | None = None
            if self.isLog:
                msgBonus = ""
                if bonus != 0:
                    msgBonus: str = str(bonus)
                    if msgBonus[0] != "-":
                        msgBonus = "+" + msgBonus
                    msgBonus += f" = {trueRollValue}"

                msg = f"   {xD}d{Dy}:[{_i:>{len(str(xD))}}] = {rollValue:>0{len(str(Dy))}} {msgBonus}{addMsg}"

                print(*color(msg, color=printColor))

            returnValueList.append(
                {"Value": trueRollValue, "msg": msg, "RollValueClass": RollValueClass}
            )
            rollValueList.append(trueRollValue)
            if self.debug:
                print(("rollValueList: ", rollValueList))

        if self.isLog:
            _ = sum(rollValueList)
            msgSumBonus = ""
            if sumBonus != 0:
                msgSumBonus = str(sumBonus)
                if msgSumBonus[0] != "-":
                    msgSumBonus = "+" + msgSumBonus
                msgSumBonus = " " + msgSumBonus
                msgSumBonus += f" = {_ + sumBonus}"
            if self.logSum:
                print(f"sum = {_}{msgSumBonus}")
            print(f"X̄ = {_ / len(rollValueList):.2f}")
            print("=" * 20)

        return {
            "rollValueList": rollValueList,
            "Type": self.rollType,
            "returnValueList": returnValueList,
        }

    def RollList(self, rollList: list[T], *, whyJudged: str = "") -> T:
        """RollList 的 Docstring

        :param self: 說明
        :type self:
        :param rollList: 說明
        :type rollList:
        :param whyJudged: 說明
        :type whyJudged: str
        :return: 說明
        :rtype: Any"""
        r: T = self.__random_obj.choice(rollList)
        if self.debug:
            print("rollValue: ", r)
        if self.isLog:
            print("=" * 20)
            print(f"Roll List:> {whyJudged}({' '.join(map(str, rollList))})")
            print(f"    r={r}")
            print("=" * 20)
        return r

    def getExpectedValue(
        self, values: list[int] | list[float], probabilities: list[float]
    ) -> float:
        """計算給定值和對應概率的期望值。

        Args:
            values (list[int] | list[float]): 一個包含數值的列表。
            probabilities (list[float]): 對應於數值的概率列表。

        Raises:
            ValueError: 如果 values 與 probabilities 長度不等。
            ValueError: 如果概率之和不等於 1。

        Returns:
            float: 計算出的期望值。
        """
        # 檢查 values 和 probabilities 的長度是否相等
        if len(values) != len(probabilities):
            raise ValueError("values 與 probabilities 長度不等。")

        # 確保概率之和為 1
        total_probability: float = sum(probabilities)
        if not (0.99 <= total_probability <= 1.01):  # 使用範圍來考慮浮點數誤差
            raise ValueError("概率之和並不等於 1，請檢查概率分配。")

        # 計算期望值
        expected_value: float = sum(v * p for v, p in zip(values, probabilities))
        return expected_value
