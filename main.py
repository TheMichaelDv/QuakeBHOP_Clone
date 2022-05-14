'''
Finally Main game loop XDDD

Basically the tick loop HAS to be separate from frametime so game logic can be run on a diff schedule than frametime
because this allows for unlimited frames and I can set things on a linear time scale. In addition, if a player lags, the game will still be logical.
http://gameprogrammingpatterns.com/game-loop.html for further reading

However I need to implement the running of the render function differently than what the module initally offers. 
I cannot modify the module itself as it will not update on your machine.
Its copy and pasted from moderngl_window.__init__.run_window_config()

Also cleaned up directories and files, wanted to do that forever

FYI texturecube.py cannot be ran anymore run this file instead to execute texturecube.py
'''

from moderngl_window import *
from moderngl_window.context.base import WindowConfig, BaseWindow
from moderngl_window.timers.clock import Timer
from moderngl_window.conf import settings
from moderngl_window.utils.module_loading import import_string
from Resources.texturecube import Game


def run(config_cls: WindowConfig, timer=None, args=None) -> None:
    """
    Run an WindowConfig entering a blocking main loop

    Args:
        config_cls: The WindowConfig class to render
    Keyword Args:
        timer: A custom timer instance
        args: Override sys.args
    """
    setup_basic_logging(config_cls.log_level)
    parser = create_parser()
    config_cls.add_arguments(parser)
    values = parse_args(args=args, parser=parser)
    config_cls.argv = values
    window_cls = get_local_window_cls(values.window)

    # Calculate window size
    size = values.size or config_cls.window_size
    size = int(size[0] * values.size_mult), int(size[1] * values.size_mult)

    # Resolve cursor
    show_cursor = values.cursor
    if show_cursor is None:
        show_cursor = config_cls.cursor

    window = window_cls(
        title=config_cls.title,
        size=size,
        fullscreen=config_cls.fullscreen or values.fullscreen,
        resizable=values.resizable
        if values.resizable is not None
        else config_cls.resizable,
        gl_version=config_cls.gl_version,
        aspect_ratio=config_cls.aspect_ratio,
        vsync=values.vsync if values.vsync is not None else config_cls.vsync,
        samples=values.samples if values.samples is not None else config_cls.samples,
        cursor=show_cursor if show_cursor is not None else True,
    )
    window.print_context_info()
    activate_context(window=window)
    timer = timer or Timer()
    window.config = config_cls(ctx=window.ctx, wnd=window, timer=timer)

    # Swap buffers once before staring the main loop.
    # This can trigged additional resize events reporting
    # a more accurate buffer size
    window.swap_buffers()
    window.set_default_viewport()

    timer.start()

    while not window.is_closing:
        #GAME LOOP
        current_time, delta = timer.next_frame()

        if window.config.clear_color is not None:
            window.clear(*window.config.clear_color)

        # Always bind the window framebuffer before calling render
        window.use()
        window.render(current_time, delta)
        if not window.is_closing:
            window.swap_buffers()

    _, duration = timer.stop()
    window.destroy()
    if duration > 0:
        logger.info(
            "Duration: {0:.2f}s @ {1:.2f} FPS".format(
                duration, window.frames / duration
            )
        )


if __name__ == "__main__":
    run(Game)