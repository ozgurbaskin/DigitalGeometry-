# DigitalGeometry-

## Panda3D Detaylı Anlatım

### Panda3D Nedir?

Panda3D, Carnegie Mellon Üniversitesi tarafından geliştirilen, ücretsiz ve açık kaynaklı bir 3D oyun ve grafik motoru. Python ve C++ ile yazılmış, güçlü özellikleri ve kolay kullanım sağlar.

### Ana Özellikleri

- **Çoklu Platform Desteği:** Windows, macOS, Linux
- **Python Entegrasyonu:** Hızlı prototipleme ve geliştirme
- **Gelişmiş Grafik:** Modern rendering, shader support
- **Fizik Motoru:** Bullet Physics entegrasyonu
- **Ses & Müzik:** OpenAL tabanlı audio
- **Kolay Ray Casting:** Etkileşimli objeler için ray tracing
- **Güçlü Dokümantasyon:** Kapsamlı tutorials ve API docs

### Kurulum

```bash
pip install panda3d
```

### Basit "Hello World" Örneği

```python
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Point3

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Bir küp oluştur
        self.cube = self.loader.loadModel("models/box")
        self.cube.reparentTo(self.render)
        self.cube.setPos(0, 0, 0)

        # Her frame'de güncelle
        self.taskMgr.add(self.spin_cube, "SpinCube")

    def spin_cube(self, task):
        self.cube.setH(self.cube.getH() + 1)
        return task.cont

app = MyApp()
app.run()
```

---

## 5 Önerilen Geometri Algoritması

### 1. Delaunay Triangulation (Delaunay Üçgenlemesi)

Bir dizi noktayı optimal üçgenler oluşturacak şekilde triangule eden algoritma. Oyunlarda terrain mesh oluşturmada kullanılır.

📄 [panda3d/01_delaunay_triangulation.py](panda3d/01_delaunay_triangulation.py)

**Kullanım Alanları:** Terrain generation, mesh oluşturma, Voronoi diagram

---

### 2. Convex Hull (Dışbükey Zarf)

Bir nokta setini çevreleyen en küçük dışbükey polihedron bulur. Fizik çarpışma detection'da kullanılır.

📄 [panda3d/02_convex_hull.py](panda3d/02_convex_hull.py)

**Kullanım Alanları:** Çarpışma algılama, fizik simulation, 3D model simplification

---

### 3. Marching Cubes (Örtülü Yüzey Oluşturma)

Voxel tabanlı veri (density grids) için üçgen mesh oluşturan algoritma. Prosedürel terrain ve Metaballs için ideal.

📄 [panda3d/03_marching_cubes.py](panda3d/03_marching_cubes.py)

**Kullanım Alanları:** Voxel-based terrain, Minecraft-like games, medical imaging visualization

---

### 4. Line-of-Sight Pathfinding (Hızlı Yol Bulma)

Funnel algorithm ile bir navigation mesh üzerinde en kısa yol hesaplar.

📄 [panda3d/04_pathfinding.py](panda3d/04_pathfinding.py)

**Kullanım Alanları:** NPC AI, game pathfinding, autonomous agents

---

### 5. Octree Spatial Partitioning (Hızlı Mekan Arama)

3D space'i recursive olarak bölerek collision detection ve frustum culling hızlandırır.

📄 [panda3d/05_octree.py](panda3d/05_octree.py)

**Kullanım Alanları:** Spatial indexing, collision detection, frustum culling, level-of-detail rendering

---

## Özet Tablosu

| Algoritma          | Kullanım               | Karmaşıklık |
|--------------------|------------------------|-------------|
| **Delaunay**       | Terrain mesh oluşturma | O(n log n)  |
| **Convex Hull**    | Çarpışma detection     | O(n log n)  |
| **Marching Cubes** | Voxel → mesh dönüşümü  | O(n³)       |
| **Pathfinding**    | NPC AI yol bulma       | O(n)        |
| **Octree**         | Hızlı mekan sorguları  | O(log n)    |