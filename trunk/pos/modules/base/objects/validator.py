#    ObjectAttrValidator.py
#
#    ------------------------------------------------------------
#    Copyright 2004 by Samuel Reynolds. All rights reserved.
#
#    Permission to use, copy, modify, and distribute this software and its
#    documentation for any purpose and without fee is hereby granted,
#    provided that the above copyright notice appear in all copies and that
#    both that copyright notice and this permission notice appear in
#    supporting documentation, and that the name of Samuel Reynolds
#    not be used in advertising or publicity pertaining to distribution
#    of the software without specific, written prior permission.
#
#    SAMUEL REYNOLDS DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
#    INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO
#    EVENT SHALL SAMUEL REYNOLDS BE LIABLE FOR ANY SPECIAL, INDIRECT, OR
#    CONSEQUENTIAL DAMAGES, OR FOR ANY DAMAGES WHATSOEVER RESULTING FROM
#    LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
#    NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
#    WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#    ------------------------------------------------------------

import wx
import sys

def validator(_val_class):
    class DataValidator(_val_class):
        __doc__ = _val_class.__doc__
        def Validate(self, parent):
            try:
                return _val_class.Validate(self, parent)
            except:
                print >>sys.stderr, 'Error in', self, '.Validate()'
                raise
        
        def TransferToWindow(self):
            try:
                return _val_class.TransferToWindow(self)
            except:
                print >>sys.stderr, 'Error in', self, '.TransferToWindow()'
                raise
    
        def TransferFromWindow(self):
            try:
                return _val_class.TransferFromWindow(self)
            except:
                print >>sys.stderr, 'Error in', self, '.TransferFromWindow()'
                raise
        
        def __repr__(self):
            return '<%s %s in %s formatter=%s>' % (self.__class__.__name__, self.key, self.panel.data, self.formatter is not None)
    
    DataValidator.__name__ = _val_class.__name__
    return DataValidator

class BaseValidator(wx.PyValidator):
    """
    Base Validator to be used with form panels.
    Most probably to be subclassed.
    """
    def __init__(self, panel, key, formatter=None):
        wx.PyValidator.__init__(self)
        self.panel = panel
        self.key = key
        self.formatter = formatter

    Clone = lambda self: self.__class__(self.panel, self.key, self.formatter)

    def Validate(self, parent):
        data = self.GetWindowData()
        if self.formatter and not self.formatter.validate(data):
                return False
        if not self.ValidateWindowData(data):
            return False
        return True

    def TransferToWindow(self):
        data = self.panel.data[self.key]
        if self.formatter:
            self.formatter.format(data)
        self.SetWindowData(data)
        return True

    def TransferFromWindow(self):
        data = self.GetWindowData()
        if self.formatter:
            self.formatter.coerce(data)
        self.panel.data[self.key] = data
        return True
        
    def GetWindowData(self):
        #win = self.GetWindow()
        return None
    
    def SetWindowData(self, data):
        #win = self.GetWindow()
        return None
    
    def ValidateWindowData(self, data):
        return True
