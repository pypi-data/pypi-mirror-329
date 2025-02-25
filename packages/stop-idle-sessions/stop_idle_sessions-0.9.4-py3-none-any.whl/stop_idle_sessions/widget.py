"""Present a GUI widget to examine the X11 idleness for the current session"""


import os
import tkinter
import tkinter.font
import tkinter.ttk

import stop_idle_sessions.x11


def retrieve_idle_time() -> str:
    """Get the idle time for the current app's DISPLAY"""

    td = stop_idle_sessions.x11.X11DisplayCollector.retrieve_idle_time(
            display=os.environ['DISPLAY'],
            xauthority=os.environ.get('XAUTHORITY', default=None)
    )
    td_seconds = int(td.total_seconds())

    return "{0}:{1:02}".format(td_seconds // 60, td_seconds % 60)


class Application(tkinter.Frame):
    """Overall main application for the GUI widget showing idleness"""

    def __init__(self, master=None):
        super().__init__(master)
        self._value = tkinter.StringVar()
        self._delay_ms = 500

        self.createWidgets()

    def createWidgets(self):
        """Set up the GUI widgets"""

        self.grid()

        font = tkinter.font.Font(family='Courier New', size=36)
        tkinter.ttk.Label(
                self,
                textvariable=self._value,
                font=font
        ).grid(column=0, row=0)

        self.after(0, self.afterTick)

    def afterTick(self):
        """Update the label value after the latest tick"""

        self._value.set(retrieve_idle_time())
        self.after(self._delay_ms, self.afterTick)


def widget_main():
    """Overall main routine for the GUI widget showing idleness"""
    root = tkinter.Tk()
    root.title('idleness')
    app = Application(master=root)
    root.mainloop()


if __name__ == "__main__":
    widget_main()
