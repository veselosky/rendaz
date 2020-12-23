# rendaz

"rendaz" is a suite of tools I use to automate my production pipeline
for producing [Ren'Py](https://renpy.org) games and image renders from
[DAZ Studio](https://www.daz3d.com/) (and maybe later Blender).

It should work fine under MacOS (on Intel processors) and Linux, but I
run it in Windows under WSL 2. If you're a Python developer, you can
probably figure out how to set it up. If you're not and you want to use
it yourself, let me know and I will document the setup instructions.
However, I don't anticipate many people will find this useful. It's
written with an audience of one (me) in mind.

## Task List

[ ] Write routines to translate between WSL Posix and Windows paths.

## Production

The Production app is your production manager. It organizes all your
projects, generates your "virtual call sheets" and shot lists, and
tracks your production tasks.

### Models Used

- Project: Holds metadata for a project and acts as the central
  organizing umbrella for other stuff.
- Location: A Location is any "filming location" corresponding to a DAZ
  Studio scene or scene subset file. I would prefer this be called a
  "Set" as in movie set, but "set" is a reserved word in Python.
- Character: A Character corresponds to a DAZ Studio Figure that has
  been prepared for use in a scene. This includes not only the Figure,
  but also the hair, and a list of presets applied to both, typically
  saved as a scene subset file. If a Character's hair or make-up needs
  to change from scene to scene, these can be stored in multiple scene
  subset files.
- Shot: A Shot is any image or animation. It tracks both the input
  files used to create the shot, and the output files of the render.
  Shots have a many to many relationship with Sets and Characters.
- Screenplay: Screenplay objects represent text files containing the
  screenplay (in the specific text format produced by Scrivener). Any
  number of screenplays may be associated with a Project.
