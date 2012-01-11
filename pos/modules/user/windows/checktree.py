import wx

wxEVT_CHECKTREECTRL = wx.NewEventType()
EVT_CHECKTREECTRL = wx.PyEventBinder(wxEVT_CHECKTREECTRL, 1)
class CheckTreeCtrlEvent(wx.PyCommandEvent):
    '''
       This event is fired when an item is checked/unchecked.
    '''
    def __init__(self, eventType, id):
        wx.PyCommandEvent.__init__(self, eventType, id)
        self._eventType = eventType

    def SetItem(self, item):
        self._item = item

    def GetItem(self):
        return self._item


CT_AUTO_CHECK_CHILD = 0x9000
CT_AUTO_TOGGLE_CHILD = 0x10000
class CheckTreeCtrl(wx.TreeCtrl):
    '''
       This class was build to be almost identical to `wx.TreeCtrl` plus
       adding support to checked/unchecked items.
       NB: ImageLists are not supported.
    '''
    def __init__(self, parent, id, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.TR_HAS_BUTTONS,
                 validator=wx.DefaultValidator, name="checkTree"):
        wx.TreeCtrl.__init__(self, parent, id, pos, size, style)
        self.__style = style
        self.__il = wx.ImageList(20, 18)
        bmp = self.__MakeBitmap(0, 20, 18)
        self.__il.Add(bmp)

        bmp = self.__MakeBitmap(1, 20, 18)
        self.__il.Add(bmp)

        bmp = self.__MakeBitmap(2, 20, 18)
        self.__il.Add(bmp)

        wx.TreeCtrl.SetImageList(self, self.__il)

        self.Bind(wx.EVT_LEFT_DOWN, self.__OnLeftDown)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.__OnActivate, self)
        #self.Bind(wx.EVT_LEFT_DCLICK, self.__OnLeftDClick)


    def __MakeBitmap(self, bmp1, width, height):
        # Makes a bitmap composed by the checkbox depending on its state(bmp1)
        bitmap = wx.EmptyBitmap(width, height, -1)

        mdc1 = wx.MemoryDC()
        mdc1.SelectObject( bitmap )
        mdc1.SetBrush(wx.BLACK_BRUSH)
        mdc1.SetTextForeground(wx.BLACK)
        mdc1.SetFont(wx.NORMAL_FONT)
        mdc1.Clear()

        render = wx.RendererNative.Get()

        if bmp1 == 0:
            # unchecked
            render.DrawCheckBox(self, mdc1, (1, 1, 16, 16))
        elif bmp1 == 1:
            # checked
            render.DrawCheckBox(self, mdc1, (1, 1, 16, 16), wx.CONTROL_CHECKED)
        elif bmp1 == 2:
            # partial check
            render.DrawCheckBox(self, mdc1, (1, 1, 16, 16), wx.CONTROL_CHECKABLE)

        mdc1.SetBackground(wx.Brush(self.GetBackgroundColour()))

        return bitmap

    def __DoCheckItem(self, item, which, checked, i):
        if i > -1: # There is an image to `which` state                    
            if checked == None: # Toggle check
                if i == 0: # Not checked
                    wx.TreeCtrl.SetItemImage(self,item, 1, which)
                elif i == 1: # Checked
                    wx.TreeCtrl.SetItemImage(self,item, 0, which)
                elif i == 2: # Partial
                    wx.TreeCtrl.SetItemImage(self,item, 1, which)
            else: # Force check/uncheck
                if checked: # Force check
                    wx.TreeCtrl.SetItemImage(self,item, 1, which)
                else: # Force uncheck
                    wx.TreeCtrl.SetItemImage(self,item, 0, which)

    def __CheckItem(self, item, checked=None):
        normal = self.GetItemImage(item, wx.TreeItemIcon_Normal)
        self.__DoCheckItem(item, wx.TreeItemIcon_Normal, checked, normal)

    def IsItemChecked(self, item):
        '''
        Returns True if the item is checked and False if unchecked or partial.
        '''
        aux = self.GetItemImage(item, wx.TreeItemIcon_Normal)
        if aux > -1: return aux == 1

        # We never should get here, but if something went wrong
        # return False anyway
        return False


    def __AutoToggleChild(self, item):
        '''
        Toggle every child of item.
        '''
        (child, cookie) = self.GetFirstChild(item)
        while child.IsOk():
            self.__CheckItem(child)
            self.__AutoToggleChild(child)
            (child, cookie) = self.GetNextChild(item, cookie)

    def __AutoCheckChild(self, item, checked):
        '''
        Check/Uncheck every child of item.
        '''
        (child, cookie) = self.GetFirstChild(item)
        while child.IsOk():
            self.__CheckItem(child, checked)
            self.__AutoCheckChild(child, checked)
            (child, cookie) = self.GetNextChild(item, cookie)

    def __ChildrenState(self, item):
        '''
        Change the state(checked/unchecked/partial) of the first parent of item.
        '''
        total = 0
        count_checked = 0
        state = None
        (child, cookie) = self.GetFirstChild(item)
        while child.IsOk():
            total += 1
            normal = self.GetItemImage(child, wx.TreeItemIcon_Normal)
            if normal == 1:
                count_checked += 1
            elif normal == 2:
                state = 2
                break
            (child, cookie) = self.GetNextChild(item, cookie)
        if state is None:
            if count_checked == total:
                state = 1
            elif count_checked == 0:
                state = 0
            else:
                state = 2
        wx.TreeCtrl.SetItemImage(self,item, state, wx.TreeItemIcon_Normal)

    def __AutoCheckParent(self, item):
        '''
        Go through all of the parents of item and changes their state(checked/unchecked/partial).
        '''
        parent = self.GetItemParent(item)
        if parent.IsOk():
            self.__ChildrenState(parent)
            self.__AutoCheckParent(parent)

    def __CheckEvent(self, item):
        '''
        Check/Uncheck item and acts depending on style flags. Triggers CheckTreeCtrl event.
        '''
        self.__CheckItem(item)

        if self.__style & CT_AUTO_CHECK_CHILD:
            ischeck = self.IsItemChecked(item)
            self.__AutoCheckChild(item, ischeck)
            self.__AutoCheckParent(item)
        elif self.__style & CT_AUTO_TOGGLE_CHILD:
            self.__AutoToggleChild(item)

        e = CheckTreeCtrlEvent(wxEVT_CHECKTREECTRL, self.GetId())
        e.SetItem(item)
        e.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(e)

    def __OnLeftDown(self, evt):
        '''
        Check/Uncheck item if icon is pressed.
        '''
        pt = evt.GetPosition()
        item, flags = self.HitTest(pt)
        if flags & wx.TREE_HITTEST_ONITEMICON:
            self.__CheckEvent(item)
        evt.Skip()

    def __OnActivate(self, evt):
        '''
        Check/Uncheck item if item is activated.
        '''
        item = evt.GetItem()
        self.__CheckEvent(item)
        evt.Skip()

