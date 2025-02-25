![EPFL Center for Imaging logo](https://imaging.epfl.ch/resources/logo-for-gitlab.svg)
# 🪐 Imaging Server Kit

Deploy image processing algorithms in FastAPI servers and easily run them from Napari, QuPath, and more.

The algorithm servers implement a common set of API endpoints for processing and to document the project. These include:
  - `/process`: Runs the algorithm
  - `/info`: Displays documentation about the algorithm usage
  - `/sample_images`: Provides one or multiple sample images

## Usage

### Algorithm servers

Set up and run a server with one, or multiple algorithms from the Imaging Server Kit collection (or your own):

  - [StarDist](https://github.com/Imaging-Server-Kit/serverkit-stardist): Object detection with star-convex shapes
  - [CellPose](https://github.com/Imaging-Server-Kit/serverkit-cellpose): A generalist algorithm for cellular segmentation
  - [Spotiflow](https://github.com/Imaging-Server-Kit/serverkit-spotiflow): Accurate and efficient spot detection
  - [Rembg](https://github.com/Imaging-Server-Kit/serverkit-rembg): A tool to remove images background
  - [LoG detector](https://github.com/Imaging-Server-Kit/serverkit-skimage-LoG): Laplacian of Gaussian filter
  - [Orientationpy](https://github.com/Imaging-Server-Kit/serverkit-orientationpy): Measurement of greyscale orientations
<!-- - [Tau Fibrils Detector](https://github.com/Imaging-Server-Kit/serverkit-tau-fibrils-yolo) -->

All of these algorithm servers can be installed locally or built and run with docker. To use docker and serve multiple algorithms, the recommended way is to edit a `docker-compose.yml` file and pull server images from `registry.rcp.epfl.ch` (EPFL users only):

```{docker-compose.yml}
services:
  servers_registry:
    image: mallorywittwerepfl/imaging-server-kit:latest
    ports:
      - "8000:8000"
    command: python3 start_registry.py
  rembg:
    image: registry.rcp.epfl.ch/imaging-server-kit/serverkit-rembg:latest
    depends_on:
      - servers_registry
  skimage-log:
    image: registry.rcp.epfl.ch/imaging-server-kit/serverkit-skimage-log:latest
    depends_on:
      - servers_registry
```

Start the server with

```
docker compose up
```

The server should be accessible at http://localhost:8000.

**Build the docker images yourself**

To build the algorithm server images yourself (e.g. if you are not from EPFL), see [Reference Deployment](https://github.com/Imaging-Server-Kit/serverkit-deploy-docker).

**Create a server for your project**

To learn how to create a server for your project, see [Algorithm Server Template](https://github.com/Imaging-Server-Kit/cookiecutter-serverkit).

### Python client

Once the server is running, connect to it and run algorithms from Python:

```python
from imaging_server_kit import Client

client = Client("http://localhost:8000")

print(client.algorithms)
# [`rembg`, `stardist`, `cellpose`]

algo_output = client.run_algorithm(
    algorithm="rembg",
    image=(...),
    rembg_model_name="silueta",
)
```

### Napari plugin

Once the server is running, use the [Napari Server Kit](https://github.com/Imaging-Server-Kit/napari-serverkit) plugin to connect to it and run algorithms in Napari.

### QuPath extension

Once the server is running, use the [QuPath Extension Server Kit](https://github.com/Imaging-Server-Kit/qupath-extension-serverkit) to connect to it and run algorithms from within QuPath.

## Install locally

Install the `imaging-server-kit` package with `pip`:

```
pip install imaging-server-kit
```

or clone the project and install the development version:

```
git clone https://github.com/Imaging-Server-Kit/imaging-server-kit.git
cd imaging-server-kit
pip install -e .
```

## Build with `docker`

Build the `imaging-server-kit` docker image for a specific Python version:

```
docker build --build-arg PYTHON_VERSION=3.9 -t imaging-server-kit:3.9 .
```

Run [build.sh](./build.sh) to build docker images for Python 3.9, 3.10, 3.11, GPU and the server kit registry:

```
bash ./build.sh
```

## Contributing

Contributions are very welcome.

## License

This software is distributed under the terms of the [BSD-3](http://opensource.org/licenses/BSD-3-Clause) license.

## Issues

If you encounter any problems, please file an issue along with a detailed description.
