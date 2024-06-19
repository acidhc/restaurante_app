from cx_Freeze import setup, Executable

build_exe_options = {
    'packages': ['tkinter', 'sqlite3'],
    'include_files': [
        'restaurant.db',  # Asegúrate de incluir el archivo de la base de datos
    ]
}

setup(
    name='RestauranteApp',
    version='1.0',
    description='Software de Gestión para Restaurantes',
    options={'build_exe': build_exe_options},
    executables=[Executable('restaurante_app/main_window.py', base='Win32GUI', target_name='RestauranteApp.exe')]
)
