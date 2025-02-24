import axinite.tools as axtools
import axinite as ax
from vpython import *
from itertools import cycle
import os, signal, time, threading
  
def to_vec(v): 
    return vec(v[0], v[1], v[2])
def to_vec_cartesian(v):
    return vec(v.x.value, v.y.value, v.z.value)

def vpython_frontend(args: axtools.AxiniteArgs, mode: str, **kwargs):
    """
    Initializes the VPython frontend for visualizing the simulation.

    Args:
        args (axtools.AxiniteArgs): The arguments for the simulation.
        mode (str): The mode of the frontend. Can be 'live', 'run', or 'show'.
        **kwargs: Additional keyword arguments for the frontend.

    Raises:
        Exception: If the mode is not 'live', 'run', or 'show'.

    Returns:
        function: A function to update the visualization in 'live' or 'run' mode.
        function: A function to stop the visualization in 'live' or 'run' mode.
    """
    if mode == "live" or mode == "run":
        if "s" not in kwargs or kwargs["s"] == -1:
            n_timesteps = ax.timesteps(args.limit, args.delta)
            kwargs["s"] = ceil((1 / abs(2 * sin(n_timesteps))) * log(n_timesteps / args.delta))
        return vpython_live(args, **kwargs)
    elif mode == "show":
        return vpython_static(args, **kwargs)
    
def vpython_live(args: axtools.AxiniteArgs, s=1):
    if args.rate is None:
        args.rate = 100
    if args.radius_multiplier is None:
        args.radius_multiplier = 1
    if args.retain is None:
       args.retain = 200

    scene = canvas(title=args.name)
    scene.select()

    colors = cycle([color.red, color.blue, color.green, color.orange, color.purple, color.yellow])

    global pause
    pause = False
    def pause_handler():
        global pause
        pause = not pause

    global _rate
    _rate = args.rate
    def rate_hander(evt):
        global _rate
        _rate = evt.value

    global _s
    _s = s
    def s_handler(evt):
        global _s
        _s = int(10 ** evt.value)

    button(text='Pause', bind=pause_handler, pos=scene.caption_anchor)
    slider(bind=rate_hander, min=1, max=1000, value=+_rate, step=1, right=15, length=300, pos=scene.caption_anchor)
    wtext(text='Rate Slider', pos=scene.caption_anchor)
    slider(bind=s_handler, min=0, max=2, value=log10(_s), step=0.01, right=15, length=300, pos=scene.caption_anchor)
    wtext(text='S Value Slider', pos=scene.caption_anchor)

    spheres = {}
    labels = {}
    lights = {}

    for body in args.bodies:
        body_color = axtools.string_to_color(body.color, "vpython") if body.color != "" else next(colors)
        body_retain = body.retain if body.retain != None else args.retain
        spheres[body.name] = sphere(pos=to_vec(body.r(0)), radius=body.radius * args.radius_multiplier, color=body_color, make_trail=True, retain=body_retain, interval=10)
        labels[body.name] = label(pos=spheres[body.name].pos, text=body.name, xoffset=15, yoffset=15, space=30, height=10, border=4, font='sans')
        if body.light == True: 
            lights[body.name] = local_light(pos=to_vec(body.r(0)), color=body_color)
            attach_light(spheres[body.name], lights[body.name])

    def fn(bodies, t, **kwargs):
        if kwargs["n"] % _s == 0: 
            bodies = ax.create_outer_bodies(bodies, kwargs["limit"], kwargs["delta"])
            global _rate, pause
            rate(_rate)
            for body in bodies:
                spheres[body.name].pos = to_vec(body.r(kwargs["n"]))
                labels[body.name].pos = spheres[body.name].pos
                try: lights[body.name].pos = spheres[body.name].pos
                except: pass
        if kwargs['n'] % 200 == 1: print(f"t = {t}, n = {kwargs['n']}, s = {_s}, rate = {_rate}", end='\r')
        if pause: 
            while pause: rate(10)

    return fn, lambda: os.kill(os.getpid(), signal.SIGINT)

def vpython_static(args: axtools.AxiniteArgs):
    if args.rate is None:
        args.rate = 100
    if args.radius_multiplier is None:
        args.radius_multiplier = 1
    if args.retain is None:
       args.retain = 200
       
    scene = canvas(title=args.name)
    scene.select()

    colors = cycle([color.red, color.blue, color.green, color.orange, color.purple, color.yellow])

    def fn1(body: axtools.Body):
        body_color = axtools.string_to_color(body.color, "vpython") if body.color != "" else next(colors)
        
        label(pos=to_vec(body.r(0)), text=body.name, xoffset=15, yoffset=15, space=30, height=10, border=4, font='sans', color=body_color)
        curve(pos=[to_vec(r) for r in body.rs], color=body_color)
        sphere(pos=to_vec(body.r(0)), radius=body.radius * args.radius_multiplier * body.radius_multiplier, color=body_color, opacity=0.2, make_trail=False)

    def exit_func():
        os.kill(os.getpid(), signal.SIGINT)

    def fn2():
        threading.Thread(target=lambda: time.sleep(1), daemon=True).start()
        signal.signal(signal.SIGINT, lambda *args, **kwargs: exit_func())
        while True: 
            rate(10)
            time.sleep(0.1)

    return fn1, fn2, lambda: exit_func()