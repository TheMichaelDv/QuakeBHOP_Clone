'''
5/14
Finally Main game loop XDDD

Basically the tick loop HAS to be separate from frametime so game logic can be run on a diff schedule than frametime
because this allows for unlimited frames and I can set things on a linear time scale. In addition, if a player lags, the game will still be logical.
http://gameprogrammingpatterns.com/game-loop.html for further reading

However I need to implement the running of the render function differently than what the module initally offers. 
I cannot modify the module itself as it will not update on your machine.
Its copy and pasted from moderngl_window.__init__.run_window_config()

Also cleaned up directories and files, wanted to do that forever. Branched as OLD so if you want 

FYI texturecube.py cannot be ran anymore run this file instead to execute texturecube.py

5/15
Problem: I am still limited by lag. The solution is to implement async processing.

My idea is to send Matrixs to the other process and then move them over here. Therefore We are not updating the positions every frame but whatever time we set in the other process.

Examples:
Render Process | Logic Process
Init()         | Init()
Waits()        | Sends first matrix
Renders Matrixs| 
Renders Matrixs|
Renders Matrixs| Sends next Matrix
Renders NEW Maxtrix|

As you can see the 2 frames since the last update, the render function renders the old matrix
The benefit of this is that if it lags, logic is not interuptted. Basically its client/server relationship
Also if the physics engine takes too long to process, the client will not see it in their frames but rather the delay of object processing.

For now however, I uncapped the framerates, so we are not vsync limited.
I will be giving the game 144 fps and leaving the rest to the logic engine.

SOLVED: A major problem I'm having is timing. If the game goes as fast as possible, then how to get the computer to sleep for about 10-15 milliseconds or less? time.sleep() is NOT accurate
5/17
Need to have two sleep functions, one to test if a conditon is met, 0.02s and one to test if 0.007s is met || gonna step around this issue by implmenting multi

5/23
Basic Multiprocessing Impmentation, Engine currently houses a process that does physics 
'''
from moderngl_window import *
import moderngl_window
from multiprocessing import Process, Queue
from queue import Empty, Full
from Resources.texturecube import Game
from Resources import logic
import time
from ctypes import windll
from ctypes.wintypes import UINT


def run(config_cls: WindowConfig, timer=None, args=None) -> None:

    setup_basic_logging(config_cls.log_level)
    #Taking in arguments
    parser = create_parser()
    #Custom Framerate Arguement
    parser.add_argument(
        '-fps',
        '--framerate',
        type=int,
        default=60,
        help='Framerate if vsync is disabled'
    )
    config_cls.add_arguments(parser)
    values = parse_args(args=args, parser=parser)
    config_cls.argv = values
    '''
    if values.window == "glfw":
        window_cls = glfw.Window
    else
        window_cls = get_local_window_cls(values.window)
    '''
    window_cls = get_local_window_cls(values.window)

    # Calculate window size
    size = values.size or config_cls.window_size
    size = int(size[0] * values.size_mult), int(size[1] * values.size_mult)

    # Resolve cursor
    show_cursor = values.cursor
    if show_cursor is None:
        show_cursor = config_cls.cursor

    #window config
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
    #Binding to our class
    window.config = config_cls(ctx=window.ctx, wnd=window, timer=timer)

    # Swap buffers once before staring the main loop.
    # This can trigged additional resize events reporting
    # a more accurate buffer size
    window.swap_buffers()
    window.set_default_viewport()

    #Calcuating Frametimes in Nanoseconds
    frametime = int(1/values.framerate * 900000000) if values.vsync is False and values.framerate != 60 else int((1/60))

    buffer = [Queue(2),Queue(1)]
    engine = Process(target=logic.physics, args=(buffer,))
    engine.start()

    delta = 0
    coords = {}

    kernel32 = windll.kernel32
    kernel32.timeBeginPeriod(UINT(1))

    timer.start()
    current_time = time.perf_counter_ns()
    while not window.is_closing:

        #busy wait function in order to not exceed the frametime, but pegs cpu at 100% looking into solutions, time.sleep is inaccurate up to 2-4ms too inaccurate.
        #need to set the timeBeginPeriod in timeapi.h to 1 ms, which is where ctypes come into play
        sleep = time.perf_counter_ns()
        while delta + (time.perf_counter_ns()-sleep) <= frametime:
            #sleep for 1 ms
            kernel32.Sleep(1)
        delta = time.perf_counter_ns()

        if window.config.clear_color is not None:
            window.clear(*window.config.clear_color)
        
        # Always bind the window framebuffer before calling render
        window.use()
        
        proj, camera = window.config.render(delta, delta)

        try:
            buffer[1].put((proj, camera), block=False)
        except Full:
            pass

        try:
            coords = buffer[0].get(block=False)
        except Empty:
            pass

        window.config.physics(delta, coords)

        if not window.is_closing:
            window.swap_buffers()

        delta = time.perf_counter_ns()-delta
    
    duration = (time.perf_counter_ns()-current_time)/1000000000
    window.destroy()
    if duration > 0:
        logger.info(
            "Duration: {0:.2f}s @ {1:.2f} FPS".format(
                duration, window.frames / duration
            )
        )
    kernel32.timeEndPeriod(UINT(1))
    buffer[1].put(True)
    engine.join()


if __name__ == "__main__":
    run(Game, args=('-vs','False','--window','glfw','-fps','120'))