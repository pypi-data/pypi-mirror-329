import threading
import tkinter as tk
import traceback


def on_error(exc: Exception):
    print(
        "--------------------------------------------------\n" +
        "".join(traceback.format_exception(type(exc), exc, exc.__traceback__)) +
        "--------------------------------------------------"
    )


def percent_validate(variable, default="100.0%"):
    try:
        value = variable.get().rstrip("%")
        value = str(float(value)) + "%"
    except Exception:
        value = default
    variable.set(value.lstrip("-"))


def float_validate(variable, default="0.0"):
    try:
        value = variable.get()
        value = str(float(value))
    except Exception:
        value = default
    variable.set(value)


def int_validate(variable, default="0"):
    try:
        value = variable.get()
        value = str(int(value))
    except Exception:
        value = default
    variable.set(value)


def adapt_widgets_width(widgets, req=True):
    """将控件列表中的控件的宽度设置为其中最大的宽度"""
    width = max(i.winfo_reqwidth() if req else i.winfo_width() for i in widgets)
    for i in widgets:
        i.configure(width=width)


class Window:
    def __init__(self, size=None, root=None, start_quit_thr=True):
        # 窗口
        self.tk = root if root else tk.Tk()
        self.tk.wm_withdraw()
        self.tk.protocol("WM_DELETE_WINDOW", self.quit)
        self.resolution = (self.tk.winfo_screenwidth(), self.tk.winfo_screenheight())
        if size:
            self.tk.geometry("{}x{}".format(*size))
        # 控制窗口退出
        self.alive = True
        # 激活状态
        self.activated = threading.Event()
        # 显示中
        self.showed = threading.Event()
        # 控制窗口退出
        self.ctrl_quit = threading.Event()
        self.thr_quit = threading.Thread(target=self._quit_window, daemon=True)
        if start_quit_thr:
            self.thr_quit.start()

    def _quit_window(self):
        """离开窗口事件处理."""
        while self.ctrl_quit.wait() and self.alive:
            if self.activated.is_set():
                self.activated.clear()
                try:
                    self.on_quit()
                except Exception as exc:
                    on_error(exc)
                try:
                    self.tk.wm_withdraw()
                except RuntimeError as exc:
                    on_error(exc)
                self.tk.quit()
                self.ctrl_quit.clear()

    def mainloop(self, show=True):
        """启动窗口."""
        self.on_mainloop()
        self.activated.set()
        if show:
            try:
                self.tk.wm_deiconify()
                self.tk.focus_force()
            except RuntimeError as exc:
                on_error(exc)
        self.tk.mainloop()

    def quit(self):
        """离开窗口."""
        self.ctrl_quit.set()

    def destroy(self):
        """销毁窗口."""
        self.alive = False
        self.activated.set()
        self.ctrl_quit.set()
        self.tk.quit()
        self.tk.destroy()
        self.on_destroy()

    def hide(self):
        self.tk.wm_withdraw()
        self.showed.clear()

    def show(self):
        self.tk.wm_deiconify()
        self.showed.set()

    def iconify(self):
        self.tk.wm_iconify()

    def on_mainloop(self):
        pass

    def on_quit(self):
        pass

    def on_destroy(self):
        pass

    def winfo_size(self):
        return self.tk.winfo_width(), self.tk.winfo_height()

    def winfo_reqsize(self):
        return self.tk.winfo_reqwidth(), self.tk.winfo_reqheight()

    def winfo_xy(self):
        return self.tk.winfo_x(), self.tk.winfo_y()

    def bind(self, *args, **kwargs):
        self.tk.bind(*args, **kwargs)

    def align_center(self, req=False):
        self.tk.update()
        w, h = self.winfo_reqsize() if req else self.winfo_size()
        self.tk.wm_geometry("+{}+{}".format((self.resolution[0] - w) // 2, (self.resolution[1] - h) // 2))


class TkMethods:
    def __init__(self, tk_obj):
        self.mainloop = tk_obj.mainloop
        self.quit = tk_obj.quit
        self.destroy = tk_obj.destroy


class WidgetMethods:
    def __init__(self, widget):
        self.pack = widget.pack
        self.place = widget.place
        self.grid = widget.grid
        self.pack_forget = widget.pack_forget
        self.place_forget = widget.place_forget
        self.grid_forget = widget.grid_forget
        self.configure = widget.configure


class MouseMessage:
    """鼠标事件绑定"""
    def __init__(self, widget):
        self.mouse_status_over = False
        self.mouse_status_left = False
        self.mouse_status_middle = False
        self.mouse_status_right = False
        self.mouse_event = None
        widget.bind("<Enter>", self.__on_mouse_enter)
        widget.bind("<Leave>", self.__on_mouse_leave)
        widget.bind("<Button-1>", self.__on_mouse_left_down)
        widget.bind("<ButtonRelease-1>", self.__on_mouse_left_up)
        widget.bind("<Button-2>", self.__on_mouse_middle_down)
        widget.bind("<ButtonRelease-2>", self.__on_mouse_middle_up)
        widget.bind("<Button-3>", self.__on_mouse_right_down)
        widget.bind("<ButtonRelease-3>", self.__on_mouse_right_up)
        widget.bind("<Motion>", self.__on_mouse_motion)
        widget.bind("<B1-Motion>", self.__on_mouse_left_motion)
        widget.bind("<B2-Motion>", self.__on_mouse_middle_motion)
        widget.bind("<B3-Motion>", self.__on_mouse_right_motion)
        widget.bind("<Double-Button-1>", self.__on_mouse_left_dclick)
        widget.bind("<Double-Button-2>", self.__on_mouse_middle_dclick)
        widget.bind("<Double-Button-3>", self.__on_mouse_right_dclick)
        widget.bind("<MouseWheel>", self.__on_mouse_wheel)

    def __on_mouse_enter(self, event):
        self.mouse_status_over = True
        self.mouse_event = event
        self.on_mouse_enter()

    def __on_mouse_leave(self, event):
        self.mouse_status_over = False
        self.mouse_event = event
        self.on_mouse_leave()

    def __on_mouse_left_down(self, event):
        self.mouse_status_left = True
        self.mouse_event = event
        self.on_mouse_left_down()

    def __on_mouse_left_up(self, event):
        self.mouse_status_left = False
        self.mouse_event = event
        self.on_mouse_left_up()

    def __on_mouse_middle_down(self, event):
        self.mouse_status_middle = True
        self.mouse_event = event
        self.on_mouse_middle_down()

    def __on_mouse_middle_up(self, event):
        self.mouse_status_middle = False
        self.mouse_event = event
        self.on_mouse_middle_up()

    def __on_mouse_right_down(self, event):
        self.mouse_status_right = True
        self.mouse_event = event
        self.on_mouse_right_down()

    def __on_mouse_right_up(self, event):
        self.mouse_status_right = False
        self.mouse_event = event
        self.on_mouse_right_up()

    def __on_mouse_motion(self, event):
        self.mouse_event = event
        self.on_mouse_motion()

    def __on_mouse_left_motion(self, event):
        self.mouse_event = event
        self.on_mouse_left_motion()

    def __on_mouse_middle_motion(self, event):
        self.mouse_event = event
        self.on_mouse_middle_motion()

    def __on_mouse_right_motion(self, event):
        self.mouse_event = event
        self.on_mouse_right_motion()

    def __on_mouse_left_dclick(self, event):
        self.mouse_event = event
        self.on_mouse_left_dclick()

    def __on_mouse_middle_dclick(self, event):
        self.mouse_event = event
        self.on_mouse_middle_dclick()

    def __on_mouse_right_dclick(self, event):
        self.mouse_event = event
        self.on_mouse_right_dclick()

    def __on_mouse_wheel(self, event):
        self.mouse_event = event
        self.on_mouse_wheel()

    def on_mouse_enter(self):
        pass

    def on_mouse_leave(self):
        pass

    def on_mouse_left_down(self):
        pass

    def on_mouse_left_up(self):
        pass

    def on_mouse_middle_down(self):
        pass

    def on_mouse_middle_up(self):
        pass

    def on_mouse_right_down(self):
        pass

    def on_mouse_right_up(self):
        pass

    def on_mouse_motion(self):
        pass

    def on_mouse_left_motion(self):
        pass

    def on_mouse_middle_motion(self):
        pass

    def on_mouse_right_motion(self):
        pass

    def on_mouse_left_dclick(self):
        pass

    def on_mouse_middle_dclick(self):
        pass

    def on_mouse_right_dclick(self):
        pass

    def on_mouse_wheel(self):
        pass


class KeyboardMessage:
    """键盘事件绑定"""
    def __init__(self, widget: tk.Misc):
        self._held_key = {}
        self.keyboard_event = None
        widget.bind("<KeyPress>", self.__on_key_press)
        widget.bind("<KeyRelease>", self.__on_key_release)

    def __on_key_press(self, event):
        self._held_key[event.keysym] = event
        self.keyboard_event = event
        self.on_key_press()

    def __on_key_release(self, event):
        if event.keysym in self._held_key:
            del self._held_key[event.keysym]
        self.keyboard_event = event
        self.on_key_release()

    def held_keys(self):
        return self._held_key.copy()

    def get_key(self, name=None):
        return self._held_key.get(name)

    def clear_held_key(self):
        self._held_key.clear()

    def on_key_press(self):
        pass

    def on_key_release(self):
        pass


class MsgBox(tk.Listbox):
    def __init__(self, *args, **kwargs):
        kwa = {"height": 1}
        kwa.update(kwargs)
        super().__init__(*args, **kwa)
        self._count = 0
        self.max = 32

    def append(self, *args):
        if self.max and self._count > self.max:
            self.delete(0)
        else:
            self._count += 1
        self.insert("end", *args)
        self.yview("moveto", 1.0)

    def clear(self):
        self.delete(0, "end")


class Var:
    def __init__(self, value):
        self.value = value
        self.bind = {}

    def apply_changes(self):
        for func in self.bind.values():
            func(self.value)
        self.on_changes()

    def set(self, value):
        self.value = value
        self.apply_changes()

    def get(self):
        return self.value

    def on_changes(self):
        pass


class IntVar(Var):
    def __init__(self, value=0):
        super().__init__(value)


class FloatVar(Var):
    def __init__(self, value=0.0):
        super().__init__(value)


class StringVar(Var):
    def __init__(self, value=""):
        super().__init__(value)


class BooleanVar(Var):
    def __init__(self, value=False):
        super().__init__(value)


class Option(WidgetMethods, MouseMessage):
    def __init__(self, master, text="", value=None, variable=None, size=(100, 32), **kwargs):
        self.master = master
        self.selected = False
        self.fg = "#000000"
        self.fg_mouse_enter = self.fg
        self.fg_mouse_held = self.fg
        self.fg_select = "#ffffff"
        self.bg = "#ffffff"
        self.bg_mouse_enter = "#99ccff"
        self.bg_mouse_held = "#66aaff"
        self.bg_select = "#3388dd"
        self.value = value
        self.variable = None
        self.size = size

        self.f = tk.Frame(self.master, width=self.size[0], height=self.size[1])
        super().__init__(self.f)
        self.f.pack_propagate(False)
        self.label = tk.Label(self.f, text=text, bg=self.bg, fg=self.fg)
        self.label.pack(fill="both", expand=True)
        MouseMessage.__init__(self, self.label)
        if variable:
            self.set_variable(variable)

        for k, v in kwargs.items():
            setattr(self, k, v)

    def resize(self, size):
        self.f.configure(width=size[0], height=size[1])
        self.size = size

    def set_variable(self, variable: Var):
        self.variable = variable
        self.variable.bind[self.value] = self.apply_select_change

    def set_text(self, text):
        self.label.configure(text=text)

    def configure_label(self, **kwargs):
        self.label.configure(kwargs)

    def on_mouse_enter(self):
        # 鼠标进入
        if not self.mouse_status_left and not self.selected:
            self.label.configure(fg=self.fg_mouse_enter, bg=self.bg_mouse_enter)

    def on_mouse_leave(self):
        # 鼠标离开
        if not self.mouse_status_left and not self.selected:
            self.label.configure(fg=self.fg, bg=self.bg)

    def on_mouse_left_down(self):
        # 鼠标按下
        if not self.selected:
            self.label.configure(fg=self.fg_mouse_held, bg=self.bg_mouse_held)

    def on_mouse_left_up(self):
        # 鼠标在范围内松开即选中
        if self.variable and not self.selected and self.mouse_status_over:
            self.variable.set(self.value)

    def apply_select_change(self, value):
        if value == self.value:
            if not self.selected:
                self._select()
        elif self.selected:
            self._unselect()

    def _select(self):
        self.label.configure(fg=self.fg_select, bg=self.bg_select)
        self.selected = True
        self.on_select()

    def _unselect(self):
        self.label.configure(fg=self.fg, bg=self.bg)
        self.selected = False
        self.on_unselect()

    def init(self):
        """初始化, 由其他对象调用此方法."""
        pass

    def on_select(self):
        """选中."""
        pass

    def on_unselect(self):
        """取消选中."""
        pass


class OptionGroup(WidgetMethods):
    def __init__(self, master, variable: Var, size=(100, 32), **kwargs):
        self.master = master
        self.size = size
        self.variable = variable

        self.f = tk.Frame(self.master)
        super().__init__(self.f)
        self.options: list[Option] = []

        for k, v in kwargs.items():
            setattr(self, k, v)

    def configure_options(self, index=None, **kwargs):
        if index:
            self.options[index].configure_label(**kwargs)
        else:
            for option in self.options:
                option.configure_label(**kwargs)

    def init(self):
        for i in self.options:
            i.init()

    def add(self, value=None, text=None, option=None, **kwargs):
        if isinstance(option, Option):
            op = option
            if text is not None:
                op.set_text(text)
            if value is not None:
                op.value = value
        else:
            if option is None:
                option = Option
            op = option(self.f, text=text if text else "", value=value, **kwargs)
        op.set_variable(self.variable)
        op.resize(self.size)
        op.pack()
        self.options.append(op)

    def switch(self, value):
        self.variable.set(value)


def main():
    import tkinter.messagebox

    class MyOption(Option):
        def __init__(self, w, name, *args, **kwargs):
            self.w = w
            self.name = name
            super().__init__(*args, **kwargs)

    class MyWindow(Window, KeyboardMessage):
        """Inherit Window."""
        def __init__(self):
            super().__init__(size=(800, 500))
            self.f = tk.Frame(self.tk)
            self.f.pack(fill="both", expand=True)
            KeyboardMessage.__init__(self, self.tk)
            self.ops = OptionGroup(self.f, Var("1"), size=(100, 50))
            self.ops.pack()
            self.ops.add(option=MyOption(self, "1", self.f, "1", "1"))
            self.ops.add(option=MyOption(self, "2", self.f, "2", "2"))
            self.ops.add(option=MyOption(self, "3", self.f, "3", "3"))
            self.ops.configure_options(font=("Consolas", 12, "bold"))
            self.ops.switch("1")
            self.mb = MsgBox(self.f)
            self.mb.pack(side="bottom", fill="x")
            self.mb.append("123")
            self.align_center()

        def quit(self):
            if tkinter.messagebox.askyesno("Exit", "Are you sure you want to exit?"):
                super().quit()

        def on_mainloop(self):
            print("Window is mainloop.")

        def on_quit(self):
            print("Quiting window.")

        def on_destroy(self):
            print("Window is destroyed.")

        def on_key_press(self, event):
            print("<down>:", event.keysym, self.held_keys())

        def on_key_release(self, event):
            print("<up>:", event.keysym, self.held_keys())

    window = MyWindow()
    window.mainloop()
    window.destroy()


if __name__ == "__main__":
    main()
