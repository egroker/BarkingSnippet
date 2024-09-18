import os

from Qt import QtCore, QtGui, QtWidgets
from ui.convert_hdr import ConvertHdrUI
from utils import split_file, convert_script

FORMATS = ["tif"]

class ConvertHdr(QtWidgets.QDialog):
    def __init__(self):
        super(ConvertHdr, self).__init__()

        self.setWindowTitle("Convert to TX")
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        self._ui = ConvertHdrUI()
        self._ui.set_ui(self)

        self._ui.cancel_button.clicked.connect(self.on_cancel)
        self._ui.choose_files_button.clicked.connect(self.choose_files)
        self._ui.choose_folder_button.clicked.connect(self.choose_folder)
        self._ui.remove_button.clicked.connect(self.remove_list_item)
        self._ui.clear_all_button.clicked.connect(self.clear_all_list_item)
        self._ui.target_path_button.clicked.connect(self.get_target_path)
        self._ui.apply_button.clicked.connect(self.convert)

        self._ui.convert_options_buttons_group.buttonClicked.connect(self.check_buttons)

        self._ui.choose_files_button.clicked.connect(self.switch_convert_button)
        self._ui.choose_folder_button.clicked.connect(self.switch_convert_button)
        self._ui.remove_button.clicked.connect(self.switch_convert_button)
        self._ui.clear_all_button.clicked.connect(self.switch_convert_button)
        self._ui.target_path_button.clicked.connect(self.switch_convert_button)
        self._ui.raw_options_radiobutton.clicked.connect(self.switch_convert_button)
        self._ui.srgb_options_radiobutton.clicked.connect(self.switch_convert_button)
        self._ui.aces_options_radiobutton.clicked.connect(self.switch_convert_button)
        self._ui.lin_options_radiobutton.clicked.connect(self.switch_convert_button)

        self.switch_convert_button()

    def on_cancel(self):
        #self._save_dialog_config()
        self.reject()

    def choose_files(self):
        input_files = QtWidgets.QFileDialog.getOpenFileNames(
            parent=self,
            caption="Choose Files",
            filter="File format (*.{})".format(
                " *.".join(FORMATS)
            )
        )
        
        if input_files[0]: 
            for input_file in input_files[0]:
                input_file = os.path.abspath(input_file)
                self.add_item_in_list(input_file)
            
            if self._ui.hdr_list.item(0):
                self._ui.hdr_list_label.setText(self._ui.hdr_list.item(0).path_to)
            
            self._ui.progress_bar.setValue(0)
            self._ui.progress_bar.setRange(0, self._ui.hdr_list.count())
            self._ui.progress_bar.setFormat('%v / %m')

    def choose_folder(self):
        source_folder = QtWidgets.QFileDialog.getExistingDirectory(
            parent=self,
            caption="Choose Folder"
        )
        if source_folder:
            filenames = os.listdir(source_folder)
            filenames = [
                f
                for f in filenames
                if os.path.isfile(os.path.join(source_folder, f))
            ]

            for file in filenames:
                
                input_file = source_folder + "/" + file
                _, _, _, file_format = split_file(input_file)

                if file_format in FORMATS:
                    self.add_item_in_list(input_file)

            self._ui.hdr_list_label.setText(source_folder)

            self._ui.progress_bar.setValue(0)
            self._ui.progress_bar.setRange(0, self._ui.hdr_list.count())
            self._ui.progress_bar.setFormat('%v / %m')

    def add_item_in_list(self, file_path):
        item = FileListItem(file_path)
        self._ui.hdr_list.addItem(item)

    def remove_list_item(self):
        items = self._ui.hdr_list.selectedItems()
        for item in items:
            row = self._ui.hdr_list.row(item)
            del_item = self._ui.hdr_list.takeItem(row)
            self._ui.hdr_list.removeItemWidget(del_item)

        if self._ui.hdr_list.count() == 0:
            self._ui.hdr_list_label.clear()

            self.reset_progress_bar()
    
    def clear_all_list_item(self):
        self._ui.hdr_list.clear()
        self._ui.hdr_list_label.clear()

        self.reset_progress_bar()

    def get_target_path(self):
        target_folder = QtWidgets.QFileDialog.getExistingDirectory(
            parent=self,
            caption="Choose Target Folder",
        )

        if target_folder:
            self._ui.target_path.setText(target_folder)
    
    def get_convert_option(self):
        option = None
        if self._ui.raw_options_radiobutton.isChecked():
            option = self._ui.raw_options_radiobutton.text()
        if self._ui.srgb_options_radiobutton.isChecked():
            option = self._ui.srgb_options_radiobutton.text()
        if self._ui.aces_options_radiobutton.isChecked():
            option = self._ui.aces_options_radiobutton.text()
        if self._ui.lin_options_radiobutton.isChecked():
            option = self._ui.lin_options_radiobutton.text()

        return option
    
    def clear_convert_option(self):
        self._ui.raw_options_radiobutton.setChecked(False)
        self._ui.srgb_options_radiobutton.setChecked(False)
        self._ui.aces_options_radiobutton.setChecked(False)
        self._ui.lin_options_radiobutton.setChecked(False)
    
    def check_buttons(self, radioButton):
        # Uncheck every other button in this group
        for button in self._ui.convert_options_buttons_group.buttons():
            if button is not radioButton:
                button.setChecked(False)

    def convert(self):
        self._ui.apply_button.setDisabled(True)
        self._ui.apply_button.repaint()

        count = self._ui.hdr_list.count()
        target_path = self._ui.target_path.text()
        option = self.get_convert_option()

        for i in range(self._ui.hdr_list.count()):
            self.update_progress_bar(i)
            source_file = self._ui.hdr_list.takeItem(count-i-1)
            convert_script(source_file, target_path, option)

        self._ui.hdr_list_label.clear()
        self._ui.target_path.clear()
        self.clear_convert_option()
        self._ui.progress_bar.setValue(100)
        self._ui.progress_bar.setFormat('Success, Master! ^(*-*)^')

    def switch_convert_button(self):
        count = self._ui.hdr_list.count()
        option = self.get_convert_option()
        target_path = self._ui.target_path.text()

        if count == 0 or option == None or target_path == "":
            self._ui.apply_button.setDisabled(True)
        else:
            self._ui.apply_button.setDisabled(False)
    
    def update_progress_bar(self, i):
        self._ui.progress_bar.setValue(i + 1)

    def reset_progress_bar(self):
        self._ui.progress_bar.setValue(0)
        self._ui.progress_bar.setFormat('Give me something to convert, Master \(^_^)/')

class FileListItem(QtWidgets.QListWidgetItem):

    def __init__(
        self,
        abs_path,
    ):
        super(FileListItem, self).__init__()

        self.abs_path = abs_path

        path_to, file_base, file_name, file_format = split_file(self.abs_path)
        self.path_to = path_to
        self.file_base = file_base
        self.file_name = file_name
        self.file_format = file_format

        self.setText(self.file_base)
    
    

    def get_abs_path(self):
        return self.abs_path
