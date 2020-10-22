import logging
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtWidgets import QHBoxLayout, QSlider, QLabel
from PySide2.QtCore import Qt
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pmc
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
        self.setMaximumHeight(200)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.scenefile = SceneFile()
        self.create_ui()
        self.create_connections()

    def create_ui(self):
        self.scatter_with = self._create_scatter_with()
        self.scatter_to = self._create_scatter_to()
        self.slider = self.create_slider()
        self.scale_min_lay = self._create_scale_min_ui()
        self.scale_max_lay = self._create_scale_max_ui()
        self.rot_min_lay = self._create_rot_min_ui()
        self.rot_max_lay = self._create_rot_max_ui()
        self.button_lay = self._create_button_ui()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addLayout(self.scatter_with)
        self.main_lay.addLayout(self.scatter_to)
        self.main_lay.addLayout(self.slider)
        self.main_lay.addLayout(self.scale_min_lay)
        self.main_lay.addLayout(self.scale_max_lay)
        self.main_lay.addLayout(self.rot_min_lay)
        self.main_lay.addLayout(self.rot_max_lay)
        self.main_lay.addStretch()
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)
        #self.create_slider()

    def create_slider(self):
        """Slider to change density from 0 to 100%"""
        hbox = QHBoxLayout()

        self.slider = QSlider()
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)

        self.slider.valueChanged.connect(self.change_density)

        self.label = QLabel("0")
        self.label.setFont(QtGui.QFont("Sanserif", 15))

        hbox.addWidget(self.slider)
        hbox.addWidget(self.label)

        #self.setLayout(hbox)

    def change_density(self):
        size = self.slider.value()
        self.label.setText(str(size))

    def create_connections(self):
        """Connects Signals and Slots"""
        self.folder_browse_btn.clicked.connect(self._browse_folder)
        self.scatter_btn.clicked.connect(self._scatter)

    @QtCore.Slot()
    def _scatter(self):
        """Execute scatter effect"""
        self._set_scenefile_properties_from_ui()
        #self.scenefile.save()

    def _set_scenefile_properties_from_ui(self):
        self.scenefile.folder_path = self.folder_le.text()
        self.scenefile.descriptor = self.descriptor_le.text()
        self.scenefile.task = self.task_le.text()
        self.scenefile.ver = self.ver_le.value()
        self.scenefile.ext = self.ext_lbl.text()

    @QtCore.Slot()
    def _browse_folder(self):
        """Opens a dialogue box to browse the folder"""
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            parent=self, caption="Select folder", dir=self.folder_le.text(),
            options=QtWidgets.QFileDialog.ShowDirsOnly |
            QtWidgets.QFileDialog.DontResolveSymlinks)
        self.folder_le.setText(folder)

    def _create_button_ui(self):
        self.scatter_btn = QtWidgets.QPushButton("Scatter")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_btn)
        return layout

    def _create_scale_min_ui(self):
        layout = self._create_xyz_headers()
        self.scale_xmin_box = QtWidgets.QLineEdit(self.scenefile.descriptor)
        self.scale_xmin_box.setFixedWidth(50)
        self.scale_ymin_box = QtWidgets.QLineEdit(self.scenefile.task)
        self.scale_ymin_box.setFixedWidth(50)
        self.scale_zmin_box = QtWidgets.QLineEdit(self.scenefile.descriptor)
        self.scale_zmin_box.setFixedWidth(50)
        self.scale_lbl_min = QtWidgets.QLabel("Random Scale Minimum")
        layout.addWidget(self.scale_xmin_box, 1, 0)
        layout.addWidget(self.scale_ymin_box, 1, 2)
        layout.addWidget(self.scale_zmin_box, 1, 4)
        layout.addWidget(self.scale_lbl_min, 1, 5)
        return layout

    def _create_scale_max_ui(self):
        layout = self._create_xyz_headers()
        self.scale_xmax_box = QtWidgets.QLineEdit(self.scenefile.descriptor)
        self.scale_xmax_box.setFixedWidth(50)
        self.scale_ymax_box = QtWidgets.QLineEdit(self.scenefile.task)
        self.scale_ymax_box.setFixedWidth(50)
        self.scale_zmax_box = QtWidgets.QLineEdit(self.scenefile.descriptor)
        self.scale_zmax_box.setFixedWidth(50)
        self.scale_lbl_max = QtWidgets.QLabel("Random Scale Maximum")
        layout.addWidget(self.scale_xmax_box, 2, 0)
        layout.addWidget(self.scale_ymax_box, 2, 2)
        layout.addWidget(self.scale_zmax_box, 2, 4)
        layout.addWidget(self.scale_lbl_max, 2, 5)
        return layout

    def _create_rot_min_ui(self):
        layout = self._create_xyz_headers()
        self.rot_xmin_box = QtWidgets.QLineEdit(self.scenefile.descriptor)
        self.rot_xmin_box.setFixedWidth(50)
        self.rot_ymin_box = QtWidgets.QLineEdit(self.scenefile.task)
        self.rot_ymin_box.setFixedWidth(50)
        self.rot_zmin_box = QtWidgets.QLineEdit(self.scenefile.descriptor)
        self.rot_zmin_box.setFixedWidth(50)
        self.rot_lbl_min = QtWidgets.QLabel("Random Rotation Minimum")
        layout.addWidget(self.rot_xmin_box, 3, 0)
        layout.addWidget(self.rot_ymin_box, 3, 2)
        layout.addWidget(self.rot_zmin_box, 3, 4)
        layout.addWidget(self.rot_lbl_min, 3, 5)
        return layout

    def _create_rot_max_ui(self):
        layout = self._create_xyz_headers()
        self.rot_xmax_box = QtWidgets.QLineEdit(self.scenefile.descriptor)
        self.rot_xmax_box.setFixedWidth(50)
        self.rot_ymax_box = QtWidgets.QLineEdit(self.scenefile.task)
        self.rot_ymax_box.setFixedWidth(50)
        self.rot_zmax_box = QtWidgets.QLineEdit(self.scenefile.descriptor)
        self.rot_zmax_box.setFixedWidth(50)
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

    def _create_scatter_with(self):
        default_folder = Path(cmds.workspace(rootDirectory=True, query=True))
        default_folder = default_folder / "scenes"
        self.folder_le = QtWidgets.QLineEdit(default_folder)
        self.folder_browse_btn = QtWidgets.QPushButton("Scatter With")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.folder_le)
        layout.addWidget(self.folder_browse_btn)
        return layout

    def _create_scatter_to(self):
        default_folder = Path(cmds.workspace(rootDirectory=True, query=True))
        default_folder = default_folder / "scenes"
        self.folder_le = QtWidgets.QLineEdit(default_folder)
        self.folder_browse_btn = QtWidgets.QPushButton("Scatter To")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.folder_le)
        layout.addWidget(self.folder_browse_btn)
        return layout


