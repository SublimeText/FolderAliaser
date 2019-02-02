import os
import sublime_plugin


def project_folder(project, path):
    for folder in (project or {}).get('folders', {}):
        if folder['path'] == path:
            return folder
    return None


def display_name(project, path):
    folder = project_folder(project, path)
    if folder:
        return folder.get('name') or os.path.basename(folder['path'])
    return None


class AliasFolderCommand(sublime_plugin.WindowCommand):

    def is_enabled(self, dirs):
        return len(dirs) == 1 and bool(project_folder(self.window.project_data(), dirs[0]))

    def run(self, dirs):
        self.window.show_input_panel(
            "Alias this folder (enter nothing to clear an alias):",
            display_name(self.window.project_data(), dirs[0]),
            lambda alias: self.on_input_panel_submit(alias, dirs[0]),
            None, None
        )

    def on_input_panel_submit(self, alias, path):
        project = self.window.project_data()
        folder = project_folder(project, path)
        if folder:
            if alias in ('', os.path.basename(path)):
                if 'name' in folder:
                    folder.pop('name')
            else:
                folder['name'] = alias
            self.window.set_project_data(project)
