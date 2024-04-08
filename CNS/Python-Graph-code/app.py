from flask import Flask, render_template, request, jsonify
from maze import Maze

app = Flask(__name__)

WIDTH, HEIGHT = 1000, 1000
BLOCKSIZE = 40
WORLD = [[1 for _ in range(WIDTH // BLOCKSIZE)] for _ in range(HEIGHT // BLOCKSIZE)]

# Fixed walls at specific coordinates
fixed_walls = [(14,1), (14,3), (15,1), (15,3), (16,1), (17,1), (18,1), (14,4), (14,5), (14,6), (14,7), 
               (14,8), (14,9), (14,10), (14,11), (14,12), (16,5), (16,6), (16,7), (16,8), (16,9), (16,10), 
               (16,11), (16,12), (17,5), (17,6), (17,7), (17,8), (17,9), (17,10),(17,11), (17,12),(1,16),
               (1,17),(1,18),(1,19),(1,20),(3,16),(3,19),(3,20),(4,15),(4,16),(5,15),(6,15),(6,16),(7,15),
               (7,18),(7,21),(8,15),(8,17),(8,18),(8,21),(4,21),(14,19),(14,20),(14,21),(14,18),(13,21),
               (21,15),(21,16),(21,17),(21,18),(21,19),(21,20),(12,23),(13,23),(14,23),(15,23),(16,23),(17,23),
               (18,23),(21,14),(9,15),(9,17),(9,18),(9,21),(10,15),(10,17),(10,18),(10,21),(11,15),(11,17),
               (11,18),(11,21),(12,15),(12,17),(12,18),(12,21),(14,2),(17,3),(18,3),(19,2),(19,1),(20,2),(19,3),
               (19,4),(19,5),(19,6),(19,7),(19,8),(19,9),(19,10),(19,11),(19,12),(19,13),(19,14),(19,15),(14,13), 
               (14,14),(15,14),(15,15),(17,15),(18,15),(1,15),(2,15),(3,15),(1,21),(2,21),(3,21)]

for wall in fixed_walls:
    i, j = wall
    WORLD[i][j] = 0  

start, end = None, None
operation = "SET_START"

@app.route('/')
def index():
    global start, end
    start, end = None, None
    return render_template('index.html', WIDTH=WIDTH, HEIGHT=HEIGHT, BLOCKSIZE=BLOCKSIZE, WORLD=WORLD)


@app.route('/update_world', methods=['POST'])
def update_world():
    global WORLD, start, end, operation

    data = request.get_json()

    if data['type'] == 'SET_START':
        i, j = data['i'], data['j']
        if WORLD[i][j] == 1:
            WORLD[i][j] = "s"
            start = j + i * (HEIGHT // BLOCKSIZE)
            operation = "SET_DESTINATION"

    elif data['type'] == 'SET_DESTINATION':
        i, j = data['i'], data['j']
        if WORLD[i][j] != "s" and WORLD[i][j] == 1:
            WORLD[i][j] = "d"
            end = j + i * (HEIGHT // BLOCKSIZE)
            operation = "SET_OBSTACLE"

    elif data['type'] == 'SET_OBSTACLE':
        i, j = data['i'], data['j']
        if WORLD[i][j] != "s" and WORLD[i][j] != "d" and WORLD[i][j] == 1:
            WORLD[i][j] = 0

    return jsonify({'success': True, 'WORLD': WORLD, 'WIDTH': WIDTH, 'HEIGHT': HEIGHT, 'BLOCKSIZE': BLOCKSIZE})


@app.route('/find_shortest_path', methods=['POST'])
def find_shortest_path():
    global WORLD, start, end

    if start is not None and end is not None:
        maze = Maze(WORLD)
        shortest_path, directions = maze.shortest_path(start, end)
        WORLD = shortest_path

    return jsonify({'success': True, 'WORLD': WORLD, 'WIDTH': WIDTH, 'HEIGHT': HEIGHT, 'BLOCKSIZE': BLOCKSIZE, 'directions': directions})


if __name__ == '__main__':
    app.run(debug=True)
