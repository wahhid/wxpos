import wx

import ConfigParser

import pos

from ..panels import MySQLConfigPanel, SqliteConfigPanel

class ConfigDialog(wx.Dialog):
    def addOption(self, name, label, panel):
        self.panelBook.AddPage(panel, label)
        panel.TransferDataToWindow()
        self.options[label] = name
    
    def __init_ctrls(self):
        self.introTxt = wx.StaticText(self, -1, label='Select and configure the database system you want to use.')
        
        self.panelBook = wx.Choicebook(self, -1)
        self.addOption('sqlite', 'Sqlite', SqliteConfigPanel(self.panelBook))
        self.addOption('mysql', 'MySQL', MySQLConfigPanel(self.panelBook))
        
        self.okBtn = wx.Button(self, wx.ID_OK, label='OK')
        self.okBtn.Bind(wx.EVT_BUTTON, self.OnOkButton)

        self.cancelBtn = wx.Button(self, wx.ID_CANCEL, label='Cancel')
    
    def __init_sizers(self):
        self.controlSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.controlSizer.Add(self.okBtn, 0, border=5, flag=wx.ALL | wx.EXPAND)
        self.controlSizer.Add(self.cancelBtn, 0, border=5, flag=wx.ALL | wx.EXPAND)
        
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.mainSizer.Add(self.introTxt, 0, border=5, flag=wx.ALL | wx.EXPAND)
        self.mainSizer.Add(self.panelBook, 1, border=5, flag=wx.ALL | wx.EXPAND)
        self.mainSizer.Add(self.controlSizer, 0, border=5, flag=wx.ALL | wx.EXPAND)

        self.SetSizer(self.mainSizer)
    
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1,
              size=wx.Size(400, 500), title='MySQL Configuration')
        
        self.options = {}
        self.__init_ctrls()
        self.__init_sizers()
        
        dbName = pos.database.config.get_used()
        for i in range(self.panelBook.GetPageCount()):
            dbLabel = self.panelBook.GetPageText(i)
            if dbName == self.options[dbLabel]:
                self.panelBook.SetSelection(i)
                break

        selected = self.panelBook.GetSelection()
        dbPanel = self.panelBook.GetPage(selected)
        dbPanel.TransferDataToWindow()

    def OnOkButton(self, event):
        selected = self.panelBook.GetSelection()
        dbPanel = self.panelBook.GetPage(selected)
        dbLabel = self.panelBook.GetPageText(selected)
        dbName = self.options[dbLabel]
        if dbPanel.Validate():
            if dbPanel.TransferDataFromWindow():
                pos.database.config.use(dbName)
                event.Skip()
