from Qt import QtCore, QtWidgets



class ConvertHdrUI(object):
    def set_ui(self, parent):

        # Main layout
        self.vertical_layout_main = QtWidgets.QVBoxLayout(parent)

        self.vertical_layout_func_buttons = QtWidgets.QVBoxLayout()
        self.vertical_layout_hdr_list = QtWidgets.QVBoxLayout()

        self.horizontal_layout_1 = QtWidgets.QHBoxLayout()
        self.horizontal_layout_2 = QtWidgets.QHBoxLayout()
        self.horizontal_layout_progress_bar = QtWidgets.QHBoxLayout()
        self.horizontal_layout_3 = QtWidgets.QHBoxLayout()

        # Create hdr list
        self.hdr_list_label = QtWidgets.QLabel()
        self.hdr_list = QtWidgets.QListWidget()
        self.hdr_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        # Add hdr list on layout
        self.vertical_layout_hdr_list.addWidget(self.hdr_list_label)
        self.vertical_layout_hdr_list.addWidget(self.hdr_list)

        # Create functional buttons
        self.choose_files_button = QtWidgets.QPushButton('Choose Files')
        self.choose_folder_button = QtWidgets.QPushButton('Choose Folder')
        self.remove_button = QtWidgets.QPushButton('Remove')
        self.clear_all_button = QtWidgets.QPushButton('Clear All')

        # Create convert optionsl battons
        self.convert_options_label = QtWidgets.QLabel()
        self.convert_options_label.setText("Convert option:")
        
        self.raw_options_radiobutton = QtWidgets.QRadioButton('raw \"raw\"')
        self.srgb_options_radiobutton = QtWidgets.QRadioButton('srgb_texture \"ACES - ACEScg\"')
        self.aces_options_radiobutton = QtWidgets.QRadioButton('raw \"ACES - ACEScg\"')
        self.lin_options_radiobutton = QtWidgets.QRadioButton('lin_srgb \"ACES - ACEScg\"')

        self.convert_options_buttons_group = QtWidgets.QButtonGroup()
        self.convert_options_buttons_group.setExclusive(False)
        self.convert_options_buttons_group.addButton(self.raw_options_radiobutton)
        self.convert_options_buttons_group.addButton(self.srgb_options_radiobutton)
        self.convert_options_buttons_group.addButton(self.aces_options_radiobutton)
        self.convert_options_buttons_group.addButton(self.lin_options_radiobutton)
        
        # Added functional and convert options buttons on layout
        self.vertical_layout_func_buttons.addStretch(1)
        self.vertical_layout_func_buttons.addWidget(self.choose_files_button)
        self.vertical_layout_func_buttons.addWidget(self.choose_folder_button)
        self.vertical_layout_func_buttons.addStretch(1)
        self.vertical_layout_func_buttons.addWidget(self.remove_button)
        self.vertical_layout_func_buttons.addWidget(self.clear_all_button)
        self.vertical_layout_func_buttons.addStretch(1)
        self.vertical_layout_func_buttons.addWidget(self.convert_options_label)
        self.vertical_layout_func_buttons.addWidget(self.raw_options_radiobutton)
        self.vertical_layout_func_buttons.addWidget(self.srgb_options_radiobutton)
        self.vertical_layout_func_buttons.addWidget(self.aces_options_radiobutton)
        self.vertical_layout_func_buttons.addWidget(self.lin_options_radiobutton)

        # Create line for target path and button of choice
        self.target_path_label = QtWidgets.QLabel()
        self.target_path_label.setText("Target path:")
        self.target_path = QtWidgets.QLineEdit()
        self.target_path.setMaximumSize(QtCore.QSize(1000,22))
        self.target_path_button = QtWidgets.QPushButton('Choose Path')

        # Add target path line and button on layout
        self.horizontal_layout_2.addWidget(self.target_path_label)
        self.horizontal_layout_2.addWidget(self.target_path)
        self.horizontal_layout_2.addWidget(self.target_path_button)

        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setMaximumSize(QtCore.QSize(1000,40))
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat('Give me something to convert, Master \(^_^)/ ')

        self.horizontal_layout_progress_bar.addWidget(self.progress_bar)

        # Create apply cancel buttons
        self.apply_button = QtWidgets.QPushButton('Convert')
        self.cancel_button = QtWidgets.QPushButton('Exit')

        # Add apply and cancel battons on layout
        #self.horizontal_layout_3.addStretch(10)
        self.horizontal_layout_3.addWidget(self.cancel_button)
        self.horizontal_layout_3.addWidget(self.apply_button)

        self.horizontal_layout_1.addLayout(self.vertical_layout_hdr_list)
        self.horizontal_layout_1.addLayout(self.vertical_layout_func_buttons)

        # add all layot on window
        self.vertical_layout_main.addLayout(self.horizontal_layout_1)
        self.vertical_layout_main.addLayout(self.horizontal_layout_2)
        self.vertical_layout_main.addLayout(self.horizontal_layout_progress_bar)
        self.vertical_layout_main.addLayout(self.horizontal_layout_3)

