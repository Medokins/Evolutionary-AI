level_map = [
'                                ',
'                                ',
'                                ',
'                                ',
'                                ',
'                                ',
'          XXXXXX                ',
'                                ',
'                                ',
'                      X         ',
'                      XXXXX   XX',
'                      XXXX     X',
'     X    XXXXXXXXX   XXX       ',
'    XX                XX        ',
'   XXX                X         ',
'  XXXX                X         ',
' XXXXX                X         ',
'XXXXXX                X         ']

tile_size = 1080 / len(level_map)
print(tile_size)
WIDTH, HEIGHT = 1920, 1080
FPS = 60
JUMP_HEIGHT_MAX = 3
PLAYER_SIZE = (128,128)