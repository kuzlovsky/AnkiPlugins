from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *
from aqt.browser import Browser
from anki.hooks import wrap, addHook


############## USER CONFIGURATION START ##############

HOTKEY_COUNT_ELLIPSE = "Ctrl+Shift+E"

############## USER CONFIGURATION END ##############


def showEllipseNotes(self):
    try:
        ids = mw.col.findNotes("deck:current …")
        notes = []
        for i in ids:
            notes.append(mw.col.getNote(i))
        kindle_notes = [note for note in notes if note.model()['name'] == 'Kindle']
        truncated_note_ids = [note.id for note in kindle_notes if len(note.fields[1]) > 0 and note.fields[1][-1] == '…']
        if len(truncated_note_ids):
            nids = [f"nid:%d" %i for i in truncated_note_ids]
            result = ' or '.join(nids)
            text = self.form.searchEdit.lineEdit().text()
            self.form.searchEdit.lineEdit().setText(f"{text} {result}")
        else:
            showInfo('No truncated cards found')
    except Exception as ex:
        showInfo(str(ex))


def onSetupMenus(self):
    """Setup menu entries and hotkeys"""
    try:
        # used by multiple add-ons, so we check for its existence first
        menu = self.menuView
    except:
        self.menuView = QMenu(_("&View"))
        self.menuBar().insertMenu(self.mw.form.menuTools.menuAction(), self.menuView)
        menu = self.menuView
    menu.addSeparator()
    a = menu.addAction('Show ellipse cards')
    a.setShortcut(QKeySequence(HOTKEY_COUNT_ELLIPSE))
    a.triggered.connect(self.showEllipseNotes)


addHook("browser.setupMenus", onSetupMenus)

Browser.showEllipseNotes = showEllipseNotes
