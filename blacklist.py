skipped_classes = [
    "Efl.Ui.Internal.Text.Interactive",
    "Efl.Canvas.Gesture_Manager",
    "Efl.Canvas.Gesture_Touch",
    "Efl.Canvas.Gesture_Tap",
    "Efl.Canvas.Gesture_Long_Tap",
    "Efl.Canvas.Gesture_Recognizer_Tap",
    "Efl.Canvas.Gesture_Recognizer_Long_Tap",
    "Efl.Canvas.Layout_Part_Invalid",
    "Efl.Canvas.Scene3d",
    "Efl.Canvas.Text",
    "Efl.Canvas.Vg.Object",
    "Efl.Canvas.Video",
    "Edje.Global",
    "Efl.Net.Ssl.Context",
    "Efl.Datetime.Manager",
    "Efl.Selection_Manager",
    "Elm_Actionslider.Part",
    "Elm_Bubble.Part",
    "Elm_Label.Part",
    "Efl.Ui.Model_State",
    "Efl.Ui.Popup_Part_Backwall",
    "Efl.Ui.View_List_Precise_Layouter",
    "Efl.Ui.Average_Model",
    "Efl.Ui.Exact_Model",
    "Efl.Ui.Homogeneous_Model",
    "Efl.Ui.Size_Model",
    "Efl.Ui.State_Model",
    "Efl.Ui.List_View_Precise_Layouter",
    "Efl.Ui.Internal_Text_Scroller",
    "Efl.Ui.Selection_Manager",
    "Efl.Ui.Spotlight.Manager_Plain",
    "Efl.Ui.Collection_Focus_Manager",
]

skipped_ns = [
    "Elm",
    "Ecore",
    "Ector",
    "Eio",
    "Eldbus",
    "Evas",
    "Efl.Io",
    "Efl.Net",
    "Efl.Net.Control",
    "Efl.Ui.Focus",
]


def is_skipped_class(eocls):
    if not eocls:
        return True

    return (
        eocls.type != eocls.type.REGULAR
        or eocls.name in skipped_classes
        or list(eocls.namespaces)[0] in skipped_ns
        or eocls.namespace in skipped_ns
        or eocls.name.endswith("Legacy")
    )
