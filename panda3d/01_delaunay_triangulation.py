"""
Delaunay Triangulation (Delaunay Üçgenlemesi)
----------------------------------------------
Bir dizi noktayı optimal üçgenler oluşturacak şekilde triangule eden algoritma.
Oyunlarda terrain mesh oluşturmada kullanılır.

Kullanım Alanları: Terrain generation, mesh oluşturma, Voronoi diagram
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import GeomNode, Geom, GeomTriangles
from scipy.spatial import Delaunay
import numpy as np


class DelaunayTriangulation(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setup_camera()

        # Random 2D points oluştur
        np.random.seed(42)
        points_2d = np.random.rand(20, 2) * 10
        points_3d = np.column_stack([points_2d, np.zeros(20)])

        # Delaunay triangulation
        tri = Delaunay(points_2d)

        # Panda3D geometry oluştur
        self.create_mesh(points_3d, tri.simplices)

    def setup_camera(self):
        self.disableMouse()
        self.camera.setPos(5, 5, 15)
        self.camera.lookAt(5, 5, 0)

    def create_mesh(self, vertices, triangles):
        from panda3d.core import GeomVertexFormat, GeomVertexData, GeomVertexWriter

        vformat = GeomVertexFormat.getV3()
        vdata = GeomVertexData("vertices", vformat, Geom.UH_static)
        vdata.setNumRows(len(vertices))

        vertex_writer = GeomVertexWriter(vdata, "vertex")
        for v in vertices:
            vertex_writer.addData3f(float(v[0]), float(v[1]), float(v[2]))

        prim = GeomTriangles(Geom.UH_static)
        for tri in triangles:
            prim.addVertices(int(tri[0]), int(tri[1]), int(tri[2]))
        prim.closePrimitive()

        geom = Geom(vdata)
        geom.addPrimitive(prim)

        gnode = GeomNode("delaunay_mesh")
        gnode.addGeom(geom)

        mesh = self.render.attachNewNode(gnode)
        mesh.setColor(0.5, 0.5, 1, 1)


app = DelaunayTriangulation()
app.run()
