from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.properties import NumericProperty, ListProperty
from kivy.animation import Animation
from kivy.clock import Clock
import random
import json
import os

class Tile(Widget):
    value = NumericProperty(0)
    pos_hint = ListProperty([0, 0])
    
    def __init__(self, value=2, **kwargs):
        super().__init__(**kwargs)
        self.value = value

class GameBoard(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 4
        self.grid = [[None for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.high_score = self.load_high_score()
        
        # 初始化游戏
        self.add_new_tile()
        self.add_new_tile()
        
    def load_high_score(self):
        try:
            if os.path.exists("scores.json"):
                with open("scores.json", "r") as f:
                    data = json.load(f)
                    return data.get("high_score", 0)
        except:
            pass
        return 0
        
    def save_high_score(self):
        try:
            data = {"high_score": self.high_score}
            with open("scores.json", "w") as f:
                json.dump(data, f)
        except:
            pass

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) 
                      if self.grid[i][j] is None]
        if empty_cells:
            i, j = random.choice(empty_cells)
            value = random.choice([2, 2, 2, 4])
            tile = Tile(value=value)
            self.grid[i][j] = tile
            self.add_widget(tile)
            
    def move(self, direction):
        moved = False
        if direction in ['LEFT', 'RIGHT']:
            for i in range(4):
                line = self.grid[i]
                if direction == 'RIGHT':
                    line = line[::-1]
                moved |= self.merge_line(line)
                if direction == 'RIGHT':
                    self.grid[i] = line[::-1]
        else:
            for j in range(4):
                line = [self.grid[i][j] for i in range(4)]
                if direction == 'DOWN':
                    line = line[::-1]
                moved |= self.merge_line(line)
                if direction == 'DOWN':
                    for i in range(4):
                        self.grid[i][j] = line[3-i]
                else:
                    for i in range(4):
                        self.grid[i][j] = line[i]
        
        if moved:
            self.add_new_tile()
            self.save_high_score()
            
        return moved

    def merge_line(self, line):
        moved = False
        # 移除空值
        tiles = [t for t in line if t]
        
        # 合并相同值
        i = 0
        while i < len(tiles) - 1:
            if tiles[i].value == tiles[i+1].value:
                tiles[i].value *= 2
                self.score += tiles[i].value
                self.high_score = max(self.score, self.high_score)
                self.remove_widget(tiles[i+1])
                tiles.pop(i + 1)
                moved = True
            i += 1
            
        # 补充空值
        tiles.extend([None] * (4 - len(tiles)))
        
        # 更新位置
        for i, tile in enumerate(tiles):
            if tile:
                anim = Animation(pos_hint={'x': i/4, 'y': 0}, duration=0.15)
                anim.start(tile)
                
        return moved

class Game2048App(App):
    def build(self):
        # 主布局
        layout = BoxLayout(orientation='vertical')
        
        # 分数显示
        scores = BoxLayout(size_hint_y=0.1)
        self.score_label = Label(text='Score: 0')
        self.high_score_label = Label(text='Best: 0')
        scores.add_widget(self.score_label)
        scores.add_widget(self.high_score_label)
        
        # 游戏面板
        self.board = GameBoard()
        
        # 控制按钮
        controls = BoxLayout(size_hint_y=0.1)
        new_game_btn = Button(text='New Game')
        new_game_btn.bind(on_press=self.new_game)
        quit_btn = Button(text='Quit')
        quit_btn.bind(on_press=self.stop)
        controls.add_widget(new_game_btn)
        controls.add_widget(quit_btn)
        
        # 添加所有组件
        layout.add_widget(scores)
        layout.add_widget(self.board)
        layout.add_widget(controls)
        
        # 绑定触摸事件
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, layout)
        self._keyboard.bind(on_key_down=self._on_key_down)
        Window.bind(on_touch_down=self._on_touch_down)
        Window.bind(on_touch_up=self._on_touch_up)
        
        self._touch_start = None
        return layout
        
    def new_game(self, *args):
        self.board.clear_widgets()
        self.board.grid = [[None for _ in range(4)] for _ in range(4)]
        self.board.score = 0
        self.board.add_new_tile()
        self.board.add_new_tile()
        self.update_score()
        
    def update_score(self):
        self.score_label.text = f'Score: {self.board.score}'
        self.high_score_label.text = f'Best: {self.board.high_score}'
        
    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None
        
    def _on_key_down(self, keyboard, keycode, text, modifiers):
        direction = None
        if keycode[1] == 'left':
            direction = 'LEFT'
        elif keycode[1] == 'right':
            direction = 'RIGHT'
        elif keycode[1] == 'up':
            direction = 'UP'
        elif keycode[1] == 'down':
            direction = 'DOWN'
            
        if direction:
            self.board.move(direction)
            self.update_score()
        return True
        
    def _on_touch_down(self, window, touch):
        self._touch_start = touch.pos
        
    def _on_touch_up(self, window, touch):
        if self._touch_start:
            dx = touch.pos[0] - self._touch_start[0]
            dy = touch.pos[1] - self._touch_start[1]
            
            if abs(dx) > abs(dy) and abs(dx) > 50:
                direction = 'RIGHT' if dx > 0 else 'LEFT'
                self.board.move(direction)
            elif abs(dy) > abs(dx) and abs(dy) > 50:
                direction = 'UP' if dy > 0 else 'DOWN'
                self.board.move(direction)
                
            self.update_score()
            self._touch_start = None

if __name__ == '__main__':
    Game2048App().run() 