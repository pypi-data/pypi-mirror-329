from IPython.core.magic import Magics, magics_class, cell_magic, line_magic
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.display import display, SVG

@magics_class
class GraphvizAnywidgetMagic(Magics):
    def __init__(self, shell):
        super(GraphvizAnywidgetMagic, self).__init__(shell)
        self.widget_name = (
            None  # Store the widget variable name as an instance attribute
        )
        self.widget = None

    def _set_widget(self, w_name=""):
        w_name = w_name.strip()
        if w_name:
            self.widget_name = w_name
        self.widget = self.shell.user_ns[self.widget_name]
        # Perhaps add a test that it is a widget type, else None?
        # print(f"graphviz_magic object set to: {self.widget_name}")

    def _run_query(self, args, q):
        if args.widget_name:
            self._set_widget(args.widget_name)
        if self.widget is None:
            print(
                "Error: No widget / widget name set. Use %set_myAnywidget_object first to set the name."
            )
            return
        elif q:
            # Get the actual widget
            w = self.widget
            w.set_code_content(q)
            autorespond = bool(args.timeout or args.embed)
            if autorespond:
                timeout = args.timeout if args.timeout > 0 else 5
                w.blocking_reply(timeout)
                if w.svg:
                    display(SVG(w.svg))
                else:
                    display(f"No SVG?")

    @line_magic
    def setwidget(self, line):
        """Set the object name to be used in subsequent myAnywidget_magic calls."""
        self._set_widget(line)

    @cell_magic
    @magic_arguments()
    @argument("-w", "--widget-name", type=str, help="widget variable name")
    @argument(
        "-e",
        "--embed",
        action="store_true",
        help="Embed response from cell (not JupyterLite)",
    )
    @argument(
        "-t",
        "--timeout",
        type=float,
        default=0,
        help="timeout period on blocking response (default: 5)",
    )
    def graphviz_magic(self, line, cell):
        args = parse_argstring(self.graphviz_magic, line)
        return self._run_query(args, cell)

## %load_ext jupyter_anywidget_graphviz
## Usage: %%graphviz_magic -w x [where x is the widget object ]
