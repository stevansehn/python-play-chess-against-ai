import pygame

square_side = 64
square_size = (square_side, square_side)
path = 'img'


class Bishop():
    def __init__(self, start_pos, surface, pieces_dict, moves_history, start_coords, color):
        self.id = start_coords
        self.kind = 'bishop'
        self.color = color
        self.surface = surface
        self.pieces_dict = pieces_dict
        img = pygame.image.load(f'{path}/{color}_{self.kind}.png').convert_alpha()
        img = pygame.transform.scale(img, square_size)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        self.coords = start_coords
        self.moves_history = moves_history
        self.moves = []
        self.my_turn = True if self.color == 'white' else False
        
    def update(self, pos=False, coords=False, move=False):
        if pos:
            self.rect.center = pos
        if coords:
            self.coords = coords
        if move:
            self.moves.append(move)

    def draw(self):
        self.surface.blit(self.image, self.rect)

    def get_pos(self):
        return self.rect.center

    def get_rect(self):
        return self.rect

    def get_possible_moves(self):
        possible_moves = []
        rank = self.coords[0]
        file = int(self.coords[1])
        ranks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        rank_index = ranks.index(rank)
        right_coords = []
        left_coords = []
        y_asc = rank_index
        y_des = rank_index

        for x in range(file+1, 8+1):
            y_asc += 1
            if (y_asc <= 7):
                right_coords.append(f'{ranks[y_asc]}{x}')
                if(self.check_if_empty(f'{ranks[y_asc]}{x}')==False):
                    break
        for x in range(file+1, 8+1):       
            y_des -= 1
            if (y_des >= 0):
                right_coords.append(f'{ranks[y_des]}{x}')
                if(self.check_if_empty(f'{ranks[y_des]}{x}')==False):
                    break

        y_asc = rank_index
        y_des = rank_index
        for x in range(file-1, 0, -1):
            y_asc += 1
            if (y_asc <= 7):
                left_coords.append(f'{ranks[y_asc]}{x}')
                if(self.check_if_empty(f'{ranks[y_asc]}{x}')==False):
                    break
        for x in range(file-1, 0, -1):
            y_des -= 1
            if (y_des >= 0):
                left_coords.append(f'{ranks[y_des]}{x}')
                if(self.check_if_empty(f'{ranks[y_des]}{x}')==False):
                    break
        
        coords_list = left_coords + right_coords

        for dest_coords in coords_list:
            if self.check_if_empty(dest_coords) == True:
                possible_moves.append(dest_coords)
            else:
                target_piece = self.give_coords_get_piece(dest_coords)
                if self.check_if_same_color(target_piece) == False:
                    possible_moves.append(dest_coords)

        possible_moves = sorted(possible_moves)
        return possible_moves

    def give_coords_get_piece(self, coords):
        for piece in self.pieces_dict.values():
            if piece.coords == coords:
                return piece

    def check_if_empty(self, dest_coords):
        piece = self.give_coords_get_piece(dest_coords)
        if piece:
            return False
        else:
            return True

    def check_if_same_color(self, target_piece):
        if self.color == target_piece.color:
            return True
        else:
            return False


