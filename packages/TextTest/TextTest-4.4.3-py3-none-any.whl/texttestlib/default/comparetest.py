import os
import filecmp
import shutil
import logging
from texttestlib.default import performance, knownbugs
from texttestlib import plugins
from collections import OrderedDict
from tempfile import mktemp
from .comparefile import FileComparison, SplitFileComparison
from fnmatch import fnmatch

plugins.addCategory("success", "succeeded")
plugins.addCategory("failure", "FAILED")


class BaseTestComparison(plugins.TestState):
    def __init__(self, category, previousInfo, completed, lifecycleChange=""):
        plugins.TestState.__init__(self, category, "", started=1, completed=completed,
                                   lifecycleChange=lifecycleChange, executionHosts=previousInfo.executionHosts)
        self.allResults = []
        self.changedResults = []
        self.newResults = []
        self.missingResults = []
        self.correctResults = []
        self.diag = logging.getLogger("TestComparison")

    def hasResults(self):
        return len(self.allResults) > 0

    def isAllNew(self):
        return len(self.newResults) == len(self.allResults)

    def findComparison(self, stem, includeSuccess=False):
        lists = [self.changedResults, self.newResults, self.missingResults]
        if includeSuccess:
            lists.append(self.correctResults)
        self.diag.info("Finding comparison for stem " + stem)
        for list in lists:
            for comparison in list:
                if comparison.stem == stem:
                    return comparison, list
        return None, None

    def findComparisonsMatching(self, pattern):
        lists = [self.changedResults, self.newResults, self.missingResults, self.correctResults]
        self.diag.info("Finding comparison matching stem " + pattern)
        comps = []
        for list in lists:
            for comparison in list:
                if fnmatch(comparison.stem, pattern):
                    comps.append(comparison)
        return comps

    def removeComparison(self, stem):
        comparison, newList = self.findComparison(stem)
        newList.remove(comparison)
        self.allResults.remove(comparison)

    def addAdditionalText(self, test):
        rerunCount = self.getRerunCount(test)
        if rerunCount and self.hasSucceeded():
            self.briefText = "after " + plugins.pluralise(rerunCount, "rerun")

    def computeFor(self, test, ignoreMissing=False, incompleteOnly=False):
        self.makeComparisons(test, ignoreMissing)
        variablesToStore = test.app.getTestRunVariables()
        isTestCase = test.classId() == "test-case"
        self.categorise(variablesToStore, isTestCase)
        self.addAdditionalText(test)
        if (not incompleteOnly or not test.state.isComplete()) and self.category != "not_started":
            test.changeState(self)

    def getRerunCount(self, test):
        number = 1
        while True:
            path = test.makeBackupFileName(number)
            if path and os.path.exists(path):
                number += 1
            else:
                return number - 1

    def fakeMissingFileText(self):
        return plugins.fakeMissingFileText()

    def findDefinitionFileStems(self, test, tmpFiles, ignoreMissing):
        if ignoreMissing:
            return test.expandedDefFileStems()

        stems = test.expandedDefFileStems("regenerate")
        for defFile in test.defFileStems("builtin") + test.defFileStems("default"):
            if defFile in tmpFiles:
                stems.append(defFile)
                # On the whole, warn the user if unexpected things get generated
                # Make an exception for recording as usecase-related files may be recorded that
                # won't necessarily be re-recorded
                if not test.app.isRecording():
                    plugins.printWarning("A file was generated with stem '" + defFile + "'.\n" +
                                         "This stem is intended to indicate a definition file and hence should not be generated.\n" +
                                         "Please change the configuration so that the file is called something else,\n" +
                                         "or adjust the config file setting 'definition_file_stems' accordingly.")
        return stems

    def makeStandardStemDict(self, test, tmpFiles, ignoreMissing):
        defFileStems = self.findDefinitionFileStems(test, tmpFiles, ignoreMissing)
        defFiles = test.getFilesFromStems(defFileStems, allVersions=False)
        resultFiles = test.listResultFiles(allVersions=False)
        resultFilesToCompare = [f for f in resultFiles + defFiles if not plugins.containsAutoGeneratedText(f)]
        return self.makeStemDict(resultFilesToCompare)

    def makeComparisons(self, test, ignoreMissing=False):
        # Might have approved some new ones or removed some old ones in the meantime...
        test.refreshFiles()
        tmpFiles = self.makeStemDict(test.listTmpFiles())
        stdFiles = self.makeStandardStemDict(test, tmpFiles, ignoreMissing)
        for tmpStem, tmpFile in list(tmpFiles.items()):
            self.notifyIfMainThread("ActionProgress")
            stdFile = stdFiles.get(tmpStem)
            self.diag.info("Comparing " + repr(stdFile) + "\nwith " + tmpFile)
            comparison = self.createFileComparison(test, tmpStem, stdFile, tmpFile)
            if comparison:
                self.addComparison(comparison)
        if not ignoreMissing:
            self.makeMissingComparisons(test, stdFiles, tmpFiles)

    def makeMissingComparisons(self, test, stdFiles, tmpFiles):
        for stdStem, stdFile in list(stdFiles.items()):
            self.notifyIfMainThread("ActionProgress")
            if stdStem not in tmpFiles:
                comparison = self.createFileComparison(test, stdStem, stdFile, None)
                if comparison:
                    self.addComparison(comparison)

    def addComparison(self, comparison):
        info = "Making comparison for " + comparison.stem + " "
        if comparison.isDefunct():
            # typically "missing file" that got "approved" and removed
            info += "(defunct)"
        else:
            self.allResults.append(comparison)
            if comparison.newResult():
                self.newResults.append(comparison)
                info += "(new)"
            elif comparison.missingResult():
                self.missingResults.append(comparison)
                info += "(missing)"
            elif comparison.hasDifferences():
                self.changedResults.append(comparison)
                info += "(diff)"
            else:
                self.correctResults.append(comparison)
                info += "(correct)"
        self.diag.info(info)

    def makeStemDict(self, files):
        stemDict = OrderedDict()
        for file in files:
            stem = os.path.basename(file).split(".")[0]
            stemDict[stem] = file
        return stemDict


