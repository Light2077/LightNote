import pyqtgraph.opengl as gl
import pyqtgraph as pg

pg.setConfigOptions(antialias=True)


class CylinderPlot(gl.GLViewWidget):
    def __init__(self):
        super().__init__()

        self.show()
        self.setCameraPosition(distance=60)

        # 创建圆柱
        self.cylinder = gl.MeshData.cylinder(
            rows=10, cols=20, radius=[5.0, 5], length=20.0
        )
        # 将圆柱整体下移10个单位
        self.cylinder._vertexes[:, 2] = self.cylinder._vertexes[:, 2] - 10

        # 设置圆柱的颜色
        cylinder = gl.GLMeshItem(
            meshdata=self.cylinder,
            smooth=True,
            color=(0.5, 0.5, 1, 0.8),
            shader="shaded",  # normalColor heightColor edgeHilight shaded
            glOptions="opaque",
        )

        self.addItem(cylinder)


if __name__ == "__main__":
    app = pg.mkQApp()
    w = CylinderPlot()
    pg.exec()
