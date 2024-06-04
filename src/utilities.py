import os

import configs



def clear_item(item):
    if hasattr(item, 'layout'):
        if callable(item.layout):
            layout = item.layout()
    else:
        layout = None

    if hasattr(item, 'widget'):
        if callable(item.widget):
            widget = item.widget()
    else:
        widget = None

    if widget:
        widget.setParent(None)
    elif layout:
        for i in reversed(range(layout.count())):
            clear_item(layout.itemAt(i))



def adjust_path(path: str):
    return os.path.join(configs.BASE_DIR, path)