class King():
    def __init__(self, start_pos, surface, pieces_dict, moves_history, start_coords, color):
        self.id = start_coords
        self.kind = 'king'
        self.color = color
        self.surface = surface
        self.pieces_dict = pieces_dict
        img = pygame.image.load(f'{path}/{color}_{self.kind}.png').convert_alpha()
        img = pygame.transform.scale(img, square_size)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        self.coords = start_coords
        self.moves_history = moves_history
        self.moves = []
        self.my_turn = True if self.color == 'white' else False
        
    def update(self, pos=False, coords=False, move=False):
        if pos:
            self.rect.center = pos
        if coords:
            self.coords = coords
        if move:
            self.moves.append(move)

    def draw(self):
        self.surface.blit(self.image, self.rect)

    def get_pos(self):
        return self.rect.center

    def get_rect(self):
        return self.rect

    def get_possible_moves(self):
        possible_moves = []
        rank = self.coords[0]
        file = int(self.coords[1])
        ranks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        rank_index = ranks.index(rank)
        inc = 1
        if self.color != 'white':
            inc *= -1

        if (self.color == 'white' and file != 8) or (self.color == 'black' and file != 1):
            dest_coords = f'{rank}{file+inc}'
            if self.check_if_empty(dest_coords) == True:
                possible_moves.append(dest_coords)
            else:
                target_piece = self.give_coords_get_piece(dest_coords)
                if self.check_if_same_color(target_piece) == False:
                    possible_moves.append(dest_coords)

        if (self.color == 'white' and file != 1) or (self.color == 'black' and file != 8):
            dest_coords = f'{rank}{file-inc}'
            if self.check_if_empty(dest_coords) == True:
                possible_moves.append(dest_coords)
            else:
                target_piece = self.give_coords_get_piece(dest_coords)
                if self.check_if_same_color(target_piece) == False:
                    possible_moves.append(dest_coords)

        if (rank_index != 0):
            dest_coords = f'{ranks[rank_index-1]}{file}'
            if self.check_if_empty(dest_coords) == True:
                possible_moves.append(dest_coords)
            else:
                target_piece = self.give_coords_get_piece(dest_coords)
                if self.check_if_same_color(target_piece) == False:
                    possible_moves.append(dest_coords)

        if (rank_index != 7):
            dest_coords = f'{ranks[rank_index+1]}{file}'
            if self.check_if_empty(dest_coords) == True:
                possible_moves.append(dest_coords)
            else:
                target_piece = self.give_coords_get_piece(dest_coords)
                if self.check_if_same_color(target_piece) == False:
                    possible_moves.append(dest_coords)

        if (self.color == 'white' and file != 8) or (self.color == 'black' and file != 1):
            if (rank_index != 0):
                dest_coords = f'{ranks[rank_index-1]}{file+inc}'
                if self.check_if_empty(dest_coords) == True:
                    possible_moves.append(dest_coords)
                else:
                    target_piece = self.give_coords_get_piece(dest_coords)
                    if self.check_if_same_color(target_piece) == False:
                        possible_moves.append(dest_coords)
            if (rank_index != 7):
                dest_coords = f'{ranks[rank_index+1]}{file+inc}'
                if self.check_if_empty(dest_coords) == True:
                    possible_moves.append(dest_coords)
                else:
                    target_piece = self.give_coords_get_piece(dest_coords)
                    if self.check_if_same_color(target_piece) == False:
                        possible_moves.append(dest_coords)
        
        if (self.color == 'white' and file != 1) or (self.color == 'black' and file != 8):
            if (rank_index != 0):
                dest_coords = f'{ranks[rank_index-1]}{file-inc}'
                if self.check_if_empty(dest_coords) == True:
                    possible_moves.append(dest_coords)
                else:
                    target_piece = self.give_coords_get_piece(dest_coords)
                    if self.check_if_same_color(target_piece) == False:
                        possible_moves.append(dest_coords)
            if (rank_index != 7):
                dest_coords = f'{ranks[rank_index+1]}{file-inc}'
                if self.check_if_empty(dest_coords) == True:
                    possible_moves.append(dest_coords)
                else:
                    target_piece = self.give_coords_get_piece(dest_coords)
                    if self.check_if_same_color(target_piece) == False:
                        possible_moves.append(dest_coords)

        possible_moves = sorted(possible_moves)
        return possible_moves

    def get_possible_opponent_moves(self):
        possible_opponent_moves = []
        for piece in self.pieces_dict.values():
            if piece.color != self.color:
                possible_opponent_moves = set(possible_opponent_moves).union(piece.get_possible_moves())
        possible_opponent_moves = list(possible_opponent_moves)
        possible_opponent_moves = sorted(possible_opponent_moves)
        return possible_opponent_moves

    def check_if_mate(self):
        possible_moves = self.get_possible_moves()
        possible_opponent_moves = self.get_possible_opponent_moves()
        status = ''
        check = set([self.coords]).issubset(possible_opponent_moves)
        checkmate = set(possible_moves).issubset(possible_opponent_moves) and len(possible_moves) > 0
        
        if check and self.my_turn == True:
            status = 'check'
        elif check and self.my_turn == False:
            status = 'checkmate'
        if checkmate and self.my_turn == True:
            status = 'checkmate'
        return status

    def give_coords_get_piece(self, coords):
        for piece in self.pieces_dict.values():
            if piece.coords == coords:
                return piece

    def check_if_empty(self, dest_coords):
        piece = self.give_coords_get_piece(dest_coords)
        if piece:
            return False
        else:
            return True

    def check_if_same_color(self, target_piece):
        if self.color == target_piece.color:
            return True
        else:
            return False


