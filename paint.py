import win32gui
import win32con
import win32api
from tkinter import *
from PIL import ImageGrab

class DesktopDrawingApp:
    def __init__(self):
        # メインウィンドウの作成
        self.root = Tk()
        self.root.title('Desktop Drawing')
        
        # ウィンドウを透明にし、最前面に表示
        self.root.attributes('-alpha', 0.3, '-topmost', True)
        
        # ウィンドウ枠を削除
        self.root.overrideredirect(True)
        
        # スクリーンサイズでウィンドウを作成
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # キャンバスの作成
        self.canvas = Canvas(self.root, width=screen_width, height=screen_height)
        self.canvas.pack()
        
        # 描画用の変数
        self.drawing = False
        self.last_x = None
        self.last_y = None
        
        # イベントバインド
        self.canvas.bind('<Button-1>', self.start_drawing)
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.stop_drawing)
        
        # ESCキーで終了
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        
        # 右クリックでクリア
        self.canvas.bind('<Button-3>', self.clear_canvas)
        
        # ウィンドウの透明化設定
        self.set_transparent()

    def set_transparent(self):
        # ウィンドウハンドルの取得
        hwnd = win32gui.GetParent(self.canvas.winfo_id())
        
        # 拡張ウィンドウスタイルの設定
        extended_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, 
                             extended_style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)
        
        # クリックスルーを可能にする
        win32gui.SetLayeredWindowAttributes(hwnd, 0, 255, win32con.LWA_ALPHA)

    def start_drawing(self, event):
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y

    def draw(self, event):
        if self.drawing:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                  fill='red', width=2)
            self.last_x = event.x
            self.last_y = event.y

    def stop_drawing(self, event):
        self.drawing = False

    def clear_canvas(self, event):
        self.canvas.delete('all')

if __name__ == '__main__':
    app = DesktopDrawingApp()
    app.root.mainloop()