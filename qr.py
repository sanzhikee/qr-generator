import os
import wx
from draw_qr import create_qr


########################################################################
class QRPanel(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.photo_max_size = 350
        sp = wx.StandardPaths.Get()
        self.defaultLocation = 'c:\\temp'

#        img = wx.EmptyImage(350, 350)
#        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(img))

        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY)

        qrDataLbl = wx.StaticText(self, label="Текст для перевода в QR код:")
        self.qrDataTxt = wx.TextCtrl(self, value="https://iou.io/assets/pdf/whitepaper.pdf",
                                     size=(200, 90), style=wx.TE_MULTILINE | wx.TE_AUTO_URL)

        qrcodeBtn = wx.Button(self, label="Создать QR при помощи qrcode")
        qrcodeBtn.Bind(wx.EVT_BUTTON, self.onUseQrcode)

        # компоновщик
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        qrDataSizer = wx.BoxSizer(wx.VERTICAL)
        qrBtnSizer = wx.BoxSizer(wx.HORIZONTAL)
        locationSizer = wx.BoxSizer(wx.HORIZONTAL)

        qrDataSizer.Add(qrDataLbl, 0, wx.ALL, 5)
        qrDataSizer.Add(self.qrDataTxt, 1, wx.ALL | wx.EXPAND, 5)

        self.mainSizer.Add(wx.StaticLine(self, wx.ID_ANY),
                           0, wx.ALL | wx.EXPAND, 5)

        self.mainSizer.Add(qrDataSizer, 0, wx.EXPAND)

        qrBtnSizer.Add(qrcodeBtn, 0, wx.ALL | wx.EXPAND, 5)
        self.mainSizer.Add(qrBtnSizer, 0, wx.ALL, 10)

        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)

        self.SetSizer(self.mainSizer)
        self.Layout()

    # ----------------------------------------------------------------------
    def onBrowse(self, event):
        """"""
        dlg = wx.DirDialog(self, "Выберите папку:",
                           style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.defaultLocation = path
            self.defaultLocationLbl.SetLabel("Сохраняем в: %s" % path)
        dlg.Destroy()

    # ----------------------------------------------------------------------
    def onUseQrcode(self, event):
        """
https://github.com/lincolnloop/python-qrcode
        """
        qr = create_qr(self.qrDataTxt.GetValue())

        qr_filename = 'qr_images/qr.jpg'
        qr_filename = os.path.abspath(qr_filename)
        img_file = open(qr_filename, 'wb')
        qr.save(img_file, 'JPEG')
        img_file.close()

        self.showQRCode(qr_filename)

    # ----------------------------------------------------------------------
    def showQRCode(self, filepath):
        """"""
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        self.Refresh()


########################################################################
class QRFrame(wx.Frame):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="QR Code Viewer", size=(600, 900))
        panel = QRPanel(self)


if __name__ == "__main__":
    app = wx.App(False)
    frame = QRFrame()
    frame.Show()
    app.MainLoop()