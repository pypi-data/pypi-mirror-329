##### Credits

# ===== Anime Game Remap (AG Remap) =====
# Authors: Albert Gold#2696, NK#1321
#
# if you used it to remap your mods pls give credit for "Albert Gold#2696" and "Nhok0169"
# Special Thanks:
#   nguen#2011 (for support)
#   SilentNightSound#7430 (for internal knowdege so wrote the blendCorrection code)
#   HazrateGolabi#1364 (for being awesome, and improving the code)

##### EndCredits

##### ExtImports
from typing import Type, List, Any, Dict, TYPE_CHECKING, Optional
##### EndExtImports

##### LocalImports
from ....tools.Builder import Builder
from .BaseIniParser import BaseIniParser

if (TYPE_CHECKING):
    from ...files.IniFile import IniFile
##### EndLocalImports


##### Script
class IniParseBuilder(Builder[BaseIniParser]):
    """
    This class inherits from :class:`Builder`

    A class to help dynamically build a :class:`BaseIniParser`

    Parameters
    ----------
    buildCls: Type[:class:`BaseIniParser`]
        The class to construct a :class:`BaseIniFixer` 

    args: Optional[List[Any]]
        The constant arguments used to build the object :raw-html:`<br />` :raw-html:`<br />`

        **Default**: ``None``

    kwargs: Optional[Dict[str, Any]]
        The constant keyword arguments used to build the object :raw-html:`<br />` :raw-html:`<br />`

        **Default**: ``None``
    """

    def __init__(self, buildCls: Type[BaseIniParser], args: Optional[List[Any]] = None, kwargs: Optional[Dict[str, Any]] = None):
        super().__init__(buildCls, args, kwargs)

    def build(self, iniFile: "IniFile") -> BaseIniParser:
        """
        Builds the parser

        Parameters
        ----------
        iniFile: :class:`IniFile`
            The .ini file to parse

        Returns
        -------
        :class:`BaseIniParser`
            The built parser
        """

        return super().build(iniFile)
##### EndScript