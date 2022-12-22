SLIDER = ("""
        QSlider::groove:horizontal {
        border: 1px solid #bbb;
        background: white;
        height: 10px;
        border-radius: 4px;
        }

        QSlider::sub-page:horizontal {

        background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #fff, stop: 0.4999 #eee, stop: 0.5 #ddd, stop: 1 #eee );
        border: 1px solid #777;
        height: 10px;
        border-radius: 4px;
        }

        QSlider::add-page:horizontal {
        background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #78d, stop: 0.4999 #46a, stop: 0.5 #45a, stop: 1 #238 );
        border: 1px solid #777;
        height: 10px;
        border-radius: 4px;
        }

        QSlider::handle:horizontal {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #eee, stop:1 #ccc);
        border: 1px solid #777;
        width: 13px;
        margin-top: -2px;
        margin-bottom: -2px;
        border-radius: 4px;
        }

        QSlider::handle:horizontal:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #fff, stop:1 #ddd);
        border: 1px solid #444;
        border-radius: 4px;
        }

        QSlider::sub-page:horizontal:disabled {
        background: #bbb;
        border-color: #999;
        }

        QSlider::add-page:horizontal:disabled {
        background: #eee;
        border-color: #999;
        }

        QSlider::handle:horizontal:disabled {
        background: #eee;
        border: 1px solid #aaa;
        border-radius: 4px;
        }
        """)

FORWARD_BUTTON  = ("""
        background-color: #155644;
        border: 1px solid rgba(27, 31, 35, .15);
        border-radius: 6px;
        color: #fff;
        font-family: -apple-system,system-ui,"Segoe UI",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji";
        font-size: 14px;
        font-weight: 600;
        line-height: 20px;
        padding: 6px 16px;
        position: relative;
        text-align: center;
        text-decoration: none;
        vertical-align: middle;
        white-space: nowrap;
        """)

BACKWARD_BUTTON  = ("""
        background-color: #f94449;
        border: 1px solid rgba(27, 31, 35, .15);
        border-radius: 6px;
        color: #fff;
        font-family: -apple-system,system-ui,"Segoe UI",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji";
        font-size: 14px;
        font-weight: 600;
        line-height: 20px;
        padding: 6px 16px;
        position: relative;
        text-align: center;
        text-decoration: none;
        vertical-align: middle;
        white-space: nowrap;
        """)

DIAL  = ("""
        
        """)

BASIC_BUTTON = ("""
        appearance: none;
        background-color: #FAFBFC;
        border: 1px solid rgba(27, 31, 35, 0.15);
        border-radius: 6px;
        box-shadow: rgba(27, 31, 35, 0.04) 0 1px 0, rgba(255, 255, 255, 0.25) 0 1px 0 inset;
        box-sizing: border-box;
        color: #24292E;
        cursor: pointer;
        display: inline-block;
        font-family: -apple-system, system-ui, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
        font-size: 14px;
        font-weight: 500;
        line-height: 20px;
        list-style: none;
        padding: 6px 16px;
        position: relative;
        transition: background-color 0.2s cubic-bezier(0.3, 0, 0.5, 1);
        user-select: none;
        -webkit-user-select: none;
        touch-action: manipulation;
        vertical-align: middle;
        white-space: nowrap;
        word-wrap: break-word;
""")

LINE_EDIT = ("""
        background-color: #ffffff;
        border-radius: 5px;
        color: darkgray;
        text-align: center;
        font-size: 14px;
        border: 1px solid rgba(27, 31, 35, .15);
        line-height: 20px;
        padding: 6px 0px;
""")

TREE = ("""

        QTreeView::branch:has-siblings:!adjoins-item {
            
        }

        QTreeView::branch:has-siblings:adjoins-item {
        }

        QTreeView::branch:!has-children:!has-siblings:adjoins-item {
        }

        QTreeView::branch:has-children:!has-siblings:closed,
        QTreeView::branch:closed:has-children:has-siblings {
                border-image: none;
        }

        QTreeView::branch:open:has-children:!has-siblings,
        QTreeView::branch:open:has-children:has-siblings  {
                border-image: none;
        }

""")
