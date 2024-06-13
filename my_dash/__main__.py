def main() -> None:
    from my_dash.callbacks import Input, Output, State, dash_table  # noqa: F401

    from .app import app
    from .layout_new import render_layout

    app.layout = render_layout()

    app.run_server(
        debug=True,
        port=9999,
    )


if __name__ == "__main__":
    main()
