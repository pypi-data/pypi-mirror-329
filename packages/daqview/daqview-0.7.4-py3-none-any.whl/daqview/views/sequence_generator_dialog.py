import logging

from PySide6.QtGui import QIcon
from PySide6.QtCore import QAbstractItemModel, QModelIndex, Qt
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QGroupBox, QLineEdit, QFileDialog,
                               QWidget, QFormLayout, QDoubleSpinBox,
                               QListView, QScrollArea, QApplication)

from .sequence_view_dialog import SequenceViewDialog
from .sequence_load_dialog import SequenceLoadDialog
from ..models import sequencing


logger = logging.getLogger(__name__)


class TemplateModel(QAbstractItemModel):
    """
    Simple list model for selecting available templates in a QListView.
    """
    def __init__(self, templates):
        super().__init__()
        self.templates = templates

    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        if not parent.isValid():
            if row < len(self.templates):
                return self.createIndex(row, column, self.templates[row])
            else:
                return QModelIndex()
        else:
            return QModelIndex()

    def parent(self, index):
        return QModelIndex()

    def rowCount(self, parent=QModelIndex()):
        if not parent.isValid():
            return len(self.templates)
        else:
            return 0

    def columnCount(self, parent=QModelIndex()):
        return 1

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid:
            return None
        item = index.internalPointer()
        col = index.column()
        if col == 0:
            if role == Qt.DisplayRole:
                return item['name']
            elif role == Qt.UserRole:
                return item
            else:
                return None
        else:
            return None

    def flags(self, index):
        return Qt.ItemIsEnabled

    def headerData(self, action, orientation, role=Qt.DisplayRole):
        return None

    def update_templates(self, templates):
        self.layoutAboutToBeChanged.emit()
        self.beginResetModel()
        self.templates = templates
        self.endResetModel()
        self.layoutChanged.emit()
        self.data


class SequenceGeneratorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sequence Generator")
        self.app = QApplication.instance()
        self.tpl_model = TemplateModel([])
        self.init_ui()
        self.rejected.connect(self.save_settings)
        self.load_settings()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        cols_layout = QHBoxLayout()
        layout.addLayout(cols_layout)

        # Column 1 is config loading and template selection
        col1 = QVBoxLayout()
        cols_layout.addLayout(col1, stretch=0)

        # Configuration file chooser
        cfg_box = QGroupBox(self)
        cfg_layout = QVBoxLayout()
        cfg_box.setLayout(cfg_layout)
        col1.addWidget(cfg_box, stretch=1)
        cfg_lbl = QLabel("<b>Configuration file</b>")
        cfg_layout.addWidget(cfg_lbl)
        cfg_file = QLineEdit(self)
        cfg_file.setReadOnly(True)
        self.cfg_file_le = cfg_file
        cfg_browse = QPushButton("Browse", self)
        if QIcon.hasThemeIcon("document-open"):
            cfg_browse.setIcon(QIcon.fromTheme("document-open"))
            cfg_browse.setText("")
        cfg_browse.clicked.connect(self.read_cfg_file)
        cfg_open_layout = QHBoxLayout()
        cfg_open_layout.addWidget(cfg_file)
        cfg_open_layout.addWidget(cfg_browse)
        cfg_layout.addLayout(cfg_open_layout)

        # Template chooser
        tpl_box = QGroupBox(self)
        tpl_layout = QVBoxLayout()
        tpl_box.setLayout(tpl_layout)
        col1.addWidget(tpl_box, stretch=4)
        tpl_lbl = QLabel("<b>Available Templates</b>")
        tpl_layout.addWidget(tpl_lbl)
        tpl_list = QListView(self)
        tpl_list.setModel(self.tpl_model)
        tpl_list.setSelectionBehavior(QListView.SelectRows)
        tpl_list.clicked.connect(self.template_clicked)
        tpl_layout.addWidget(tpl_list)
        self.tpl_list_view = tpl_list

        # Column 2 is template info
        col2 = QVBoxLayout()
        cols_layout.addLayout(col2, stretch=1)
        info_box = QGroupBox(self)
        info_layout = QVBoxLayout()
        info_box.setLayout(info_layout)
        col2.addWidget(info_box)
        info_lbl = QLabel("<b>Template Information</b>")
        info_layout.addWidget(info_lbl)

        name_lbl = QLabel()
        self.tpl_name_lbl = name_lbl
        desc_lbl = QLabel()
        self.tpl_desc_lbl = desc_lbl
        desc_lbl.setWordWrap(True)
        tzero_off_lbl = QLabel()
        self.tpl_tzero_off_lbl = tzero_off_lbl

        info_layout.addWidget(QLabel("<i>Name</i>"))
        info_layout.addWidget(name_lbl)
        info_layout.addWidget(QLabel("<i>Description</i>"))
        info_layout.addWidget(desc_lbl)
        info_layout.addWidget(tzero_off_lbl)
        info_layout.addWidget(QLabel("<i>DAQ Boxes</i>"))

        # Scroll area contains automatically generated DAU QGroupBoxes
        self.tpl_daus_scroll = QScrollArea(self)
        tpl_daus_widget = QWidget()
        self.tpl_daus_layout = QVBoxLayout()
        tpl_daus_widget.setLayout(self.tpl_daus_layout)
        self.tpl_daus_scroll.setWidget(tpl_daus_widget)
        self.tpl_daus_scroll.setWidgetResizable(True)
        info_layout.addWidget(self.tpl_daus_scroll)

        # Column 3 is variables
        col3 = QVBoxLayout()
        cols_layout.addLayout(col3, stretch=1)
        vars_box = QGroupBox(self)
        vars_layout = QVBoxLayout()
        vars_box.setLayout(vars_layout)
        col3.addWidget(vars_box)
        vars_lbl = QLabel("<b>Variables</b>")
        vars_layout.addWidget(vars_lbl)

        # Scroll area contains automatically generated variable QGroupBoxes
        self.tpl_vars_scroll = QScrollArea(self)
        tpl_vars_widget = QWidget()
        self.tpl_vars_layout = QVBoxLayout()
        tpl_vars_widget.setLayout(self.tpl_vars_layout)
        self.tpl_vars_scroll.setWidget(tpl_vars_widget)
        self.tpl_vars_scroll.setWidgetResizable(True)
        vars_layout.addWidget(self.tpl_vars_scroll)

        # Buttons
        btns_layout = QHBoxLayout()
        close_btn = QPushButton("Close", self)
        gen_btn = QPushButton("Generate", self)
        close_btn.clicked.connect(self.reject)
        gen_btn.clicked.connect(self.generate_clicked)
        gen_btn.setDefault(True)
        btns_layout.addStretch()
        btns_layout.addWidget(close_btn)
        btns_layout.addWidget(gen_btn)
        layout.addLayout(btns_layout)

        # Default QDialog is 640x480 which is a little tight for this dialog,
        # so resize once to a larger initial size.
        self.resize(1024, 768)

    def get_current_template(self):
        index = self.tpl_list_view.currentIndex()
        tpl = self.tpl_model.data(index, role=Qt.UserRole)
        if tpl is None:
            tpl = {}
        return tpl

    def draw_dau_boxes(self):
        # Display names for profile types
        type_names = {
            "profile_dist": "Distance",
            "profile_ol": "Open Loop",
            "profile_cl": "Closed Loop",
            "sequence": "Valve Sequence",
        }

        tpl = self.get_current_template()

        # Remove existing DAU boxes
        while True:
            w = self.tpl_daus_layout.takeAt(0)
            if not w:
                break
            if w.widget():
                w.widget().deleteLater()

        # Add new DAU boxes
        for dau in tpl.get('daus', []):
            dau_box = QGroupBox(dau.get('dau'))
            dau_layout = QFormLayout()
            dau_box.setLayout(dau_layout)
            dau_layout.addRow("Name:", QLabel(dau.get('name')))
            dau_layout.addRow("URL:", QLabel(dau.get('addr')))
            dau_type = dau.get('type')
            type_name = type_names.get(dau_type, "Unknown")
            dau_layout.addRow("Profile Type:", QLabel(type_name))
            if dau_type.startswith("profile_"):
                dau_units = dau.get('units', '')
                dau_scale = dau.get('scale_max', '')
                dau_dt = dau.get('dt_ms', '')
                dau_cutoff = dau.get('cutoff_freq', '')
                dau_layout.addRow("Timestep:", QLabel(f"{dau_dt} ms"))
                dau_layout.addRow("Scale:", QLabel(f"{dau_scale} {dau_units}"))
                dau_layout.addRow("Cutoff:", QLabel(f"{dau_cutoff} Hz"))
            self.tpl_daus_layout.addWidget(dau_box)
        self.tpl_daus_layout.addStretch(1)

    def draw_var_boxes(self):
        tpl = self.get_current_template()
        self.var_inputs = {}

        # Clear existing boxes
        while True:
            w = self.tpl_vars_layout.takeAt(0)
            if not w:
                break
            if w.widget():
                w.widget().deleteLater()

        # Add new boxes
        for var in tpl.get('variables', []):
            var_box = QGroupBox()
            var_layout = QFormLayout()
            var_box.setLayout(var_layout)
            var_layout.addRow("Name:", QLabel(var.get('name')))
            var_layout.addRow("Description:", QLabel(var.get('description')))
            if var.get('type', 'float') == 'float':
                var_val = QDoubleSpinBox(var_box)
                var_val.setSuffix(" " + var.get('units', ''))
                var_val.setSingleStep(float(var.get('step', 0.01)))
                var_val.setDecimals(int(var.get('decimals', 3)))
                var_val.setMinimum(float(var.get('minimum', 0.0)))
                var_val.setMaximum(float(var.get('maximum', 100.0)))
                var_val.setValue(float(var.get('default', 0.0)))
                self.var_inputs[var['id']] = (var_val.value, var_val.setValue)
            else:
                var_val = QLineEdit(var.get('default', ''), var_box)
                self.var_inputs[var['id']] = (var_val.text, var_val.setText)
            var_layout.addRow("Value:", var_val)
            self.tpl_vars_layout.addWidget(var_box)
        self.tpl_vars_layout.addStretch(1)

    def get_variables(self):
        return {v: f() for (v, (f, _)) in self.var_inputs.items()}

    def set_variables(self, variables):
        for k, v in variables.items():
            if k in self.var_inputs and v:
                self.var_inputs[k][1](v)

    def template_clicked(self, index):
        tpl = self.get_current_template()

        # Diplay name and description
        self.tpl_name_lbl.setText(tpl.get('name', 'Unknown'))
        self.tpl_desc_lbl.setText(tpl.get('description', 'Unknown'))
        tzero = float(tpl.get('tzero_offset', 0.0))
        self.tpl_tzero_off_lbl.setText(f"T0 Offset: {tzero:.1f}")

        # Draw DAU and variable boxes from this template
        self.draw_dau_boxes()
        self.draw_var_boxes()

        # Save new template choice
        self.save_settings()

    def generate_clicked(self):
        self.save_settings()
        template = self.get_current_template()
        variables = self.get_variables()
        seq_view = SequenceViewDialog(template, variables, self)
        seq_view.accepted.connect(self.profiles_accepted)
        seq_view.setModal(True)
        seq_view.show()

    def profiles_accepted(self):
        template = self.get_current_template()
        variables = self.get_variables()
        load_dialog = SequenceLoadDialog(template, variables, self)
        load_dialog.setModal(True)
        load_dialog.show()

    def save_settings(self):
        cfg_file = self.cfg_file_le.text()
        tpl_index = self.tpl_list_view.currentIndex().row()
        variables = self.get_variables()
        self.app.prefs.set_recent_sequencing_cfg({
            'fname': cfg_file, 'tpl_index': tpl_index, 'variables': variables})

    def load_settings(self):
        settings = self.app.prefs.get_recent_sequencing_cfg()
        fname = settings.get('fname')
        tpl_index = settings.get('tpl_index')
        variables = settings.get('variables', {})

        if fname:
            self.read_cfg_file(fname=fname)
            if tpl_index is not None:
                idx = self.tpl_model.index(tpl_index, 0)
                self.tpl_list_view.setCurrentIndex(idx)
                self.tpl_list_view.setFocus()
                self.template_clicked(idx)
                if variables:
                    self.set_variables(variables)

    def read_cfg_file(self, *args, fname=None):
        """
        Read a configuration file given by `fname`, or if None, display a
        file selection dialogue to the user first.

        Populates the template model and selects the first one, causing
        template information and variables to be updated.
        """
        # Open file selection dialogue if no fname provided
        if fname is None:
            fname = QFileDialog.getOpenFileName(
                self, "Open Config File...", "",
                "Config File (*.yml *.yaml)", "")[0]

        if not fname:
            logger.info("No file provided, not opening config")
            return False

        logger.info("Opening config file from '%s'", fname)

        self.cfg_file_le.setText(fname)
        templates = sequencing.read_templates_from_config(fname)
        self.tpl_model.update_templates(templates)

        # Select first template by default
        idx = self.tpl_model.index(0, 0)
        self.tpl_list_view.setCurrentIndex(idx)
        self.tpl_list_view.setFocus()
        self.template_clicked(idx)

        # Save empty preferences for newly selected template,
        # to ensure we open the same file next time.
        self.save_settings()
