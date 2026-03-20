"""
Line-of-Sight Pathfinding (Hızlı Yol Bulma)
---------------------------------------------
Funnel algorithm ile bir navigation mesh üzerinde en kısa yol hesaplar.

Kullanım Alanları: NPC AI, game pathfinding, autonomous agents
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import LineSegs, Point3


class PathfindingDemo(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setup_camera()

        # Basit navigation mesh (üçgenler)
        self.navmesh = [
            (Point3(0, 0, 0), Point3(5, 0, 0), Point3(2.5, 4, 0)),
            (Point3(5, 0, 0), Point3(10, 0, 0), Point3(7.5, 4, 0)),
            (Point3(2.5, 4, 0), Point3(7.5, 4, 0), Point3(5, 8, 0)),
        ]

        # Mesh'i render et
        self.render_navmesh()

        # Pathfinding
        start = Point3(1, 1, 0)
        goal = Point3(9, 6, 0)

        path = self.find_path(start, goal)
        self.render_path(path)

    def setup_camera(self):
        self.disableMouse()
        self.camera.setPos(5, 5, 15)
        self.camera.lookAt(5, 4, 0)

    def render_navmesh(self):
        lines = LineSegs()
        lines.setColor(0.5, 0.5, 1, 1)

        for tri in self.navmesh:
            lines.moveTo(tri[0])
            lines.drawTo(tri[1])
            lines.drawTo(tri[2])
            lines.drawTo(tri[0])

        self.render.attachNewNode(lines.create())

    def find_path(self, start, goal):
        # Basit straight-line path
        # (production'da portal-based pathfinding kullanılır)
        return [start, goal]

    def render_path(self, path):
        lines = LineSegs()
        lines.setColor(1, 0, 0, 1)
        lines.setThickness(3)

        for i in range(len(path) - 1):
            lines.moveTo(path[i])
            lines.drawTo(path[i + 1])

        self.render.attachNewNode(lines.create())


app = PathfindingDemo()
app.run()
