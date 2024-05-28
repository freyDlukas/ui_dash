def main() -> None:
    import dash.callbacks  # noqa: F401

    from .app import app
    from .layout import render_layout

    app.layout = render_layout()

    app.run_server(
        debug=True,
        port=9999,
    )


if __name__ == "__main__":
    main()