class TestComparison(BaseTestComparison):
    def __init__(self, previousInfo, app, lifecycleChange="", copyFailedPrediction=True):
        BaseTestComparison.__init__(self, "failure", previousInfo, completed=1, lifecycleChange=lifecycleChange)
        self.failedPrediction = None
        if copyFailedPrediction and hasattr(previousInfo, "failedPrediction") and previousInfo.failedPrediction:
            self.setFailedPrediction(previousInfo.failedPrediction)
        # Cache these only so it gets output when we pickle, so we can re-interpret if needed... data may be moved
        self.appAbsPath = app.getDirectory()
        self.appWriteDir = app.writeDirectory

    def categoryRepr(self):
        if self.failedPrediction:
            longDescription = self.categoryDescriptions[self.category][1]
            return longDescription + " (" + self.failedPrediction.briefText + ")"
        else:
            return plugins.TestState.categoryRepr(self)

    def __getstate__(self):
        # don't pickle the diagnostics
        state = {}
        for var, value in list(self.__dict__.items()):
            if var != "diag":
                state[var] = value
        return state

    def __setstate__(self, state):
        self.__dict__ = state
        self.diag = logging.getLogger("TestComparison")

    def updateAfterLoad(self, app=None, updatePaths=False, newTmpPath=None):
        pathsToChange = []
        if updatePaths:
            if newTmpPath is None:
                newTmpPath = app.writeDirectory
            if self.appWriteDir != newTmpPath:
                self.diag.info("Updating tmppath " + self.appWriteDir + " to " + newTmpPath)
                pathsToChange.append((self.appWriteDir, newTmpPath))
                self.appWriteDir = newTmpPath

            newAbsPath = app.getDirectory()
            if newAbsPath != self.appAbsPath:
                self.diag.info("Updating abspath " + self.appAbsPath + " to " + newAbsPath)
                pathsToChange.append((self.appAbsPath, newAbsPath))
                self.appAbsPath = newAbsPath

        for comparison in self.allResults:
            comparison.updateAfterLoad(pathsToChange)

    def setFailedPrediction(self, prediction, usePreviousText=False):
        self.diag.info("Setting failed prediction to " + str(prediction))
        self.failedPrediction = prediction
        if usePreviousText:
            self.freeText = str(prediction) + "\n" + self.freeText
        else:
            self.freeText = str(prediction)
        self.briefText = prediction.briefText
        self.category = prediction.category

    def hasSucceeded(self):
        return self.category == "success"

    def getExitCode(self):
        if self.hasFailed():
            if self.failedPrediction is not None:
                return self.failedPrediction.getExitCode()
            fileComp = self.getMostSevereFileComparison()
            # performance diffs return 2
            return 1 if fileComp.getType() == "failure" else 2
        else:
            return 0

    def warnOnSave(self):
        return bool(self.failedPrediction)

    def getComparisonsForRecalculation(self):
        comparisons = []
        for comparison in self.allResults:
            if self.diag.isEnabledFor(logging.INFO):
                self.diag.info(comparison.stem + " dates " + comparison.modifiedDates())
            if comparison.needsRecalculation():
                self.diag.info("Recalculation needed for file " + comparison.stem)
                comparisons.append(comparison)
        self.diag.info("All file comparisons up to date")
        return comparisons

    def getMostSevereFileComparison(self):
        worstSeverity = None
        worstResult = None
        for result in self.getComparisons():
            severity = result.severity
            if not worstSeverity or severity < worstSeverity:
                worstSeverity = severity
                worstResult = result
        return worstResult

    def getTypeBreakdown(self):
        if self.hasSucceeded():
            return self.category, self.briefText
        if self.failedPrediction:
            return self.failedPrediction.getTypeBreakdown()

        worstResult = self.getMostSevereFileComparison()
        worstSeverity = worstResult.severity
        self.diag.info("Severity " + str(worstSeverity) + " for failing test")
        details = worstResult.getSummary()
        if len(self.getComparisons()) > 1:
            details += "(+)"
        if worstSeverity == 1:
            return "failure", details
        else:
            return "success", details

    def getComparisons(self):
        return self.changedResults + self.newResults + self.missingResults

    def _comparisonsString(self, comparisons):
        return ",".join([repr(x) for x in comparisons])
    # Sort according to failure_display_priority. Lower means show earlier,
    # files with the same prio should be not be shuffled.

    def getSortedComparisons(self):
        return sorted(self.changedResults, key=self.displayPriority) + \
            sorted(self.newResults, key=self.displayPriority) + \
            sorted(self.missingResults, key=self.displayPriority)

    def displayPriority(self, item):
        return item.displayPriority, item.stem

    def description(self):
        return repr(self) + self.getDifferenceSummary()

    def getDifferenceSummary(self):
        texts = []
        if len(self.newResults) > 0:
            texts.append("new results in " + self._comparisonsString(self.newResults))
        if len(self.missingResults) > 0:
            texts.append("missing results for " + self._comparisonsString(self.missingResults))
        if len(self.changedResults) > 0:
            texts.append("differences in " + self._comparisonsString(self.changedResults))
        if len(texts) > 0:
            return " " + ", ".join(texts)
        else:
            return ""

    def getPostText(self):
        if not self.hasResults():
            return " - NONE!"
        if len(self.getComparisons()) == 0:
            return " - SUCCESS! (on " + self.attemptedComparisonsOutput() + ")"
        return " (on " + self.attemptedComparisonsOutput() + ")"

    def attemptedComparisonsOutput(self):
        baseNames = []
        for comparison in self.allResults:
            if comparison.newResult():
                baseNames.append(os.path.basename(comparison.tmpFile))
            else:
                baseNames.append(os.path.basename(comparison.stdFile))
        return ",".join(baseNames)

    def getPerformanceStems(self, test):
        return ["performance"] + list(test.getConfigValue("performance_logfile_extractor").keys())

    def createFileComparison(self, test, stem, standardFile, tmpFile):
        if stem in self.getPerformanceStems(test):
            if tmpFile:
                return performance.PerformanceFileComparison(test, stem, standardFile, tmpFile)
            elif not test.app.executingOnPerformanceMachine(test, stem):
                # Don't care if performance is missing if we aren't on performance machines
                return None

        return FileComparison(test, stem, standardFile, tmpFile, testInProgress=0)

    def categorise(self, variablesToStore=[], successOnNoResult=True):
        if self.failedPrediction:
            # Keep the category we had before
            self.freeText += self.getFreeTextInfo(variablesToStore)
            return
        worstResult = self.getMostSevereFileComparison()
        if not worstResult:
            if successOnNoResult:
                self.category = "success"
                self.freeText += "".join(self.variablesToText(variablesToStore))
                if "approve" in self.lifecycleChange:
                    self.freeText = "(Approved at " + plugins.localtime("%H:%M") + ")"
            else:
                self.category = "not_started"
        else:
            self.category = worstResult.getType()
            self.freeText = self.getFreeTextInfo(variablesToStore)

    def getFreeTextInfo(self, variablesToStore=[]):
        texts = self.variablesToText(variablesToStore)
        texts += [fileComp.getFreeText() for fileComp in self.getSortedComparisons()]
        return "".join(texts)

    def variablesToText(self, variables):
        return [self.variableToText(var) + "\n" for var in variables if os.getenv(var)]

    def variableToText(self, var):
        texts = [t[0] + t[1:] for t in var.split("_")]
        return " ".join(texts) + ":" + os.getenv(var)

    def findParentStems(self, onlyStems):
        parents = set()
        for stem in onlyStems:
            if "/" in stem:
                parent = stem.split("/")[0]
                if parent not in onlyStems:
                    parents.add(parent)
        return parents

    def rebuildFromSplit(self, onlyStems, *args):
        parentStems = self.findParentStems(onlyStems)
        for stem in parentStems:
            parentComp, splitComps = self.findComparisonsForSplit(stem)
            parentComp.overwriteFromSplit(splitComps, *args)

    def findComparisonsForSplit(self, stem):
        parentComp, splitComps = None, []
        for comp in self.allResults:
            if comp.stem == stem:
                parentComp = comp
            elif parentComp and comp.getParent() == parentComp:
                splitComps.append(comp)
        return parentComp, splitComps

    def hasCaptureMockStems(self, onlyStems):
        return "externalmocks" in onlyStems or "traffic" in onlyStems

    def save(self, test, exact=True, versionString=None, overwriteSuccessFiles=False, onlyStems=[], backupVersions=[]):
        self.diag.info("Approving " + repr(test) + " stems " + repr(onlyStems) + ", exact=" + repr(exact))
        for comparison in self.filterComparisons(self.changedResults, onlyStems):
            self.updateStatus(test, str(comparison), versionString)
            comparison.overwrite(test, exact, versionString, backupVersions)
        for comparison in self.filterComparisons(self.newResults, onlyStems):
            self.updateStatus(test, str(comparison), versionString)
            comparison.saveNew(test, versionString)
        for comparison in self.filterComparisons(self.missingResults, onlyStems):
            self.updateStatus(test, str(comparison), versionString)
            comparison.saveMissing(versionString, self.fakeMissingFileText(), backupVersions)
        # Save any external file edits we may have made. Only do this on partial saves for CaptureMock related files
        if len(onlyStems) == 0 or self.hasCaptureMockStems(onlyStems):
            self.saveFileEdits(test, versionString)
        elif any(("/" in stem for stem in onlyStems)):  # We've explicitly selected split files
            self.rebuildFromSplit(onlyStems, test, exact, versionString, backupVersions)
        if overwriteSuccessFiles:
            for comparison in self.filterComparisons(self.correctResults, onlyStems):
                self.updateStatus(test, str(comparison), versionString)
                comparison.overwrite(test, exact, versionString, backupVersions)

    def saveFileEdits(self, test, versionString):
        tmpFileEditDir = os.path.join(self.appWriteDir, test.getWriteDirRelPath(), "file_edits")
        fileEditDir = test.dircache.pathName("file_edits")
        if versionString:
            fileEditDir += "." + versionString
        if os.path.isdir(fileEditDir) and test.app.isRecording():
            # Recording that we've approved the CaptureMock part of. Don't let files from previous recordings get left behind!
            shutil.rmtree(fileEditDir)
        if os.path.isdir(tmpFileEditDir):
            for root, _, files in os.walk(tmpFileEditDir):
                for file in sorted(files):
                    fullPath = os.path.join(root, file)
                    savePath = fullPath.replace(tmpFileEditDir, fileEditDir)
                    self.updateStatus(test, "edited file " + file, versionString)
                    plugins.ensureDirExistsForFile(savePath)
                    shutil.copyfile(fullPath, savePath)

    def recalculateStdFiles(self, test):
        self.diag.info("Recalculating standard files for " + repr(test))
        test.refreshFiles()
        resultFiles, defFiles = test.listApprovedFiles(allVersions=False)
        stdFiles = self.makeStemDict(resultFiles + defFiles)
        for fileComp in self.allResults:
            stdFile = stdFiles.get(fileComp.stem)
            self.diag.info("Recomputing against " + repr(stdFile))
            fileComp.setStandardFile(stdFile)

    def recalculateComparisons(self, test):
        self.removeSplitComparisons(test)
        for fileComp in self.allResults:
            fileComp.recompute(test)

    def splitResultFiles(self, *args):
        return sum((fileComp.split(*args) for fileComp in self.allResults), [])

    def stemMatches(self, stem, onlyStems):
        return stem in onlyStems or ("/" in stem and stem.split("/")[0] in onlyStems)

    def filterComparisons(self, resultList, onlyStems):
        if len(onlyStems) == 0:
            return resultList
        else:
            return [comp for comp in resultList if self.stemMatches(comp.stem, onlyStems)]

    def updateStatus(self, test, compStr, versionString):
        testRepr = "Approving " + repr(test) + " : "
        if versionString is not None:
            versionRepr = ", version " + repr(versionString)
        else:
            versionRepr = ", existing version"
        self.notify("Status", testRepr + compStr + versionRepr)
        self.notifyIfMainThread("ActionProgress")

    def makeNewState(self, test, lifeCycleDest):
        crashed = hasattr(
            self, "failedPrediction") and self.failedPrediction is not None and self.failedPrediction.category == "crash"
        newState = self.__class__(self, test.app, "be " + lifeCycleDest, copyFailedPrediction=crashed)
        for comparison in self.allResults:
            newState.addComparison(comparison)
        variablesToStore = test.app.getTestRunVariables()
        newState.categorise(variablesToStore)
        return knownbugs.CheckForBugs().checkTest(test, newState)[0] or newState

    def removeSplitComparisons(self, test):
        toRemove = []
        for fileComp in self.allResults:
            if isinstance(fileComp, SplitFileComparison):
                toRemove.append(fileComp)
                fileComp.unsplit(test)
        for comp in toRemove:
            self.allResults.remove(comp)


