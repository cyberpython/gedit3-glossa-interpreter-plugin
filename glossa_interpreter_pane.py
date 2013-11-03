# coding=UTF-8
'''
Copyright (C) 2013 Georgios Migdos <cyberpython@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
from gi.repository import GObject, Gtk, Gedit, Vte, GLib
import os.path, tempfile

MENU_XML = """<ui>
<menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
      <placeholder name="ToolsOps_3">
        <menuitem name="GlossaInterpreterPaneExecAction" action="GlossaInterpreterPaneExecAction"/>
      </placeholder>
    </menu>
</menubar>
</ui>"""


class GlossaInterpreterPanePlugin(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "GlossaInterpreterPanePlugin"
    window = GObject.property(type=Gedit.Window)
   
    def __init__(self):
        GObject.Object.__init__(self)
    
    def _add_ui(self):
        self._add_menuitem()
        self._add_bottom_pane()
   
    def _add_bottom_pane(self):
        icon = Gtk.Image()
        icon.set_from_icon_name("gnome-terminal", Gtk.IconSize.MENU)
        self._terminal = Vte.Terminal()
        self._terminal.connect("child-exited", lambda term: self.window.get_active_view().grab_focus())
        panel = self.window.get_bottom_panel()
        panel.add_item(self._terminal, "GlossaInterpreterPane", "Glossa Interpreter", icon)
#        panel.activate_item(self._terminal)
        self._terminal.show_all()
    
    def _add_menuitem(self):
        manager = self.window.get_ui_manager()
        self._actions = Gtk.ActionGroup("GlossaInterpreterPaneActions")
        self._actions.add_actions([
                ('GlossaInterpreterPaneExecAction', Gtk.STOCK_INFO, "Execute with glossa-interpreter", 
                'F5', "Execute with glossa-interpreter.", 
                self.on_exec_action_activate)
        ]);
        manager.insert_action_group(self._actions)
        self._ui_merge_id = manager.add_ui_from_string(MENU_XML)
        manager.ensure_update()
        
    def do_activate(self):
        self._add_ui()

    def do_deactivate(self):
        self._remove_ui()

    def do_update_state(self):
        pass
    
    def on_exec_action_activate(self, action, data=None):
        self.exec_active_document()
                    
    def exec_active_document(self):
        document = self.window.get_active_document()
        view = self.window.get_active_view()
        if(view and document):
            buf = view.get_buffer()
            if (buf):
                f = tempfile.NamedTemporaryFile(delete=False)
                f.write(buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False))
                f.write("\n");
                f.close()
                parent_dir,fname = os.path.split(f.name)
                if(self._terminal):
                    self._terminal.reset(True, True)
                    self.window.get_bottom_panel().activate_item(self._terminal)
                    self._terminal.grab_focus()
                    self._terminal.fork_command_full(
                        Vte.PtyFlags.DEFAULT,
                        parent_dir,
                        ["/usr/bin/glossa-interpreter", fname],
                        [],
                        GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                        None,
                        None,
                        )
        
    def _remove_ui(self):
        manager = self.window.get_ui_manager()
        manager.remove_ui(self._ui_merge_id)
        manager.remove_action_group(self._actions)
        manager.ensure_update()
        
        panel = self.window.get_bottom_panel()
        panel.remove_item(self._terminal)


