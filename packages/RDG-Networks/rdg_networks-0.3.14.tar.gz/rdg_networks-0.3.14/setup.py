from setuptools import setup, find_packages

setup(
    name='RDG-Networks',
    version='0.3.14',
    author='Niek Mooij',
    author_email='mooij.niek@gmail.com',
    description='RDG Networks project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/NiekMooij/RDG_networks',
    classifiers=[
            'Programming Language :: Python :: 3',
            'Operating System :: OS Independent'],
    license='All Rights Reserved',
    packages=find_packages(),
    install_requires=[
        'networkx',
        'numpy',
        'scipy',
        'shapely',
        'typing'
    ],
    entry_points={
        'console_scripts': [
            'generate_line_segments=RDG_networks.generate_line_segments:main',
            'generate_line_segments_thickness=RDG_networks.thickness.generate_line_segments_thickness:main',
            
            'orientate_network=RDG_networks.thickness.orientate_network:main',

            'translate_network=RDG_networks.thickness.translate_network:main',
            'clip_network=RDG_networks.thickness.clip_network:main',

            'rotate_network=RDG_networks.thickness.rotate_network:main',

            'get_alignment_mean=RDG_networks.thickness.get_alignment_mean:main',

            'generate_line_segments_dynamic=RDG_networks.generate_line_segments_dynamic:main',

            'generate_line_segments_static=RDG_networks.generate_line_segments_static:main',
            'generate_line_segments_thickness_static=RDG_networks.generate_line_segments_thickness_static:main',

            'generate_line_network=RDG_networks.generate_line_network:main',

            'get_intersection_segments=RDG_networks.get_intersection_segments:main',

            'draw_segments=RDG_networks.draw_segments:main',

            'save_data=RDG_networks.save_to_stl:main',
            'save_to_json=RDG_networks.save_to_json:main',
            'load_from_json=RDG_networks.load_from_json:main'
        ],
    },
)