# for back-compatibility, preserve old names
performance.PerformanceTestComparison = TestComparison


class ProgressTestComparison(BaseTestComparison):
    def __init__(self, previousInfo):
        BaseTestComparison.__init__(self, previousInfo.category, previousInfo,
                                    completed=0, lifecycleChange="be recalculated")
        if isinstance(previousInfo, ProgressTestComparison):
            self.runningState = previousInfo.runningState
        else:
            self.runningState = previousInfo

    def createFileComparison(self, test, stem, standardFile, tmpFile):
        return FileComparison(test, stem, standardFile, tmpFile, testInProgress=1)

    def categorise(self, *args, **kwargs):
        self.briefText = self.runningState.briefText
        self.freeText = self.runningState.freeText + self.progressText()

    def progressText(self):
        perc = self.calculatePercentage()
        if perc is not None:
            return "\nReckoned to be " + str(int(perc)) \
                + "% complete by comparing total file sizes at " \
                + plugins.localtime() + "."
        else:
            return ""

    def getSize(self, fileName):
        if fileName and os.path.isfile(fileName):
            return os.path.getsize(fileName)
        else:
            return 0

    def calculatePercentage(self):
        stdSize, tmpSize = 0, 0
        for comparison in self.changedResults + self.correctResults:
            stdSize += self.getSize(comparison.stdFile)
            tmpSize += self.getSize(comparison.tmpFile)

        if stdSize > 0:
            return (tmpSize * 100) / stdSize

    def makeModifiedState(self, *args):
        newRunningState = self.runningState.makeModifiedState(*args)
        if newRunningState:
            newState = self.__class__(newRunningState)
            newState.lifecycleChange = newRunningState.lifecycleChange
            newState.changedResults = self.changedResults
            newState.correctResults = self.correctResults
            newState.allResults = self.allResults
            newState.newResults = self.newResults
            newState.missingResults = self.missingResults
            newState.categorise()
            return newState


