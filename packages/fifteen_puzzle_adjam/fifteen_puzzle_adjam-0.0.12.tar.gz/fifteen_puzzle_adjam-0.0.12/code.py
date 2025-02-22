# Andrea Diamantini
# Fifteen Puzzle

import random

import wx


def posToId(row, col):
    return (row - 1) * 4 + col


def idToPos(id):
    (row, col) = (id + 3) // 4, id % 4
    if col == 0:
        col = 4
    return row, col


class FifteenPuzzle(wx.Frame):
    def __init__(self):
        super().__init__(None, title="fifteen puzzle", size=(450, 450))

        panel = wx.Panel(self)

        # un font appropriato
        font = wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        panel.SetFont(font)

        grid = wx.GridSizer(rows=4, cols=4, vgap=5, hgap=5)
        self.buttons = {}
        for n in range(1, 17):
            btn = wx.Button(panel, label=str(n), size=(100, 100), id=n)
            btn.Bind(wx.EVT_BUTTON, self.play)
            grid.Add(btn, proportion=0, flag=wx.EXPAND, border=0)
            self.buttons[n] = btn

        # il 16esimo pulsante c'è... ma NON si vede ;)
        btn.Hide()
        self.hiddenButtonPosition = (4, 4)

        panel.SetSizer(grid)
        self.Centre()

        # mischia...
        self.shuffle()

    def play(self, event):
        btn_id = event.GetId()
        self.tryMoveButton(btn_id)
        return

    def tryMoveButton(self, btn_id, check=True):
        btn = self.buttons[btn_id]
        if not btn.IsShown():
            return

        # trovo la posizione del pulsante cliccato, in base al suo ID
        (clickedButtonRow, clickedButtonCol) = idToPos(btn_id)
        hiddenButtonRow, hiddenButtonCol = self.hiddenButtonPosition
        if (
            clickedButtonRow != hiddenButtonRow
            and clickedButtonCol != hiddenButtonCol
        ):
            return

        hiddenButtonId = posToId(hiddenButtonRow, hiddenButtonCol)
        hiddenButton = self.buttons[hiddenButtonId]
        hiddenButton.Show()
        btn.Hide()

        if clickedButtonRow == hiddenButtonRow:
            direction = 1
            if hiddenButtonCol > clickedButtonCol:
                direction = -1
            for col in range(hiddenButtonCol, clickedButtonCol, direction):
                buttonR = self.buttons[posToId(clickedButtonRow, col)]
                buttonL = self.buttons[
                    posToId(clickedButtonRow, col + direction)
                ]
                buttonR.SetLabel(buttonL.GetLabel())
        else:
            direction = 1
            if hiddenButtonRow > clickedButtonRow:
                direction = -1
            for row in range(hiddenButtonRow, clickedButtonRow, direction):
                buttonR = self.buttons[posToId(row, clickedButtonCol)]
                buttonL = self.buttons[
                    posToId(row + direction, clickedButtonCol)
                ]
                buttonR.SetLabel(buttonL.GetLabel())

        self.hiddenButtonPosition = clickedButtonRow, clickedButtonCol

        if check and self.checkWin():
            dial = wx.MessageDialog(
                None,
                "Hai Vinto!",
                "EVVIVA!",
                wx.OK | wx.CANCEL | wx.ICON_INFORMATION,
            )
            dial.SetOKCancelLabels("Chiudi", "Ricomincia")
            if dial.ShowModal() == wx.ID_OK:
                self.Close()
                return
            self.shuffle()
        return

    def checkWin(self):
        for n in range(1, 16):
            btn = self.buttons[n]
            if btn.GetLabel() != str(n) or not btn.IsShown():
                return False
        return True

    def shuffle(self):
        for n in range(500):
            btn_id = random.randint(1, 16)
            self.tryMoveButton(btn_id, False)
        return


# ----------------------------------------
def run():
    app = wx.App()
    window = FifteenPuzzle()
    window.Show()
    app.MainLoop()
    return


if __name__ == "__main__":
    run()
