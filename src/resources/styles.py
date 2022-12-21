SLIDER = ("""
        QSlider::groove:horizontal {
        border: 1px solid #999999;
        height: 15px;
        border-radius: 9px;
        }

        QSlider::add-page:qlineargradient {
        background: lightgrey;
        border-top-right-radius: 9px;
        border-bottom-right-radius: 9px;
        border-top-left-radius: 0px;
        border-bottom-left-radius: 0px;
        }

        QSlider::sub-page:qlineargradient {
        background: #1f77b4;
        border-top-right-radius: 0px;
        border-bottom-right-radius: 0px;
        border-top-left-radius: 9px;
        border-bottom-left-radius: 9px;
        }
        """)

FORWARD_BUTTON  = ("""
        background-color: #2ea44f;
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
        background-color: white;
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
