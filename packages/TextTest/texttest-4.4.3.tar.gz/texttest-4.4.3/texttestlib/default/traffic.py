
import os
import shutil
import subprocess
import sys
from texttestlib import plugins
from locale import getpreferredencoding

class SetUpCaptureMockHandlers(plugins.Action):
    def __init__(self, recordSetting):
        self.recordSetting = recordSetting
        libexecDir = plugins.installationDir("libexec")
        self.siteCustomizeFile = os.path.join(libexecDir, "sitecustomize.pyx")

    def __call__(self, test):
        pythonCustomizeFiles = test.getAllPathNames("testcustomize.py")
        pythonCoverage = test.hasEnvironment("COVERAGE_PROCESS_START")
        captureMock = test.app.usesCaptureMock() and self.recordSetting != 3
        if captureMock or pythonCoverage or pythonCustomizeFiles:
            rcFiles = test.getAllPathNames("capturemockrc")
            if rcFiles or pythonCoverage or pythonCustomizeFiles:
                self.setUpIntercepts(test, rcFiles, pythonCoverage, pythonCustomizeFiles)
        elif self.recordSetting == 3:
            self.disableCaptureMockComparison(test.app)

    def disableCaptureMockComparison(self, app):
        for name in ["traffic", "externalmocks", "pythonmocks"]:
            app.removeConfigEntry("regenerate", name, "definition_file_stems")
            app.addConfigEntry("builtin", name, "definition_file_stems")

    def setUpIntercepts(self, test, rcFiles, pythonCoverage, pythonCustomizeFiles):
        interceptDir = test.makeTmpFileName("traffic_intercepts", forComparison=0)
        captureMockActive = False
        if rcFiles:
            captureMockActive = self.setUpCaptureMock(test, interceptDir, rcFiles)

        if pythonCustomizeFiles:
            self.intercept(pythonCustomizeFiles[-1], interceptDir)  # most specific

        useSiteCustomize = captureMockActive or pythonCoverage or pythonCustomizeFiles
        if useSiteCustomize:
            self.intercept(self.siteCustomizeFile, interceptDir)
            for var in ["PYTHONPATH", "JYTHONPATH"]:
                test.setEnvironment(var, interceptDir + os.pathsep + test.getEnvironment(var, ""))

    def setUpCaptureMock(self, test, interceptDir, rcFiles):
        extReplayFile = test.getFileName("traffic")
        clientServer = test.app.clientServerEnabled(rcFiles)
        if extReplayFile:
            # "Legacy" setup to avoid the need to rename hundreds of files
            extRecordFile = test.makeTmpFileName("traffic")
            pyReplayFile = extReplayFile
            pyRecordFile = extRecordFile
        elif clientServer:
            clientServerMockName = test.getConfigValue("capturemock_clientserver_mock_name")
            extReplayFile = test.getFileName(clientServerMockName)
            extRecordFile = test.makeTmpFileName(clientServerMockName)
        else:
            extReplayFile = test.getFileName("externalmocks")
            extRecordFile = test.makeTmpFileName("externalmocks")
            pyReplayFile = test.getFileName("pythonmocks")
            pyRecordFile = test.makeTmpFileName("pythonmocks")
        recordEditDir = test.makeTmpFileName("file_edits", forComparison=0)
        replayEditDir = test.getFileName("file_edits") if extReplayFile else None
        if clientServer:
            # translate as mixed mode (2) isn't used in this context
            cpMockMode = "3" if self.recordSetting == 2 else str(self.recordSetting)
            # Let a "test rig" script control what to do with capturemock, easier to have control there
            test.setEnvironment("TEXTTEST_CAPTUREMOCK_MODE", cpMockMode) # For use in your test rig. See CaptureMock docs
            test.setEnvironment("TEXTTEST_CAPTUREMOCK_RCFILES", ",".join(rcFiles)) # For use in your test rig. See CaptureMock docs
            if extReplayFile:
                test.setEnvironment("TEXTTEST_CAPTUREMOCK_REPLAY", extReplayFile) # For use in your test rig. See CaptureMock docs
            test.setEnvironment("TEXTTEST_CAPTUREMOCK_RECORD", extRecordFile) # For use in your test rig. See CaptureMock docs
            if replayEditDir:
                test.setEnvironment("TEXTTEST_CAPTUREMOCK_REPLAY_EDIT_DIR", replayEditDir) # For use in your test rig. See CaptureMock docs
            test.setEnvironment("TEXTTEST_CAPTUREMOCK_RECORD_EDIT_DIR", recordEditDir) # For use in your test rig. See CaptureMock docs
        else:
            sutDirectory = test.getDirectory(temporary=1, local=1)
            capturemock_path = test.getConfigValue("capturemock_path")
            if capturemock_path:
                sys.path.insert(0, capturemock_path)
            try:
                from capturemock import setUpServer, setUpPython
                externalActive = setUpServer(self.recordSetting, extRecordFile, extReplayFile,
                                             recordEditDir=recordEditDir, replayEditDir=replayEditDir,
                                             rcFiles=rcFiles, interceptDir=interceptDir,
                                             sutDirectory=sutDirectory, environment=test.environment)
                pythonActive = setUpPython(self.recordSetting, pyRecordFile, pyReplayFile, rcFiles=rcFiles,
                                           environment=test.environment)
                return externalActive or pythonActive
            except ImportError as e:
                raise plugins.TextTestError(
                    "Test requires CaptureMock to be installed, but the capturemock module could not be found\nError was: " + str(e) + "\nSearched in " + repr(sys.path))

    def intercept(self, moduleFile, interceptDir):
        interceptName = os.path.join(interceptDir, os.path.basename(moduleFile).replace(".pyx", ".py"))
        plugins.ensureDirExistsForFile(interceptName)
        self.copyOrLink(moduleFile, interceptName)

    def copyOrLink(self, src, dst):
        if os.name == "posix":
            os.symlink(src, dst)
        else:
            shutil.copy(src, dst)


