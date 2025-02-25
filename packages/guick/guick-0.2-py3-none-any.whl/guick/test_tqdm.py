import wx
from tqdm import tqdm
import threading
import time

class TqdmRedirect:
    def __init__(self, text_ctrl):
        self.text_ctrl = text_ctrl

    def write(self, message):
        if message.strip():  # Avoid printing empty lines
            wx.CallAfter(self.update_text_ctrl, message)

    def flush(self):
        pass  # Required by tqdm but not used here

    def update_text_ctrl(self, message):
        if "\r" in message:
            print("tqdm")
        self.text_ctrl.SetValue(message)  # Overwrite text without newlines
        self.text_ctrl.SetInsertionPointEnd()  # Keep the cursor at the end


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="tqdm in TextCtrl", size=(400, 200))
        panel = wx.Panel(self)

        self.text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        run_button = wx.Button(panel, label="Run Progress")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.text_ctrl, 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(run_button, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        panel.SetSizer(sizer)

        run_button.Bind(wx.EVT_BUTTON, self.on_run)

        self.Show()

    def on_run(self, event):
        threading.Thread(target=self.run_progress, daemon=True).start()

    def run_progress(self):
        redirect = TqdmRedirect(self.text_ctrl)
        for _ in tqdm(range(100), file=redirect, ncols=40):
            time.sleep(0.05)  # Simulate work


if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()

