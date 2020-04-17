# -*- coding: utf-8 -*-
def bg_editor(background, overlay):
    copy_background = background.copy()
    copy_background.paste(overlay, (0, 0), overlay)

    return copy_background