class SceneFile(object):
    """"An abstract representation of a Scene file."""
    def __init__(self, path=None):
        self._folder_path = Path(cmds.workspace(query=True, rootDirectory=True)) / "scenes"
        self.descriptor = 'main'
        self.task = 'model'
        self.ver = 1
        self.ext = '.ma'
        scene = pmc.system.sceneName()
        if not path and scene:
            path = scene
        if not path and not scene:
            log.info("Initialize with default properties.")
            return
        self._init_from_path(path)

    @property
    def folder_path(self):
        return self._folder_path

    @folder_path.setter
    def folder_path(self, val):
        self._folder_path = Path(val)

    @property
    def filename(self):
        pattern = "{descriptor}_{task}_v{ver:03d}{ext}"
        return pattern.format(descriptor=self.descriptor,
                              task=self.task,
                              ver=self.ver,
                              ext=self.ext)

    @property
    def path(self):
        return self.folder_path / self.filename

    def _init_from_path(self, path):
        path = Path(path)
        self.folder_path = path.parent
        self.ext = path.ext
        self.descriptor, self.task, ver = path.name.stripext().split("_")
        self.ver = int(ver.split("v")[-1])

    def save(self):
        """Saves the scene file.

        Returns:
            Path: The path to the scene file if successful
        """
        try:
            return pmc.system.saveAs(self.path)
        except RuntimeError as err:
            log.warning("Missing directories in path. Creating folder...")
            self.folder_path.makedirs_p()
            return pmc.system.saveAs(self.path)


