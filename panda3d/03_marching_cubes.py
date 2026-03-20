"""
Marching Cubes (Örtülü Yüzey Oluşturma)
-----------------------------------------
Voxel tabanlı veri (density grids) için üçgen mesh oluşturan algoritma.
Prosedürel terrain ve Metaballs için ideal.

Kullanım Alanları: Voxel-based terrain, Minecraft-like games, medical imaging visualization
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Geom, GeomNode, GeomTriangles, GeomVertexData, GeomVertexFormat, GeomVertexWriter
import numpy as np


class MarchingCubes(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setup_camera()

        # Voxel grid oluştur (basitleştirilmiş)
        self.create_metaball_mesh()

    def setup_camera(self):
        self.disableMouse()
        self.camera.setPos(10, 10, 10)
        self.camera.lookAt(5, 5, 5)

    def create_metaball_mesh(self):
        # Basit metaball: sphere-like density field
        size = 10
        scale = 1.0

        vertices = []
        triangles = []

        # Density field (2 merkezli metaball)
        centers = [np.array([4, 4, 4]), np.array([6, 6, 6])]

        for x in range(size - 1):
            for y in range(size - 1):
                for z in range(size - 1):
                    # Her voxel için density hesapla
                    pos = np.array([x, y, z]) * scale

                    density = 0
                    for center in centers:
                        dist = np.linalg.norm(pos - center)
                        density += 2.5 / (1 + dist ** 2)

                    # Basit voxel rendering (küpü göster/gizle)
                    if density > 1.5:
                        # Küp vertices
                        idx = len(vertices)
                        vertices.extend([
                            (x, y, z), (x + 1, y, z),
                            (x + 1, y + 1, z), (x, y + 1, z),
                            (x, y, z + 1), (x + 1, y, z + 1),
                            (x + 1, y + 1, z + 1), (x, y + 1, z + 1)
                        ])

                        # Küp faces
                        faces = [
                            (0, 1, 2), (0, 2, 3), (4, 6, 5), (4, 7, 6),
                            (0, 4, 5), (0, 5, 1), (2, 6, 7), (2, 7, 3),
                            (0, 3, 7), (0, 7, 4), (1, 5, 6), (1, 6, 2)
                        ]
                        for f in faces:
                            triangles.append((idx + f[0], idx + f[1], idx + f[2]))

        self.render_geometry(vertices, triangles)

    def render_geometry(self, vertices, triangles):
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

        gnode = GeomNode("metaball")
        gnode.addGeom(geom)

        mesh = self.render.attachNewNode(gnode)
        mesh.setColor(0, 1, 0.5, 1)


app = MarchingCubes()
app.run()
