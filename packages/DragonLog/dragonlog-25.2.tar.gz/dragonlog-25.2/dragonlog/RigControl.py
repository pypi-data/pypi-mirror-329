import os
import socket
import logging
import platform
import subprocess
import sys

from PyQt6 import QtCore

from .Logger import Logger


class NoExecutableFoundException(Exception):
    pass

class RigctldNotConfiguredException(Exception):
    pass

class CATSettingsMissingException(Exception):
    pass


class RigControl(QtCore.QObject):
    frequencyChanged = QtCore.pyqtSignal(float)
    bandChanged = QtCore.pyqtSignal(str)
    modeChanged = QtCore.pyqtSignal(str)
    submodeChanged = QtCore.pyqtSignal(str)
    powerChanged = QtCore.pyqtSignal(int)
    statusChanged = QtCore.pyqtSignal(bool)

    def __init__(self, parent, settings: QtCore.QSettings, logger: Logger,
                 bands: dict, modes: dict):
        super().__init__(parent)

        # From QSOForm
        self.log = logging.getLogger('RigControl')
        self.log.addHandler(logger)
        self.log.setLevel(logger.loglevel)
        self.logger = logger
        self.log.debug('Initialising...')

        self.settings = settings

        self.bands = bands
        self.modes = modes

        self.rig_modes = {'USB': ('SSB', 'USB'),
                          'LSB': ('SSB', 'LSB'),
                          'CW': ('CW', ''),
                          'CWR': ('CW', ''),
                          'RTTY': ('RTTY', ''),
                          'RTTYR': ('RTTY', ''),
                          'AM': ('AM', ''),
                          'FM': ('FM', ''),
                          'FMN': ('FM', ''),
                          'WFM': ('FM', ''),
                          'PKTUSB': ('SSB', 'USB'),
                          'PKTLSB': ('SSB', 'LSB'),
                          }
        self.__last_mode__ = ''
        self.__last_band__ = ''
        self.__last_freq__ = 0.0
        self.__last_pwr_lvl__ = ''
        self.__last_pwr__ = 0

        self.__rig_ids__ = None
        self.__rigs__ = None
        self.__rigctld_path__ = None
        self.__rigctld__ = None
        self.__rig_caps__ = []

        self.__rigctl_startupinfo__ = None
        if platform.system() == 'Windows':
            self.__rigctl_startupinfo__ = subprocess.STARTUPINFO()
            self.__rigctl_startupinfo__.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            if self.settings.value('cat/rigctldPath', None):
                if self.__is_exe__(self.settings.value('cat/rigctldPath')):
                    self.__init_hamlib__(self.settings.value('cat/rigctldPath'))
                else:
                    raise NoExecutableFoundException(self.settings.value('cat/rigctldPath', ''))
        else:
            self.__init_hamlib__('rigctld')

        self.__refreshTimer__ = QtCore.QTimer(self)
        self.__refreshTimer__.timeout.connect(self.__refreshRigData__)
        self.__checkHamlibTimer__ = QtCore.QTimer(self)
        self.__checkHamlibTimer__.timeout.connect(self.__checkRigctld__)

    @staticmethod
    def __is_exe__(path) -> bool:
        return os.path.isfile(path) and os.access(path, os.X_OK)

    def __checkRigctld__(self):
        if not self.isRigctldActive():
            self.log.error('rigctld died unexpectedly')
            self.__rig_caps__ = []
            self.__checkHamlibTimer__.stop()
            self.statusChanged.emit(False)

    def isRigctldActive(self) -> bool:
        return self.__rigctld__ and not self.__rigctld__.poll()

    def __init_hamlib__(self, rigctld_path):
        if rigctld_path:
            try:
                res = subprocess.run([rigctld_path, '-l'], capture_output=True)
                stdout = str(res.stdout, sys.getdefaultencoding()).replace('\r', '')
                if res.returncode != 0 or not stdout:
                    self.log.error(f'Error executing rigctld: {res.returncode}')
                    # self.checkHamlibLabel.setText(self.tr('Error executing rigctld'))
                    self.settings.setValue('cat/rigctldPath', '')
                    # self.hamlibPathLineEdit.setText('')
                    return
                self.log.debug('Executed rigctld to list rigs')
            except FileNotFoundError:
                self.log.info('rigctld is not available')
                # self.checkHamlibLabel.setText(self.tr('rigctld is not available'))
                self.settings.setValue('cat/rigctldPath', '')
                # self.hamlibPathLineEdit.setText('')
                return

            first = True
            rig_pos = 0
            mfr_pos = 0
            model_pos = 0
            end_pos = 0
            self.__rigs__ = {}
            self.__rig_ids__ = {}
            for rig in stdout.split('\n'):
                if first:
                    first = False
                    rig_pos = rig.index('Rig #')
                    mfr_pos = rig.index('Mfg')
                    model_pos = rig.index('Model')
                    end_pos = rig.index('Version')
                    continue
                elif not rig.strip():  # Empty line
                    continue

                rig_id = rig[rig_pos:mfr_pos - 1].strip()
                mfr_name = rig[mfr_pos:model_pos - 1].strip()
                model_name = rig[model_pos:end_pos - 1].strip()

                self.__rig_ids__[f'{mfr_name}/{model_name}'] = rig_id
                if mfr_name in self.__rigs__:
                    self.__rigs__[mfr_name].append(model_name)
                else:
                    self.__rigs__[mfr_name] = [model_name]

            #self.manufacturerComboBox.clear()
            #self.manufacturerComboBox.insertItems(0, sorted(self.__rigs__.keys()))
            # if self.settings.value('cat/rigMfr', None):
            #     self.manufacturerComboBox.setCurrentText(self.settings.value('cat/rigMfr'))
            # else:
            #     self.manufacturerComboBox.setCurrentIndex(0)

            self.settings.setValue('cat/rigctldPath', rigctld_path)
            # self.hamlibPathLineEdit.setText(rigctld_path)
            # self.checkHamlibLabel.setText('')
            self.__rigctld_path__ = rigctld_path

    # From Settings
    def __collectRigCaps__(self, rig_id):
        res = subprocess.run([self.__rigctld_path__, f'--model={rig_id}', '-u'],
                             capture_output=True,
                             startupinfo=self.__rigctl_startupinfo__)
        stdout = str(res.stdout, sys.getdefaultencoding()).replace('\r', '')
        self.__rig_caps__ = []
        for ln in stdout.split('\n'):
            if ln.startswith('Can '):
                cap, able = ln.split(':')
                if able.strip() == 'Y':
                    self.__rig_caps__.append(cap[4:].lower())
    
    @property
    def capabilities(self) -> list:
        return self.__rig_caps__

    # noinspection PyUnresolvedReferences
    def ctrlRigctld(self, start):
        if start:
            if not self.__rigctld_path__:
                self.log.warning('rigctld is not available')
                raise RigctldNotConfiguredException()

            if not self.__rigctld__:
                rig_mfr = self.settings.value('cat/rigMfr', '')
                rig_model = self.settings.value('cat/rigModel', '')
                rig_if = self.settings.value('cat/interface', '')
                rig_speed = self.settings.value('cat/baud', '')
                if not rig_mfr or not rig_model or not rig_if or not rig_speed:
                    raise CATSettingsMissingException()

                rig_id = self.__rig_ids__[f'{rig_mfr}/{rig_model}']

                self.__collectRigCaps__(rig_id)

                self.__rigctld__ = subprocess.Popen([self.__rigctld_path__,
                                                 f'--model={rig_id}',
                                                 f'--rig-file={rig_if}',
                                                 f'--serial-speed={rig_speed}',
                                                 '--listen-addr=127.0.0.1'],
                                                    startupinfo=self.__rigctl_startupinfo__)

                if self.__rigctld__.poll():
                    self.statusChanged.emit(False)
                else:
                    self.log.info(f'rigctld is running with pid #{self.__rigctld__.pid} and arguments {self.__rigctld__.args}')
                    self.__checkHamlibTimer__.start(1000)
                    self.statusChanged.emit(True)
        else:
            self.__checkHamlibTimer__.stop()
            if self.isRigctldActive():
                os.kill(self.__rigctld__.pid, 9)
                self.log.info('Killed rigctld')
            self.__rigctld__ = None
            self.__rig_caps__ = []
            self.statusChanged.emit(False)

    # From QSOForm
    def rigctldChanged(self, state):
        self.__last_mode__ = ''
        self.__last_band__ = ''
        self.__last_freq__ = 0.0
        self.__last_pwr_lvl__ = ''
        self.__last_pwr__ = 0

    @property
    def mode(self) -> str:
        return self.__last_mode__

    @property
    def band(self) -> str:
        return self.__last_band__

    @property
    def frequency(self) -> float:
        return self.__last_freq__

    @property
    def power(self) -> int:
        return self.__last_pwr__

    def startTimers(self, start: bool):
        if start:
            self.__refreshTimer__.start(500)
        else:
            self.__refreshTimer__.stop()

    def setRigFreq(self, freq):
        self.sendToRig(f'set_freq {int(freq * 1000)}')

    def sendToRig(self, cmd: str):
        if not self.isRigctldActive():
            return

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('127.0.0.1', 4532))
                s.settimeout(1)
                try:
                    s.sendall(f'\\{cmd}\n'.encode())
                    res = s.recv(1024).decode('utf-8').strip()
                    if not res.startswith('RPRT 0'):
                        #self.hamlib_error.setText(self.tr('Error') + ':' + res.split()[1])
                        self.log.error(f'rigctld error "{cmd}": {res.split()[1]}')
                    else:
                        self.log.debug(f'rigctld "{cmd}" successful')
                except socket.timeout:
                    # self.hamlib_error.setText(self.tr('rigctld timeout'))
                    self.log.error('rigctld error: timeout')
        except ConnectionRefusedError:
            self.log.error('Could not connect to rigctld')

    # noinspection PyBroadException
    def __refreshRigData__(self):
        if self.isRigctldActive():
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect(('127.0.0.1', 4532))
                    s.settimeout(1)
                    try:
                        # Get frequency
                        s.sendall(b'\\get_freq\n')
                        freq_s = s.recv(1024).decode('utf-8').strip()
                        if freq_s.startswith('RPRT'):
                            # self.hamlib_error.setText(self.tr('Error') + ':' + freq_s.split()[1])
                            self.log.error(f'rigctld error get_freq: {freq_s.split()[1]}')
                            return

                        try:
                            freq = float(freq_s) / 1000
                            if freq != self.__last_freq__:
                                for b in self.bands:
                                    if freq < self.bands[b][1]:
                                        if freq > self.bands[b][0]:
                                            if b != self.__last_band__:
                                                self.bandChanged.emit(b)
                                                self.log.info(f'CAT changed band to {b}')
                                                self.__last_band__ = b
                                                self.__last_mode__ = ''
                                        break
                                self.frequencyChanged.emit(freq)
                                self.__last_freq__ = freq
                        except Exception:
                            pass

                        # Get mode
                        s.sendall(b'\\get_mode\n')
                        mode_s = s.recv(1024).decode('utf-8').strip()
                        if mode_s.startswith('RPRT'):
                            # self.hamlib_error.setText(self.tr('Error') + ':' + mode_s.split()[1])
                            self.log.error(f'rigctld error get_mode: {mode_s.split()[1]}')
                            return

                        try:
                            mode, passband = [v.strip() for v in mode_s.split('\n')]
                            if mode in self.rig_modes and mode != self.__last_mode__:
                                self.modeChanged.emit(self.rig_modes[mode][0])
                                self.log.info(f'CAT changed mode to {self.rig_modes[mode][0]}')
                                if self.rig_modes[mode][1]:
                                    self.submodeChanged.emit(self.rig_modes[mode][1])
                                self.__last_mode__ = mode
                        except Exception:
                            pass

                        # Get power
                        if 'get level' in self.__rig_caps__ and 'get power2mw' in self.__rig_caps__:
                            # Get power level
                            s.sendall(b'\\get_level RFPOWER\n')
                            pwrlvl_s = s.recv(1024).decode('utf-8').strip()
                            if pwrlvl_s.startswith('RPRT'):
                                # self.hamlib_error.setText(self.tr('Error') + ':' + pwrlvl_s.split()[1])
                                self.log.error(f'rigctld error get_level: {pwrlvl_s.split()[1]}')
                                return

                            if pwrlvl_s != self.__last_pwr_lvl__:
                                self.__last_pwr_lvl__ = pwrlvl_s
                                # Convert level to W
                                s.sendall(f'\\power2mW {pwrlvl_s} {freq_s} {mode}\n'.encode())
                                pwr_s = s.recv(1024).decode('utf-8').strip()
                                if pwr_s.startswith('RPRT'):
                                    # self.hamlib_error.setText(self.tr('Error') + ':' + pwr_s.split()[1])
                                    self.log.error(f'rigctld error power2mW: {pwr_s.split()[1]}')
                                    return

                                try:
                                    self.__last_pwr__ = int(int(pwr_s) / 1000 + .9)
                                    self.powerChanged.emit(self.__last_pwr__)
                                except Exception:
                                    pass
                    except socket.timeout:
                        # self.hamlib_error.setText(self.tr('rigctld timeout'))
                        self.log.error('rigctld error: timeout')
            except ConnectionRefusedError:
                self.log.error('Could not connect to rigctld')
                self.__refreshTimer__.stop()