#    def __OnLeftDClick(self, evt):
#        pt = evt.GetPosition()
#        item, flags = self.HitTest(pt)
#        if not flags & wx.TREE_HITTEST_ONITEMICON:
#            self.Toggle(item)
#        evt.Skip()

    def CheckItem(self, item, checked=True):
        '''
        Check/Uncheck/Toggle item and acts depending on style flags. Does not trigger CheckTreeCtrl event.
        '''
        self.__CheckItem(item, checked)
        if self.__style & CT_AUTO_CHECK_CHILD:
            ischeck = self.IsItemChecked(item)
            self.__AutoCheckChild(item, ischeck)
            self.__AutoCheckParent(item)
        elif self.__style & CT_AUTO_TOGGLE_CHILD:
            self.__AutoToggleChild(item)

    def CheckChildren(self, item, checked=True):
        '''
        Check/Uncheck/Toggle item. Does not trigger CheckTreeCtrl event.
        '''
        if checked == None:
            self.__AutoToggleChild(item)
        else:
            self.__AutoCheckChild(item, checked)
            self.__AutoCheckParent(item)

    def GetChecked(self, checked=True, parent=None):
        '''
        Return all children of parent(or root) that have no child and are checked/unchecked.
        '''
        if parent is None:
            parent = self.GetRootItem()
        items = self.__SeeChildrenChecked(parent, checked)
        return items
    
    def __SeeChildrenChecked(self, item, checked):
        '''
        Return all children of item that have no child and are checked/unchecked.
        '''
        state = self.GetItemImage(item, wx.TreeItemIcon_Normal)
        if (state == 1 and not checked) or (state == 0 and checked):
            return []
        (child, cookie) = self.GetFirstChild(item)
        if not child.IsOk() and self.IsItemChecked(item) == checked:
            return [item]
        else:
            items = []
            while child.IsOk():
                normal = self.GetItemImage(child, wx.TreeItemIcon_Normal)
                items.extend(self.__SeeChildrenChecked(child, checked))
                (child, cookie) = self.GetNextChild(item, cookie)
            return items

    def AddRoot(self, text, image=-1, selImage=-1, data=None):
        return wx.TreeCtrl.AddRoot(self, text, 0, -1, data)
    def AppendItem(self, parent, text, image=-1, selImage=-1, data=None):
        return wx.TreeCtrl.AppendItem(self, parent, text, 0, -1, data)
    def PrependItem(self, parent, text, image=-1, selImage=-1, data=None):
        return wx.TreeCtrl.PrependItem(self, parent, text, 0, -1, data)
    def SetItemImage(self, item, image, which = wx.TreeItemIcon_Normal):
        pass
    def AssignImageList(self, il):
        pass
    def SetImageList(self, il):
        pass
