Description
-----------

A simple plugin that integrates glossa-interpreter with gedit3.
The currently active document can be executed by the interpreter by hitting `F5`.
Requires glossa-interpreter to be installed under `/usr/bin`.

Installation
------------

Just copy the files to `~/.local/share/gedit/plugins/`, restart gedit and 
enable the plugin from the `Edit - Preferences - Plugins` dialog.

Syntax highlighting
-------------------

To get syntax highlighting for ΓΛΩΣΣΑ, copy [this file](https://raw.github.com/cyberpython/lingua/master/sourceview-files/glossa.lang) to `/usr/share/gtksourceview-3.0/language-specs/` :

    sudo wget -P /usr/share/gtksourceview-3.0/language-specs/ https://raw.github.com/cyberpython/lingua/master/sourceview-files/glossa.lang

Restart gedit.


License
-------

Distributed under the terms of the [MIT license](http://www.opensource.org/licenses/mit-license.php).