class TerminateCaptureMockHandlers(plugins.Action):
    def __call__(self, test):
        try:
            from capturemock import terminate
            terminate()
        except ImportError:
            pass


class ModifyTraffic(plugins.ScriptWithArgs):
    scriptDoc = "Apply a script to all the client server data"

    def __init__(self, args):
        argDict = self.parseArguments(args, ["script", "types", "file"])
        self.script = argDict.get("script")
        self.fileName = argDict.get("file", "traffic")
        self.trafficTypes = plugins.commasplit(argDict.get("types", "CLI,SRV"))

    def __repr__(self):
        return "Updating CaptureMock files in"

    def __call__(self, test):
        fileName = test.getFileName(self.fileName)
        if not fileName:
            return

        self.describe(test)
        try:
            newTexts = [self.getModified(t, test.getDirectory()) for t in self.readIntoList(fileName)]
        except plugins.TextTestError as e:
            print(str(e).strip())
            return

        newFileName = fileName + "tmpedit"
        newFile = open(newFileName, "w")
        for text in newTexts:
            self.write(newFile, text)
        newFile.close()
        shutil.move(newFileName, fileName)

    def readIntoList(self, fileName):
        # Copied from CaptureMock ReplayInfo, easier than trying to reuse it
        trafficList = []
        currTraffic = ""
        for line in open(fileName):
            if line.startswith("<-") or line.startswith("->"):
                if currTraffic:
                    trafficList.append(currTraffic)
                currTraffic = ""
            currTraffic += line
        if currTraffic:
            trafficList.append(currTraffic)
        return trafficList

    def getModified(self, fullLine, dir):
        trafficType = fullLine[2:5]
        args = [self.script, fullLine[6:]]
        if os.name == "nt":
            interpreter = plugins.getInterpreter(self.script)
            if interpreter:
                args = plugins.splitcmd(interpreter) + args
        if trafficType in self.trafficTypes:
            proc = subprocess.Popen(args, cwd=dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = proc.communicate()
            if len(stderr) > 0:
                raise plugins.TextTestError("Couldn't modify traffic :\n " + str(stderr, getpreferredencoding()))
            else:
                return fullLine[:6] + str(stdout, getpreferredencoding())
        else:
            return fullLine

    def write(self, newFile, desc):
        if not desc.endswith("\n"):
            desc += "\n"
        newFile.write(desc)

    def setUpSuite(self, suite):
        self.describe(suite)


class ConvertToCaptureMock(plugins.Action):
    def convert(self, confObj, newFile):
        from configparser import ConfigParser
        from collections import OrderedDict
        parser = ConfigParser(dict_type=OrderedDict)
        multiThreads = confObj.getConfigValue("collect_traffic_use_threads") == "true"
        if not multiThreads:
            parser.add_section("general")
            parser.set("general", "server_multithreaded", str(multiThreads))
        cmdTraffic = confObj.getCompositeConfigValue("collect_traffic", "asynchronous")
        if cmdTraffic:
            parser.add_section("command line")
            parser.set("command line", "intercepts", ",".join(cmdTraffic))
            asynchronous = confObj.getConfigValue("collect_traffic").get("asynchronous", [])
            for cmd in cmdTraffic:
                env = confObj.getConfigValue("collect_traffic_environment").get(cmd)
                cmdAsync = cmd in asynchronous
                if env or cmdAsync:
                    parser.add_section(cmd)
                    if env:
                        parser.set(cmd, "environment", ",".join(env))
                    if cmdAsync:
                        parser.set(cmd, "asynchronous", str(cmdAsync))

        envVars = confObj.getConfigValue("collect_traffic_environment").get("default")
        if envVars:
            parser.set("command line", "environment", ",".join(envVars))

        pyTraffic = confObj.getConfigValue("collect_traffic_python")
        if pyTraffic:
            parser.add_section("python")
            ignore_callers = confObj.getConfigValue("collect_traffic_python_ignore_callers")
            parser.set("python", "intercepts", ",".join(pyTraffic))
            if ignore_callers:
                parser.set("python", "ignore_callers", ",".join(ignore_callers))

        if len(parser.sections()) > 0:  # don't write empty files
            print("Wrote file at", newFile)
            parser.write(open(newFile, "w"))

    def setUpApplication(self, app):
        newFile = os.path.join(app.getDirectory(), "capturemockrc." + app.name + app.versionSuffix())
        print("Converting", repr(app))
        self.convert(app, newFile)

    def __call__(self, test):
        self.checkTest(test)

    def setUpSuite(self, suite):
        self.checkTest(suite)

    def checkTest(self, test):
        configFile = test.getFileName("config")
        if configFile and test.parent:
            print("Converting", repr(test))
            newFile = os.path.join(test.getDirectory(), "capturemockrc." + test.app.name + test.app.versionSuffix())
            self.convert(test, newFile)
