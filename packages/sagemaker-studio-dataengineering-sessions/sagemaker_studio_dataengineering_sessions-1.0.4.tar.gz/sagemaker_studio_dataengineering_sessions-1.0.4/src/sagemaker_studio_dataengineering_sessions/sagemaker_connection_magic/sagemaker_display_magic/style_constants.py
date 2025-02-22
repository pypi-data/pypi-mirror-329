#STYLING CONSTANTS
ROW_STYLE = {
    "text-align": "center",
    "vertical-align": "middle",
    "width": "100%"
}

TEXT_STYLE = {
    "text-align": "center",
    "vertical-align": "middle",
}

GRAPH_STYLE = {
    "width": "98%",
    "height": "98%",
    "vertical-align": "middle",
}

PAGE_STYLE = {
    "height":"100%",
    "max_height":"100%",
    "width":"100%",
    "max_width":"100%",
    "margin-bottom":"1rem",
    "background-color":"transparent",
    "scrollbar-color":"grey transparent",
    "overflow-x":"scroll"
}

TABLE_STYLESHEET = """
    <style>* {
        font-family: var(--jp-content-font-family);
        font-size: var(--jp-code-font-size);
    }

    .table {
        width: 100%;
        max-width: 100%;
        margin-bottom: 1rem;
        background-color: transparent;
        border-collapse: collapse;
    }

    .table td,
    .table th {
        padding: .75rem;
        vertical-align: top;
        border-top: var(--jp-border-width) solid var(--jp-border-color0)
    }

    .table thead th {
        vertical-align: bottom;
        border-bottom: var(--jp-border-width) solid var(--jp-border-color0)
    }

    .table tbody+tbody {
        border-top: var(--jp-border-width) solid var(--jp-border-color0)
    }

    .table .table {
        background-color: var(--jp-rendermime-table-row-background)
    }

    .table-sm td,
    .table-sm th {
        padding: .3rem
    }

    .table-bordered {
        border: var(--jp-border-width) solid var(--jp-border-color0)
    }

    .table-bordered td,
    .table-bordered th {
        border: var(--jp-border-width) solid var(--jp-border-color0)
    }

    .table-bordered thead td,
    .table-bordered thead th {
        border-bottom-width: var(--jp-border-width)
    }

    .table-striped tbody tr:nth-of-type(odd) {
        background-color: var(--jp-rendermime-table-row-background)
    }

    .table-hover tbody tr:hover {
        background-color: var(--jp-rendermime-table-row-hover-background)
    }

    .table-primary,
    .table-primary>td,
    .table-primary>th {
        background-color: var(--jp-rendermime-table-row-background)
    }

    .table-hover .table-primary:hover {
        background-color: var(--jp-rendermime-table-row-hover-background)
    }

    .table-hover .table-primary:hover>td,
    .table-hover .table-primary:hover>th {
        background-color: var(--jp-rendermime-table-row-hover-background)
    }

    .table-secondary,
    .table-secondary>td,
    .table-secondary>th {
        background-color: var(--jp-rendermime-table-row-background)
    }

    .table-hover .table-secondary:hover {
        background-color: var(--jp-rendermime-table-row-hover-background)
    }

    .table-hover .table-secondary:hover>td,
    .table-hover .table-secondary:hover>th {
        background-color: var(--jp-rendermime-table-row-hover-background)
    }

    .table-success,
    .table-success>td,
    .table-success>th {
        background-color: var(--jp-rendermime-table-row-background)
    }

    .table-hover .table-success:hover {
        background-color: var(--jp-rendermime-table-row-hover-background)
    }

    .table-hover .table-success:hover>td,
    .table-hover .table-success:hover>th {
        background-color: var(--jp-rendermime-table-row-hover-background)
    }

    .table-info,
    .table-info>td,
    .table-info>th {
        background-color: var(--jp-rendermime-table-row-background)
    }

    .table-hover .table-info:hover {
        background-color: var(--jp-rendermime-table-row-hover-background)
    }

    .table-hover .table-info:hover>td,
    .table-hover .table-info:hover>th {
        background-color: var(--jp-rendermime-table-row-hover-background)
    }

    .table-warning,
    .table-warning>td,
    .table-warning>th {
        background-color: var(--jp-rendermime-table-row-background)
    }

    .table-hover .table-warning:hover {
        background-color: var(--jp-rendermime-table-row-hover-background)
    }

    .table-hover .table-warning:hover>td,
    .table-hover .table-warning:hover>th {
        background-color: var(--jp-rendermime-table-row-hover-background)
    }

    .table-danger,
    .table-danger>td,
    .table-danger>th {
        background-color: var(--jp-rendermime-table-row-background)
    }

    .table-hover .table-danger:hover {
        background-color: var(--jp-rendermime-table-row-hover-background)
    }

    .table-hover .table-danger:hover>td,
    .table-hover .table-danger:hover>th {
        background-color: var(--jp-rendermime-table-row-hover-background)
    }

    .table-light,
    .table-light>td,
    .table-light>th {
        background-color: var(--jp-rendermime-table-row-background)
    }

    .table-hover .table-light:hover {
        background-color: var(--jp-rendermime-table-row-hover-background)
    }

    .table-hover .table-light:hover>td,
    .table-hover .table-light:hover>th {
        background-color: var(--jp-rendermime-table-row-hover-background)
    }

    .table-dark,
    .table-dark>td,
    .table-dark>th {
        background-color: var(--jp-rendermime-table-row-background)
    }

    .table-hover .table-dark:hover {
        background-color: var(--jp-rendermime-table-row-hover-background)
    }

    .table-hover .table-dark:hover>td,
    .table-hover .table-dark:hover>th {
        background-color: var(--jp-rendermime-table-row-hover-background)
    }

    .table-active,
    .table-active>td,
    .table-active>th {
        background-color: var(--jp-rendermime-table-row-background)
    }

    .table-hover .table-active:hover {
        background-color: var(--jp-rendermime-table-row-hover-background)
    }

    .table-hover .table-active:hover>td,
    .table-hover .table-active:hover>th {
        background-color: var(--jp-rendermime-table-row-hover-background)
    }

    .table .thead-dark th {
        color: var(--jp-content-font-color1);
        background-color: var(--jp-rendermime-table-row-background);
        border-color: var(--jp-border-color0)
    }

    .table .thead-light th {
        color: var(--jp-content-font-color1);
        background-color: var(--jp-rendermime-table-row-background);
        border-color: var(--jp-border-color0)
    }

    .table-dark {
        color: var(--jp-content-font-color1);
        background-color: var(--jp-rendermime-table-row-background)
    }

    .table-dark td,
    .table-dark th,
    .table-dark thead th {
        border-color: var(--jp-border-color0)
    }

    .table-dark.table-bordered {
        border: 0
    }

    .table-dark.table-striped tbody tr:nth-of-type(odd) {
        background-color: var(--jp-rendermime-table-row-background)
    }

    .table-dark.table-hover tbody tr:hover {
        background-color: var(--jp-rendermime-table-row-hover-background)
    }

    @media (max-width:575.98px) {
        .table-responsive-sm {
            display: block;
            width: 100%;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            -ms-overflow-style: -ms-autohiding-scrollbar
        }

        .table-responsive-sm>.table-bordered {
            border: 0
        }
    }

    @media (max-width:767.98px) {
        .table-responsive-md {
            display: block;
            width: 100%;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            -ms-overflow-style: -ms-autohiding-scrollbar
        }

        .table-responsive-md>.table-bordered {
            border: 0
        }
    }

    @media (max-width:991.98px) {
        .table-responsive-lg {
            display: block;
            width: 100%;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            -ms-overflow-style: -ms-autohiding-scrollbar
        }

        .table-responsive-lg>.table-bordered {
            border: 0
        }
    }

    @media (max-width:1199.98px) {
        .table-responsive-xl {
            display: block;
            width: 100%;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            -ms-overflow-style: -ms-autohiding-scrollbar
        }

        .table-responsive-xl>.table-bordered {
            border: 0
        }
    }

    .table-responsive {
        display: block;
        width: 100%;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        -ms-overflow-style: -ms-autohiding-scrollbar
    }

    .table-responsive>.table-bordered {
        border: 0
    }

    </style>
"""

