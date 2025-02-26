# use following command to compil: python setup_cython.py build_ext --inplace
import contextlib
import errno
import logging
import os
import shutil
from sysconfig import get_config_var

import setuptools
from Cython.Build import cythonize

import songfinder


def prepare():
    if songfinder.__myOs__ == "windows":
        compileArgs = [
            "/O2"
        ]  # Do not use /fp:fast, this will screw up with correction algorithm
    else:
        compileArgs = ["-O3"]

    cExtensions = []
    cythonExtensions = []
    names = []

    cheminScr = os.path.abspath(
        os.path.join(songfinder.__chemin_root__, songfinder.__appName__)
    )
    cheminComp = os.path.join(songfinder.__chemin_root__, "comp")
    cheminLib = os.path.join(cheminScr, "lib")
    libExt = [".so", ".dll", ".pyd"]

    logging.info(f'[cython] source dir: "{cheminScr}"')
    logging.info(f'[cython] comp dir: "{cheminComp}"')
    logging.info(f'[cython] lib dir: "{cheminLib}"')

    try:
        os.makedirs(cheminComp)
    except OSError as error:
        if error.errno == errno.EEXIST:
            pass
        else:
            raise
    try:
        os.makedirs(cheminLib)
        with open(os.path.join(cheminLib, "__init__.py"), "w"):
            pass
    except OSError as error:
        if error.errno == errno.EEXIST:
            pass
        else:
            raise

    fileToCompil = {"creplace"}
    fileToCythonize = {"pyreplace", "distances", "fonctions", "dataBase", "gestchant"}

    def _getLibName(name):
        libName = str(f"{songfinder.__appName__}.lib.{name}")
        if not targetInfo:
            libName = str(f"{libName}_{songfinder.__arch__}")
        return libName

    def _getFileName(name, ext):
        if targetInfo:
            fileName = str(f"{name}{targetInfo}")
        else:
            fileName = str(f"{name}_{songfinder.__arch__}")
        fileName = f"{fileName}{ext}"
        return fileName

    try:
        targetInfo = os.path.splitext(get_config_var("EXT_SUFFIX"))[0]
    except AttributeError:
        targetInfo = ""

    for _root, _dirs, files in os.walk(cheminLib):
        for fichier in files:
            nom = os.path.splitext(os.path.split(fichier)[1])[0]
            nom = nom.replace(targetInfo, "")
            if targetInfo:
                firstPartName = nom.split("_")[0]
            else:
                firstPartName = nom.split(".")[0]
            setToTest = set((nom, firstPartName))
            allSources = fileToCythonize | fileToCompil
            if (
                setToTest & allSources == set()
                and os.path.splitext(fichier)[1] in libExt
            ):
                with contextlib.suppress(OSError, IOError):
                    os.remove(os.path.join(cheminLib, fichier))

    # Copy file to compile in the comp directory
    # Delete old library files
    for file_comp in fileToCythonize:
        pySrcFile = os.path.join(cheminScr, f"{file_comp}.py")
        pyxSrcFile = os.path.join(cheminScr, f"{file_comp}.pyx")
        if os.path.isfile(pyxSrcFile):
            srcFile = pyxSrcFile
        else:
            srcFile = pySrcFile
        dstFile = os.path.join(cheminComp, f"{file_comp}.pyx")

        if (
            not os.path.isfile(dstFile)
            or os.stat(srcFile).st_mtime > os.stat(dstFile).st_mtime
        ):
            for ext in libExt:
                with contextlib.suppress(OSError, IOError):
                    os.remove(os.path.join(cheminLib, _getFileName(file_comp, ext)))
            shutil.copy(srcFile, dstFile)

    # Find all module to compile with Cython
    for root, _dirs, files in os.walk(cheminComp):
        for fichier in files:
            nom = os.path.splitext(os.path.split(fichier)[1])[0]
            fullName = os.path.join(root, fichier)
            tests = [
                os.path.isfile(tested)
                for tested in [
                    os.path.join(cheminLib, _getFileName(nom, ext)) for ext in libExt
                ]
            ]
            tests += [nom not in fileToCythonize]
            if os.path.splitext(fichier)[1] == ".pyx" and not sum(tests) > 0:
                names.append(nom)
                # https://stackoverflow.com/questions/31043774/customize-location-of-so-file-generated-by-cython
                cythonExtensions.append(
                    setuptools.Extension(
                        _getLibName(nom),
                        [str(fullName)],
                        extra_compile_args=compileArgs,
                    )
                )

    # Compiling c source files
    for root, _dirs, files in os.walk(cheminComp):
        for fichier in files:
            nom = os.path.splitext(os.path.split(fichier)[1])[0]
            if nom in fileToCompil:
                srcFile = os.path.join(root, fichier)
                maxDate = os.stat(srcFile).st_mtime
                for ext in libExt:
                    fileToTest = os.path.join(cheminLib, _getFileName(nom, ext))
                    if (
                        os.path.isfile(fileToTest)
                        and maxDate < os.stat(fileToTest).st_mtime
                    ):
                        maxDate = os.stat(fileToTest).st_mtime
                if maxDate <= os.stat(srcFile).st_mtime:
                    names.append(nom)
                    cExtensions.append(
                        setuptools.Extension(
                            _getLibName(nom),
                            [str(srcFile)],
                            extra_compile_args=compileArgs,
                        )
                    )

    extensions = cExtensions + cythonize(cythonExtensions)

    return names, extensions


def docompile():
    names, extensions = prepare()

    if extensions != []:
        logging.debug(f"[cython] Compiling modules: {', '.join(names)}")
        setuptools.setup(ext_modules=extensions)


if __name__ == "__main__":
    docompile()
