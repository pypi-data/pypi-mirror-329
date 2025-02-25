import os

from setuptools import setup, find_packages

setup(
    name='bdext',
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    package_data={'bdpn': [os.path.join('..', 'README.md'),
                           #  os.path.join('dl', 'models_pinball', 'BD*', '*.keras'),
                           #  os.path.join('dl', 'models_pinball', 'BD*', '*.h5'),
                           #  os.path.join('dl', 'models_pinball', 'BD*', '*.json'),
                           #  os.path.join('dl', 'models_pinball', 'BD*', '*.txt'),
                           #  os.path.join('dl', 'models_pinball', 'BD*', '*.npy'),
                           #  os.path.join('dl', 'models_pinball', 'BD*', '*.gz'),
                           # os.path.join('dl', 'training_data', 'BD*', '*.csv.xz'),
                            os.path.join('..', 'LICENCE')]},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    version='0.1.22',
    description='Estimation of BD and BDCT parameters from phylogenetic trees.',
    author='Anna Zhukova',
    author_email='anna.zhukova@pasteur.fr',
    url='https://github.com/evolbioinfo/bdpn',
    keywords=['phylogenetics', 'birth-death model', 'partner notification', 'contact tracing'],
    install_requires=['tensorflow==2.18.0', 'six', 'ete3', 'numpy==2.0.2', "scipy==1.14.1", 'biopython',
                      'scikit-learn==1.5.2', 'pandas==2.2.3', 'treesumstats==0.6'],
    entry_points={
            'console_scripts': [
                'bdct_infer = bdpn.bdpn_model:main',
                'bdct_mf = bdpn.dl.bdct_model_finder:main',
                'bdctdl_infer = bdpn.dl.bdct_estimator:main',
                'bdct_encode = bdpn.dl.tree_encoder:main',
                'bdct_train = bdpn.dl.training:main',
                'bdct_train_model_finder = bdpn.dl.training_model_finder:main',
                'bd_infer = bdpn.bd_model:main',
                'bdmult_infer = bdpn.bdmult_model:main',
                'bdssmult_infer = bdpn.bdssmult_model:main',
                'bdct_loglikelihood = bdpn.bdpn_model:loglikelihood_main',
                'bd_loglikelihood = bdpn.bd_model:loglikelihood_main',
                'bdmult_loglikelihood = bdpn.bdmult_model:loglikelihood_main',
                'bdssmult_loglikelihood = bdpn.bdssmult_model:loglikelihood_main',
                'ct_test = bdpn.model_distinguisher:main',
            ]
    },
)
