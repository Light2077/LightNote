"""
使用numpy 生成的椭圆
"""
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np

pg.setConfigOptions(antialias=True)


def get_cylinder(radius, height, num_segments=30):
    angle = np.linspace(0, 2 * np.pi, num_segments + 1)[:-1].reshape(1, -1)
    x = np.cos(angle) * radius
    y = np.sin(angle) * radius
    z = height

    vertices = []
    faces = []

    for i in range(len(height) - 1):
        for j in range(num_segments):
            next_j = (j + 1) % num_segments

            base_index = len(vertices)
            vertices.extend(
                [
                    (x[i][j], y[i][j], height[i]),
                    (x[i + 1][j], y[i + 1][j], height[i + 1]),
                    (x[i][next_j], y[i][next_j], height[i]),
                    (x[i + 1][next_j], y[i + 1][next_j], height[i + 1]),
                ]
            )

            faces.extend(
                [
                    (base_index, base_index + 1, base_index + 2),
                    (base_index + 1, base_index + 3, base_index + 2),
                ]
            )
    vertices = np.array(vertices, dtype=np.float32)
    faces = np.array(faces, dtype=np.uint32)

    return vertices, faces


# 旋转顶点
def rotate_vertices(vertices, angle):
    rotation_matrix = np.array(
        [
            [1, 0, 0],
            [0, np.cos(angle), -np.sin(angle)],
            [0, np.sin(angle), np.cos(angle)],
        ]
    )

    return np.dot(vertices, rotation_matrix)


class CylinderPlot(gl.GLViewWidget):
    def __init__(self):
        super().__init__()

        self.show()
        self.setCameraPosition(distance=60)

        # 创建圆柱
        # self.cylinder = gl.MeshData.cylinder(
        #     rows=10, cols=20, radius=[5.0, 5], length=20.0
        # )
        # 将圆柱整体下移10个单位
        # self.cylinder._vertexes[:, 2] = self.cylinder._vertexes[:, 2] - 10

        # 设置圆柱的颜色
        # self.set_cylinder_colormap()
        # m = gl.GLMeshItem(meshdata=self.cylinder, smooth=True)

        num = 10
        r = np.random.uniform(30.8, 31.2, num)
        radius = np.array(r).reshape(-1, 1)
        height = (np.array(range(num)) - len(r) // 2) * 100
        vertices, faces = get_cylinder(radius, height, num_segments=20)

        vertices = rotate_vertices(vertices, np.pi / 2)  # 绕x轴旋转90度（π/2弧度）
        mesh_data = gl.MeshData(vertexes=vertices, faces=faces)
        cylinder = gl.GLMeshItem(
            meshdata=mesh_data,
            smooth=True,
            color=(0.5, 0.5, 1, 0.8),
            shader="shaded",  # normalColor heightColor edgeHilight shaded
            glOptions="opaque",
        )
        # window.addItem(cylinder)
        self.addItem(cylinder)


if __name__ == "__main__":
    app = pg.mkQApp()
    w = CylinderPlot()
    pg.exec()
