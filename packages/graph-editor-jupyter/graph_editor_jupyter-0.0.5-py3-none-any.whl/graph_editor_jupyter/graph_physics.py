import random
import pymunk

from .settings import NODE_RADIUS
from .visual_graph import VisualGraph
from .fancy_drawing import get_tutte_embedding
from enum import Enum
VERTEX_BODY_MASS = 1
VERTEX_BODY_MOMENT = 1
WALLS_WIDTH = 10
GRAVITY = (0, 0)

class DrawingMode(Enum):
    GRAVITY_ON = 0
    GRAVITY_OFF = 1
    TUTTE_NOT_DRAWN = 2
    TUTTE_DRAWN = 3

def create_border(space, bounds: (int, int)):
    width, height = bounds
    ground = pymunk.Segment(space.static_body, (0, -WALLS_WIDTH), (width, -WALLS_WIDTH), WALLS_WIDTH)
    ground.friction = 1.0
    space.add(ground)
    ceiling = pymunk.Segment(space.static_body, (0, height + WALLS_WIDTH), (width, height + WALLS_WIDTH), WALLS_WIDTH)
    ceiling.friction = 1.0
    space.add(ceiling)
    left_wall = pymunk.Segment(space.static_body, (-WALLS_WIDTH, 0), (-WALLS_WIDTH, height), WALLS_WIDTH)
    left_wall.friction = 1.0
    space.add(left_wall)
    right_wall = pymunk.Segment(space.static_body, (width + WALLS_WIDTH, 0), (width + WALLS_WIDTH, height), WALLS_WIDTH)
    right_wall.friction = 1.0
    space.add(right_wall)


class GraphPhysics:
    def __init__(self, visual_graph: VisualGraph):
        self.visual_graph = visual_graph
        self.space = pymunk.Space()
        create_border(self.space, visual_graph.bounds)
        self.space.gravity = (0, 0)
        self.vertex_body: dict[any, pymunk.Body] = {}
        self.edge_body: dict[any, pymunk.Body] = {}
        self.connection_body = {}
        
        width, height = visual_graph.bounds
        self.center_pos = (width / 2, height / 2)
        
        for node in visual_graph.graph.nodes:
            offset = (random.uniform(-10, 10), random.uniform(-10, 10))
            initial_pos = (self.center_pos[0] + offset[0], self.center_pos[1] + offset[1])
            self.add_vert(node, initial_pos)
            
        for edge in visual_graph.graph.edges:
            self.add_edge(edge[0], edge[1])
        
        visual_graph.add_node.subscribable.subscribe(self.add_vert)
        visual_graph.remove_node.subscribable.subscribe(self.remove_vert)
        visual_graph.add_edge.subscribable.subscribe(self.add_edge)
        visual_graph.remove_edge.subscribable.subscribe(self.remove_edge)
        visual_graph.move_node.subscribable.subscribe(self.move_node)

        visual_graph.drag_start.subscribable.subscribe(self.drag_start)
        visual_graph.drag_end.subscribable.subscribe(self.drag_end)

    def drag_start(self, node):
        self.vertex_body[node].body_type = pymunk.Body.STATIC

    def drag_end(self):
        node = self.visual_graph.dragged_node
        if node is not None:
            self.vertex_body[node].body_type = pymunk.Body.DYNAMIC
            self.vertex_body[node].mass = VERTEX_BODY_MASS
            self.vertex_body[node].moment = VERTEX_BODY_MOMENT

    def add_vert(self, node, pos: (int, int)):
        body = pymunk.Body(VERTEX_BODY_MASS, VERTEX_BODY_MOMENT)
        body.position = pos
        body.damping = 0.5
        
        shape = pymunk.Circle(body, radius=10)  # Adjust the radius as needed
        shape.elasticity = 1.0  # Elasticity of collisions
        shape.friction = 0.0  # Friction of collisions
        self.space.add(body, shape)
        self.vertex_body[node] = body
        self.edge_body[node] = {}
        self.connection_body[node] = {}
        for node1, body1 in self.vertex_body.items():
            if node1 != node:
                connection_body = pymunk.DampedSpring(body, body1, (0, 0), (0, 0), rest_length=200, stiffness=10,
                                                      damping=2)
                self.space.add(connection_body)
                self.connection_body[node][node1] = connection_body
                self.connection_body[node1][node] = connection_body

    def remove_vert(self, node):
        self.space.remove(self.vertex_body[node])
        del self.vertex_body[node]
        for other in self.edge_body[node]:  
            self.space.remove(self.edge_body[node][other])
            del self.edge_body[other][node]
        for other in self.connection_body[node]:
            self.space.remove(self.connection_body[node][other])
            del self.connection_body[other][node]
        del self.edge_body[node]
        del self.connection_body[node]

    def add_edge(self, node1, node2):
        edge_body = pymunk.DampedSpring(self.vertex_body[node1], self.vertex_body[node2], (0, 0), (0, 0),
                                        rest_length=100, stiffness=500, damping=2)
        self.space.add(edge_body)
        self.edge_body[node1][node2] = edge_body
        self.edge_body[node2][node1] = edge_body

    def remove_edge(self, node1, node2):
        body = self.edge_body[node1][node2]
        self.space.remove(body)
        del self.edge_body[node1][node2]
        del self.edge_body[node2][node1]

    def move_node(self, node, pos: (int, int)):
        self.vertex_body[node].position = pos

    def update_physics(self, dt, drawing_mode):
        
        if drawing_mode==DrawingMode.GRAVITY_ON:
            for node, body in self.vertex_body.items():
                resistance = 7.0
                velocity = body.velocity
                resistance_force = -resistance * velocity
                body.apply_force_at_local_point(resistance_force, (0, 0))
                
            self.space.step(dt)
            
            for node, body in self.vertex_body.items():
                self.visual_graph.move_node(node, [body.position.x, body.position.y])
            self.normalize_positions()

        elif drawing_mode==DrawingMode.TUTTE_NOT_DRAWN:
            positions = get_tutte_embedding(self.visual_graph.graph)
            for node in self.visual_graph.graph.nodes:
                width, height = self.visual_graph.bounds
                pos_x=(positions[node][0]+1)/2*width
                pos_y=(positions[node][1]+1)/2*height
                self.visual_graph.move_node(node, [pos_x, pos_y])

    def normalize_positions(self):
        for node, node_pos in self.visual_graph.coordinates.items():
            if node_pos[0] < 0:
                self.visual_graph.move_node(node, [NODE_RADIUS + 10, node_pos[1]])
                self.vertex_body[node].velocity = [0, 0]
            if node_pos[1] < 0:
                self.visual_graph.move_node(node, [node_pos[0], NODE_RADIUS + 10])
                self.vertex_body[node].velocity = [0, 0]
            if node_pos[0] > self.visual_graph.bounds[0]:
                self.visual_graph.move_node(node, [self.visual_graph.bounds[0] - NODE_RADIUS - 10, node_pos[1]])
                self.vertex_body[node].velocity = [0, 0]
            if node_pos[1] > self.visual_graph.bounds[1]:
                self.visual_graph.move_node(node, [node_pos[0], self.visual_graph.bounds[1] - NODE_RADIUS - 10])
                self.vertex_body[node].velocity = [0, 0]