TEXT_STYLESHEET = """
    :host {
        --design-primary-text-color: var(--jp-content-font-color1);
        --design-secondary-text-color: var(--jp-content-font-color1);
        --design-background-text-color: var(--jp-content-font-color1);
        --design-surface-text-color: var(--jp-content-font-color1);
        font-family: var(--jp-content-font-family);
        font-size: var(--jp-code-font-size);
    }
"""

BUTTON_STYLESHEET = """
    :host(.outline) .bk-btn-light {
        border-color: var(--jp-inverse-layout-color0);
    }

    :host(.outline) .bk-btn-light:hover {
        background-color: var(--jp-inverse-layout-color0);
        color: var(--jp-ui-inverse-font-color0);
    }
"""

SELECT_STYLESHEET = """
    select:not([multiple]).bk-input, select:not([size]).bk-input {
        background-image: url('data:image/svg+xml;utf8,<svg version="1.1" viewBox="0 0 25 20" xmlns="http://www.w3.org/2000/svg"><path d="M 0,0 25,0 12.5,20 Z" fill="white" stroke="black" stroke-width="3"/></svg>')
    }
"""

GENERAL_HEIGHT = 1050
SUMMARY_TEXT_HEIGHT = 35
PLOT_HEIGHT = 225
PLOT_WIDTH = 300
HALF_SELECT_WIDTH = 150

PLOT_COLOR = "#0072b5"
TEXT_COLOR = "#ffffff"
AXIS_COLOR = "#999"

ECHART_TEMPLATE = "default"

