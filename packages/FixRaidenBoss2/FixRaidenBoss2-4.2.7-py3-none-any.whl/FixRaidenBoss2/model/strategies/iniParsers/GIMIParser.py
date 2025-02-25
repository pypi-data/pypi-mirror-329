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
import re
from functools import cmp_to_key
from typing import TYPE_CHECKING, Set, Optional, Callable, Dict, List
##### EndExtImports

##### LocalImports
from ....constants.IniConsts import IniKeywords
from .BaseIniParser import BaseIniParser
from ....constants.IniConsts import IniKeywords
from ...IniSectionGraph import IniSectionGraph
from ...iniresources.IniResourceModel import IniResourceModel

if (TYPE_CHECKING):
    from ...files.IniFile import IniFile
##### EndLocalImports


##### Script
class GIMIParser(BaseIniParser):
    """
    This class inherits from :class:`BaseIniParser`

    Parses a .ini file used by a GIMI related importer

    Parameters
    ----------
    iniFile: :class:`IniFile`
        The .ini file to parse

    Attributes
    ----------
    blendCommandsGraph: :class:`IniSectionGraph`
        All the `sections`_ that use some ``[Resource.*Blend.*]`` section.

    nonBlendHashIndexCommandsGraph: :class:`IniSectionGraph`
        All the `sections`_ that are not used by the ``[Resource.*Blend.*]`` sections and contains the target hashes/indices that need to be replaced

    resourceCommandsGraph: :class:`IniSectionGraph`
        All the related `sections`_ to the ``[Resource.*Blend.*]`` sections that are used by `sections`_ related to the ``[TextureOverride.*Blend.*]`` sections.
        The keys are the name of the `sections`_.

    _sectionRoots: Dict[:class:`str`, List[:class:`str`]]
        The names of the `sections`_ that are the root nodes to a particular group of `sections`_ in the
        `section`_ caller/callee `graph`_  :raw-html:`<br />` :raw-html:`<br />`

        The keys are the ids for a particular group of `sections`_ and the values are the root `section`_ names for that group
    """

    BlendRootPattern = re.compile(r"^textureoverride((?!remap).)*blend")
    PositionRootPattern = re.compile(r"^textureoverride((?!remap).)*position")

    def __init__(self, iniFile: "IniFile"):
        super().__init__(iniFile)
        self.blendCommandsGraph = IniSectionGraph(set(), {})
        self.nonBlendHashIndexCommandsGraph = IniSectionGraph(set(), {})
        self.resourceCommandsGraph = IniSectionGraph(set(), {})
        self._sectionRoots: Dict[str, List[str]] = {}

    def clear(self):
        super().clear()
        self.blendCommandsGraph.build(newTargetSections = set(), newAllSections = {})
        self.nonBlendHashIndexCommandsGraph.build(newTargetSections = set(), newAllSections = {})
        self.resourceCommandsGraph.build(newTargetSections = set(), newAllSections = {})
        self._sectionRoots.clear()

    # _getCommonMods(): Retrieves the common mods that need to be fixed between all target graphs
    #   that are used for the fix
    def _getCommonMods(self) -> Set[str]:
        modType = self._iniFile.type
        if (modType is None):
            return set()
        
        result = set()
        hashes = modType.hashes
        indices = modType.indices

        graphs = [self.blendCommandsGraph, self.nonBlendHashIndexCommandsGraph, self.resourceCommandsGraph]
        for graph in graphs:
            commonMods = graph.getCommonMods(hashes, indices, version = self._iniFile.version)
            if (not result):
                result = commonMods
            elif (commonMods):
                result = result.intersection(commonMods)

        return result
    
    def _setToFix(self) -> Set[str]:
        """
        Sets the names for the types of mods that will used in the fix

        Returns
        -------
        Set[:class:`str`]
            The names of the mods that will be used in the fix        
        """

        commonMods = self._getCommonMods()
        toFix = commonMods
        iniModsToFix = self._iniFile.modsToFix
        if (iniModsToFix):
            toFix = toFix.intersection(iniModsToFix)

        type = self._iniFile.availableType

        if (not toFix and type is not None):
            self._modsToFix = type.getModsToFix()
        elif (not toFix):
            self._modsToFix = commonMods
        else:
            self._modsToFix = toFix

        return self._modsToFix
    
    # _makeRemapNames(): Makes the required names used for the fix
    def _makeRemapNames(self):
        self.blendCommandsGraph.getRemapBlendNames(self._modsToFix)
        self.nonBlendHashIndexCommandsGraph.getRemapBlendNames(self._modsToFix)
        self.resourceCommandsGraph.getRemapBlendNames(self._modsToFix)

    def _makeRemapModels(self, resourceGraph: IniSectionGraph, getFixedFile: Optional[Callable[[str], str]] = None) -> Dict[str, IniResourceModel]:
        """
        Creates all the data needed for fixing the ``[Resource.*Blend.*]`` `sections`_ in the .ini file

        Parameters
        ----------
        resourceGraph: :class:`IniSectionGraph`
            The graph of `sections`_ for the resources

        getFixedFile: Optional[Callable[[:class:`str`], :class:`str`]]
            The function for transforming the file path of a found .*Blend.buf file into a .*RemapBlend.buf file :raw-html:`<br />` :raw-html:`<br />`

            If this value is ``None``, then will use :meth:`IniFile.getFixedBlendFile` :raw-html:`<br />` :raw-html:`<br />`

            **Default**: ``None``

        Returns
        -------
        Dict[:class:`str`, :class:`IniResourceModel`]
            The data for fixing the resource `sections`_

            The keys are the original names for the resource `sections`_ and the values are the required data for fixing the `sections`_
        """

        resourceCommands = resourceGraph.sections
        for resourceKey in resourceCommands:
            resourceIftemplate = resourceCommands[resourceKey]
            remapBlendModel = self._iniFile.makeResourceModel(resourceIftemplate, toFix = self._modsToFix, getFixedFile = getFixedFile)
            self._iniFile.remapBlendModels[resourceKey] = remapBlendModel

        return self._iniFile.remapBlendModels
    
    def _getSectionRoots(self):
        """
        Retrieves the root `sections`_ names that correspond to a either 
        ``TextureOverride.*Blend`` or ``TextureOverride.*Position``
        """

        blendRoots = self._sectionRoots.get(IniKeywords.Blend.value)
        if (blendRoots is None):
            blendRoots = []
            self._sectionRoots[IniKeywords.Blend.value] = blendRoots

        positionRoots = self._sectionRoots.get(IniKeywords.Position.value)
        if (positionRoots is None):
            positionRoots = []
            self._sectionRoots[IniKeywords.Position.value] = positionRoots

        positionRoots = self._sectionRoots.get(IniKeywords.Position.value)
        if (positionRoots is None):
            positionRoots = []
            self._sectionRoots[IniKeywords.Position.value] = positionRoots

        for sectionName in self._iniFile.sectionIfTemplates:
            cleanedSectionName = sectionName.lower()
            if (re.search(self.BlendRootPattern, cleanedSectionName)):
                blendRoots.append(sectionName)
            elif (re.search(self.PositionRootPattern, cleanedSectionName)):
                positionRoots.append(sectionName)

    def parse(self):
        self._getSectionRoots()
        blendRoots = self._sectionRoots[IniKeywords.Blend.value]

        self.blendCommandsGraph.remapNameFunc = self._iniFile.getRemapBlendName
        self.nonBlendHashIndexCommandsGraph.remapNameFunc = self._iniFile.getRemapFixName
        self.resourceCommandsGraph.remapNameFunc = self._iniFile.getRemapBlendResourceName

        if (blendRoots):
            blendResources = set()

            # build the blend commands DFS forest
            subCommands = blendRoots
            self.blendCommandsGraph.build(newTargetSections = subCommands, newAllSections = self._iniFile.sectionIfTemplates)

            # keep track of all the needed blend dependencies
            self._iniFile.getResources(self.blendCommandsGraph, lambda part: IniKeywords.Vb1.value in part, lambda part: set(map(lambda resourceData: resourceData[1], part[IniKeywords.Vb1.value])),
                                    lambda resource, part: blendResources.update(resource))

            # sort the resources
            resourceCommandLst = list(map(lambda resourceName: (resourceName, self._iniFile.getMergedResourceIndex(resourceName)), blendResources))
            resourceCommandLst.sort(key = cmp_to_key(self._iniFile.compareResources))
            resourceCommandLst = list(map(lambda resourceTuple: resourceTuple[0], resourceCommandLst))

            # keep track of all the subcommands that the resources call
            self.resourceCommandsGraph.build(newTargetSections = resourceCommandLst, newAllSections = self._iniFile.sectionIfTemplates)

        # build the DFS forest for the other sections that contain target hashes/indices that are not part of the blend commands
        hashIndexSections = self._iniFile.getTargetHashAndIndexSections(set(self.blendCommandsGraph.sections.keys()))
        self.nonBlendHashIndexCommandsGraph.build(newTargetSections = hashIndexSections, newAllSections= self._iniFile.sectionIfTemplates)

        # get the required files that need fixing
        self._setToFix()
        self._makeRemapNames()
        self._makeRemapModels(self.resourceCommandsGraph)
##### EndScript