class Knight():
    def __init__(self, start_pos, surface, pieces_dict, moves_history, start_coords, color):
        self.id = start_coords
        self.kind = 'knight'
        self.color = color
        self.surface = surface
        self.pieces_dict = pieces_dict
        img = pygame.image.load(f'{path}/{color}_{self.kind}.png').convert_alpha()
        img = pygame.transform.scale(img, square_size)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        self.coords = start_coords
        self.moves_history = moves_history
        self.moves = []
        self.my_turn = True if self.color == 'white' else False
        
    def update(self, pos=False, coords=False, move=False):
        if pos:
            self.rect.center = pos
        if coords:
            self.coords = coords
        if move:
            self.moves.append(move)

    def draw(self):
        self.surface.blit(self.image, self.rect)

    def get_pos(self):
        return self.rect.center

    def get_rect(self):
        return self.rect

    def get_possible_moves(self):
        possible_moves = []
        rank = self.coords[0]
        file = int(self.coords[1])
        ranks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        rank_index = ranks.index(rank)

        if (file <= 6):
            if (rank_index >= 1):
                dest_coords = f'{ranks[rank_index-1]}{file+2}'
                if self.check_if_empty(dest_coords) == True:
                    possible_moves.append(dest_coords)
                else:
                    target_piece = self.give_coords_get_piece(dest_coords)
                    if self.check_if_same_color(target_piece) == False:
                        possible_moves.append(dest_coords)
            if (rank_index <= 6):
                dest_coords = f'{ranks[rank_index+1]}{file+2}'
                if self.check_if_empty(dest_coords) == True:
                    possible_moves.append(dest_coords)
                else:
                    target_piece = self.give_coords_get_piece(dest_coords)
                    if self.check_if_same_color(target_piece) == False:
                        possible_moves.append(dest_coords)
        
        if (file >= 3):
            if (rank_index >= 1):
                dest_coords = f'{ranks[rank_index-1]}{file-2}'
                if self.check_if_empty(dest_coords) == True:
                    possible_moves.append(dest_coords)
                else:
                    target_piece = self.give_coords_get_piece(dest_coords)
                    if self.check_if_same_color(target_piece) == False:
                        possible_moves.append(dest_coords)
            if (rank_index <= 6):
                dest_coords = f'{ranks[rank_index+1]}{file-2}'
                if self.check_if_empty(dest_coords) == True:
                    possible_moves.append(dest_coords)
                else:
                    target_piece = self.give_coords_get_piece(dest_coords)
                    if self.check_if_same_color(target_piece) == False:
                        possible_moves.append(dest_coords)

        if (rank_index <= 5):
            if (file >= 2):
                dest_coords = f'{ranks[rank_index+2]}{file-1}'
                if self.check_if_empty(dest_coords) == True:
                    possible_moves.append(dest_coords)
                else:
                    target_piece = self.give_coords_get_piece(dest_coords)
                    if self.check_if_same_color(target_piece) == False:
                        possible_moves.append(dest_coords)
            if (file <= 7):
                dest_coords = f'{ranks[rank_index+2]}{file+1}'
                if self.check_if_empty(dest_coords) == True:
                    possible_moves.append(dest_coords)
                else:
                    target_piece = self.give_coords_get_piece(dest_coords)
                    if self.check_if_same_color(target_piece) == False:
                        possible_moves.append(dest_coords)

        if (rank_index >= 2):
            if (file >= 2):
                dest_coords = f'{ranks[rank_index-2]}{file-1}'
                if self.check_if_empty(dest_coords) == True:
                    possible_moves.append(dest_coords)
                else:
                    target_piece = self.give_coords_get_piece(dest_coords)
                    if self.check_if_same_color(target_piece) == False:
                        possible_moves.append(dest_coords)
            if (file <= 7):
                dest_coords = f'{ranks[rank_index-2]}{file+1}'
                if self.check_if_empty(dest_coords) == True:
                    possible_moves.append(dest_coords)
                else:
                    target_piece = self.give_coords_get_piece(dest_coords)
                    if self.check_if_same_color(target_piece) == False:
                        possible_moves.append(dest_coords)
        
        possible_moves = sorted(possible_moves)
        return possible_moves

    def give_coords_get_piece(self, coords):
        for piece in self.pieces_dict.values():
            if piece.coords == coords:
                return piece

    def check_if_empty(self, dest_coords):
        piece = self.give_coords_get_piece(dest_coords)
        if piece:
            return False
        else:
            return True

    def check_if_same_color(self, target_piece):
        if self.color == target_piece.color:
            return True
        else:
            return False


