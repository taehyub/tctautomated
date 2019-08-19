"""List of classes and members to be skipped when generating the tests"""


SKIPPED_CLASSES = [
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

SKIPPED_NS = [
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


def should_skip_class(eocls):
    """Whether we should skip generating tests for this class"""
    if not eocls:
        return True

    return (
        eocls.type != eocls.type.REGULAR
        or eocls.name in SKIPPED_CLASSES
        or list(eocls.namespaces)[0] in SKIPPED_NS
        or eocls.namespace in SKIPPED_NS
        or eocls.name.endswith("Legacy")
    )


# List of members to be skipped.
#
# Format:
# (criteria, target_class, declaring_class, full member c name)
#
# - "*" can be used for wildcards for both criteria and member
# - Target class is the class being generated
# - Declaring class is the class declaring the member
#   - For events, it is the same as target class
#
# Currently, it skips only items for classes explicitly declared here.
# i.e. it will not skip items from parents of the declaring class.
SKIP_LIST = set(
    [
        ("*", "Efl.Ui.Popup", "Efl.Ui.Focus.Manager", "*"),
        ("*", "Efl.Ui.Popup", "Efl.Ui.Focus.Layer", "*"),
    ]
)


def should_skip_method(eocls, method, criteria):
    """Whether we should skip the given method"""
    c_name = method.full_c_name_get(method.type)
    target_class = eocls.name
    declaring_class = method.class_.name

    return query(criteria, target_class, declaring_class, c_name)


def should_skip_event(eocls, event, criteria):
    """Whether we should skip the given event"""
    c_name = event.name
    target_class = eocls.name
    declaring_class = target_class

    return query(criteria, target_class, declaring_class, c_name)


def query(criteria, target_class, declaring_class, c_name):
    """Checks if the given data is in the skip list"""

    queries = set(
        [
            (criteria, target_class, declaring_class, c_name),
            (criteria, target_class, declaring_class, "*"),
            ("*", target_class, declaring_class, c_name),
            ("*", target_class, declaring_class, "*"),
        ]
    )

    if not queries.isdisjoint(SKIP_LIST):
        print("Skipping", criteria, target_class, declaring_class, c_name)
        return True

    return False
