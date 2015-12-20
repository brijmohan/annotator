#from PyQt4 import *
from PyQt4 import QtGui
from PyQt4.QtGui import QFileDialog, QVBoxLayout, QCheckBox
import sys
from annotator_auto import Ui_Dialog
import os, datetime
import imp

class Editor(QtGui.QMainWindow):

    def __init__(self):
        super(Editor, self).__init__()

        self.taggedData = {}

        self.ui=Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.selectFile)
        self.ui.pushButton_2.clicked.connect(self.highlightNext)
        self.ui.pushButton_3.clicked.connect(self.highlightPrev)
        self.ui.pushButton_4.clicked.connect(self.saveFile)

        self.ui.label_2.setWordWrap(True)
        
        self.highlightformat = QtGui.QTextCharFormat()
        self.highlightformat.setBackground(QtGui.QBrush(QtGui.QColor("yellow")))
        
        self.normalformat = QtGui.QTextCharFormat()
        self.normalformat.setBackground(QtGui.QBrush(QtGui.QColor("white")))

        self.taggedformat = QtGui.QTextCharFormat()
        #self.taggedformat.setBackground(QtGui.QBrush(QtGui.QColor(0, 0, 255, 127)))
        self.taggedformat.setBackground(QtGui.QBrush(QtGui.QColor("cyan")))
        
        self.cursor = self.ui.textEdit.textCursor()
        self.cpos = 0
        self.sel_text = ''
        self.cursor.setPosition(self.cpos)
       
        with open('tags') as tfile:
            for i in tfile:
                self.addCheckbox(i.strip())

        self.show()

    def addCheckbox(self, name):
        checkBox = QtGui.QCheckBox(name)
        self.ui.verticalLayout.addWidget(checkBox)
        checkBox.setText(name)
        checkBox.clicked.connect(self.tagWord)
        newHeight = self.geometry().height()+21#Compensate for new checkbox
        self.resize(self.geometry().width(),  newHeight)

    def tagWord(self, state):
        print self.cpos, self.sel_text, ':'
        
        selected_tags = []
        for i in self.findChildren(QtGui.QCheckBox):
            if i.isChecked():
                selected_tags.append(str(i.text()))
        
        k = (self.cpos, str(self.sel_text))
        self.taggedData[k] = selected_tags

        print '1', selected_tags, self.taggedData

    def showTags(self):
        for i in self.findChildren(QtGui.QCheckBox):
            i.setChecked(False)
        
        k = (self.cpos, str(self.sel_text))
        print '2', k, self.taggedData
        if k in self.taggedData:
            for i in self.findChildren(QtGui.QCheckBox):
                if str(i.text()) in self.taggedData[k]:
                    i.setChecked(True)


    def selectFile(self):
        self.now = datetime.datetime.now()
        self.inpfile = str(QFileDialog.getOpenFileName())
        self.ui.label.setText(self.inpfile)
        #self.outfile = "%s/%s_%d%d%d%d%d%d.mzXML" % (os.path.dirname(self.inpfile),os.path.splitext(os.path.basename(self.inpfile))[0],self.now.year, self.now.month, self.now.day, self.now.hour, self.now.minute, self.now.second)
        if self.inpfile != '':
            self.filetext = open(self.inpfile).read().strip()
            self.textlen = len(self.filetext)
            self.ui.textEdit.setText(self.filetext)

            self.highlightNext()

    def saveFile(self):
        self.now = datetime.datetime.now()
        self.outfile = str(QFileDialog.getSaveFileName())

        with open(self.outfile, 'wb') as ofile:
            for k, v in sorted(self.taggedData.items()):
                ofile.write(str(k[0]) + ', ' + k[1] + ' : ' + ','.join(v) + '\n')

        self.ui.label_2.setText('File saved as \"' + os.path.basename(self.outfile) + '\" at ' + self.now.strftime('%d %b, %Y %H:%M:%S'))

    def highlightNext(self):
        k = (self.cpos, str(self.sel_text))
        print k
        if k in self.taggedData and len(self.taggedData[k]) > 0:
            self.cursor.mergeCharFormat(self.taggedformat)
        else:
            self.cursor.mergeCharFormat(self.normalformat)
        
        self.cursor.setPosition(self.cpos, 0)
        #self.cursor.setPosition(self.ui.textEdit.textCursor().position(),0)
        self.cpos = self.cursor.position()
        #print self.cursor.position(), self.cursor.anchor(), self.textlen
        if self.cpos < self.textlen:
            if self.cpos != 0:
                self.ui.textEdit.setTextCursor(self.cursor)
                self.cursor.movePosition(QtGui.QTextCursor.NextWord, 0)
            self.cursor.movePosition(QtGui.QTextCursor.EndOfWord, 1)
            
            self.sel_text = self.cursor.selectedText()
            
            self.cpos = self.cursor.position()
            #self.ui.textEdit.textCursor().setPosition(self.cpos, 0)
            #print self.sel_text
            if self.sel_text == '' or not str(self.sel_text).isalnum():
                #self.cursor.movePosition(QtGui.QTextCursor.NextWord, 0)
                self.highlightNext()
            self.cursor.mergeCharFormat(self.highlightformat)

            self.showTags()
    
    def highlightPrev(self):
        
        k = (self.cpos, str(self.sel_text))
        if k in self.taggedData and len(self.taggedData[k]) > 0:
            self.cursor.mergeCharFormat(self.taggedformat)
        else:
            self.cursor.mergeCharFormat(self.normalformat)
        
        self.cursor.setPosition(self.cpos, 0)
        self.ui.textEdit.setTextCursor(self.cursor)
        self.ui.textEdit.ensureCursorVisible()
        
        #print self.cursor.position()
        if self.cursor.position > 0:
            self.cursor.movePosition(QtGui.QTextCursor.PreviousWord, 0)
            self.cursor.movePosition(QtGui.QTextCursor.PreviousWord, 0)
            self.cursor.movePosition(QtGui.QTextCursor.EndOfWord, 1)
            
            self.sel_text = self.cursor.selectedText()
            #print self.sel_text
            if self.sel_text == ''  or not str(self.sel_text).isalnum():
                self.cpos = self.cursor.position()
                self.highlightPrev()

            self.cursor.mergeCharFormat(self.highlightformat)

            self.cpos = self.cursor.position()
            self.showTags()

def main():
    app = QtGui.QApplication(sys.argv)
    ex = Editor()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