class Pawn():
    def __init__(self, start_pos, surface, pieces_dict, moves_history, start_coords, color):
        self.id = start_coords
        self.kind = 'pawn'
        self.color = color
        self.surface = surface
        self.pieces_dict = pieces_dict
        img = pygame.image.load(f'{path}/{color}_{self.kind}.png').convert_alpha()
        img = pygame.transform.scale(img, square_size)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        self.coords = start_coords
        self.moves_history = moves_history
        self.moves = []
        self.en_passant = False
        self.my_turn = True if self.color == 'white' else False
        
    def update(self, pos=False, coords=False, move=False):
        if pos:
            self.rect.center = pos
        if coords:
            self.coords = coords
        if move:
            self.moves.append(move)

    def draw(self):
        self.surface.blit(self.image, self.rect)

    def get_pos(self):
        return self.rect.center

    def get_rect(self):
        return self.rect

    def get_possible_moves(self):
        possible_moves = []
        rank = self.coords[0]
        file = int(self.coords[1])
        ranks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        rank_index = ranks.index(rank)
        inc = 1
        if self.color != 'white':
            inc *= -1
        
        if (self.color == 'white' and file != 8) or (self.color == 'black' and file != 1):
            dest_coords = f'{rank}{file+inc}'
            if self.check_if_empty(dest_coords) == True:
                possible_moves.append(dest_coords)
                if len(self.moves) < 1:
                    possible_moves.append(f'{rank}{file+2*inc}')
            if (rank_index != 0):
                dest_coords = f'{ranks[rank_index-1]}{file+inc}'
                if self.check_if_empty(dest_coords) == False:
                    target_piece = self.give_coords_get_piece(dest_coords)
                    if self.check_if_same_color(target_piece) == False:
                        possible_moves.append(dest_coords)
            if (rank_index != 7):
                dest_coords = f'{ranks[rank_index+1]}{file+inc}'
                if self.check_if_empty(dest_coords) == False:
                    target_piece = self.give_coords_get_piece(dest_coords)
                    if self.check_if_same_color(target_piece) == False:
                        possible_moves.append(dest_coords)
            if (rank_index != 0):
                left_coords = f'{ranks[rank_index-1]}{file}'
                if self.check_en_passant(left_coords) == True:
                    self.en_passant = True
                    dest_coords = f'{ranks[rank_index-1]}{file+inc}'
                    if self.check_if_empty(dest_coords) == True:
                        possible_moves.append(dest_coords)
            if (rank_index != 7):
                right_coords = f'{ranks[rank_index+1]}{file}'
                if self.check_en_passant(right_coords) == True:
                    self.en_passant = True
                    dest_coords = f'{ranks[rank_index+1]}{file+inc}'
                    if self.check_if_empty(dest_coords) == True:
                        possible_moves.append(dest_coords)

        possible_moves = sorted(possible_moves)
        return possible_moves

    def give_coords_get_piece(self, coords):
        for piece in self.pieces_dict.values():
            if piece.coords == coords:
                return piece
    
    def check_en_passant(self, coords):
        target_piece = self.give_coords_get_piece(coords)
        if target_piece:
            if self.check_if_same_color(target_piece) == False:
                if len(target_piece.moves) == 1 and target_piece.moves[-1]['index'] == self.moves_history[-1]['index']:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def perform_en_passant(self):
        letter = self.coords[0]
        num = int(self.coords[1])
        inc = -1
        if self.color != 'white':
            inc *= -1
        capture_coords = f'{letter}{num+inc}'
        return capture_coords

    def check_if_empty(self, dest_coords):
        piece = self.give_coords_get_piece(dest_coords)
        if piece:
            return False
        else:
            return True

    def check_if_same_color(self, target_piece):
        if self.color == target_piece.color:
            return True
        else:
            return False
    

