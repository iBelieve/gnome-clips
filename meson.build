project('gnome-clips', version: '0.0.1')

project_id = 'org.gnome.Clips'

python = import('python3')
gnome = import('gnome')

message('Looking for dependencies')
python_bin = python.find_python()
if not python_bin.found()
  error('No valid python3 binary found')
else
  message('Found python3 binary')
endif
glib = dependency('glib-2.0')
dependency('gobject-introspection-1.0')
gtk = dependency('gtk+-3.0')

python_dir = join_paths(get_option('prefix'), python.sysconfig_path('purelib'))
bindir = join_paths(get_option('prefix'), get_option('bindir'))
libdir = join_paths(get_option('prefix'), get_option('libdir'))
DATA_DIR = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())

conf = configuration_data()
conf.set('VERSION', meson.project_version())
conf.set('DATA_DIR', DATA_DIR)
conf.set('LIB_DIR', libdir)
conf.set('PYTHON', python_bin.path())

subdir('data')

install_subdir('gnomeclips', install_dir: python_dir)

configure_file(input: 'gnome-clips.in', output: 'gnome-clips', configuration: conf, install_dir: bindir)
configure_file(input: 'gnome-clips-paste.in', output: 'gnome-clips-paste', configuration: conf, install_dir: libdir)