class MakeComparisons(plugins.Action):
    def __init__(self, testComparisonClass=None, progressComparisonClass=None, ignoreMissing=False, enableColor=False, compareSuites=False):
        self.testComparisonClass = self.getClass(testComparisonClass, TestComparison)
        self.progressComparisonClass = self.getClass(progressComparisonClass, ProgressTestComparison)
        self.ignoreMissing = ignoreMissing
        self.enableColor = enableColor
        self.compareSuites = compareSuites

    def getClass(self, given, defaultClass):
        if given:
            return given
        else:
            return defaultClass

    def __repr__(self):
        return "Comparing differences for"

    def __call__(self, test):
        newState = self.testComparisonClass(test.state, test.app)
        newState.computeFor(test, ignoreMissing=self.ignoreMissing)
        from . import colorer
        if self.enableColor and not test.state.hasFailed():
            colorer.enableOutputColor(colorer.GREEN)
            self.describe(test, newState.getPostText())
            colorer.disableOutputColor()
        else:
            self.describe(test, newState.getPostText())

    def recomputeProgress(self, test, state, observers):
        newState = self.progressComparisonClass(state)
        newState.setObservers(observers)
        if not test.state.isComplete():
            newState.computeFor(test, ignoreMissing=True, incompleteOnly=True)

    def setUpSuite(self, suite):
        if self.compareSuites:
            self(suite)
        else:
            self.describe(suite)


