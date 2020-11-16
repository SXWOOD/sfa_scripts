import random
import logging
from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QCheckBox
from PySide2.QtCore import Qt
from shiboken2 import wrapInstance
import pymel.core as pm
import maya.cmds as cmds
import maya.OpenMayaUI as omui
from pymel.core.system import Path


log = logging.getLogger(__name__)


def maya_main_window():
    """Return the Maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterToolUI(QtWidgets.QDialog):
    """Scatter Tool UI Class"""

    def __init__(self):
        super(ScatterToolUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter Tool")
        self.setMinimumWidth(500)
        self.setMaximumHeight(300)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.set_scatter = ScatterFX()
        self.create_ui()
        self.create_connections()

    def create_ui(self):
        self.scatter_instructions = self._create_scatter_instruct()
        self.density_sbox = self._create_density_sbox()
        self.scale_min_lay = self._create_scale_min_ui()
        self.scale_max_lay = self._create_scale_max_ui()
        self.rot_min_lay = self._create_rot_min_ui()
        self.rot_max_lay = self._create_rot_max_ui()
        self.normals_lay = self.create_normals_checkbox()
        self.button_lay = self._create_button_ui()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.ui_add_layout()
        self.main_lay.addStretch()
        self.setLayout(self.main_lay)

    def ui_add_layout(self):
        self.main_lay.addLayout(self.scatter_instructions)
        self.main_lay.addLayout(self.density_sbox)
        self.main_lay.addLayout(self.scale_min_lay)
        self.main_lay.addLayout(self.scale_max_lay)
        self.main_lay.addLayout(self.rot_min_lay)
        self.main_lay.addLayout(self.rot_max_lay)
        self.main_lay.addLayout(self.normals_lay)
        self.main_lay.addLayout(self.button_lay)

    def create_connections(self):
        """Connects Signals and Slots"""
        self.scatter_btn.clicked.connect(self._scatter)
        self.scatter_rand_btn.clicked.connect(self._scatter_random)

    @QtCore.Slot()
    def _scatter(self):
        """Execute scatter effect"""
        self._set_scatter_properties_from_ui()
        self.scatter_fx()

    @QtCore.Slot()
    def _scatter_random(self):
        """Randomly Generate Numbers for Each Setting"""
        self.randomize_values()

    def _set_scatter_properties_from_ui(self):
        self.set_scatter.density_percentage = self.dens_sbox.value()
        self.set_scatter.scale_min = self.scale_min_sbox.value()
        self.set_scatter.scale_max = self.scale_max_sbox.value()
        self.set_scatter.rot_x_min = self.rot_xmin_box.value()
        self.set_scatter.rot_y_min = self.rot_ymin_box.value()
        self.set_scatter.rot_z_min = self.rot_zmin_box.value()
        self.set_scatter.rot_x_max = self.rot_xmax_box.value()
        self.set_scatter.rot_y_max = self.rot_ymax_box.value()
        self.set_scatter.rot_z_max = self.rot_zmax_box.value()

    def _create_button_ui(self):
        self.scatter_btn = QtWidgets.QPushButton("Execute Scatter Effect")
        self.scatter_rand_btn = QtWidgets.QPushButton("Randomize All Values")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_btn)
        layout.addWidget(self.scatter_rand_btn)
        return layout

    def _create_density_sbox(self):
        layout = QtWidgets.QGridLayout()
        self.dens_sbox = QtWidgets.QSpinBox()
        self.dens_sbox.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.dens_sbox.setFixedWidth(100)
        self.dens_sbox.setRange(1, 100)
        self.dens_sbox.setValue(100)
        self.dens_lbl = QtWidgets.QLabel("Random Density Percentage")
        layout.addWidget(self.dens_sbox, 1, 4)
        layout.addWidget(self.dens_lbl, 1, 5)
        return layout

    def _create_scale_min_ui(self):
        layout = QtWidgets.QGridLayout()
        self.scale_min_sbox = QtWidgets.QDoubleSpinBox()
        self.scale_min_sbox.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.scale_min_sbox.setFixedWidth(100)
        self.scale_min_sbox.setRange(0.0, 1.0)
        self.scale_min_sbox.setSingleStep(0.01)
        self.scale_min_lbl = QtWidgets.QLabel("Random Scale Minimum")
        layout.addWidget(self.scale_min_sbox, 1, 4)
        layout.addWidget(self.scale_min_lbl, 1, 5)
        return layout

    def _create_scale_max_ui(self):
        layout = QtWidgets.QGridLayout()
        self.scale_max_sbox = QtWidgets.QDoubleSpinBox()
        self.scale_max_sbox.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.scale_max_sbox.setFixedWidth(100)
        self.scale_max_sbox.setRange(0.0, 1.0)
        self.scale_max_sbox.setSingleStep(0.01)
        self.scale_max_sbox.setValue(1.0)
        self.scale_max_lbl = QtWidgets.QLabel("Random Scale Maximum")
        layout.addWidget(self.scale_max_sbox, 1, 4)
        layout.addWidget(self.scale_max_lbl, 1, 5)
        return layout

    def _create_rot_min_ui(self):
        layout = self._create_xyz_headers()
        self.rot_xmin_box = QtWidgets.QDoubleSpinBox()
        self.rot_xmin_box.setFixedWidth(50)
        self.rot_xmin_box.setMaximum(361)
        self.rot_xmin_box.setValue(self.set_scatter.rot_x_min)
        self.rot_xmin_box.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)

        self.rot_ymin_box = QtWidgets.QDoubleSpinBox()
        self.rot_ymin_box.setFixedWidth(50)
        self.rot_ymin_box.setMaximum(361)
        self.rot_ymin_box.setValue(self.set_scatter.rot_y_min)
        self.rot_ymin_box.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)

        self.rot_zmin_box = QtWidgets.QDoubleSpinBox()
        self.rot_zmin_box.setFixedWidth(50)
        self.rot_zmin_box.setMaximum(361)
        self.rot_zmin_box.setValue(self.set_scatter.rot_z_min)
        self.rot_zmin_box.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        return self.rot_min_add_widgets(layout)

    def rot_min_add_widgets(self, layout):
        self.rot_lbl_min = QtWidgets.QLabel("Random Rotation Minimum")
        layout.addWidget(self.rot_xmin_box, 3, 0)
        layout.addWidget(self.rot_ymin_box, 3, 2)
        layout.addWidget(self.rot_zmin_box, 3, 4)
        layout.addWidget(self.rot_lbl_min, 3, 5)
        return layout

    def _create_rot_max_ui(self):
        layout = QtWidgets.QGridLayout()
        self.rot_xmax_box = QtWidgets.QDoubleSpinBox()
        self.rot_xmax_box.setFixedWidth(50)
        self.rot_xmax_box.setMaximum(361)
        self.rot_xmax_box.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.rot_xmax_box.setValue(self.set_scatter.rot_x_max)

        self.rot_ymax_box = QtWidgets.QDoubleSpinBox()
        self.rot_ymax_box.setFixedWidth(50)
        self.rot_ymax_box.setMaximum(361)
        self.rot_ymax_box.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.rot_ymax_box.setValue(self.set_scatter.rot_y_max)

        self.rot_zmax_box = QtWidgets.QDoubleSpinBox()
        self.rot_zmax_box.setFixedWidth(50)
        self.rot_zmax_box.setMaximum(361)
        self.rot_zmax_box.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.rot_zmax_box.setValue(self.set_scatter.rot_z_max)
        return self.rot_max_add_widgets(layout)

    def rot_max_add_widgets(self, layout):
        self.rot_lbl_max = QtWidgets.QLabel("Random Rotation Maximum")
        layout.addWidget(self.rot_xmax_box, 3, 0)
        layout.addWidget(self.rot_ymax_box, 3, 2)
        layout.addWidget(self.rot_zmax_box, 3, 4)
        layout.addWidget(self.rot_lbl_max, 3, 5)
        return layout

    def _create_xyz_headers(self):
        self.scale_x_lbl = QtWidgets.QLabel("X")
        self.scale_y_lbl = QtWidgets.QLabel("Y")
        self.scale_z_lbl = QtWidgets.QLabel("Z")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.scale_x_lbl, 0, 0)
        layout.addWidget(self.scale_y_lbl, 0, 2)
        layout.addWidget(self.scale_z_lbl, 0, 4)
        return layout

    def _create_scatter_instruct(self):
        self.scatter_instructions = QtWidgets.QLabel("Select polygon to Scatter With FIRST, then select vertices"
                                                     " of second polygon to Scatter To \n")
        self.scatter_instructions.setStyleSheet("font: bold 15px")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_instructions, 0, 0)
        return layout

    def create_normals_checkbox(self):
        self.normals_cbox = QCheckBox("Align to Normals", self)
        self.normals_cbox.stateChanged.connect(self.checkbox_change)
        self.normals_cbox.toggle()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.normals_cbox, 5)
        return layout

    def checkbox_change(self, state):
        if state == Qt.Checked:
            self.align_to_normal = True

        else:
            self.align_to_normal = False

    def scatter_fx(self):
        selection = cmds.ls(sl=True, fl=True)
        vertex_names = cmds.filterExpand(selection, selectionMask=31, expand=True)

        random.shuffle(vertex_names)
        number_of_points = int(len(vertex_names) * self.dens_sbox.value() / 100)
        random_sample = random.sample(vertex_names, number_of_points)

        object_to_instance = selection[0]

        if cmds.objectType(object_to_instance) == 'transform':
            for vertex in random_sample:
                new_instance = cmds.instance(object_to_instance)[0]
                position = cmds.pointPosition(vertex, w=1)
                cmds.move(position[0], position[1], position[2], new_instance, a=1, ws=1)

                if self.align_to_normal:
                    mesh_vert = pm.MeshVertex(vertex)
                    vert_normal = mesh_vert.getNormal()
                    up_vector = pm.dt.Vector(0.0, 1.0, 0.0)
                    tangent = vert_normal.cross(up_vector).normal()
                    tangent2 = vert_normal.cross(tangent).normal()
                    pos = cmds.xform([vertex], query=True, worldSpace=True, translation=True)

                    matrix_trans = [tangent2.x, tangent2.y, tangent2.z, 0.0,
                                    vert_normal.x, vert_normal.y, vert_normal.z, 0.0,
                                    tangent.x, tangent.y, tangent.z, 0.0,
                                    pos[0], pos[1], pos[2], 1.0]

                    cmds.xform(new_instance, worldSpace=True, matrix=matrix_trans)

                new_rotation = [random.uniform(self.set_scatter.rot_x_min, self.set_scatter.rot_x_max),
                                random.uniform(self.set_scatter.rot_y_min, self.set_scatter.rot_y_max),
                                random.uniform(self.set_scatter.rot_z_min, self.set_scatter.rot_z_max)]

                cmds.rotate(new_rotation[0], new_rotation[1], new_rotation[2], new_instance,
                            a=1, ws=1)

                new_scale = random.uniform(self.set_scatter.scale_min, self.set_scatter.scale_max)
                cmds.scale(new_scale, new_scale, new_scale, new_instance,
                           a=1, ws=1)

        else:
            print("Please ensure the first object you select is a transform")

    def randomize_values(self):
        self.set_scatter.density_percentage = random.uniform(0, 100)
        self.set_scatter.scale_min = random.uniform(0.0, 0.5)
        self.set_scatter.scale_max = random.uniform(0.5, 1.0)
        self.set_scatter.rot_x_min = random.uniform(0, 180)
        self.set_scatter.rot_y_min = random.uniform(0, 180)
        self.set_scatter.rot_z_min = random.uniform(0, 180)
        self.set_scatter.rot_x_max = random.uniform(180, 360)
        self.set_scatter.rot_y_max = random.uniform(180, 360)
        self.set_scatter.rot_z_max = random.uniform(180, 360)
        self.display_random_values()

    def display_random_values(self):
        self.dens_sbox.setValue(self.set_scatter.density_percentage)
        self.scale_min_sbox.setValue(self.set_scatter.scale_min)
        self.scale_max_sbox.setValue(self.set_scatter.scale_max)
        self.rot_xmin_box.setValue(self.set_scatter.rot_x_min)
        self.rot_ymin_box.setValue(self.set_scatter.rot_y_min)
        self.rot_zmin_box.setValue(self.set_scatter.rot_z_min)
        self.rot_xmax_box.setValue(self.set_scatter.rot_x_max)
        self.rot_ymax_box.setValue(self.set_scatter.rot_y_max)
        self.rot_zmax_box.setValue(self.set_scatter.rot_z_max)


class ScatterFX(object):
    """Scatter Effect Default Values"""
    def __init__(self, path=None):
        self.density_percentage = 100
        self.scale_max = 1.0
        self.scale_min = 0.0
        self.rot_x_min = 0.0
        self.rot_y_min = 0.0
        self.rot_z_min = 0.0
        self.rot_x_max = 360.0
        self.rot_y_max = 360.0
        self.rot_z_max = 360.0
