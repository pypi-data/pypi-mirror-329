from setuptools import setup, find_packages

setup(
    name='PredDNAContam', 
    version='0.0.3',  
    description='A Machine Learning Model to Estimate Within-Species DNA Contamination.',  # A brief description
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown', 
    author='Raziyeh Mohseni', 
    author_email='raziyeh.mohseni.y@gmail.com',  
    packages=find_packages(include=["PredDNAContam", "PredDNAContam.*"]), 
    install_requires=[  
        'pandas==1.4.4',
        'numpy>=1.19.5',
        'scikit-learn==1.1.2',
        'matplotlib==3.6.2',
        'seaborn==0.12.2',
        'joblib==1.4.2',
    ],
    python_requires='>=3.8' ,  
    package_data={  
        'PredDNAContam': [
            'scripts/config.txt',  
            'model/Random_Forest_Contamination_Model.joblib', 
            'model/scaler.joblib',
        ],
    },
    entry_points={  
        'console_scripts': [
            'PredDNAContam=PredDNAContam.scripts.PredDNAContam:main',
        ],
    },
    include_package_data=True,  
)


