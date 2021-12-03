WHITE = 1
BLACK = 2


def correct_coords(row, col):
    """Функция проверяет, что координаты (row, col) лежат
    внутри доски"""
    return 0 <= row < 8 and 0 <= col < 8


# Удобная функция для вычисления цвета противника
def opponent(color):
    if color == WHITE:
        return BLACK
    return WHITE


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        """Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела."""
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def move_piece(self, row, col, row1, col1):
        """Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернет True.
        Если нет --- вернет False"""

        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if not piece.can_move(row1, col1):
            return False
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        piece.set_position(row1, col1)
        self.color = opponent(self.color)
        return True

    def is_under_attack(self, row, col, color):
        # бой конем Knight
        for i in range(-1, 2, 2):
            for j in range(-2, 3, 4):
                if correct_coords(row + i, col + j):
                    if (isinstance(self.field[row + i][col + j], Knight)
                            and self.field[row + i][col + j].get_color() == color):
                        return True
                if correct_coords(row + j, col + i):
                    if (isinstance(self.field[row + j][col + i], Knight)
                            and self.field[row + j][col + i].get_color() == color):
                        return True
        # проверка на остальное
        # Rook and Queen
        for i in range(8):
            if (isinstance(self.field[i][col], Rook) or isinstance(self.field[i][col], Queen))\
                    and self.field[i][col].get_color() == color:
                return True
            if (isinstance(self.field[row][i], Rook) or isinstance(self.field[row][i], Queen)) \
                    and self.field[row][i].get_color() == color:
                return True

        # Queen and Bishop
        kostil = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
        const_row, const_col = row, col
        for i in kostil:
            row, col = const_row, const_col
            while correct_coords(row + i[0], col + i[1]):
                if ((isinstance(self.field[row + i[0]][col + i[1]], Queen)
                        or isinstance(self.field[row + i[0]][col + i[1]], Bishop))
                        and self.field[row + i[0]][col + i[1]].get_color() == color):
                    return 'x'

                row += i[0]
                col += i[1]
        return False


class Queen:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def can_move(self, row1, col1):
        if 0 <= row1 < 8 and 0 <= col1 < 8:
            if abs(self.row - row1) == abs(self.col - col1)\
                    or ((self.row == row1 and self.col != col1)
                        or (self.row != row1 and self.col == col1)):
                return True
            else:
                return False
        else:
            return False

    def set_position(self, row1, col1):
        self.row = row1
        self.col = col1

    def get_color(self):
        return self.color

    def char(self):
        return 'Q'


class Rook:

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def set_position(self, row, col):
        self.row = row
        self.col = col

    def char(self):
        return 'R'

    def get_color(self):
        return self.color

    def can_move(self, row, col):
        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
        if self.row != row and self.col != col:
            return False

        return True


class Bishop:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def can_move(self, row1, col1):
        if 0 <= row1 < 8 and 0 <= col1 < 8:
            if abs(self.row - row1) == abs(self.col - col1):
                return True
            else:
                return False
        else:
            return False

    def set_position(self, row1, col1):
        self.row = row1
        self.col = col1

    def get_color(self):
        return self.color

    def char(self):
        return 'B'


class Knight:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def can_move(self, row1, col1):
        return 0 <= row1 < 8 and 0 <= col1 < 8 and abs(self.row - row1) * abs(self.col - col1) == 2

    def set_position(self, row1, col1):
        self.row = row1
        self.col = col1

    def get_color(self):
        return self.color

    def char(self):
        return 'N'

