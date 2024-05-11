import pygame
import asyncio
import json
from pieces import Bishop, King, Knight, Pawn, Queen, Rook

import google.generativeai as genai

GOOGLE_API_KEY = "MY_API_KEY"
genai.configure(api_key=GOOGLE_API_KEY)
generation_config = {
    "candidate_count": 1,
    "temperature": 0,
}
safety_settings = {
    "HARASSMENT": "BLOCK_NONE",
    "HATE": "BLOCK_NONE",
    "SEXUAL": "BLOCK_NONE",
    "DANGEROUS": "BLOCK_NONE",
}
model = genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_config, safety_settings=safety_settings)
chat = model.start_chat(history=[])

async def make_initial_prompt():
    prompt = """Let's play chess! I'm going to be White and you're going to be Black. Since I'm White, I go first. I'm going to move a white piece on the chess board, then I'm going to describe to you my move in long algebraic notation, that is, the starting and ending coordinates separated by a hyphen (e.g. Nf3-Nf6), and nothing else (this is very important). We will call this a move prompt.

    Move prompts always have the starting and ending coordinates. If they lack any of these, they are invalid.

    If I make a move prompt, that means I have made a move and you may only reply with another move prompt. If I make any other kind of prompt, that means I have not made a move, and you may not reply with another move prompt. After I make a move, it's your turn. In your turn, you are going to describe to me the move you want to make with a move prompt, and I'm going to move the piece on the board for you. Then it's my turn again, and so on until the game ends.  The game only begins when I make my first move prompt. After this initial prompt, stand by until I make my first move prompt.

    When the game begins, the pieces are in their respective starting coordinates. A piece may only be moved from its current coordinate (thus it'd make no sense for your first move to be Nf3-Nc6 because f3 is not a starting coordinate for a black knight). The starting coordinates for all the piece are as follows:

    {'whites': ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2', 'e1', 'd1', 'c1', 'f1', 'b1', 'g1', 'a1', 'h1'], 'blacks': ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7', 'e8', 'd8', 'c8', 'f8', 'b8', 'g8', 'a8', 'h8']}

    Whenever you make a move that is not valid, I will send a prompt with the string "Invalid move" and the updated positions of the pieces. Whenever you receive a prompt starting with "Invalid move" you must reacess the current positions of the pieces and remake your move, then respond with a move prompt and with a move prompt only.

    Again, you may only move the black pieces.

    Only I can say when a move is valid or not. When prompted with a move prompt, you can only respond with another move prompt.

    When there's a capture, an "x" is placed between the starting and ending coordinates instead of the hyphen (e.g. Rd3xd7). A captured piece may not be moved again for the remainder of the match.

    Example:
    Me:
    Let's play chess!
    You: 
    Sounds like fun! You go first.
    Me:
    e2-e4
    You:
    e7-e5
    Me:
    How are you doing?
    You: 
    I'm fine and you?
    Me:
    d2-d4
    You:
    e5xd4
    Me:
    How are you doing?
    You: 
    I'm fine and you?
    Me:
    d2-d4
    You:
    e5xd4"""

    response = await chat.send_message_async(prompt)
    return response

async def prompt_gemini_async(prompt):
    response = await chat.send_message_async(prompt)
    return response

def prompt_gemini(prompt):
    print('Me: ', prompt)
    response = chat.send_message(prompt)
    return response

pygame.init()
response = asyncio.run(make_initial_prompt())
# print(response.text)

clock = pygame.time.Clock()
fps = 60

# define game variables
mouse_down = False
game_state = 'start'
current_player = 'white'
players = ['black', 'white']
player_index = 1
white = True
# take_screenshot_flag = False

# game window
square_side = 64
square_size = (square_side, square_side)
screen_width = 8*square_side
screen_height = 8*square_side
board = pygame.Rect(0, 0, screen_width, screen_height)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Board')

# function for drawing the board
def draw_board():
    val = 1
    for y in range(0, screen_height, square_side):
        val = 1 - val
        for x in range(0, screen_width, square_side):
            val = 1 - val
            draw_rect(x, y, val, 'wood')

def draw_rect(x, y, val, palette):
    black = (0, 0, 0)
    white = (255, 255, 255)
    dark = (93, 41, 6) # HEX: #5d2906
    light = (212, 187, 126) # HEX: #d4bb7e
    bw = [black, white]
    wood = [dark, light]
    colors_dict = {'bw': bw, 'wood': wood}
    colors = colors_dict[palette]
    rect = pygame.Rect(x, y, square_side, square_side)
    pygame.draw.rect(screen, colors[val], rect)
    return rect

