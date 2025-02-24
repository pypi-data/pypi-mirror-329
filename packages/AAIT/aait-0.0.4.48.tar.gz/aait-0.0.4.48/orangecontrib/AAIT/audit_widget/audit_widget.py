import os
import sys
from Orange.data import Table, Domain, StringVariable,ContinuousVariable
from AnyQt.QtWidgets import QApplication
from AnyQt.QtCore import QEventLoop

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\","/"):
     from Orange.widgets.orangecontrib.AAIT.audit_widget import widgets_model, widget_optimisation, widget_mpnet_create_embeddings, widget_queryllm, widget_traduction, widget_spacy_md_fr_lemmatizer, widget_optimisationselection, widget_4all, widget_edit_table
else:
     from orangecontrib.AAIT.audit_widget import widgets_model, widget_optimisation, widget_mpnet_create_embeddings, widget_queryllm, widget_traduction, widget_spacy_md_fr_lemmatizer, widget_optimisationselection, widget_4all, widget_edit_table


if __name__ == "__main__":
    exit = False
    erreur = []
    if widgets_model.check_models() != 0: # Don't run online
        erreur.append("widgets_model \n")
        if exit == True:
            exit(1)

    if widget_optimisation.check_widget_optimisation() != 0:
        erreur.append("widget_optimisation \n")
        if exit == True:
            exit(1)

    if widget_optimisationselection.check_widget_optimisationselection() != 0:
        erreur.append("widget_optimisation_selection \n")
        if exit == True:
            exit(1)

    if widget_mpnet_create_embeddings.check_widget_mpnet_create_embeddings() != 0:
        erreur.append("widget_mpnet_create_embeddings \n")
        if exit == True:
            exit(1)

    if widget_4all.check_widget_llm4all() != 0:
        erreur.append("widget_llm4all \n")
        if exit == True:
            exit(1)

    if widget_queryllm.check_widget_solar_queryllm() != 0:
        erreur.append("widget_queryllm \n")
        if exit == True:
            exit(1)

    if widget_traduction.check_widget_traduction() != 0:
        erreur.append("widget_traduction \n")
        if exit == True:
            exit(1)

    if widget_spacy_md_fr_lemmatizer.check_widget_lemmes() != 0:
        erreur.append("widget_spacy_md_fr_lemmatizer \n")
        if exit == True:
            exit(1)

    if widget_edit_table.check_widget_edit_table() != 0:
        erreur.append("widget_edit_table  \n")
        if exit == True:
            exit(1)

    if len(erreur) != 0:
        print("\n")
        print("L'audit des widgets a été réalisé avec success")
    else:
        print("erreur dans les widgets suivants : \n")
        print(erreur)
    exit(0)