from setuptools import setup, find_packages
import os


setup(
    name='dart_physics',
    version='2.1.11',
    packages=find_packages(),
    install_requires=[
        'mujoco',
        'gdown',
        'adam-robotics[jax]==0.3.0',
        'dm_control',
        'loop_rate_limiters',
        'avp_stream',
        'robot_descriptions',
        'obj2mjcf',
        'flask>=3.0.3',
        'psutil', 
        'mediapy', 
        'pyzmq', 
        'grpcio',
        'grpcio-tools',
        'numpy',
        'imageio>=2.36.0',
        'opencv-python',
        'qpsolvers[quadprog] >= 4.3.1',
        'typing_extensions',
        'dexhub-api>=0.3',
        'gdown', 
    ],
    author='Younghyo Park',
    author_email='younghyo@mit.edu',
    python_requires='>=3.6',
    include_package_data=True,
)