# function for setting up the coordinates
letters_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
coords_dict = {}
def draw_board_once():
    val = 1
    j = 8
    for y in range(0, screen_height, square_side):
        val = 1 - val
        i = 0
        for x in range(0, screen_width, square_side):
            val = 1 - val
            rect = draw_rect(x, y, val, 'wood')
            coords = f'{letters_list[i]}{j}'
            coords_dict[coords] = rect
            i += 1
        j -= 1

draw_board_once()

def take_screenshot(screen, filename):
  """Takes a screenshot of the Pygame surface and saves it as the filename."""
  screenshot = pygame.Surface.copy(screen)  
  pygame.image.save(screenshot, filename)

def draw_warning():
    global game_state
    str = game_state
    str = f'{str[0].upper()}{str[1:]}'
    font = pygame.font.SysFont(None, 25)
    text = font.render(str, True, (255,255,255), (255,0,0))
    screen.blit(text, board)

def game_over():
    draw_warning()
    font = pygame.font.SysFont(None, 25)
    text = font.render('Game over', True, (255,255,255), (0,0,0))
    text_rect = text.get_rect()
    text_rect.center = board.center
    screen.blit(text, text_rect)

def check_if_move_is_inside_board(pos):
    return board.collidepoint(pos)

def check_if_move_is_possible(coords, possible_moves):
    return coords in possible_moves

def lock_piece_in_square(pos):
    for key in coords_dict:
        rect = coords_dict[key]
        if rect.collidepoint(pos) == True:
            return rect.center, key
    return pos

def get_rect_given_pos(pos):
    for coords in coords_dict.keys():
        rect = coords_dict[coords]
        if rect.collidepoint(pos) == True:
            return rect

def get_coords_given_pos(pos):
    for coords in coords_dict.keys():
        rect = coords_dict[coords]
        if rect.collidepoint(pos) == True:
            return coords

def get_center_given_coords(coords):
    if len(coords) > 2:
        coords = coords[-2:]
    rect = coords_dict[coords]
    return rect.center

def get_piece_given_coords(coords):
    if len(coords) > 2:
        coords = coords[-2:]
    for piece in pieces_dict.values():
        if piece.coords == coords:
            return piece

def check_if_square_is_empty(dest_coords):
    piece = get_piece_given_coords(dest_coords)
    if piece:
        return False
    else:
        return True

def check_if_piece_is_the_same_color(this_piece, target_piece):
    if this_piece.color == target_piece.color:
        return True
    else:
        return False
    
def get_coords_from_response(response_text):
    if "-" in response_text:
        separator = "-"
    elif "x" in response_text:
        separator = "x"
    else:
        return response_text, None

    depart_coords, dest_coords = response_text.split(separator)
    return depart_coords, dest_coords
    
def move_opponent_piece(response_text, attempt):
    try:
        max_retry = 4
        print("Gemini: ", response_text)
        depart_coords, dest_coords = get_coords_from_response(response_text)
        if (not dest_coords):
            if (attempt < max_retry):
                attempt = attempt + 1
                prompt = f'Please reply with a move prompt'
                response = prompt_gemini(prompt)
                move_opponent_piece(response.text, attempt)
            else:
                print("Please move the black piece manually to proceed.")

        # depart_pos = give_coords_get_center(depart_coords)
        dest_pos = get_center_given_coords(dest_coords)
        piece = get_piece_given_coords(depart_coords)
        if (piece):
            possible_moves = piece.get_possible_moves()
            if check_if_move_is_possible(dest_coords, possible_moves) == True:
                if check_if_square_is_empty(dest_coords) == True:
                    piece.update(dest_pos, dest_coords)
                    update_coords()
                    if piece.kind == 'pawn':
                        if piece.en_passant == True:
                            capture_coords = piece.perform_en_passant()
                            target_piece = get_piece_given_coords(capture_coords)
                            if target_piece:
                                if check_if_piece_is_the_same_color(piece, target_piece) == False:
                                    del pieces_dict[target_piece.id]
                                    move = update_history(piece, True, depart_coords, dest_coords, True)
                                    piece.update(move=move)
                                    piece.en_passant == False
                        else:
                            move = update_history(piece, False, depart_coords, dest_coords)
                            piece.update(move=move)
                    else:
                        move = update_history(piece, False, depart_coords, dest_coords)
                        piece.update(move=move)
                    
                    end_turn()
                    update_game_state()
                else:
                    target_piece = get_piece_given_coords(dest_coords)
                    if target_piece:
                        if check_if_piece_is_the_same_color(piece, target_piece) == True:
                            piece.update(depart_pos)
                            if (attempt < max_retry):
                                attempt = attempt + 1
                                prompt = f'Invalid move' + f'\nCurrent positions: {json.dumps(current_coords)}.\nPlease reply with a move prompt'
                                response = prompt_gemini(prompt)
                                move_opponent_piece(response.text, attempt)
                            else:
                                print("Please move the black piece manually to proceed.")
                        else:
                            del pieces_dict[target_piece.id]
                            move = update_history(piece, True, depart_coords, dest_coords)
                            piece.update(dest_pos, dest_coords, move)
                            update_coords()

                            end_turn()
                            update_game_state()
        else:
            if (attempt < max_retry):
                attempt = attempt + 1
                prompt = f'Invalid move' + f'\nCurrent positions: {json.dumps(current_coords)}.\nPlease reply with a move prompt'
                response = prompt_gemini(prompt)
                move_opponent_piece(response.text, attempt)
            else:
                print("Please move the black piece manually to proceed.")
    except:
        print("There was an exception. Please move the black piece manually to proceed.")

