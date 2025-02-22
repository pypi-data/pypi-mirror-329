# Andrea Diamantini
# Fifteen Puzzle

import random

import wx


class FifteenPuzzle(wx.Frame):
    def __init__(self):
        super().__init__(None, title="15 puzzle", size=(450, 450))

        panel = wx.Panel(self)

        # un font appropriato
        font = wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        panel.SetFont(font)

        grid = wx.GridSizer(rows=4, cols=4, vgap=5, hgap=5)
        self.buttons = {}
        for n in range(1, 16):
            btn = wx.Button(panel, label=str(n), size=(100, 100), id=n)
            self.buttons[n] = btn
            grid.Add(btn, proportion=0, flag=wx.EXPAND, border=0)
            btn.Bind(wx.EVT_BUTTON, self.play)

        # il 16esimo pulsante c'è... ma NON si vede ;)
        btn = wx.Button(panel, label=str(16), size=(100, 100), id=16)
        btn.Hide()
        self.buttons[16] = btn
        grid.Add(btn, proportion=0, flag=wx.EXPAND, border=0)
        btn.Bind(wx.EVT_BUTTON, self.play)

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

        moves = {
            1: (2, 5),
            2: (1, 3, 6),
            3: (2, 4, 7),
            4: (3, 8),
            5: (1, 6, 9),
            6: (2, 5, 7, 10),
            7: (3, 6, 8, 11),
            8: (4, 7, 12),
            9: (5, 10, 13),
            10: (6, 9, 11, 14),
            11: (7, 10, 12, 15),
            12: (8, 11, 16),
            13: (9, 14),
            14: (10, 13, 15),
            15: (11, 14, 16),
            16: (12, 15),
        }

        second = -1
        for n in moves[btn_id]:
            if not self.buttons[n].IsShown():
                second = n
                break

        if second == -1:
            return

        secondButton = self.buttons[second]
        secondButton.SetLabel(btn.GetLabel())
        btn.Hide()
        secondButton.Show()

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