class PrintObsoleteVersions(plugins.Action):
    scriptDoc = "Lists all files with version IDs that are equivalent to a non-versioned file"

    def __init__(self):
        self.filesToRemove = []

    def __repr__(self):
        return "Removing obsolete versions for"

    def __del__(self):
        if len(self.filesToRemove):
            print("Summary : Remove these files!")
            print("=============================")
            for file in self.filesToRemove:
                print(file)

    def __call__(self, test):
        self.describe(test)
        compFiles = {}
        resultFiles = test.listApprovedFiles(allVersions=True)[0]
        for file in resultFiles:
            stem = file.split(".")[0]
            compFile = self.filterFile(test, file)
            if stem not in compFiles:
                compFiles[stem] = []
            compFiles[stem].append((file, compFile))
        for compFilesMatchingStem in list(compFiles.values()):
            for index1 in range(len(compFilesMatchingStem)):
                for index2 in range(index1 + 1, len(compFilesMatchingStem)):
                    self.compareFiles(test, compFilesMatchingStem[index1], compFilesMatchingStem[index2])
                os.remove(compFilesMatchingStem[index1][1])

    def cmpFile(self, file):
        basename = os.path.basename(file)
        return mktemp(basename + "cmp")

    def filterFile(self, test, file):
        newFile = self.cmpFile(file)
        stem = os.path.basename(file).split(".")[0]
        from .rundependent import FilterAction
        action = FilterAction()
        action.performAllFilterings(test, stem, file, newFile)
        return newFile

    def compareFiles(self, test, filePair1, filePair2):
        origFile1, cmpFile1 = filePair1
        origFile2, cmpFile2 = filePair2
        if origFile1 in self.filesToRemove or origFile2 in self.filesToRemove:
            return
        if filecmp.cmp(cmpFile1, cmpFile2, 0):
            local1 = os.path.basename(origFile1)
            local2 = os.path.basename(origFile2)
            vlist1 = set(local1.split(".")[2:])
            vlist2 = set(local2.split(".")[2:])
            if vlist1.issuperset(vlist2):
                self.checkObsolete(test, origFile1, local1, origFile2)
            elif vlist2.issuperset(vlist1):
                self.checkObsolete(test, origFile2, local2, origFile1)
            else:
                print(test.getIndent() + local1, "equivalent to", local2)

    def checkObsolete(self, test, obsoleteFile, obsoleteLocal, causeFile):
        fallbackFile = self.getFallbackFile(test, obsoleteFile)
        if plugins.samefile(fallbackFile, causeFile):
            print(test.getIndent() + obsoleteLocal, "obsolete due to", os.path.basename(causeFile))
            self.filesToRemove.append(obsoleteFile)
        else:
            print(test.getIndent() + obsoleteLocal, "is a version-priority-fixing copy of", os.path.basename(causeFile))

    def getFallbackFile(self, test, fileName):
        parts = os.path.basename(fileName).split(".", 2)
        names = test.getAllFileNames(parts[0], parts[-1])
        if len(names) > 1:
            return names[-2]

    def setUpSuite(self, suite):
        self.describe(suite)
