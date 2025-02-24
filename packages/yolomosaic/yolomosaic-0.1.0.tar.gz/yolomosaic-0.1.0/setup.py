from setuptools import setup, find_packages

setup(
    name="yolomosaic",  # The name of your package
    version="0.1.0",  # The initial version of your package
    packages=find_packages(),  # This automatically finds all packages in the directory
    install_requires=[  # List of dependencies your package needs
        'sahi==0.11.20',
	#'GDAL==3.4.1',
	'geopandas==1.0.1',
	'ultralytics==8.3.27',
	'ultralytics-thop==2.0.13',
	'torch==2.5.0',
	'torchaudio>=2.5.0',
	'torchvision',
	'pandas==2.2.3',
	'numpy==1.26.0',
	'rasterio', # or 1.4.3
	'shapely', # 2.0.7
    ],
    description="A Python library for visualizing YOLO detections and segmented instances on large orthomosaic images, with the ability to generate shapefiles for GIS integration",  # A brief description of your package
    long_description=open('README.md','r').read(),  # Long description (usually from README file)
    long_description_content_type="text/markdown",  # The type of content in README (markdown)
    author="Jithin Mathew",  # Your name
    url="https://github.com/jithin8mathew/YOLOmosaic",  # URL for your project (GitHub or similar)
    classifiers=[  # These help others find your package based on categories
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # The minimum Python version required for your package
    license="MIT",
    entry_points={
    'console_scripts': [
        'ymosaic=yolomosaic.cli:main',  # Make sure this points to the correct path
    ],
},
)

