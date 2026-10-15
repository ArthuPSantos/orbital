def get_stylesheet() -> str:
    return """
    QMainWindow {
        background-color: #070a0e;
    }

    QWidget {
        color: #d9e1e8;
        font-family: "Segoe UI";
        font-size: 13px;
    }

    #central_widget {
        background-color: #070a0e;
    }

    /* =========================
       HEADER
       ========================= */

    #brand {
        color: #f2f5f7;
        font-size: 25px;
        font-weight: 600;
        letter-spacing: 3px;
    }

    #subtitle {
        color: #687582;
        font-size: 10px;
        font-weight: 500;
        letter-spacing: 2px;
    }

    #system_status {
        color: #6fae8b;
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 1.5px;
    }
    
    /* =========================
       ANALYSIS SELECTORS
       ========================= */

    #analysis_selector {
        background-color: #0d131a;
        color: #7f8c98;
        border: 1px solid #202b35;
        border-radius: 4px;
        padding: 6px 10px;
        min-height: 16px;
        font-size: 9px;
        font-weight: 600;
        letter-spacing: 1px;
    }

    #analysis_selector:hover {
        background-color: #121a22;
        color: #b8c4ce;
        border-color: #2b3844;
    }

    #analysis_selector:checked {
        background-color: #18232d;
        color: #e1e8ed;
        border: 1px solid #3a4b5a;
    }

    #analysis_selector:checked:hover {
        background-color: #1b2833;
        color: #f0f4f7;
    }

    /* =========================
       PANELS
       ========================= */

    #panel,
    #simulation_panel {
        background-color: #0c1117;
        border: 1px solid #1b252e;
        border-radius: 7px;
    }

    #panel {
        min-width: 315px;
        max-width: 380px;
    }

    #simulation_panel {
        background-color: #080d12;
    }

    /* =========================
       SCROLL AREA
       ========================= */

    QScrollArea {
        background-color: #0b0f14;
        border: none;
    }

    QScrollArea > QWidget {
        background-color: #0b0f14;
    }

    QScrollArea > QWidget > QWidget {
        background-color: #0b0f14;
    }

    #experiment_content {
        background-color: #0b0f14;
    }

    /* =========================
       SECTION TITLES
       ========================= */

    #section_title {
        color: #e8edf2;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 1.5px;
    }

    #description {
        color: #687582;
        font-size: 11px;
    }

    #field_title {
        color: #7f8c98;
        font-size: 9px;
        font-weight: 600;
        letter-spacing: 1.2px;
    }

    #separator {
        background-color: #1b252e;
        border: none;
        max-height: 1px;
    }
        /* =========================
       MAIN TABS
       ========================= */

    QTabWidget::pane {
        background-color: #080d12;
        border: 1px solid #1b252e;
        border-radius: 7px;
        top: -1px;
    }

    QTabBar::tab {
        background-color: #0b0f14;
        color: #66737f;
        border: 1px solid transparent;
        border-bottom: 1px solid #1b252e;
        padding: 9px 22px;
        min-width: 110px;
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 1.2px;
    }

    QTabBar::tab:hover {
        background-color: #10161d;
        color: #aebbc5;
    }

    QTabBar::tab:selected {
        background-color: #10161d;
        color: #e6edf3;
        border: 1px solid #27313c;
        border-bottom: 1px solid #10161d;
    }

    QTabBar::tab:!selected {
        margin-top: 2px;
    }
    /* =========================
       COMBO BOX
       ========================= */

    QComboBox {
        background-color: #10161d;
        color: #e6edf3;
        border: 1px solid #27313c;
        border-radius: 5px;
        padding: 7px 9px;
        min-height: 18px;
    }

    QComboBox:hover {
        background-color: #121a22;
        border: 1px solid #3a4b5b;
    }

    QComboBox:focus {
        background-color: #10161d;
        color: #ffffff;
        border: 1px solid #4c6478;
    }

    QComboBox:disabled {
        background-color: #0b0f14;
        color: #66717c;
        border: 1px solid #1c252e;
    }

    QComboBox::drop-down {
        background-color: #10161d;
        border: none;
        width: 28px;
    }

    QComboBox::down-arrow {
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 5px solid #8b98a5;
        margin-right: 8px;
    }

    QComboBox QAbstractItemView {
        background-color: #10161d;
        color: #e6edf3;
        border: 1px solid #27313c;
        outline: none;
        selection-background-color: #263746;
        selection-color: #ffffff;
    }

    QComboBox QAbstractItemView::item {
        background-color: #10161d;
        color: #e6edf3;
        padding: 7px 10px;
        min-height: 24px;
    }

    QComboBox QAbstractItemView::item:hover {
        background-color: #1a2732;
        color: #ffffff;
    }

    QComboBox QAbstractItemView::item:selected {
        background-color: #263746;
        color: #ffffff;
    }

    /* =========================
       DOUBLE SPIN BOX
       ========================= */

    QDoubleSpinBox {
        background-color: #10161d;
        color: #e6edf3;
        border: 1px solid #27313c;
        border-radius: 5px;
        padding: 7px 9px;
        min-height: 18px;
        selection-background-color: #314454;
        selection-color: #ffffff;
    }

    QDoubleSpinBox:hover {
        background-color: #121a22;
        border: 1px solid #3a4b5b;
    }

    QDoubleSpinBox:focus {
        background-color: #10161d;
        color: #ffffff;
        border: 1px solid #4c6478;
    }

    QDoubleSpinBox:disabled {
        background-color: #0b0f14;
        color: #66717c;
        border: 1px solid #1c252e;
    }

    /* =========================
       BODY CARDS
       ========================= */

    #body_card {
        background-color: #10161d;
        border: 1px solid #202b35;
        border-radius: 5px;
    }

    #body_card_category {
        color: #66737f;
        font-size: 8px;
        font-weight: 600;
        letter-spacing: 1.3px;
    }

    #body_card_name {
        color: #dce4ea;
        font-size: 12px;
        font-weight: 500;
    }

    /* =========================
       RUN BUTTON
       ========================= */

    #run_button {
        background-color: #18242e;
        color: #dfe7ed;
        border: 1px solid #334451;
        border-radius: 5px;
        padding: 10px 14px;
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 1.2px;
    }

    #run_button:hover {
        background-color: #21313e;
        border: 1px solid #496172;
        color: #ffffff;
    }

    #run_button:pressed {
        background-color: #111b23;
        border: 1px solid #536c7d;
    }

    #run_button:disabled {
        background-color: #0e141a;
        color: #596570;
        border: 1px solid #202a33;
    }

    /* =========================
       SIMULATION CANVAS
       ========================= */

    #simulation_canvas {
        background-color: #05080b;
        border: 1px solid #151e26;
        border-radius: 5px;
    }

    #coordinates {
        color: #53616d;
        font-family: "Consolas";
        font-size: 9px;
        letter-spacing: 0.8px;
    }

    /* =========================
       METRICS
       ========================= */

    #metrics {
        background-color: #0c1117;
        border: 1px solid #1b252e;
        border-radius: 7px;
    }

    #metric_title {
        color: #66737f;
        font-size: 8px;
        font-weight: 600;
        letter-spacing: 1.2px;
    }

    #metric_value {
        color: #dce4ea;
        font-family: "Consolas";
        font-size: 12px;
        font-weight: 500;
    }
    """