current_coords = {}
def update_coords():
    global current_coords
    whites = []
    blacks = []
    for piece in pieces_dict.values():
        if(piece.coords):
            if (piece.color == "white"):
                whites.append(piece.coords)
            else:
                blacks.append(piece.coords)
            
    current_coords['whites'] = whites
    current_coords['blacks'] = blacks

moves_history = []
move_index = 1
def update_history(piece, capture, depart_coords, dest_coords, en_passant=False):
    global moves_history, move_index
    p = piece.kind[0].upper() if piece.kind != 'pawn' else ''
    x = 'x' if capture else '-'
    ep = ' e.p.' if en_passant else ''
    algebraic_notation = f'{p}{depart_coords}{x}{dest_coords}{ep}'
    move = {
        'index': move_index,
        'piece': piece.kind,
        'capture': capture,
        'from': depart_coords,
        'to': dest_coords,
        'en_passant': en_passant,
        'algebraic_notation': algebraic_notation
    }
    move_index += 1
    moves_history.append(move)
    return move

# set up the pieces
pieces_dict = {}
kings_list = []
for i in range(0, 8):
    start_coords = f'{letters_list[i]}2'
    start_pos = get_center_given_coords(start_coords)
    pieces_dict[start_coords] = Pawn(start_pos, screen, pieces_dict, moves_history, start_coords, 'white')
    start_coords = f'{letters_list[i]}7'
    start_pos = get_center_given_coords(start_coords)
    pieces_dict[start_coords] = Pawn(start_pos, screen, pieces_dict, moves_history, start_coords, 'black')

start_coords = f'e1'
start_pos = get_center_given_coords(start_coords)
pieces_dict[start_coords] = King(start_pos, screen, pieces_dict, moves_history, start_coords, 'white')
kings_list.append(pieces_dict[start_coords])
start_coords = f'e8'
start_pos = get_center_given_coords(start_coords)
pieces_dict[start_coords] = King(start_pos, screen, pieces_dict, moves_history, start_coords, 'black')
kings_list.append(pieces_dict[start_coords])

start_coords = f'd1'
start_pos = get_center_given_coords(start_coords)
pieces_dict[start_coords] = Queen(start_pos, screen, pieces_dict, moves_history, start_coords, 'white')
start_coords = f'd8'
start_pos = get_center_given_coords(start_coords)
pieces_dict[start_coords] = Queen(start_pos, screen, pieces_dict, moves_history, start_coords, 'black')

start_coords = f'c1'
start_pos = get_center_given_coords(start_coords)
pieces_dict[start_coords] = Bishop(start_pos, screen, pieces_dict, moves_history, start_coords, 'white')
start_coords = f'f1'
start_pos = get_center_given_coords(start_coords)
pieces_dict[start_coords] = Bishop(start_pos, screen, pieces_dict, moves_history, start_coords, 'white')
start_coords = f'c8'
start_pos = get_center_given_coords(start_coords)
pieces_dict[start_coords] = Bishop(start_pos, screen, pieces_dict, moves_history, start_coords, 'black')
start_coords = f'f8'
start_pos = get_center_given_coords(start_coords)
pieces_dict[start_coords] = Bishop(start_pos, screen, pieces_dict, moves_history, start_coords, 'black')

