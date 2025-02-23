import json
import locale
import os
import time
from enum import Enum

from .__init__ import logger

__all__ = ["I18n"]


class I18n:
    ver = "1.0.0.0"

    LANG_MAP = {"zh": "zh_cn", "chinese (traditional)_hong kong sar": "zh_hk"}

    @staticmethod
    def langReplace(lang: str) -> str:
        """
        Replaces hyphens with underscores in the given language code and maps it to a standardized language code.

        Args:
            lang (str): The language code to be replaced.

        Returns:
            str: The standardized language code. If the input is "sys", it returns the system language code.
        """
        lang = lang.replace("-", "_")
        if lang == "sys":
            logger.debug(
                f"langReplace({lang})-> {(r := I18n.langReplace(I18n.getSysLang()))}"
            )
            return r
        logger.debug(f"langReplace({lang})-> {(r := I18n.LANG_MAP.get(lang, lang))}")
        return r

    @staticmethod
    def getSysLang() -> str:
        """
        Get the current system language code.

        This function retrieves the current system language code using the locale settings
        and returns it as a lowercase string.

        Returns:
            str: The current system language code in lowercase.
        """
        """Get the current system language code."""
        logger.debug(
            f"getSysLang()-> {(r := str(locale.getlocale(locale.LC_CTYPE)[0]).lower())}"
        )
        return r

    def __init__(
        self,
        Langs: list[str] = ["sys", "en_us"],
        dirRoot: str = os.getcwd(),
        langJson: dict[str, dict[str, str]] = {},
    ) -> None:
        """
        Initialize the I18n class.
        Args:
            Langs (list[str]): A list of language codes to load. Defaults to ["sys", "en_us"].
            dirRoot (str): The root directory where language files are stored. Defaults to the current working directory.
            langJson (dict[str, dict[str, str]]): A dictionary containing language-specific JSON data to merge with the loaded files. Defaults to an empty dictionary.
        Raises:
            ValueError: If the Langs list is empty.
        """
        self.DIR_ROOT = dirRoot
        self.DIR_LANGS_ROOT: str = os.path.join(self.DIR_ROOT, "langs")
        self.LANG_JSON: dict[str, str] = {}

        if len(Langs) == 0:
            raise ValueError("Langs must contain at least one language code.")
        self.langs = [self.langReplace(lang) for lang in Langs]
        logger.debug(f"langs: {self.langs}")
        logger.debug(f"langJson: {langJson}")
        logger.debug(f"DIR_LANGS_ROOT: {self.DIR_LANGS_ROOT}")

        # #tag load
        for lang in reversed(self.langs):
            # print(lang, end=" ")
            dF = {
                "#": "{file_name}__{class_name}__{func_name}__{id}",
                "updata": time.strftime("%Y/%m/%d %H:%M UTC%z"),
                "any": "{}",
                "file_lang": lang,
            }
            try:
                with open(
                    os.path.join(self.DIR_LANGS_ROOT, f"{lang}.json"),
                    "r",
                    encoding="utf8",
                ) as f:
                    fileJson = json.load(f)
            except FileNotFoundError:
                fileJson = dF  # 使用默認值
            except json.JSONDecodeError:
                fileJson = dF

            # breakpoint()
            self.LANG_JSON.update(fileJson)
            self.LANG_JSON.update(langJson.get(lang, {}))
        logger.debug(f"LANG_JSON: {self.LANG_JSON}")
        logger.debug(f"Initialized I18n with langs: {self.langs}")

    class Langs(Enum):
        """Enum class representing different language-related constants.
        Attributes:
            LANG_JSON (int): Constant representing a JSON language file.
            updata (int): Constant representing an update action.
            any (int): Constant representing any language.
            file_lang (int): Constant representing a file language.
        """

        LANG_JSON = -1
        updata = 0
        any = 1
        file_lang = 2

    def locale(self, raw: str | Langs, *args: object, **kwargs: object) -> str:
        """Translates a given string or Langs enum to the corresponding localized string.
        Args:
            raw (str | Langs): The raw string or Langs enum to be translated.
            *args (object): Positional arguments to format the translated string.
            **kwargs (object): Keyword arguments to format the translated string.
        Returns:
            str: The localized and formatted string if found, otherwise the original string.
        Raises:
            IndexError: If there is an issue with formatting the string using the provided arguments.
        Logs:
            Warnings if the translation is not found or if there is an issue with formatting.
            Debug information about the translation process.
        """
        text = raw.name if isinstance(raw, self.Langs) else raw

        langText = self.LANG_JSON.get(text)

        # errText = f"{{ no {repr(text)} in lang file {repr(self.langs)} }}"
        errText = text
        if langText is not None:
            try:
                langText = langText.format(*args, **kwargs)
            except IndexError as e:
                logger.warning(
                    f"{repr(e)}: {repr(langText)} -> {repr(args)} -> {repr(kwargs)}"
                )
            logger.debug(f"locale({repr(raw)}) -> {repr(text)} -> {repr(langText)}")
            return langText
        else:
            logger.warning(f"locale({repr(raw)}) -> {repr(text)} -> {repr(errText)}")
            return errText

    get = locale
