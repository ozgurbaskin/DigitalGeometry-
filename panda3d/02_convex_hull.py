"""
Convex Hull (Dışbükey Zarf)
----------------------------
Bir nokta setini çevreleyen en küçük dışbükey polihedron bulur.
Fizik çarpışma detection'da kullanılır.

Kullanım Alanları: Çarpışma algılama, fizik simulation, 3D model simplification
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Geom, GeomNode, GeomTriangles, GeomVertexData, GeomVertexFormat, GeomVertexWriter
from scipy.spatial import ConvexHull
import numpy as np


class ConvexHullDemo(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setup_camera()

        # Random 3D points
        np.random.seed(42)
        points = np.random.randn(30, 3) * 5

        # Convex Hull hesapla
        hull = ConvexHull(points)

        # Mesh oluştur
        self.create_hull_mesh(points, hull.simplices)

    def setup_camera(self):
        self.disableMouse()
        self.camera.setPos(0, 0, 20)
        self.camera.lookAt(0, 0, 0)

    def create_hull_mesh(self, vertices, faces):
        vformat = GeomVertexFormat.getV3()
        vdata = GeomVertexData("vertices", vformat, Geom.UH_static)
        vdata.setNumRows(len(vertices))

        vertex_writer = GeomVertexWriter(vdata, "vertex")
        for v in vertices:
            vertex_writer.addData3f(float(v[0]), float(v[1]), float(v[2]))

        prim = GeomTriangles(Geom.UH_static)
        for face in faces:
            prim.addVertices(int(face[0]), int(face[1]), int(face[2]))
        prim.closePrimitive()

        geom = Geom(vdata)
        geom.addPrimitive(prim)

        gnode = GeomNode("convex_hull")
        gnode.addGeom(geom)

        mesh = self.render.attachNewNode(gnode)
        mesh.setColor(1, 0.5, 0.5, 0.7)


app = ConvexHullDemo()
app.run()