start_coords = f'b1'
start_pos = get_center_given_coords(start_coords)
pieces_dict[start_coords] = Knight(start_pos, screen, pieces_dict, moves_history, start_coords, 'white')
start_coords = f'g1'
start_pos = get_center_given_coords(start_coords)
pieces_dict[start_coords] = Knight(start_pos, screen, pieces_dict, moves_history, start_coords, 'white')
start_coords = f'b8'
start_pos = get_center_given_coords(start_coords)
pieces_dict[start_coords] = Knight(start_pos, screen, pieces_dict, moves_history, start_coords, 'black')
start_coords = f'g8'
start_pos = get_center_given_coords(start_coords)
pieces_dict[start_coords] = Knight(start_pos, screen, pieces_dict, moves_history, start_coords, 'black')

start_coords = f'a1'
start_pos = get_center_given_coords(start_coords)
pieces_dict[start_coords] = Rook(start_pos, screen, pieces_dict, moves_history, start_coords, 'white')
start_coords = f'h1'
start_pos = get_center_given_coords(start_coords)
pieces_dict[start_coords] = Rook(start_pos, screen, pieces_dict, moves_history, start_coords, 'white')
start_coords = f'a8'
start_pos = get_center_given_coords(start_coords)
pieces_dict[start_coords] = Rook(start_pos, screen, pieces_dict, moves_history, start_coords, 'black')
start_coords = f'h8'
start_pos = get_center_given_coords(start_coords)
pieces_dict[start_coords] = Rook(start_pos, screen, pieces_dict, moves_history, start_coords, 'black')

def draw_pieces():
    for piece in pieces_dict.values():
        piece.draw()

def draw_current_player():
    str = "White" if white else "Black"
    font = pygame.font.SysFont(None, 25)
    text = font.render(str, True, (255,255,255), (0,0,0))
    screen.blit(text, (0, screen_height-16))

def end_turn():
    global white
    white = not white
    for piece in pieces_dict.values():
        piece.my_turn = not piece.my_turn

def update_game_state():
    global game_state
    for king in kings_list:
        status = king.check_if_mate()
        game_state = status

run = True

while run:

    clock.tick(fps)

    draw_board()
    draw_pieces()
    draw_current_player()
    if game_state == 'check':
        draw_warning()
    elif game_state == 'checkmate':
        # game_over()
        draw_warning()

    if game_state != 'checkmate':
        if mouse_down == True:
            pos = pygame.mouse.get_pos()
            if piece and piece.my_turn:
                rect = piece.get_rect()
                if rect.collidepoint(pos) == True:
                    piece.update(pos)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                take_screenshot(screen, "screenshot.png")
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
                pos = pygame.mouse.get_pos()
                coords = get_coords_given_pos(pos)
                piece = get_piece_given_coords(coords)
                if piece and piece.my_turn:
                    possible_moves = piece.get_possible_moves()
                    rect = piece.get_rect()
                    if rect.collidepoint(pos) == True:
                        depart_pos = rect.center
                        depart_coords = piece.coords
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
                if piece and piece.my_turn:
                    dest_pos, dest_coords = lock_piece_in_square(pos)
                    if check_if_move_is_possible(dest_coords, possible_moves) == True:
                        if check_if_square_is_empty(dest_coords) == True:
                            piece.update(dest_pos, dest_coords)
                            update_coords()
                            if piece.kind == 'pawn':
                                if piece.en_passant == True:
                                    capture_coords = piece.perform_en_passant()
                                    target_piece = get_piece_given_coords(capture_coords)
                                    if target_piece:
                                        if check_if_piece_is_the_same_color(piece, target_piece) == False:
                                            del pieces_dict[target_piece.id]
                                            move = update_history(piece, True, depart_coords, dest_coords, True)
                                            piece.update(move=move)
                                            piece.en_passant == False
                                else:
                                    move = update_history(piece, False, depart_coords, dest_coords)
                                    piece.update(move=move)
                            else:
                                move = update_history(piece, False, depart_coords, dest_coords)
                                piece.update(move=move)
                            
                            end_turn()
                            update_game_state()

                            if piece.color == 'white':
                                response = prompt_gemini(move['algebraic_notation'])
                                move_opponent_piece(response.text, 1)

                        else:
                            target_piece = get_piece_given_coords(dest_coords)
                            if target_piece:
                                if check_if_piece_is_the_same_color(piece, target_piece) == True:
                                    piece.update(depart_pos)
                                else:
                                    del pieces_dict[target_piece.id]
                                    move = update_history(piece, True, depart_coords, dest_coords)
                                    piece.update(dest_pos, dest_coords, move)
                                    update_coords()
                                    end_turn()
                                    update_game_state()
                                    
                                    if piece.color == 'white':
                                        response = prompt_gemini(move['algebraic_notation'])
                                        move_opponent_piece(response.text, 1)
                    else:
                        piece.update(depart_pos)
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
    pygame.display.update()

pygame.quit()