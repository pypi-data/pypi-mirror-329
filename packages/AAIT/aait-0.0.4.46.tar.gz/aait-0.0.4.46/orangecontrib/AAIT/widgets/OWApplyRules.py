import os
import sys
import re
import Orange.data
from Orange.widgets import widget, gui, settings
from Orange.widgets.widget import Input, Output
from Orange.data import Table, Domain, ContinuousVariable, StringVariable, DiscreteVariable

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    from Orange.widgets.orangecontrib.AAIT.utils.import_uic import uic
    from Orange.widgets.orangecontrib.AAIT.utils.initialize_from_ini import apply_modification_from_python_file
else:
    from orangecontrib.AAIT.utils.import_uic import uic
    from orangecontrib.AAIT.utils.initialize_from_ini import apply_modification_from_python_file

@apply_modification_from_python_file(filepath_original_widget=__file__)
class OWApplyRules(widget.OWWidget):
    name = "Apply Rules to data"
    description = "Apply Rules to data fron an over workflow."
    icon = "icons/apply_rules.svg"
    if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
        icon = "icons_dev/apply_rules.svg"
    priority = 1145
    keywords = "Apply Rules to data"
    gui = os.path.join(os.path.dirname(os.path.abspath(__file__)), "designer/ownumberpointinrules.ui")

    class Inputs:
        rules = Input("Rules", Orange.data.Table)
        data = Input("Data", Orange.data.Table)

    class Outputs:
        out_data = Output("Out data", Orange.data.Table)


    @Inputs.rules
    def set_rules(self, data):
        self.rules_data = data
        if self.data is not None:
            self.run()


    @Inputs.data
    def set_new_point_from_scatter_plot(self, data):
        self.data = data
        if self.rules_data is not None:
            self.run()

    def __init__(self):
        super().__init__()
        # Set the fixed width and height of the widget
        self.setFixedWidth(470)
        self.setFixedHeight(300)

        # Load the user interface file
        uic.loadUi(self.gui, self)
        self.rules_data = None
        self.data = None
        self.post_initialized()

    def post_initialized(self):
        """
        used for overloading only
        """
        return

    def del_space_debut_fin(self, text_to_edit):
        if text_to_edit[0] == " ":
            text_to_edit = text_to_edit[1:]
        if text_to_edit[-1] == " ":
            text_to_edit = text_to_edit[:-1]
        return text_to_edit



    def run(self):
        self.error("")
        if self.rules_data is None or self.data is None:
            self.error("You must have rules and data")
            return

        from Orange.data import Table, Domain, ContinuousVariable, StringVariable, DiscreteVariable

        data_regle = self.rules_data
        data_value = self.data
        num_col_regle = data_regle.domain.index("regle")
        a_recuperer = []
        error = False
        for i in range(len(data_value)):
            a_recuperer.append(False)
        for regle in data_regle:
            current_regle = regle[num_col_regle]
            for i in range(len(data_value)):
                new_regle = str(current_regle)
                for j in range(len(data_value[i])):
                    new_regle = new_regle.replace(data_value.domain[j].name, str(data_value[i][j].value))
                a_recuperer[i] = 0
                try:
                    if eval(new_regle):
                        a_recuperer[i] = 1
                except Exception as e:
                    error = True
                    print(f"Error : {e}")
                    self.error("You have to edit your rule to be correct")


        data = []
        for idx, element in enumerate(a_recuperer):
            d = []
            for i, elem in enumerate(data_value[idx]):
                d.append(elem)
            d.append(element)
            data.append(d)

        domain = []
        for i, elem in enumerate(data_value.domain):
            domain.append(elem)
        domain.append(ContinuousVariable("ok"))
        out_data = Table(Domain(domain), data)
        if error == False:
            self.Outputs.out_data.send(out_data)


if __name__ == "__main__":
    from AnyQt.QtWidgets import QApplication
    app = QApplication(sys.argv)
    my_widget = OWApplyRules()
    my_widget.show()
    app.exec_()
