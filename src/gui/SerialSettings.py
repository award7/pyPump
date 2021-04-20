from random import randrange
import sys
from serial import Serial
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QHBoxLayout,
                             QVBoxLayout,
                             QFormLayout,
                             QPushButton,
                             QMainWindow,
                             QWidget,
                             QLineEdit,
                             QComboBox,
                             QSpinBox)


class Window(QMainWindow):

    def __init__(self, parent: QMainWindow = None) -> None:
        super().__init__()
        if parent is None:
            # TODO: open error dialog box stating no active serial connection is present
            pass
        self.parent = parent

        self.ser = Serial()
        self._bool_opts = ["True", "False"]
        self.initUI()

    # ui creation methods
    def initUI(self):
        self.setWindowTitle("Connection Settings")

        # create widgets
        self.createPortEdit()
        self.createStatusEdit()
        self.createBaudrateCb()
        self.createByteCb()
        self.createParityCb()
        self.createStopbitsCb()
        self.createReadTimeoutSb()
        self.createWriteTimeoutSb()
        self.createByteTimeoutSb()
        self.createFlowControlCb()
        self.createRtsCb()
        self.createDtrCb()
        self.createApplyBtn()
        self.createCancelBtn()

        # create form
        form = self.createForm()

        # make button group
        horz_layout = QHBoxLayout()
        horz_layout.addWidget(self.ApplyBtn)
        horz_layout.addWidget(self.CancelBtn)

        # bring together form and btn group
        main_layout = QVBoxLayout()
        main_layout.addLayout(form)
        main_layout.addLayout(horz_layout)

        wdg = QWidget()
        wdg.setLayout(main_layout)
        self.setCentralWidget(wdg)

    def createForm(self) -> QFormLayout:
        # add rows of settings
        form = QFormLayout()
        form.addRow("Port", self.PortEdit)
        form.addRow("Status", self.StatusEdit)
        form.addRow("Baud Rate", self.BaudRateCb)
        form.addRow("Byte Size", self.BytesSizeCb)
        form.addRow("Stop Bits", self.StopBitsCb)
        form.addRow("Read Timeout", self.ReadTimeoutSb)
        form.addRow("Write Timeout", self.WriteTimeoutSb)
        form.addRow("Inter-Byte Timeout", self.ByteTimeoutSb)
        form.addRow("Software Flow Control", self.SoftwareFlowCb)
        form.addRow("Flow Control: RTS/CTS", self.RtsctsCb)
        form.addRow("Flow Control: DSR/DTR", self.DsrdtrCb)

        return form

    def createPortEdit(self) -> None:
        self.PortEdit = QLineEdit()
        self.PortEdit.setText(self.ser.port)
        self.PortEdit.setDisabled(True)

    def createStatusEdit(self) -> None:
        self.StatusEdit = QLineEdit()
        tf = self.ser.is_open
        if tf:
            status = "Opened"
        else:
            status = "Closed"
        self.StatusEdit.setText(status)
        self.StatusEdit.setDisabled(True)

    def createBaudrateCb(self) -> None:
        self.BaudRateCb = QComboBox()
        for opt in self.ser.BAUDRATES:
            self.BaudRateCb.addItem(str(opt))
        idx = self.BaudRateCb.findText(str(self.ser.baudrate))
        self.BaudRateCb.setCurrentIndex(idx)

    def createByteCb(self) -> None:
        self.BytesSizeCb = QComboBox()
        for opt in self.ser.BYTESIZES:
            self.BytesSizeCb.addItem(str(opt))
        idx = self.BytesSizeCb.findText(str(self.ser.bytesize))
        self.BytesSizeCb.setCurrentIndex(idx)

    def createParityCb(self) -> None:
        self.ParityCb = QComboBox()
        for opt in self.ser.PARITIES:
            self.ParityCb.addItem(opt)
        idx = self.ParityCb.findText(self.ser.parity)
        self.ParityCb.setCurrentIndex(idx)

    def createStopbitsCb(self) -> None:
        self.StopBitsCb = QComboBox()
        for opt in self.ser.STOPBITS:
            self.StopBitsCb.addItem(str(opt))
        idx = self.StopBitsCb.findText(str(self.ser.stopbits))
        self.StopBitsCb.setCurrentIndex(idx)

    def createReadTimeoutSb(self) -> None:
        self.ReadTimeoutSb = QSpinBox()
        self.ReadTimeoutSb.setMinimum(0)
        self.ReadTimeoutSb.setSingleStep(1)
        self.ReadTimeoutSb.setSuffix("s")
        val = self.ser.timeout
        if val is None:
            val = 0
        self.ReadTimeoutSb.setValue(val)

    def createWriteTimeoutSb(self) -> None:
        # write timeout
        self.WriteTimeoutSb = QSpinBox()
        self.WriteTimeoutSb.setMinimum(0)
        self.WriteTimeoutSb.setSingleStep(1)
        self.WriteTimeoutSb.setSuffix("s")
        val = self.ser.write_timeout
        if val is None:
            val = 0
        self.WriteTimeoutSb.setValue(val)

    def createByteTimeoutSb(self) -> None:
        # inter-byte timeout
        self.ByteTimeoutSb = QSpinBox()
        self.ByteTimeoutSb.setMinimum(0)
        self.ByteTimeoutSb.setSingleStep(1)
        self.ByteTimeoutSb.setSuffix("s")
        val = self.ser.inter_byte_timeout
        if val is None:
            val = 0
        self.ByteTimeoutSb.setValue(val)

    def createFlowControlCb(self) -> None:
        # software flow control
        self.SoftwareFlowCb = QComboBox()
        for opt in self._bool_opts:
            self.SoftwareFlowCb.addItem(opt)
        idx = self.SoftwareFlowCb.findText(str(self.ser.xonxoff))
        self.SoftwareFlowCb.setCurrentIndex(idx)

    def createRtsCb(self) -> None:
        # hardware flow: RTS/CTS
        self.RtsctsCb = QComboBox()
        for opt in self._bool_opts:
            self.RtsctsCb.addItem(opt)
        idx = self.RtsctsCb.findText(str(self.ser.rtscts))
        self.RtsctsCb.setCurrentIndex(idx)

    def createDtrCb(self) -> None:
        # hardware flow: DSR/DTR
        self.DsrdtrCb = QComboBox()
        for opt in self._bool_opts:
            self.DsrdtrCb.addItem(opt)
        idx = self.DsrdtrCb.findText(str(self.ser.dsrdtr))
        self.DsrdtrCb.setCurrentIndex(idx)

    def createApplyBtn(self) -> None:
        self.ApplyBtn = QPushButton()
        self.ApplyBtn.setText("Apply")
        self.ApplyBtn.clicked.connect(lambda: Callbacks().clickedApplyBtn(self))

    def createCancelBtn(self) -> None:
        self.CancelBtn = QPushButton()
        self.CancelBtn.setText("Cancel")
        self.CancelBtn.clicked.connect(lambda: Callbacks().clickedCancelBtn(self))

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        pass

class Callbacks:

    def __init__(self):
        pass

    def clickedApplyBtn(self, parent: Window) -> None:
        parent.close()

    def clickedCancelBtn(self, parent: Window) -> None:
        parent.close()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.showNormal()
    sys.exit(app.exec_())