class Queen():
    def __init__(self, start_pos, surface, pieces_dict, moves_history, start_coords, color):
        self.id = start_coords
        self.kind = 'queen'
        self.color = color
        self.surface = surface
        self.pieces_dict = pieces_dict
        img = pygame.image.load(f'{path}/{color}_{self.kind}.png').convert_alpha()
        img = pygame.transform.scale(img, square_size)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        self.coords = start_coords
        self.moves_history = moves_history
        self.moves = []
        self.my_turn = True if self.color == 'white' else False
        
    def update(self, pos=False, coords=False, move=False):
        if pos:
            self.rect.center = pos
        if coords:
            self.coords = coords
        if move:
            self.moves.append(move)

    def draw(self):
        self.surface.blit(self.image, self.rect)

    def get_pos(self):
        return self.rect.center

    def get_rect(self):
        return self.rect

    def get_possible_moves(self):
        possible_moves = []
        rank = self.coords[0]
        file = int(self.coords[1])
        ranks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        rank_index = ranks.index(rank)
        vertical_coords = []
        horizontal_coords = []

        for y in range(rank_index+1, 8):
            horizontal_coords.append(f'{ranks[y]}{file}')
            if(self.check_if_empty(f'{ranks[y]}{file}')==False):
                break
        for y in range(rank_index-1, -1, -1):
            horizontal_coords.append(f'{ranks[y]}{file}')
            if(self.check_if_empty(f'{ranks[y]}{file}')==False):
                break

        for x in range(file+1, 8+1):
            vertical_coords.append(f'{rank}{x}')
            if(self.check_if_empty(f'{rank}{x}')==False):
                break
        for x in range(file-1, 0, -1):
            vertical_coords.append(f'{rank}{x}')
            if(self.check_if_empty(f'{rank}{x}')==False):
                break

        right_coords = []
        left_coords = []
        y_asc = rank_index
        y_des = rank_index

        for x in range(file+1, 8+1):
            y_asc += 1
            if (y_asc <= 7):
                right_coords.append(f'{ranks[y_asc]}{x}')
                if(self.check_if_empty(f'{ranks[y_asc]}{x}')==False):
                    break
        for x in range(file+1, 8+1):       
            y_des -= 1
            if (y_des >= 0):
                right_coords.append(f'{ranks[y_des]}{x}')
                if(self.check_if_empty(f'{ranks[y_des]}{x}')==False):
                    break

        y_asc = rank_index
        y_des = rank_index
        for x in range(file-1, 0, -1):
            y_asc += 1
            if (y_asc <= 7):
                left_coords.append(f'{ranks[y_asc]}{x}')
                if(self.check_if_empty(f'{ranks[y_asc]}{x}')==False):
                    break
        for x in range(file-1, 0, -1):
            y_des -= 1
            if (y_des >= 0):
                left_coords.append(f'{ranks[y_des]}{x}')
                if(self.check_if_empty(f'{ranks[y_des]}{x}')==False):
                    break
        
        coords_list = horizontal_coords + vertical_coords + left_coords + right_coords

        for dest_coords in coords_list:
            if self.check_if_empty(dest_coords) == True:
                possible_moves.append(dest_coords)
            else:
                target_piece = self.give_coords_get_piece(dest_coords)
                if self.check_if_same_color(target_piece) == False:
                    possible_moves.append(dest_coords)

        possible_moves = sorted(possible_moves)
        return possible_moves

    def give_coords_get_piece(self, coords):
        for piece in self.pieces_dict.values():
            if piece.coords == coords:
                return piece

    def check_if_empty(self, dest_coords):
        piece = self.give_coords_get_piece(dest_coords)
        if piece:
            return False
        else:
            return True

    def check_if_same_color(self, target_piece):
        if self.color == target_piece.color:
            return True
        else:
            return False

