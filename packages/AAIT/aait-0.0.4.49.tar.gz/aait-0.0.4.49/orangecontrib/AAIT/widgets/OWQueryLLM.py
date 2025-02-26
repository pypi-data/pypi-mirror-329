import os
import sys

import Orange.data
from AnyQt.QtWidgets import QApplication, QLabel
from Orange.widgets import widget
from Orange.widgets.utils.signals import Input, Output

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    from Orange.widgets.orangecontrib.AAIT.llm import answers
    from Orange.widgets.orangecontrib.AAIT.utils import thread_management
    from Orange.widgets.orangecontrib.AAIT.utils.import_uic import uic
    from Orange.widgets.orangecontrib.AAIT.utils.initialize_from_ini import apply_modification_from_python_file
else:
    from orangecontrib.AAIT.llm import answers
    from orangecontrib.AAIT.utils import thread_management
    from orangecontrib.AAIT.utils.import_uic import uic
    from orangecontrib.AAIT.utils.initialize_from_ini import apply_modification_from_python_file


@apply_modification_from_python_file(filepath_original_widget=__file__)
class OWQueryLLM(widget.OWWidget):
    name = "Query LLM"
    description = "Generate a response to a column 'prompt' with a LLM"
    icon = "icons/owqueryllm.svg"
    if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
        icon = "icons_dev/owqueryllm.svg"
    gui = os.path.join(os.path.dirname(os.path.abspath(__file__)), "designer/owqueryllm.ui")
    want_control_area = False
    priority = 1089
    class Inputs:
        data = Input("Data", Orange.data.Table)
        model_path = Input("Model", str)

    class Outputs:
        data = Output("Data", Orange.data.Table)

    @Inputs.data
    def set_data(self, in_data):
        self.data = in_data
        if self.autorun:
            self.run()

    @Inputs.model_path
    def set_model_path(self, in_model_path):
        self.model_path = in_model_path
        answers.check_gpu(in_model_path, self)
        if self.autorun:
            self.run()

    def __init__(self):
        super().__init__()
        # Qt Management
        self.setFixedWidth(470)
        self.setFixedHeight(300)
        uic.loadUi(self.gui, self)
        self.label_description = self.findChild(QLabel, 'Description')

        # Data Management
        self.data = None
        self.model_path = None
        self.thread = None
        self.autorun = True
        self.use_gpu = False
        self.result = None

        # Custom updates
        self.post_initialized()

    def run(self):
        # If Thread is already running, interrupt it
        if self.thread is not None:
            if self.thread.isRunning():
                self.thread.safe_quit()

        if self.data is None:
            return

        if self.model_path is None:
            return

        # Start progress bar
        self.progressBarInit()

        # Connect and start thread : main function, progress, result and finish
        # --> progress is used in the main function to track progress (with a callback)
        # --> result is used to collect the result from main function
        # --> finish is just an empty signal to indicate that the thread is finished
        self.thread = thread_management.Thread(answers.generate_answers, self.data, self.model_path, self.use_gpu)
        self.thread.progress.connect(self.handle_progress)
        self.thread.result.connect(self.handle_result)
        self.thread.finish.connect(self.handle_finish)
        self.thread.start()

    def handle_progress(self, value: float) -> None:
        self.progressBarSet(value)

    def handle_result(self, result):
        try:
            self.result = result
            self.Outputs.data.send(result)
        except Exception as e:
            print("An error occurred when sending out_data:", e)
            self.Outputs.data.send(None)
            return

    def handle_finish(self):
        print("Generation finished")
        self.progressBarFinished()

    def post_initialized(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_widget = OWQueryLLM()
    my_widget.show()
    app.exec_()
