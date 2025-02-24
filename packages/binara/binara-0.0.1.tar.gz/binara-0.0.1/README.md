# Binara

Code to fit the lightcurves of close main-sequence binary systems. It includes an analytical model for the lightcurves based on [Engel 2020](https://academic.oup.com/mnras/article/497/4/4884/5881975), and performs the fitting using a MCMC method.

### Lightcurve Model
The lightcurve model includes flux contributions from Doppler beaming, reflection effects, ellipsoidal variations and eclipses. The changes in eclipse depths from limb darkening effects are also modeled. For a more detailed version of the 

### MCMC Fitting


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Contact](#contact)

## Installation

### Downloading the code
The code is available on GitHub. Simply run:

```sh

# Clone the repository
git clone https://github.com/golmschenk/binara.git

cd binara
```

### Building with CMake
Building with CMake is not necessary since the source code is contained in only three C files. However, it is extremely convenient. In your terminal, simply run:

```sh
# Install dependencies
cmake -B build

cd build

# Build the project
make -j
```

Note: Building with OpenMP support on some of the Apple machines with M1 or M2 chips may require you to specify a different compiler than AppleClang. E.g., if you have downloaded OpenMP and gcc via brew, you may instead want to do:

```sh

cmake -B build -D CMAKE_CXX_COMPILER=/opt/homebrew/bin/g++-14 \
-D CMAKE_C_COMPILER=/opt/homebrew/bin/gcc-14
```

### Building Directly
The executable can also be compiled and linked directly. 

```sh
mkdir build

gcc src/mcmc_wrapper.c src/likelihood.c src/util.c -O3 -fopenmp -o build/binara
```

## Usage

Examples of how to use the project.

```sh
# Run the project

```

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## Contact

Siddhant Solanki - [siddhant@umd.edu](mailto:siddhant@umd.edu)