class Rook():
    def __init__(self, start_pos, surface, pieces_dict, moves_history, start_coords, color):
        self.id = start_coords
        self.kind = 'rook'
        self.color = color
        self.surface = surface
        self.pieces_dict = pieces_dict
        img = pygame.image.load(f'{path}/{color}_{self.kind}.png').convert_alpha()
        img = pygame.transform.scale(img, square_size)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        self.coords = start_coords
        self.moves_history = moves_history
        self.moves = []
        self.my_turn = True if self.color == 'white' else False
        
    def update(self, pos=False, coords=False, move=False):
        if pos:
            self.rect.center = pos
        if coords:
            self.coords = coords
        if move:
            self.moves.append(move)

    def draw(self):
        self.surface.blit(self.image, self.rect)

    def get_pos(self):
        return self.rect.center

    def get_rect(self):
        return self.rect

    def get_possible_moves(self):
        possible_moves = []
        rank = self.coords[0]
        file = int(self.coords[1])
        ranks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        rank_index = ranks.index(rank)
        vertical_coords = []
        horizontal_coords = []

        for y in range(rank_index+1, 8):
            horizontal_coords.append(f'{ranks[y]}{file}')
            if(self.check_if_empty(f'{ranks[y]}{file}')==False):
                break
        for y in range(rank_index-1, -1, -1):
            horizontal_coords.append(f'{ranks[y]}{file}')
            if(self.check_if_empty(f'{ranks[y]}{file}')==False):
                break

        for x in range(file+1, 8+1):
            vertical_coords.append(f'{rank}{x}')
            if(self.check_if_empty(f'{rank}{x}')==False):
                break
        for x in range(file-1, 0, -1):
            vertical_coords.append(f'{rank}{x}')
            if(self.check_if_empty(f'{rank}{x}')==False):
                break

        coords_list = horizontal_coords + vertical_coords

        for dest_coords in coords_list:
            if self.check_if_empty(dest_coords) == True:
                possible_moves.append(dest_coords)
            else:
                target_piece = self.give_coords_get_piece(dest_coords)
                if self.check_if_same_color(target_piece) == False:
                    possible_moves.append(dest_coords)
        
        possible_moves = sorted(possible_moves)
        return possible_moves

    def give_coords_get_piece(self, coords):
        for piece in self.pieces_dict.values():
            if piece.coords == coords:
                return piece

    def check_if_empty(self, dest_coords):
        piece = self.give_coords_get_piece(dest_coords)
        if piece:
            return False
        else:
            return True

    def check_if_same_color(self, target_piece):
        if self.color == target_piece.color:
            return True
        else:
            return False