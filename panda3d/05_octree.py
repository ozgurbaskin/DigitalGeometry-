"""
Octree Spatial Partitioning (Hızlı Mekan Arama)
-------------------------------------------------
3D space'i recursive olarak bölerek collision detection ve frustum culling hızlandırır.

Kullanım Alanları: Spatial indexing, collision detection, frustum culling, level-of-detail rendering
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import LineSegs, Point3
import numpy as np


class OctreeNode:
    def __init__(self, bounds, depth=0, max_depth=3):
        self.bounds = bounds
        self.depth = depth
        self.max_depth = max_depth
        self.objects = []
        self.children = None

    def insert(self, pos, obj_id):
        if self.depth < self.max_depth and len(self.objects) > 2:
            if self.children is None:
                self.subdivide()

            for child in self.children:
                if self.point_in_bounds(pos, child.bounds):
                    child.insert(pos, obj_id)
                    return

        self.objects.append((pos, obj_id))

    def subdivide(self):
        min_p, max_p = self.bounds
        mid = (min_p + max_p) * 0.5

        self.children = []
        for i in range(8):
            new_min = Point3(
                min_p[0] if i & 1 == 0 else mid[0],
                min_p[1] if i & 2 == 0 else mid[1],
                min_p[2] if i & 4 == 0 else mid[2],
            )
            new_max = Point3(
                mid[0] if i & 1 == 0 else max_p[0],
                mid[1] if i & 2 == 0 else max_p[1],
                mid[2] if i & 4 == 0 else max_p[2],
            )
            self.children.append(
                OctreeNode((new_min, new_max), self.depth + 1, self.max_depth)
            )

    def query_range(self, pos, radius):
        result = []

        for obj_pos, obj_id in self.objects:
            if np.linalg.norm(np.array(obj_pos) - np.array(pos)) <= radius:
                result.append(obj_id)

        if self.children:
            for child in self.children:
                if self.sphere_intersects_bounds(pos, radius, child.bounds):
                    result.extend(child.query_range(pos, radius))

        return result

    @staticmethod
    def point_in_bounds(pos, bounds):
        min_p, max_p = bounds
        return (min_p[0] <= pos[0] <= max_p[0] and
                min_p[1] <= pos[1] <= max_p[1] and
                min_p[2] <= pos[2] <= max_p[2])

    @staticmethod
    def sphere_intersects_bounds(pos, radius, bounds):
        min_p, max_p = bounds
        closest = np.array([
            np.clip(pos[0], min_p[0], max_p[0]),
            np.clip(pos[1], min_p[1], max_p[1]),
            np.clip(pos[2], min_p[2], max_p[2])
        ])
        return np.linalg.norm(np.array(pos) - closest) <= radius


class Octree:
    def __init__(self, bounds, max_depth=3):
        self.root = OctreeNode(bounds, max_depth=max_depth)

    def insert(self, pos, obj_id):
        self.root.insert(pos, obj_id)

    def query_range(self, pos, radius):
        return self.root.query_range(pos, radius)


class OctreeDemo(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setup_camera()

        # Octree oluştur
        bounds = (Point3(-10, -10, -10), Point3(10, 10, 10))
        self.octree = Octree(bounds, max_depth=3)

        # Random objects ekle
        np.random.seed(42)
        objects = [(np.random.uniform(-9, 9, 3), i) for i in range(15)]

        for pos, obj_id in objects:
            self.octree.insert(pos, obj_id)

        # Octree'yi visualize et
        self.visualize_octree()

        # Query example
        query_pos = Point3(0, 0, 0)
        query_radius = 5
        nearby = self.octree.query_range(query_pos, query_radius)
        print(f"Nearby objects: {nearby}")

    def setup_camera(self):
        self.disableMouse()
        self.camera.setPos(15, 15, 15)
        self.camera.lookAt(0, 0, 0)

    def visualize_octree(self):
        lines = LineSegs()
        lines.setColor(0, 1, 0, 1)
        self.draw_octree_bounds(self.octree.root, lines)
        self.render.attachNewNode(lines.create())

    def draw_octree_bounds(self, node, lines):
        if node is None:
            return

        min_p, max_p = node.bounds

        corners = [
            Point3(min_p[0], min_p[1], min_p[2]),
            Point3(max_p[0], min_p[1], min_p[2]),
            Point3(max_p[0], max_p[1], min_p[2]),
            Point3(min_p[0], max_p[1], min_p[2]),
            Point3(min_p[0], min_p[1], max_p[2]),
            Point3(max_p[0], min_p[1], max_p[2]),
            Point3(max_p[0], max_p[1], max_p[2]),
            Point3(min_p[0], max_p[1], max_p[2]),
        ]

        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]

        for a, b in edges:
            lines.moveTo(corners[a])
            lines.drawTo(corners[b])

        if node.children:
            for child in node.children:
                self.draw_octree_bounds(child, lines)


app = OctreeDemo()
app.run()
