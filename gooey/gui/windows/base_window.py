'''
Created on Jan 19, 2014
@author: Chris
'''

import os
import sys
import time
from collections import deque

import wx

from gooey.gui.message_event import MessageEvent
from gooey import i18n
from gooey import image_repository
from gooey.gui.controller import Controller
from gooey.gui.message_router import MessageRouter
from gooey.gui.windows.runtime_display_panel import RuntimeDisplay
from gooey.gui import styling
from gooey.gui.windows import footer, header


class BaseWindow(wx.Frame):
  def __init__(self, BodyPanel, build_spec, params):
    wx.Frame.__init__(self, parent=None, id=-1)

    self._params = params
    self.build_spec = build_spec

    self._controller = None

    # Components
    self.icon = None
    self.head_panel = None
    self.config_panel = None
    self.runtime_display = None
    self.foot_panel = None
    self.panels = None

    self._init_properties()
    self._init_components(BodyPanel)
    self._do_layout()
    self._init_controller()
    self.registerControllers()
    self.Bind(wx.EVT_SIZE, self.onResize)

  def _init_properties(self):
    if not self._params['program_name']:
      title = os.path.basename(sys.argv[0].replace('.py', ''))
    else:
      title = self._params['program_name']
    self.SetTitle(title)
    self.SetSize(self.build_spec['default_size'])
    # self.SetMinSize((400, 300))
    self.icon = wx.Icon(image_repository.icon, wx.BITMAP_TYPE_ICO)
    self.SetIcon(self.icon)

  def _init_components(self, BodyPanel):
    # init gui
    _desc = self.build_spec['program_description']
    self.head_panel = header.FrameHeader(
        heading=i18n.translate("settings_title"),
        subheading=_desc if _desc is not None else '',
        parent=self)
    self.config_panel = BodyPanel(self)
    self.runtime_display = RuntimeDisplay(self)
    self.foot_panel = footer.Footer(self, self._controller)
    self.panels = [self.head_panel, self.config_panel, self.foot_panel]

  def _do_layout(self):
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(self.head_panel, 0, wx.EXPAND)
    sizer.Add(styling.HorizontalRule(self), 0, wx.EXPAND)
    sizer.Add(self.config_panel, 1, wx.EXPAND)
    self.runtime_display.Hide()
    sizer.Add(self.runtime_display, 1, wx.EXPAND)
    sizer.Add(styling.HorizontalRule(self), 0, wx.EXPAND)
    sizer.Add(self.foot_panel, 0, wx.EXPAND)
    self.SetSizer(sizer)

  def _init_controller(self):
    self._controller = Controller(base_frame=self)

  def registerControllers(self):
    for panel in self.panels:
      panel.RegisterController(self._controller)

  def GetOptions(self):
    return self.config_panel.GetOptions()

  def GetRequiredArgs(self):
    return self.config_panel.GetRequiredArgs()

  def GetOptionalArgs(self):
    return self.config_panel.GetOptionalArgs()


  def NextPage(self):
    self.head_panel.NextPage()
    self.foot_panel.NextPage()
    self.config_panel.Hide()
    self.runtime_display.Show()
    self.Layout()

  # def AttachPayload(self, payload):
  #   self._payload = payload

  def ManualStart(self):
    self._controller.ManualStart()

  def onResize(self, evt):
    evt.Skip()


  def PublishConsoleMsg(self, text):
    self.runtime_display.cmd_textbox.AppendText(text)
    # evt = MessageEvent(message=text)
    # self.GetEventHandler().ProcessEvent(evt)
    # wx.PostEvent(self.runtime_display, evt)


if __name__ == '__main__':
  pass
