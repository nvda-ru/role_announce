# role announce
# Sulaiman Al Qusaimi
# This addon will let you recognize the type of the selected object using a particular shortcut


import globalPluginHandler
import ui
import controlTypes
import api
import os
import winsound
from . import sounds
import wx
import gui
import config
import addonHandler


def initConfig():
	options = {"sounds": "boolean(default=True)"}
	config.conf.spec["roleannounce"] = options

def addSettingsDialogItem():
	prefsMenuItem  = gui.mainFrame.sysTrayIcon.preferencesMenu.Append(wx.ID_ANY, _("role announce..."))
	gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, lambda e: gui.mainFrame._popupSettingsDialog(PreferencesDialog), prefsMenuItem)
initConfig()
addSettingsDialogItem()
addonHandler.initTranslation()


class PreferencesDialog(gui.SettingsDialog):
	title = _("role announce settings")
	def __init__(self, *args, **kwds):
		super(PreferencesDialog, self).__init__(*args, **kwds)
	def makeSettings(self, settingsSizer):
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.playSounds = wx.CheckBox(self, wx.ID_ANY, _("play sound effects"))
		self.playSounds.Value = config.conf["roleannounce"]["sounds"]
		sizer.Add(self.playSounds)
	def onOk(self, event):
		config.conf["roleannounce"]["sounds"] = self.playSounds.Value
		super(PreferencesDialog, self).onOk(event)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	soundsPath = os.path.abspath(os.path.dirname(sounds.__file__))
	def playSound(self, role):
		filePath = os.path.join(self.soundsPath, "{}.wav".format(role))
		if os.path.exists(filePath):
			winsound.PlaySound(filePath, winsound.SND_FILENAME+winsound.SND_ASYNC)
	def script_announce(self, gesture):
		obj = api.getNavigatorObject()
		if config.conf["roleannounce"]["sounds"]:
			self.playSound(obj.role)
		ui.message(controlTypes.roleLabels[obj.role])
	__gestures={
		"kb:shift+nvda+q": "announce",
}