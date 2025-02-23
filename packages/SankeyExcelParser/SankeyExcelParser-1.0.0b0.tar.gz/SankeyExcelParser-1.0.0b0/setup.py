from setuptools import setup
import setuptools.command.sdist
import setuptools.command.install
import setuptools.command.egg_info
import wheel.bdist_wheel

import shutil
import setuptools
import os


def get_long_description():
    try:
        with open('mfa_problem/README.md') as f:
            long_description = f.read()
            return long_description
    except Exception:
        with open('README.md') as f:
            long_description = f.read()
            return long_description


class BuildPyCommand(setuptools.command.sdist.sdist):
    """Custom build command."""
    def run(self):
        build_py = self.get_finalized_command('build_py')
        mfa_problem_dir = build_py.get_package_dir('SankeyExcelParser')
        root_dir = os.path.dirname(mfa_problem_dir)
        # shutil.copyfile(os.path.join(root_dir, 'requirements.txt'), os.path.join(mfa_problem_dir, 'requirements.txt'))
        test_dir = os.path.join(root_dir, 'tests')
        cp_test_dir = os.path.join(mfa_problem_dir, 'tests')
        if os.path.exists(cp_test_dir):
            shutil.rmtree(cp_test_dir)
        shutil.copytree(test_dir, cp_test_dir)
        super(BuildPyCommand, self).run()
        # shutil.rmtree(cp_test_dir)
        # shutil.rmtree(cp_data_dir)


class InstallPyCommand(setuptools.command.install.install):
    """Custom build command."""
    def run(self):
        build_py = self.get_finalized_command('build_py')
        mfa_problem_dir = build_py.get_package_dir('SankeyExcelParser')
        root_dir = os.path.dirname(mfa_problem_dir)
        print(root_dir)
        # shutil.copyfile(os.path.join(root_dir, 'requirements.txt'), os.path.join(mfa_problem_dir, 'requirements.txt'))
        test_dir = os.path.join(root_dir, 'tests')
        cp_test_dir = os.path.join(mfa_problem_dir, 'tests')
        if os.path.exists(cp_test_dir):
            shutil.rmtree(cp_test_dir)
        shutil.copytree(test_dir, cp_test_dir)
        super(InstallPyCommand, self).run()
        # shutil.rmtree(cp_test_dir)
        # shutil.rmtree(cp_data_dir)


class EggInfoPyCommand(setuptools.command.egg_info.egg_info):
    """Custom build command."""
    def run(self):
        build_py = self.get_finalized_command('build_py')
        mfa_problem_dir = build_py.get_package_dir('SankeyExcelParser')
        root_dir = os.path.dirname(mfa_problem_dir)
        print(root_dir)
        # shutil.copyfile(os.path.join(root_dir, 'requirements.txt'), os.path.join(mfa_problem_dir, 'requirements.txt'))
        test_dir = os.path.join(root_dir, 'tests')
        cp_test_dir = os.path.join(mfa_problem_dir, 'tests')
        if os.path.exists(cp_test_dir):
            shutil.rmtree(cp_test_dir)
        shutil.copytree(test_dir, cp_test_dir)
        super(EggInfoPyCommand, self).run()
        # shutil.rmtree(cp_test_dir)
        # shutil.rmtree(cp_data_dir)


class BDistWheelInfoPyCommand(wheel.bdist_wheel.bdist_wheel):
    """Custom build command."""
    def run(self):
        build_py = self.get_finalized_command('build_py')
        mfa_problem_dir = build_py.get_package_dir('SankeyExcelParser')
        root_dir = os.path.dirname(mfa_problem_dir)
        print(root_dir)
        # shutil.copyfile(os.path.join(root_dir, 'requirements.txt'), os.path.join(mfa_problem_dir, 'requirements.txt'))
        test_dir = os.path.join(root_dir, 'tests')
        cp_test_dir = os.path.join(mfa_problem_dir, 'tests')
        if os.path.exists(cp_test_dir):
            shutil.rmtree(cp_test_dir)
        shutil.copytree(test_dir, cp_test_dir)
        super(BDistWheelInfoPyCommand, self).run()
        # shutil.rmtree(cp_test_dir)
        # shutil.rmtree(cp_data_dir)


setup(
    name='SankeyExcelParser',
    version='1.0.0b',
    description='Excel Parser for OpenSankey suite',
    url='https://gitlab.com/su-model/sankeyexcelparser',
    author='TerriFlux',
    author_email='julien.alapetite@terriflux.fr',
    test_suite='tests',
    scripts=[
        'bin/run_parse_excel.py',
        'bin/run_parse_and_write_excel.py'],
    packages=[
        'SankeyExcelParser',
        'SankeyExcelParser.sankey_utils',
        'SankeyExcelParser.sankey_utils.protos',
        'SankeyExcelParser.tests.integration',
        'SankeyExcelParser.tests.unit'],
    package_dir={'SankeyExcelParser': 'SankeyExcelParser'},
    install_requires=[
        'openpyxl',
        'pandas',
        'argparse',
        'xmltodict',
        'psutil',
        'xlrd',
        'numpy',
        'seaborn',
        'Unidecode',
        'xlwings'],
    cmdclass={
        'sdist': BuildPyCommand,
        'install': InstallPyCommand,
        'egg_info': EggInfoPyCommand,
        'bdist_wheel': BDistWheelInfoPyCommand},
    long_description=get_long_description(),
    long_description_content_type='text/markdown'
)

# Command to run
# check rst is valid
# pip install readme_renderer
# python setup.py check -r -s
#
