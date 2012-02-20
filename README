# Cobra Commander - Henchman
You mindless husk, you.


## Snakefiles
A snakefile is what is used to configure and run a Henchman build. A snakefile can be any arbitrary file or executable so long as it outputs valid JSON to stdout when it is invoked.

There is only one key/value that __must__ be in your snakfile JSON;

- `build`: an array of strings containing the steps required to build your project. These are executed serially.

However there are also a bunch of other optional properties that you can set in your snakefile to achieve different outcomes, here are a few;

- `environment`: an object whose keys/values are environment variables that should be set prior to any `build` steps being invoked.
- `hooks`:
  - `before_build`
  - `after_build`
  - `after_passing`
  - `after_failing`


## Extensions (notes for future spec)

Extensions come a in a bunch of different flavours, usually depending on the function that they provide.

Extensions may add extra abilities and functionality at certain registration points within the build process (eg; post build, during hooks, etc.)

If an extension needs configuration or params before being invoked at its registration point they can be passed in the snakefile as such;

    'hooks': {
      'before_build':[
        ['my_extension', ['args'], {'kwargs':'foo'}],
        ['my_other_extension', ['args']],
        ['etc']
      ]
    }
